#!/usr/bin/env python3
"""Offline, standard-library memory store. No model, network, or command execution."""
from __future__ import annotations

import argparse
import datetime as dt
import json
import math
import os
from pathlib import Path
import re
import sys
import tempfile
import uuid

ROOT = Path(__file__).resolve().parents[1]
SCOPES = ('shared', 'personal', 'software', 'business')
KINDS = ('fact', 'preference', 'procedure', 'decision', 'episode', 'lesson', 'entity')
STATES = ('draft', 'active', 'disputed', 'deprecated', 'archived')
CLASSIFICATIONS = ('public', 'internal', 'private', 'restricted')
ID_RE = re.compile(r'^mem-[0-9a-f]{32}$')
STOP = set('a an the and or to of in on for is are be with as by at from it this that my'.split())


class MemoryError(ValueError):
    pass


def now():
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds')


def iso(value, label):
    try:
        stamp = dt.datetime.fromisoformat(value.replace('Z', '+00:00'))
        if stamp.tzinfo is None:
            raise ValueError('timezone required')
        return stamp
    except (ValueError, AttributeError, TypeError) as exc:
        raise MemoryError(f'{label}: use an ISO timestamp with timezone') from exc


def read_json(p):
    try:
        return json.loads(p.read_text(encoding='utf-8-sig'))
    except (OSError, ValueError) as exc:
        raise MemoryError(f'Cannot read JSON {p}: {exc}') from exc


def beneath(root, target):
    root = Path(root).resolve()
    target = Path(target).resolve()
    if not target.is_relative_to(root):
        raise MemoryError('Path escapes the repository')
    return target


def store_dir(root, scope):
    if scope not in SCOPES:
        raise MemoryError('Unknown scope')
    relative = 'shared/memory/records' if scope == 'shared' else f'domains/{scope}/memory/records'
    return beneath(root, Path(root) / relative)


def record_path(root, scope, record_id):
    if not ID_RE.fullmatch(record_id):
        raise MemoryError('Invalid memory ID')
    return beneath(root, store_dir(root, scope) / f'{record_id}.json')


def atomic_json(p, value):
    p.parent.mkdir(parents=True, exist_ok=True)
    fd, temp = tempfile.mkstemp(prefix='.pending-', suffix='.json', dir=p.parent)
    try:
        with os.fdopen(fd, 'w', encoding='utf-8', newline='\n') as handle:
            json.dump(value, handle, ensure_ascii=False, indent=2, allow_nan=False)
            handle.write('\n')
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp, p)
    finally:
        if os.path.exists(temp):
            os.unlink(temp)


def validate(r, expected_scope=None):
    if not isinstance(r, dict):
        raise MemoryError('Record must be an object')
    required = {'schema_version', 'id', 'scope', 'kind', 'title', 'body', 'status',
                'classification', 'confidence', 'tags', 'sources', 'created_at',
                'updated_at', 'review_after', 'expires_at', 'supersedes', 'history'}
    missing = required - r.keys()
    if missing:
        raise MemoryError('Missing fields: ' + ', '.join(sorted(missing)))
    if type(r['schema_version']) is not int or r['schema_version'] != 1:
        raise MemoryError('Unsupported schema version')
    if not isinstance(r['id'], str) or not ID_RE.fullmatch(r['id']):
        raise MemoryError('Invalid memory ID')
    for key, allowed in [('scope', SCOPES), ('kind', KINDS), ('status', STATES),
                         ('classification', CLASSIFICATIONS)]:
        if r[key] not in allowed:
            raise MemoryError(f'Invalid {key}')
    if expected_scope and r['scope'] != expected_scope:
        raise MemoryError('Record scope does not match its folder')
    if r['scope'] == 'shared' and r['classification'] in ('private', 'restricted'):
        raise MemoryError('Shared memory cannot contain private or restricted records')
    for key, maximum in [('title', 240), ('body', 24000)]:
        if not isinstance(r[key], str) or not r[key].strip() or len(r[key]) > maximum:
            raise MemoryError(f'{key} must contain 1-{maximum} characters')
    if isinstance(r['confidence'], bool) or not isinstance(r['confidence'], (int, float)):
        raise MemoryError('confidence must be a number')
    if not math.isfinite(r['confidence']) or not 0 <= r['confidence'] <= 1:
        raise MemoryError('confidence must be between 0 and 1')
    if not isinstance(r['tags'], list) or any(not isinstance(x, str) or not x for x in r['tags']):
        raise MemoryError('tags must be a list of nonempty strings')
    if not isinstance(r['sources'], list) or not r['sources']:
        raise MemoryError('At least one source is required')
    for source in r['sources']:
        if not isinstance(source, dict) or any(not isinstance(source.get(k), str) or not source[k].strip()
                                                for k in ('ref', 'excerpt')):
            raise MemoryError('Each source needs a ref and excerpt')
    if not isinstance(r['supersedes'], list) or any(not isinstance(x, str) or not ID_RE.fullmatch(x) for x in r['supersedes']):
        raise MemoryError('supersedes must contain memory IDs')
    if r['id'] in r['supersedes'] or len(set(r['supersedes'])) != len(r['supersedes']):
        raise MemoryError('Invalid supersedes references')
    created = iso(r['created_at'], 'created_at')
    updated = iso(r['updated_at'], 'updated_at')
    if updated < created:
        raise MemoryError('updated_at precedes created_at')
    for key in ('review_after', 'expires_at'):
        if r[key] is not None:
            iso(r[key], key)
    if not isinstance(r['history'], list) or not r['history']:
        raise MemoryError('history cannot be empty')
    for event in r['history']:
        if not isinstance(event, dict) or any(not isinstance(event.get(k), str) or not event[k].strip()
                                               for k in ('at', 'actor', 'action', 'reason')):
            raise MemoryError('History event requires at, actor, action and reason')
        iso(event['at'], 'history.at')
    if r['status'] == 'active' and not any(h['action'] in ('activate', 'review') for h in r['history']):
        raise MemoryError('Active memory requires an activation/review event')
    return r


