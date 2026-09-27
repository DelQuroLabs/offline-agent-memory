# Business operations and content creation

Scope ID: `business`

Plan work, standardize operations, create grounded content, and interpret results.

## Specialists

- [Business Strategist](agents/bu-strategist.md): Turn business goals and evidence into options, assumptions, and bounded experiments.
- [Operations Designer](agents/bu-operations.md): Create repeatable business procedures with ownership, checks, and exception handling.
- [Content Studio](agents/bu-content.md): Create grounded, audience-appropriate content from an approved brief and source pack.
- [Business Analyst](agents/bu-analyst.md): Explain business measurements with clear definitions, data quality checks, and uncertainty.

The six core roles can support this domain in a separate `business` session. Their access remains limited to this domain and shared memory.

## How work moves

Strategist frames an objective → Operations Designer or Content Studio creates the artifact → Analyst checks available measurements → Reviewer checks claims → Steward records approved reusable knowledge.

## Example uses

- Create an internal client intake procedure.
- Draft a newsletter from an approved source pack.
- Analyze supplied campaign data with explicit metric definitions.

## Folder responsibilities

`agents/` contains role instructions. `memory/records/` contains structured durable memory. `sources/` preserves evidence. `projects/` contains active outcomes and deliverables. `sessions/` contains bounded work notes. `decisions/` records significant choices. `inbox/` holds unprocessed material. `archive/` holds retired project material; archived memory records remain in `memory/records/` with archived status.

## Boundaries

Keep client-sensitive records private and isolate clients in separate repositories when access must differ. Treat forecasts as assumptions, not facts. Content remains a draft until the owner authorizes publication through an actual tool or external workflow.

Shared memory may be read, but nothing in this domain is automatically shared. Use the sharing playbook and a separately reviewed draft when cross-domain reuse is justified. Tags and project folders organize material; they do not add new CLI access boundaries.

## First step

Create one project from `templates/project-brief.md`, run one real task, and review one useful memory proposal. Expand from demonstrated needs.
