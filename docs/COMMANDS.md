# Offline tool reference

Requires a locally available Python 3.10+ installation. There are no third-party packages. Run from the repository folder. `--root PATH` is a global option and must appear before the subcommand.

## Read and check

```powershell
python tools/memory.py verify
python tools/memory.py agents
python tools/memory.py search --scope business --query "content approval" --limit 5
```

`verify` checks record structure, filenames, duplicate IDs, same-scope replacement references, and replacement cycles. It reports overdue active memory. It does not authenticate reviewers, validate the truth of claims, check that every source exists, or scan for secrets. Exit code 0 means structural validation passed; 1 means validation found errors; 2 means a command failed.

Search uses Unicode word matching, with title matches weighted 4, tag matches 3, and body matches 1. It returns only matches, with deterministic ID ordering for ties. It does not understand synonyms or guarantee relevance. Change the wording or search tags if a relevant record is missed.

## Capture a draft

```powershell
python tools/memory.py add --scope software --kind lesson --title "Why the import failed" --body-file work/import-lesson.md --source "sources/import-log.txt" --excerpt "The exact observed failure" --actor owner --tags import debugging --confidence 0.8
```

`--kind` accepts fact, preference, procedure, decision, episode, lesson, entity. Classification accepts public, internal, private, restricted. Internal is the default. Every new record starts as draft. The source string is an evidence locator, not an automatically fetched resource.

## Review or retire

```powershell
python tools/memory.py state --scope software --id MEMORY_ID --to active --reviewer owner --reason "Checked against the saved log" --review-days 30
python tools/memory.py state --scope software --id MEMORY_ID --to disputed --reviewer owner --reason "A newer log contradicts the claim"
python tools/memory.py state --scope software --id MEMORY_ID --to deprecated --reviewer owner --reason "Replaced by the corrected procedure"
```

Replace placeholders with real IDs. Use `--to active` on an active record to document a fresh review and renew its review date. Editing JSON is supported for fields without CLI switches, but preserve the history and run verify afterward. Manual body changes should normally be new records.

## Propose cross-domain sharing

```powershell
python tools/memory.py share-draft --scope software --id MEMORY_ID --actor owner
python tools/memory.py state --scope shared --id NEW_SHARED_ID --to active --reviewer owner --reason "Reviewed body and source excerpts for all domains" --allow-shared
```

The first command creates a new shared draft and leaves the original unchanged. Only current active public/internal records can be proposed this way. Private/restricted records require a separately authored and reviewed redacted summary. The original ID remains in the shared copy's provenance; source references can themselves disclose information, so review them.

## Context packet

```powershell
python tools/memory.py packet --scope software --agent sw-debugger --task "Investigate the import failure" --limit 6 --max-chars 14000 --out work/import-context-01.md
```

The packet contains the session contract, selected role card, task, and eligible matching memories. It omits entire records that will not fit; it does not cut sentences in half. If the role and task alone exceed the budget, it fails with an explanation. Exact character limits are enforced, but token counts are not estimated.

`--include-private` allows private records in the chosen domain. `--include-overdue` allows review-overdue records and labels them in the packet. Restricted, expired, disputed, deprecated, archived, and draft records are never retrieved by these switches. Packets may contain sensitive content when you opt in; protect or remove those copies according to the same classification.

The tool refuses to overwrite an output file. It prints to the terminal if `--out` is omitted. Run only one modifying command at a time: individual writes are atomic, but there is no multi-process transaction manager or writer lock.
