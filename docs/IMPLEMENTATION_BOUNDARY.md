# Implementation boundary

| Capability | Present status |
|---|---|
| Three domain folders and shared library | Implemented as files |
| 18 role definitions and routing rules | Implemented as reusable instructions |
| Draft capture and state transitions | Implemented in CLI |
| Scoped keyword retrieval | Implemented in CLI |
| Private/overdue opt-in; restricted exclusion | Implemented in CLI |
| Bounded context packet creation | Implemented in CLI |
| Evidence fields and history | Implemented as editable records |
| Structural record validation | Implemented in CLI and tests |
| Semantic truth checking | Human/model review; not automatically verified |
| Local model inference | User-provided runtime; not installed or connected |
| Role execution, handoffs, scheduling | Manual workflows and templates |
| Authenticated reviewer identities | Not implemented |
| OS-level access control or encryption | Must be provided externally |
| Client/project-level retrieval restrictions | Not implemented; use separate repositories for strict isolation |
| Conflict detection by meaning | Manual review; no automatic semantic detector |
| Concurrent writers and transactions | Not supported; use one writer |
| Vector search, embeddings, automatic ingestion | Future options, not required |
| Network blocking | Not configured by this repository |
| Backup/restore | Documented owner procedure, no automatic backup service |

The CLI does not read unrelated domain memory during a scoped search. It is nevertheless a local program running under the operator's permissions, not a security sandbox. Anyone with direct filesystem access can open or edit files outside the CLI. For stronger isolation, use separate OS accounts, filesystem permissions, containers, or physically separated repositories as appropriate to your environment.

An agent cannot gain authority by editing a role card. Keep policies and configuration operator-owned, and give integrated models only the working paths needed for the task. The code validates structure but cannot stop a human with file access from fabricating a history event. Keep independent protected backups or a version history when provenance matters.
