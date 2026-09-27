# Naming and versions

Memory IDs use `mem-` plus a random 32-character hexadecimal identifier. The filename matches the ID. Do not encode private names or secrets in IDs. Human-readable titles belong inside records.

Use lowercase folder names and short descriptive filenames. Suggested project IDs are `personal-learning-plan`, `software-offline-search`, and `business-content-pilot`. Add dates to session and decision filenames when order matters. Use ISO timestamps with timezone offsets in memory records.

Keep source filenames stable when possible. If a source is moved, update its locators or leave a documented redirect note. A source reference is not automatically verified by the memory tool.

The initial record schema version is 1. Do not silently change schema meaning. A future migration should preserve old backups, validate every new record, and include a reversible migration note. Agent IDs remain stable even if a role's display name changes.

Tag vocabulary should be small and consistent. Tags support retrieval; they do not grant access. Project and client isolation requires a real access boundary, not a naming convention.
