# Verify an offline backup

Stop writes. Create a complete local snapshot. Record file count and checksums. Restore the snapshot into a separate location. Run `python tools/memory.py --root RESTORED_PATH verify` using the restored tool or the original tool with the explicit root. Compare file hashes against the snapshot inventory. Open several sources and agent cards, then build one context packet.

Record the exact snapshot, restore location, checks performed, and any missing files. Do not overwrite the live repository to test a backup. Protect temporary restore folders because they may contain the same sensitive data as the live copy.

The delivery ZIP is an initial snapshot only. Create new backups after adding your own memory. Optional checksum manifests detect accidental changes but do not prove authenticity if an attacker can modify the manifest too.
