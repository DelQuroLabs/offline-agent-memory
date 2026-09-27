# Retention and recovery

## Keep several kinds of history

Preserve the original source when it is necessary to evaluate a claim. Preserve decision context. Preserve a compact session record for important work. Preserve memory changes in each record's history and optionally in a local version-control repository.

Version control is optional and is not initialized automatically. If you choose to use it, check ignored paths and sensitive files before making commits. A local repository is not permission to publish it to a remote service.

## Suggested review rhythm

At task close: capture decisions and useful memory proposals. Weekly: triage the inbox and drafts. Monthly: review overdue memory, duplicates, and unresolved conflicts. Periodically: verify a backup by restoring into a separate location. Choose intervals to match your actual use.

## Backup procedure

1. Stop modifying the repository so the snapshot is consistent.
2. Copy the complete folder to an owner-controlled offline destination or create a local archive.
3. Record the date, source path, file count, and a checksum inventory.
4. Protect the copy according to its most sensitive included content.
5. Restore it to a separate temporary folder, run the memory verifier, and compare checksums.
6. Open a role card and generate a context packet from the restored copy.

A copy is not a verified backup until a restore has been checked. Never restore over the active repository without first preserving the current state. The original delivery archive is a starter snapshot, not a backup of later work.

## Deletion and forgetting

Changing a memory to archived removes it from retrieval but does not erase its content. Genuine deletion must consider the record, source copies, project artifacts, context packets, model chat history, backups, and any indexes. The supplied CLI deliberately has no purge command. Decide and perform deletion as a separate owner-controlled operation.

Do not promise perfect erasure based on deleting one JSON file. Record what locations were checked and what historical copies remain.