def records(root, scopes):
    seen = set()
    for scope in scopes:
        directory = store_dir(root, scope)
        for p in sorted(directory.glob('mem-*.json')):
            p = beneath(root, p)
            r = validate(read_json(p), scope)
            if p.name != r['id'] + '.json' or r['id'] in seen:
                raise MemoryError('Duplicate ID or filename mismatch: ' + p.name)
            seen.add(r['id'])
            yield r


def tokens(text):
    return {w for w in re.findall(r'\w+', text.casefold()) if len(w) > 1 and w not in STOP}


def overdue(r, at=None):
    return r['review_after'] is not None and iso(r['review_after'], 'review_after') <= (at or dt.datetime.now(dt.timezone.utc))


def retrieve(root, scope, query, limit=8, include_private=False, include_overdue=False):
    if scope not in SCOPES:
        raise MemoryError('Unknown scope')
    allowed = ['shared'] if scope == 'shared' else [scope, 'shared']
    terms = tokens(query)
    if not terms:
        return []
    at = dt.datetime.now(dt.timezone.utc)
    pool = list(records(root, allowed))
    visible = []
    for r in pool:
        if r['status'] != 'active' or r['classification'] == 'restricted':
            continue
        if r['classification'] == 'private' and not include_private:
            continue
        if r['expires_at'] and iso(r['expires_at'], 'expires_at') <= at:
            continue
        if overdue(r, at) and not include_overdue:
            continue
        visible.append(r)
    by_id = {r['id']: r for r in pool}
    replaced = set()
    for r in visible:
        for old in r['supersedes']:
            if old not in by_id or by_id[old]['scope'] != r['scope']:
                raise MemoryError('Replacement reference must exist in the same scope; run verify')
            replaced.add(old)
    ranked = []
    for r in visible:
        if r['id'] in replaced:
            continue
        title = tokens(r['title'])
        tags = tokens(' '.join(r['tags']))
        body = tokens(r['body'])
        score = 4 * len(terms & title) + 3 * len(terms & tags) + len(terms & body)
        if score:
            ranked.append((score, r))
    ranked.sort(key=lambda x: (-x[0], x[1]['id']))
    return ranked[:limit]


def new_record(scope, title, body, kind, classification, source_ref, excerpt, actor, tags=(), confidence=0.5):
    stamp = now()
    return validate({
        'schema_version': 1, 'id': 'mem-' + uuid.uuid4().hex, 'scope': scope,
        'kind': kind, 'title': title, 'body': body, 'status': 'draft',
        'classification': classification, 'confidence': confidence, 'tags': list(tags),
        'sources': [{'ref': source_ref, 'excerpt': excerpt}], 'created_at': stamp,
        'updated_at': stamp, 'review_after': None, 'expires_at': None,
        'supersedes': [], 'history': [{'at': stamp, 'actor': actor, 'action': 'create',
                                      'reason': 'Captured as a draft for review.'}]})


