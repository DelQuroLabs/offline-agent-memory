# Offline Agent Memory Repository

A substantial, local-first foundation for a personal AI agent team: **three independent domains, 18 defined roles, reusable workflows, and a searchable memory store**. Everything in this folder can be copied to an offline computer. The included tools use Python's standard library and make no network calls.

**Start with [START_HERE.md](START_HERE.md)** or open **[START_HERE.html](START_HERE.html)** in your browser for a searchable offline document library. Explore the roles in **[ROLE_MAP.html](ROLE_MAP.html)**, or open the **[static outline](ROLE_MAP.png)**.

## Your three separate areas

| Folder | What belongs here | Specialist roles |
|---|---|---|
| [domains/personal](domains/personal/README.md) | Personal and work organization, plans, learning, reflection | Organizer, Planner, Learning Coach, Reflection Analyst |
| [domains/software](domains/software/README.md) | Software engineering, debugging, architecture, technical research | Architect, Builder, Debugger, Technical Researcher |
| [domains/business](domains/business/README.md) | Business planning, operating procedures, content, performance analysis | Strategist, Operations Designer, Content Studio, Business Analyst |

Six reusable support roles serve one selected domain per session: Coordinator, Memory Steward, Evidence Researcher, Quality Reviewer, Privacy Guardian, and Archivist. A role is a set of instructions and boundaries. You can run all roles sequentially on one local model.

## What is implemented

- Plain Markdown role cards, policies, playbooks, templates, and domain maps.
- One JSON file per memory, with evidence, status, classification, review date, and change history.
- Local draft capture, review transitions, search, and size-limited context packet generation.
- Scope filtering: a personal session receives personal plus shared records; the equivalent applies to software and business.
- Draft, disputed, deprecated, archived, expired, and restricted records are excluded from ordinary retrieval. Private and overdue records require explicit flags.
- A test suite for the boundaries that matter, worked examples, and an offline HTML library.

## What this foundation does not do automatically

It does not install or download an AI model, run a background agent swarm, enforce operating-system permissions, or provide semantic/vector search. There is no cloud account, API key, server, subscription, or package install required for the repository tools. Your local model runtime is a separate component. The included CLI does not invoke models or execute model-generated commands.

The roles and policies describe the intended operating system for your team; the CLI implements a small, useful part of it. The [implementation boundary](docs/IMPLEMENTATION_BOUNDARY.md) identifies which parts are enforced, manual, or future work.

## Fast local commands

Run these from this repository folder with Python 3.10 or later already available locally. On Windows, `py` may be available instead of `python`.

```powershell
python tools/memory.py verify
python tools/memory.py agents
python tools/memory.py search --scope software --query "offline memory"
python tools/memory.py packet --scope software --agent sw-architect --task "Design a simple offline memory workflow" --out work/software-context.md
python -m unittest discover -s tests -v
```

Read the packet, then provide it to your local model using its supported prompt or file interface. A generated packet is a snapshot; rebuild it after memory changes. The tool refuses to overwrite an existing packet, so use a new filename for each run.

## Directory guide

`config/` holds the agent registry and session contract. `agents/core/` holds reusable support roles. `domains/` holds the three separate systems. `shared/` holds approved cross-domain memory and common reference material. `docs/` explains architecture and operation. `policies/` defines boundaries. `playbooks/` describes complete workflows. `templates/` provides blank records. `examples/` contains fictional demonstrations, excluded from live retrieval. `tools/` and `tests/` provide the working local utilities. `work/` holds disposable session packets and scratch work.

The repository is a memory and operating manual, not a model training dataset by default. Editing memory does not retrain model weights. Do not put credentials or secret keys here. See [privacy and isolation](policies/PRIVACY_AND_ISOLATION.md) before adding sensitive material.
