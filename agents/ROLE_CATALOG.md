# Agent role catalog

These are reusable roles for your local models. They are definitions, not running services. Use a short sequence of roles for one task and keep each session inside one selected domain.

| ID | Role | Group | Responsibility |
|---|---|---|---|
| `co-coordinator` | [Coordinator](../agents/core/co-coordinator.md) | core | Turn a request into a bounded task and route it to the smallest useful set of roles. |
| `co-memory-steward` | [Memory Steward](../agents/core/co-memory-steward.md) | core | Convert useful evidence into concise, traceable memory proposals. |
| `co-evidence-researcher` | [Evidence Researcher](../agents/core/co-evidence-researcher.md) | core | Find and compare relevant evidence in the authorized local source collection. |
| `co-quality-reviewer` | [Quality Reviewer](../agents/core/co-quality-reviewer.md) | core | Evaluate an artifact against the original task and evidence without inheriting its conclusions. |
| `co-privacy-guardian` | [Privacy Guardian](../agents/core/co-privacy-guardian.md) | core | Review proposed context, sharing, and source imports for unnecessary disclosure. |
| `co-archivist` | [Archivist](../agents/core/co-archivist.md) | core | Keep memory maintainable and recoverable while preserving useful history. |
| `pe-organizer` | [Personal & Work Organizer](../domains/personal/agents/pe-organizer.md) | personal | Turn scattered notes and obligations into a clear, owner-reviewed inventory. |
| `pe-planner` | [Personal & Work Planner](../domains/personal/agents/pe-planner.md) | personal | Create feasible plans using explicit priorities, time limits, and dependencies. |
| `pe-learning-coach` | [Learning Coach](../domains/personal/agents/pe-learning-coach.md) | personal | Turn an learning objective into evidence-based practice using local materials. |
| `pe-reflection-analyst` | [Reflection Analyst](../domains/personal/agents/pe-reflection-analyst.md) | personal | Help the owner review events and decisions without overinterpreting personal data. |
| `sw-architect` | [Software Architect](../domains/software/agents/sw-architect.md) | software | Translate requirements into a coherent design with explicit tradeoffs and boundaries. |
| `sw-builder` | [Software Builder](../domains/software/agents/sw-builder.md) | software | Implement a bounded, reviewable change in an authorized local project. |
| `sw-debugger` | [Debugger](../domains/software/agents/sw-debugger.md) | software | Find the cause of an observed failure and demonstrate an appropriate correction. |
| `sw-technical-researcher` | [Technical Researcher](../domains/software/agents/sw-technical-researcher.md) | software | Answer technical questions from a dated, local collection of primary sources. |
| `bu-strategist` | [Business Strategist](../domains/business/agents/bu-strategist.md) | business | Turn business goals and evidence into options, assumptions, and bounded experiments. |
| `bu-operations` | [Operations Designer](../domains/business/agents/bu-operations.md) | business | Create repeatable business procedures with ownership, checks, and exception handling. |
| `bu-content` | [Content Studio](../domains/business/agents/bu-content.md) | business | Create grounded, audience-appropriate content from an approved brief and source pack. |
| `bu-analyst` | [Business Analyst](../domains/business/agents/bu-analyst.md) | business | Explain business measurements with clear definitions, data quality checks, and uncertainty. |

## Minimum useful team

Coordinator chooses the scope and acceptance criteria. One specialist does the work. Quality Reviewer checks the result. Memory Steward captures what is reusable after the task. Privacy Guardian is useful when sharing or importing sensitive sources. Archivist is useful during periodic maintenance.

The same local model can perform each role in a fresh session using the corresponding context packet. A fresh reviewer session reduces conversational carryover but does not guarantee independence or correctness.

For a shared-only task, use a core role with `--scope shared`. Domain specialists cannot generate shared-scope packets. For new roles, follow `docs/EXPANSION_PLAN.md` from the repository root.