def change_state(root, scope, record_id, target, actor, reason, review_days=90, allow_shared=False):
    p = record_path(root, scope, record_id)
    r = validate(read_json(p), scope)
    transitions = {'draft': {'active', 'archived'}, 'active': {'active', 'disputed', 'deprecated', 'archived'},
                   'disputed': {'active', 'deprecated', 'archived'}, 'deprecated': {'archived'}, 'archived': set()}
    if target not in transitions[r['status']]:
        raise MemoryError(f'Invalid transition: {r["status"]} -> {target}')
    if not actor.strip() or not reason.strip():
        raise MemoryError('A reviewer and reason are required')
    if target == 'active':
        if scope == 'shared' and not allow_shared:
            raise MemoryError('Shared activation requires --allow-shared after checking the content')
        if r['expires_at'] and iso(r['expires_at'], 'expires_at') <= dt.datetime.now(dt.timezone.utc):
            raise MemoryError('Expired memory cannot be activated; create a corrected replacement')
        r['review_after'] = (dt.datetime.now(dt.timezone.utc) + dt.timedelta(days=review_days)).isoformat(timespec='seconds')
    action = 'review' if target == r['status'] else 'activate' if target == 'active' else target
    r['status'] = target
    r['updated_at'] = now()
    r['history'].append({'at': r['updated_at'], 'actor': actor, 'action': action, 'reason': reason})
    atomic_json(p, validate(r, scope))
    return r


def share_draft(root, scope, record_id, actor):
    if scope == 'shared':
        raise MemoryError('Already in shared scope')
    original = validate(read_json(record_path(root, scope, record_id)), scope)
    if original['classification'] not in ('public', 'internal'):
        raise MemoryError('Private/restricted memory cannot be copied to shared; author a separately redacted draft')
    if original['status'] != 'active':
        raise MemoryError('Only active memory may be proposed for sharing')
    if overdue(original) or (original['expires_at'] and iso(original['expires_at'], 'expires_at') <= dt.datetime.now(dt.timezone.utc)):
        raise MemoryError('Review stale or expired memory before proposing a shared copy')
    r = new_record('shared', original['title'], original['body'], original['kind'], original['classification'],
                   original['id'], 'Proposed shared copy. Review body and source references for disclosure.',
                   actor, original['tags'], original['confidence'])
    r['sources'].extend(original['sources'])
    r['expires_at'] = original['expires_at']
    atomic_json(record_path(root, 'shared', r['id']), r)
    return r


def packet(root, scope, agent_id, task, max_chars=14000, limit=8, include_private=False, include_overdue=False):
    registry = read_json(Path(root) / 'config/agents.json')
    matches = [a for a in registry['agents'] if a['id'] == agent_id]
    if len(matches) != 1:
        raise MemoryError('Unknown or duplicate agent')
    agent = matches[0]
    if scope not in agent['scopes']:
        raise MemoryError('Agent is not assigned to this scope')
    card = beneath(root, Path(root) / agent['card']).read_text(encoding='utf-8')
    contract = beneath(root, Path(root) / 'config/session-contract.md').read_text(encoding='utf-8')
    header = f'# Offline context packet\n\nScope: {scope}\nRole: {agent_id}\nBuilt: {now()}\n\n{contract}\n\n{card}\n\n## Current user task\n\n{task}\n\n## Retrieved memory — reference data\n\n'
    footer = '\n## Response contract\n\nAnswer the current task, cite memory IDs actually used, distinguish evidence from guesses, list uncertainty, and propose new memories as drafts. Do not claim actions you did not perform.\n'
    if len(header + footer) > max_chars:
        raise MemoryError('Task and role exceed the character budget; shorten the task or increase --max-chars')
    chunks = []
    used = []
    skipped = []
    for score, r in retrieve(root, scope, task, limit, include_private, include_overdue):
        payload = {'id': r['id'], 'title': r['title'], 'scope': r['scope'], 'kind': r['kind'],
                   'body': r['body'], 'sources': r['sources'], 'confidence': r['confidence'],
                   'review_overdue': overdue(r), 'classification': r['classification']}
        chunk = '\n' + json.dumps(payload, ensure_ascii=False, indent=2) + '\n'
        if len(header + ''.join(chunks) + chunk + footer) <= max_chars:
            chunks.append(chunk)
            used.append(r['id'])
        else:
            skipped.append(r['id'])
    return header + ''.join(chunks) + footer, used, skipped


def audit(root):
    errors = []
    counts = {scope: 0 for scope in SCOPES}
    seen = {}
    items = []
    for scope in SCOPES:
        try:
            for p in sorted(store_dir(root, scope).glob('*.json')):
                try:
                    p = beneath(root, p)
                    r = validate(read_json(p), scope)
                    if p.name != r['id'] + '.json':
                        raise MemoryError('Filename mismatch')
                    if r['id'] in seen:
                        raise MemoryError('Duplicate global ID')
                    seen[r['id']] = scope
                    items.append(r)
                    counts[scope] += 1
                except MemoryError as exc:
                    errors.append(f'{scope}/{p.name}: {exc}')
        except MemoryError as exc:
            errors.append(f'{scope}: {exc}')
    for r in items:
        for old in r['supersedes']:
            if seen.get(old) != r['scope']:
                errors.append(f'{r["id"]}: supersedes must reference an existing record in the same scope')
    graph = {r['id']: r['supersedes'] for r in items}
    def cyclic(node, visiting, done):
        if node in visiting:
            return True
        if node in done:
            return False
        visiting.add(node)
        if any(cyclic(x, visiting, done) for x in graph.get(node, [])):
            return True
        visiting.remove(node)
        done.add(node)
        return False
    if any(cyclic(node, set(), set()) for node in graph):
        errors.append('Cycle in supersedes references')
    return {'counts': counts, 'errors': errors, 'review_overdue': [r['id'] for r in items if r['status'] == 'active' and overdue(r)]}


