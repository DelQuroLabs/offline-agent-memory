# Start here

For a visual overview, open [the interactive role map](ROLE_MAP.html) or [the static outline](ROLE_MAP.png). Select a role to see its purpose.

## 1. Choose the compartment

- **Personal**: organize your life and work, learn, plan, and reflect.
- **Software**: understand systems, write software, investigate defects, and retain technical evidence.
- **Business**: operate a business, develop content, and reason about performance.

Choose one primary domain for each task. A cross-domain project gets separate tasks and a reviewed summary for the shared folder. The coordinator does not need access to every file to coordinate work.

## 2. Start with three roles

Use **Coordinator → one Specialist → Quality Reviewer**. Add Memory Steward after the work produces something worth remembering. The remaining roles are available when needed; do not create meetings between bots for trivial work.

For a first session, read [the session contract](config/session-contract.md), your [agent card](agents/ROLE_CATALOG.md), and the relevant domain README. Paste those into your local model with a clear task. The model can help even before you add memory.

## 3. Understand the distinction

An **agent** is a role plus tools plus a session. A **model** generates responses. A **memory record** is stored evidence outside the model. A **context packet** is the small selection of role instructions and memories you provide for one task. A **repository** organizes and preserves all of this.

Nothing here assumes the model will remember past chats by itself. The files carry continuity between sessions and between local models.

## 4. Capture your first real memory

Write a short note in `work/my-note.md`. Keep it to one durable claim or procedure and include the evidence you actually have. Then:

```powershell
python tools/memory.py add --scope personal --kind preference --title "Preferred planning format" --body-file work/my-note.md --source "owner statement, dated locally" --excerpt "The exact supporting statement" --tags planning
```

The command prints an ID. Inspect the new JSON file under `domains/personal/memory/records/`. When you have checked its wording and source, replace `MEMORY_ID` below with the actual ID:

```powershell
python tools/memory.py state --scope personal --id MEMORY_ID --to active --reviewer owner --reason "Checked against my original statement" --review-days 90
python tools/memory.py search --scope personal --query "planning format"
```

The reviewer name is a local annotation, not an authenticated identity. Keep write access with the operator while learning the system.

## 5. Build a bounded prompt

```powershell
python tools/memory.py packet --scope personal --agent pe-planner --task "Plan my week using my planning format" --max-chars 14000 --out work/weekly-plan-context.md
```

Inspect the file and provide it to your local model. The budget is measured in characters, not tokens. Model token counts vary; leave room for the model's answer and reduce the packet if your runtime reports a context limit. The packet does not include every document in the repository.

## 6. Close the loop

Save the useful result in the domain's `projects/` folder. Record the decision and evidence. Have the Memory Steward propose durable memories. Review before activation. Let temporary details expire or stay in session notes. Run `verify` after manual edits and before using a collection restored from backup.

## Where to go next

- [Architecture](docs/ARCHITECTURE.md): the whole design.
- [Agent catalog](agents/ROLE_CATALOG.md): choose a role.
- [Memory handbook](docs/MEMORY_HANDBOOK.md): what to store and how.
- [Command guide](docs/COMMANDS.md): all implemented tools.
- [Offline runtime checklist](docs/OFFLINE_RUNTIME.md): connect the files to a local model.
- [30-day rollout](docs/ROLLOUT.md): grow the system without creating clutter.
