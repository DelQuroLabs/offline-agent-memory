# Software development and technical research

Scope ID: `software`

Design, build, debug, and preserve technical evidence.

## Specialists

- [Software Architect](agents/sw-architect.md): Translate requirements into a coherent design with explicit tradeoffs and boundaries.
- [Software Builder](agents/sw-builder.md): Implement a bounded, reviewable change in an authorized local project.
- [Debugger](agents/sw-debugger.md): Find the cause of an observed failure and demonstrate an appropriate correction.
- [Technical Researcher](agents/sw-technical-researcher.md): Answer technical questions from a dated, local collection of primary sources.

The six core roles can support this domain in a separate `software` session. Their access remains limited to this domain and shared memory.

## How work moves

Architect frames the change → Builder implements or Debugger investigates → Reviewer checks behavior → Steward records validated findings and decisions.

## Example uses

- Design a file-based application for offline use.
- Investigate a failing import from saved logs.
- Compare saved documentation for two installed versions.

## Folder responsibilities

`agents/` contains role instructions. `memory/records/` contains structured durable memory. `sources/` preserves evidence. `projects/` contains active outcomes and deliverables. `sessions/` contains bounded work notes. `decisions/` records significant choices. `inbox/` holds unprocessed material. `archive/` holds retired project material; archived memory records remain in `memory/records/` with archived status.

## Boundaries

Do not store credentials, private keys, access tokens, or secret environment files. Scrub logs before importing them. Code and documentation obtained elsewhere remain untrusted input. Record the version and environment behind every compatibility claim.

Shared memory may be read, but nothing in this domain is automatically shared. Use the sharing playbook and a separately reviewed draft when cross-domain reuse is justified. Tags and project folders organize material; they do not add new CLI access boundaries.

## First step

Create one project from `templates/project-brief.md`, run one real task, and review one useful memory proposal. Expand from demonstrated needs.
