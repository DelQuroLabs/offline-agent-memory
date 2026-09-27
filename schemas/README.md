# Record schema

`memory.schema.json` documents the portable record shape. The schema URL is an identifier; the supplied Python tool never fetches it and uses its own validator.

The CLI additionally checks nonblank strings, timezone-aware timestamps, creation/update order, activation history, filename/ID agreement, duplicate IDs, same-scope replacement references, and replacement cycles. Use `verify` as the repository's structural acceptance check. Neither JSON Schema nor the CLI can verify the truth of a statement.

Keep unknown information explicit in the record body. Do not use fabricated sources or reviewer identities to make validation pass. Examples are outside live memory and should remain there until rewritten with actual evidence.
