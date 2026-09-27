# Personal and work knowledge

Scope ID: `personal`

Organize commitments, make realistic plans, learn, and reflect.

## Specialists

- [Personal & Work Organizer](agents/pe-organizer.md): Turn scattered notes and obligations into a clear, owner-reviewed inventory.
- [Personal & Work Planner](agents/pe-planner.md): Create feasible plans using explicit priorities, time limits, and dependencies.
- [Learning Coach](agents/pe-learning-coach.md): Turn an learning objective into evidence-based practice using local materials.
- [Reflection Analyst](agents/pe-reflection-analyst.md): Help the owner review events and decisions without overinterpreting personal data.

The six core roles can support this domain in a separate `personal` session. Their access remains limited to this domain and shared memory.

## How work moves

Organizer triages notes → Planner chooses a feasible next action → specialist produces an artifact → Reviewer checks assumptions → Steward proposes reusable memory.

## Example uses

- Prepare a weekly plan from confirmed commitments.
- Build a local study plan from saved materials.
- Summarize project decisions without copying an entire diary.

## Folder responsibilities

`agents/` contains role instructions. `memory/records/` contains structured durable memory. `sources/` preserves evidence. `projects/` contains active outcomes and deliverables. `sessions/` contains bounded work notes. `decisions/` records significant choices. `inbox/` holds unprocessed material. `archive/` holds retired project material; archived memory records remain in `memory/records/` with archived status.

## Boundaries

Private journal material belongs here and should normally be classified private. Do not treat inferred personality or health conclusions as facts. Employer or client material with separate confidentiality requirements belongs in a separately protected repository.

Shared memory may be read, but nothing in this domain is automatically shared. Use the sharing playbook and a separately reviewed draft when cross-domain reuse is justified. Tags and project folders organize material; they do not add new CLI access boundaries.

## First step

Create one project from `templates/project-brief.md`, run one real task, and review one useful memory proposal. Expand from demonstrated needs.
