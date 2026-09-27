# Memory handbook

## Memory layers

| Layer | Store | Lifetime | Intended use |
|---|---|---|---|
| Working context | A local model session and `work/` packet | One task | Immediate reasoning inputs |
| Session journal | Domain `sessions/` | Review periodically | What happened and what remains open |
| Project record | Domain `projects/` and `decisions/` | Project plus retention needs | Deliverables, choices, evidence |
| Durable memory | Domain `memory/records/` | Until replaced, expired, or archived | Reusable facts and procedures |
| Shared memory | `shared/memory/records/` | Reviewed periodically | Cross-domain conventions and approved knowledge |

Do not copy every conversation into durable memory. A transcript is a source, not an automatically reliable fact database. Preserve concise, auditable conclusions and a reference to the evidence.

## Seven durable types

- **fact**: a supported descriptive claim with a defined context and time.
- **preference**: an explicit owner or stakeholder preference, not a personality inference.
- **procedure**: repeatable steps, prerequisites, checks, and failure handling.
- **decision**: choice, rationale, alternatives, owner, and reversal trigger.
- **episode**: a bounded event summary with observed results.
- **lesson**: a takeaway connected to an actual episode and its limits.
- **entity**: a stable description of a project, system, term, or organization, with only necessary attributes.

## A good record

Store one main idea. Use a concrete title and a body that names the conditions under which it applies. Add a source reference and a short supporting excerpt. Set the narrowest useful scope and the correct classification. Use tags for discovery, not access control. State uncertainty in words; the optional confidence value is only an operator annotation and does not drive ranking.

Example: “Project A validates a backup by restoring into a temporary directory and comparing file hashes.” This is more useful than “Backups are good.” If you have only proposed that process, store it as a draft procedure rather than a fact about what Project A already does.

## Lifecycle

`draft → active → disputed / deprecated / archived`

A disputed record can return to active after a documented review. An active record can be reviewed again to renew its review date. Deprecated records can be archived. Archived records remain historical; create a new corrected record rather than reactivating one. The tools do not delete records.

`review_after` means “review before ordinary reuse.” Overdue memories are excluded by default and can be deliberately included with a visible warning. `expires_at` means “do not use after this instant”; expired records remain excluded even when overdue material is allowed. Use timezone-aware ISO dates.

## Promotion rubric

Check source quality, accurate wording, reusable value, correct scope, sensitivity, duplication, conflicts, and an appropriate review interval. Confidence alone never activates memory. For shared material, check that every body sentence and source excerpt can be shown in all three domains. Shared activation requires a separate explicit flag in the CLI.

## Conflicts and corrections

When two sources disagree, preserve both references. Mark the unreliable active claim `disputed` while investigating. A correction should be a new record; put the older same-scope ID in the new record's `supersedes` list and validate the repository. Once the replacement is active and eligible for retrieval, the old item is suppressed. Also mark the old record deprecated so it cannot resurface when the replacement expires or becomes disputed.

These updates are a manual multi-step process; the CLI has no transactional replacement command. Use one writer at a time. An archived or deprecated status is preferable to silently rewriting the meaning of an existing record.

## Retention defaults to adapt

Review fast-changing operational facts in 30 days, ordinary preferences and procedures in 90 days, and durable conceptual notes in 180 days. These are starting suggestions, not legal retention requirements. Session scratch can be pruned after useful decisions and lessons are preserved. Backup retention and deletion are owner-controlled, including old snapshots and copied context packets.
