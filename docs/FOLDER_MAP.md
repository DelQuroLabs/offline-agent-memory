# Folder map

The three domain folders use the same structure, so you can move between them without learning a new filing system.

```text
offline-agent-memory/
├── START_HERE.html             Searchable offline instruction library
├── ROLE_MAP.html               Interactive role outline
├── ROLE_MAP.png                Static role outline
├── agents/
│   ├── ROLE_CATALOG.md         All 18 roles
│   └── core/                  Six support roles
├── domains/
│   ├── personal/              Personal and work
│   ├── software/              Software and technical research
│   └── business/              Business operations and content
├── shared/
│   ├── memory/records/        Explicitly shared JSON memories
│   └── sources/               Supporting evidence
├── config/                    Agent registry and session contract
├── docs/                      Architecture and operating manuals
├── policies/                  Privacy, evidence, review, retention
├── playbooks/                 Complete workflows
├── templates/                 Reusable task and record formats
├── examples/                  Fictional demonstrations
├── schemas/                   Memory record format
├── tools/                     Local memory and library utilities
├── tests/                     Automated behavior checks
└── work/                      Temporary context packets
```

Each domain contains:

```text
personal/   or   software/   or   business/
├── README.md                  Purpose and boundaries
├── TAXONOMY.md                Suggested knowledge areas and tags
├── WORKFLOW.md                How work moves through this domain
├── agents/                    Four specialist role cards
├── memory/records/            Durable structured memories
├── sources/                   Original evidence
├── projects/                  Deliverables organized by outcome
├── sessions/                  What happened during a task
├── decisions/                 Choices and their rationale
├── inbox/                     Material awaiting classification
└── archive/                   Retired project material
```

Folders organize your information. The local memory tool enforces the domain choice when selecting records for a packet. Direct filesystem isolation still depends on your actual local permissions.

The archive folder holds retired project files. An archived memory remains in memory/records with an archived status and is excluded from retrieval. This keeps its history and stable ID intact.
