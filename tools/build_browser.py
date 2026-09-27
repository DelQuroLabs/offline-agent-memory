#!/usr/bin/env python3
"""Rebuild a standalone offline browser for the repository's instruction library.

Does not embed live memory, source collections, project files, or session notes.
No external packages or network access required.
"""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]


def documents(root):
    candidates = set()
    for name in ('README.md', 'START_HERE.md', 'CHANGELOG.md', 'BUILD_REPORT.md'):
        p = root / name
        if p.exists():
            candidates.add(p)
    for area in ('docs', 'policies', 'playbooks', 'templates', 'examples', 'agents', 'schemas'):
        candidates.update((root / area).rglob('*.md'))
        candidates.update((root / area).rglob('*.json'))
    for scope in ('personal', 'software', 'business'):
        base = root / 'domains' / scope
        for name in ('README.md', 'TAXONOMY.md', 'WORKFLOW.md'):
            candidates.add(base / name)
        candidates.update((base / 'agents').glob('*.md'))
    candidates.add(root / 'config/session-contract.md')
    candidates.add(root / 'shared/README.md')
    result = []
    for p in sorted(candidates):
        resolved = p.resolve()
        if not resolved.is_relative_to(root.resolve()):
            raise ValueError('Refusing to embed a file outside the repository')
        text = p.read_text(encoding='utf-8')
        rel = p.relative_to(root).as_posix()
        first = text.splitlines()[0] if text else p.stem
        title = first.lstrip('# ') if first.startswith('#') else p.name
        group = rel.split('/')[1] if rel.startswith('domains/') else rel.split('/')[0] if '/' in rel else 'start'
        result.append({'path': rel, 'title': title, 'group': group, 'text': text})
    return result