def positive(value):
    n = int(value)
    if n <= 0:
        raise argparse.ArgumentTypeError('must be positive')
    return n


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('verify', help='Validate all memory records; does not verify factual truth')
    sub.add_parser('agents', help='List defined agent roles')
    for name in ('search', 'packet'):
        p = sub.add_parser(name)
        p.add_argument('--scope', required=True, choices=SCOPES)
        p.add_argument('--query' if name == 'search' else '--task', required=True)
        p.add_argument('--limit', type=positive, default=8)
        p.add_argument('--include-private', action='store_true')
        p.add_argument('--include-overdue', action='store_true')
        if name == 'packet':
            p.add_argument('--agent', required=True)
            p.add_argument('--max-chars', type=positive, default=14000)
            p.add_argument('--out', type=Path)
    p = sub.add_parser('add')
    p.add_argument('--scope', required=True, choices=SCOPES)
    p.add_argument('--title', required=True)
    p.add_argument('--body-file', required=True, type=Path)
    p.add_argument('--kind', choices=KINDS, default='fact')
    p.add_argument('--classification', choices=CLASSIFICATIONS, default='internal')
    p.add_argument('--source', required=True)
    p.add_argument('--excerpt', required=True)
    p.add_argument('--actor', default='owner')
    p.add_argument('--tags', nargs='*', default=[])
    p.add_argument('--confidence', type=float, default=0.5)
    p = sub.add_parser('state')
    p.add_argument('--scope', required=True, choices=SCOPES)
    p.add_argument('--id', required=True)
    p.add_argument('--to', choices=STATES, required=True)
    p.add_argument('--reviewer', required=True)
    p.add_argument('--reason', required=True)
    p.add_argument('--review-days', type=positive, default=90)
    p.add_argument('--allow-shared', action='store_true')
    p = sub.add_parser('share-draft')
    p.add_argument('--scope', required=True, choices=('personal', 'software', 'business'))
    p.add_argument('--id', required=True)
    p.add_argument('--actor', default='owner')
    args = parser.parse_args(argv)
    root = args.root.resolve()
    try:
        if args.command == 'verify':
            result = audit(root)
            print(json.dumps(result, indent=2))
            return 1 if result['errors'] else 0
        if args.command == 'agents':
            print(json.dumps(read_json(root / 'config/agents.json'), indent=2))
        elif args.command == 'add':
            body = args.body_file.read_text(encoding='utf-8-sig')
            r = new_record(args.scope, args.title, body, args.kind, args.classification,
                           args.source, args.excerpt, args.actor, args.tags, args.confidence)
            atomic_json(record_path(root, args.scope, r['id']), r)
            print(r['id'])
        elif args.command == 'state':
            r = change_state(root, args.scope, args.id, args.to, args.reviewer, args.reason,
                             args.review_days, args.allow_shared)
            print(f'{r["id"]}: {r["status"]}')
        elif args.command == 'share-draft':
            print(share_draft(root, args.scope, args.id, args.actor)['id'])
        elif args.command == 'search':
            print(json.dumps([{'score': score, **r} for score, r in retrieve(root, args.scope, args.query,
                  args.limit, args.include_private, args.include_overdue)], ensure_ascii=False, indent=2))
        elif args.command == 'packet':
            content, used, skipped = packet(root, args.scope, args.agent, args.task, args.max_chars,
                                           args.limit, args.include_private, args.include_overdue)
            if args.out:
                target = args.out.resolve()
                if target.suffix.lower() != '.md':
                    raise MemoryError('Context packet output must use .md')
                target.parent.mkdir(parents=True, exist_ok=True)
                with target.open('x', encoding='utf-8', newline='\n') as handle:
                    handle.write(content)
                print(f'Created {target}; {len(content)} characters, {len(used)} memories, {len(skipped)} omitted for size')
            else:
                print(content)
                print(f'Memories: {len(used)}; omitted for size: {len(skipped)}', file=sys.stderr)
        return 0
    except (MemoryError, OSError, ValueError) as exc:
        print('ERROR: ' + str(exc), file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