PAGE = r'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; img-src data:; connect-src 'none'; base-uri 'none'; form-action 'none'">
<title>Offline Agent Memory — Library</title>
<style>
:root{color-scheme:light;--ink:#172c38;--muted:#566a76;--line:#d9e3e7;--paper:#fff;--blue:#145e73;--bg:#eef3f4}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.65 system-ui,-apple-system,"Segoe UI",sans-serif}
button,input,select{font:inherit}button,a{touch-action:manipulation}a{color:var(--blue)}button{cursor:pointer}
.shell{display:grid;grid-template-columns:300px 1fr;min-height:100vh}.sidebar{background:#112e3a;color:#f3f8fa;padding:30px 22px;position:sticky;top:0;height:100vh;overflow:auto}
.mark{font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:#9fcbd2;font-weight:700}.sidebar h1{font-size:24px;line-height:1.25;margin:9px 0 10px}.sidebar p{font-size:13px;color:#b6ced5;margin:0 0 24px}
.sidebar label{display:block;font-size:12px;color:#c3d7dd;margin:15px 0 6px}.sidebar input,.sidebar select{width:100%;padding:10px;border:1px solid #41616d;border-radius:7px;background:#1c3b48;color:white}
.sidebar option{background:#1c3b48}.sidebar input::placeholder{color:#b5c7cd}.results{margin-top:20px}.navitem{display:block;width:100%;text-align:left;background:transparent;color:#d1e1e6;border:0;border-radius:6px;padding:9px 10px;font-size:13px;line-height:1.35;margin:2px 0}.navitem:hover,.navitem[aria-current=true]{background:#2a4b58;color:#fff}.count{font-size:12px;color:#9dbac4;margin-top:16px}
main{min-width:0;padding:42px 5vw 64px;max-width:1340px;width:100%;margin:auto}.eyebrow{font-size:12px;text-transform:uppercase;letter-spacing:.12em;color:var(--blue);font-weight:750}.hero h2{font-size:clamp(29px,3.5vw,46px);line-height:1.15;letter-spacing:-.03em;margin:10px 0 16px}.hero p{max-width:760px;color:var(--muted);margin:0 0 24px}.chips{display:flex;gap:9px;flex-wrap:wrap;margin:18px 0 26px}.chip{border:1px solid #c4d7dc;border-radius:30px;padding:5px 12px;background:#e4eef0;font-size:12px;font-weight:650;color:#2b5666}
.cards{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px;margin:24px 0}.card{border:1px solid var(--line);border-top:4px solid var(--accent);background:white;border-radius:10px;padding:22px;text-align:left;color:var(--ink)}.card:hover{box-shadow:0 5px 16px #193f4d12;transform:translateY(-1px)}.card small{color:var(--muted);font-size:11px;text-transform:uppercase;letter-spacing:.1em}.card h3{margin:7px 0;font-size:20px;line-height:1.3}.card p{font-size:13px;color:var(--muted);margin:0}.card span{display:block;margin-top:20px;font-size:12px;color:var(--blue);font-weight:650}
.flow{display:flex;align-items:center;gap:10px;flex-wrap:wrap;padding:18px 20px;border:1px solid var(--line);background:#f8fbfb;border-radius:9px;font-size:13px}.flow b{font-weight:650}.flow i{color:#78939e;font-style:normal}.flow-label{font-size:12px;color:var(--muted);margin:8px 0 28px}
.document{background:var(--paper);border:1px solid var(--line);border-radius:12px;overflow:hidden;margin-top:30px}.toolbar{display:flex;justify-content:space-between;gap:12px;align-items:center;padding:15px 24px;background:#f7fafb;border-bottom:1px solid var(--line);font-size:12px;color:var(--muted);flex-wrap:wrap}.toolbar a{text-decoration:none;font-weight:600}.docbody{padding:24px 34px 36px;overflow-wrap:anywhere}.docbody h1{font-size:29px;line-height:1.25;letter-spacing:-.02em;margin:6px 0 23px}.docbody h2{font-size:20px;line-height:1.4;margin:30px 0 12px}.docbody h3{font-size:17px;margin:22px 0 10px}.docbody p,.docbody li{font-size:15px}.docbody p{margin:12px 0}.docbody ul,.docbody ol{padding-left:24px}.docbody li{margin:7px 0}.docbody pre{font:12px/1.65 ui-monospace,Consolas,monospace;background:#eef3f5;padding:17px;border-radius:7px;overflow:auto;white-space:pre-wrap}.docbody code{font:12px/1.5 ui-monospace,Consolas,monospace;background:#eef3f5;padding:2px 4px;border-radius:3px}.docbody pre code{padding:0}.tablewrap{overflow:auto}table{border-collapse:collapse;width:100%;font-size:13px;margin:15px 0}th,td{border-bottom:1px solid var(--line);padding:10px 12px;text-align:left;vertical-align:top}th{background:#eff5f6;font-weight:650}.note{font-size:12px;color:var(--muted);margin-top:22px;max-width:850px}.home{background:none;border:0;padding:0;color:#d9ecf1;text-align:left;margin-bottom:6px}.empty{padding:10px;font-size:13px;color:#c0d0d7}
:focus-visible{outline:3px solid #c6912c;outline-offset:3px}@media(max-width:1050px){.shell{grid-template-columns:250px 1fr}main{padding:28px 28px 50px}.cards{grid-template-columns:1fr}.card{padding:16px}.card span{margin-top:10px}.docbody{padding:22px}}@media(max-width:680px){.shell{display:block}.sidebar{position:relative;height:auto;padding:22px}.results{max-height:220px;overflow:auto}.sidebar p{margin-bottom:12px}main{padding:26px 16px}.hero h2{font-size:32px}.docbody{padding:20px}.toolbar{padding:12px 20px}.cards{gap:10px}.flow{font-size:12px}}
</style>
</head>
<body>
<div class="shell">
<aside class="sidebar" aria-label="Library navigation">
<div class="mark">Local knowledge system</div><button class="home" id="home"><h1>Agent Memory<br>Library</h1></button>
<p>Three compartments. Eighteen roles.<br>Readable files that stay with you.</p>
<label for="search">Search the instruction library</label><input id="search" type="search" placeholder="Roles, memory, sharing…" autocomplete="off">
<label for="group">Choose an area</label><select id="group"><option value="all">All areas</option><option value="start">Start here</option><option value="personal">Personal &amp; work</option><option value="software">Software &amp; research</option><option value="business">Business &amp; content</option><option value="agents">Core agent roles</option><option value="docs">Operating manuals</option><option value="policies">Boundaries &amp; policies</option><option value="playbooks">Workflows</option><option value="templates">Reusable templates</option><option value="examples">Worked examples</option><option value="schemas">Memory schema</option><option value="config">Session contract</option><option value="shared">Shared library</option></select>
<div class="count" id="count" aria-live="polite"></div><nav class="results" id="results" aria-label="Documents"></nav>
</aside>
<main>
<section class="hero"><div class="eyebrow">Your offline agent foundation</div><h2>A place for every role.<br>A source for every memory.</h2><p>Define what each agent does, keep its knowledge in the right compartment, and carry useful evidence from one local session to the next.</p>
<div class="chips"><span class="chip">18 reusable roles</span><span class="chip">3 separate domains</span><span class="chip">No network needed</span><span class="chip">Local search &amp; context tools</span></div></section>
<section class="cards" aria-label="Domains">
<button class="card" style="--accent:#368a80" data-doc="domains/personal/README.md"><small>01 / Personal</small><h3>Personal &amp; work</h3><p>Organize, plan, learn, and reflect with explicit preferences and useful continuity.</p><span>Explore four specialist roles →</span></button>
<button class="card" style="--accent:#3c79b4" data-doc="domains/software/README.md"><small>02 / Software</small><h3>Software &amp; research</h3><p>Design, build, debug, and preserve versioned technical evidence.</p><span>Explore four specialist roles →</span></button>
<button class="card" style="--accent:#b78639" data-doc="domains/business/README.md"><small>03 / Business</small><h3>Business &amp; content</h3><p>Develop strategy, repeatable operations, grounded content, and clear analysis.</p><span>Explore four specialist roles →</span></button>
</section>
<div class="flow"><b>Choose one scope</b><i>→</i><b>Coordinate</b><i>→</i><b>Specialist work</b><i>→</i><b>Review</b><i>→</i><b>Draft memory</b><i>→</i><b>Owner approval</b></div><p class="flow-label">One local model can perform these roles sequentially. No background agent runner is installed.</p>
<section class="document" aria-label="Selected document"><div class="toolbar"><span id="docpath"></span><a href="ROLE_MAP.html">Explore the role map ↗</a><a id="raw" href="START_HERE.md">Open source file ↗</a></div><article class="docbody" id="document"></article></section>
<p class="note">This is an offline snapshot of the instruction library. It excludes live memory, source collections, projects, and session notes. Use the local memory tool to search records. Rebuild this page with <code>python tools/build_browser.py</code> after changing the manuals. No model is installed or connected.</p>
</main>
</div>
<script id="library" type="application/json">__LIBRARY_DATA__</script>
<script>
'use strict';
const docs=JSON.parse(document.getElementById('library').textContent);
const byPath=new Map(docs.map(d=>[d.path,d]));
const search=document.getElementById('search'),group=document.getElementById('group'),results=document.getElementById('results');
let selected='START_HERE.md';
function normalize(base,ref){const parts=(base.slice(0,base.lastIndexOf('/')+1)+ref).split('/'),out=[];for(const p of parts){if(p==='..')out.pop();else if(p&&p!=='.')out.push(p)}return out.join('/')}
function inline(el,text,base){const pattern=/(`[^`]+`|\*\*[^*]+\*\*|\[[^\]]+\]\([^)]+\))/g;let pos=0;for(const m of text.matchAll(pattern)){el.append(document.createTextNode(text.slice(pos,m.index)));const t=m[0];if(t.startsWith('`')){const c=document.createElement('code');c.textContent=t.slice(1,-1);el.append(c)}else if(t.startsWith('**')){const b=document.createElement('strong');b.textContent=t.slice(2,-2);el.append(b)}else{const match=t.match(/^\[([^\]]+)\]\(([^)]+)\)$/);const ref=normalize(base,match[2].split('#')[0]);const target=byPath.has(ref)?ref:byPath.has(ref+'/README.md')?ref+'/README.md':null;if(target){const a=document.createElement('a');a.href='#'+encodeURIComponent(target);a.textContent=match[1];el.append(a)}else el.append(document.createTextNode(match[1]+' ('+match[2]+')'))}pos=m.index+t.length}el.append(document.createTextNode(text.slice(pos)))}
function render(doc){const area=document.getElementById('document');area.replaceChildren();if(doc.path.endsWith('.json')){const pre=document.createElement('pre');pre.textContent=doc.text;area.append(pre);return}const lines=doc.text.split('\n');let i=0;while(i<lines.length){let s=lines[i];if(!s.trim()){i++;continue}if(s.startsWith('```')){const block=[];i++;while(i<lines.length&&!lines[i].startsWith('```'))block.push(lines[i++]);i++;const pre=document.createElement('pre');pre.textContent=block.join('\n');area.append(pre);continue}const h=s.match(/^(#{1,6})\s+(.*)$/);if(h){const e=document.createElement('h'+Math.min(h[1].length,4));inline(e,h[2],doc.path);area.append(e);i++;continue}if(s.startsWith('|')){const wrap=document.createElement('div');wrap.className='tablewrap';const table=document.createElement('table');let row=0;while(i<lines.length&&lines[i].startsWith('|')){const cells=lines[i++].split('|').slice(1,-1).map(x=>x.trim());if(cells.every(c=>/^:?-+:?$/.test(c)))continue;const tr=document.createElement('tr');for(const value of cells){const td=document.createElement(row===0?'th':'td');inline(td,value,doc.path);tr.append(td)}table.append(tr);row++}wrap.append(table);area.append(wrap);continue}const list=s.match(/^(- |\d+\. )(.*)$/);if(list){const ordered=/^\d/.test(s),ul=document.createElement(ordered?'ol':'ul');while(i<lines.length){const item=lines[i].match(ordered?/^\d+\. (.*)$/:/^- (.*)$/);if(!item)break;const li=document.createElement('li');inline(li,item[1],doc.path);ul.append(li);i++}area.append(ul);continue}const paragraph=[s];i++;while(i<lines.length&&lines[i].trim()&&!/^(#|```|\||- |\d+\. )/.test(lines[i]))paragraph.push(lines[i++]);const p=document.createElement('p');inline(p,paragraph.join(' '),doc.path);area.append(p)}}
function show(path){const doc=byPath.get(path)||byPath.get('START_HERE.md');selected=doc.path;document.getElementById('docpath').textContent=doc.path;document.getElementById('raw').href=doc.path;render(doc);list()}
function list(){const q=search.value.trim().toLowerCase();const terms=q.split(/\s+/).filter(Boolean);const matches=docs.filter(d=>(group.value==='all'||d.group===group.value)&&terms.every(t=>(d.title+' '+d.path+' '+d.text).toLowerCase().includes(t)));results.replaceChildren();document.getElementById('count').textContent=matches.length+' documents';for(const d of matches){const b=document.createElement('button');b.className='navitem';b.textContent=d.title;b.setAttribute('aria-current',String(d.path===selected));b.addEventListener('click',()=>{location.hash=encodeURIComponent(d.path)});results.append(b)}if(!matches.length){const e=document.createElement('div');e.className='empty';e.textContent='No matching documents. Try fewer words or another area.';results.append(e)}}
search.addEventListener('input',list);group.addEventListener('change',list);
document.querySelectorAll('[data-doc]').forEach(b=>b.addEventListener('click',()=>location.hash=encodeURIComponent(b.dataset.doc)));
document.getElementById('home').addEventListener('click',()=>{search.value='';group.value='all';location.hash=encodeURIComponent('START_HERE.md');show('START_HERE.md')});
function fromHash(){let p='START_HERE.md';try{p=decodeURIComponent(location.hash.slice(1))||p}catch{}show(p)}
window.addEventListener('hashchange',fromHash);fromHash();
</script>
</body></html>'''


def main():
    library = documents(ROOT)
    payload = json.dumps(library, ensure_ascii=False).replace('<', '\\u003c').replace('\u2028', '\\u2028').replace('\u2029', '\\u2029')
    output = ROOT / 'START_HERE.html'
    output.write_text(PAGE.replace('__LIBRARY_DATA__', payload), encoding='utf-8')
    print(f'Built {output.name}: {len(library)} instruction documents; live memory excluded.')


if __name__ == '__main__':
    main()
