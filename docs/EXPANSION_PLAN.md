# Expand the repository without losing control

## Add a role

Copy `templates/agent-card.md`. Give it one outcome, a unique ID, one permitted scope or explicit core scope list, concrete inputs, a precise output contract, and measurable completion checks. Add the card to `config/agents.json`. Use `packet` to confirm its scope restrictions. The command reads the registry, so no new Python code is needed for a new role within existing scopes.

Do not add a role merely for a new tone or personality. A task variant can be a template. Examples of justified additions are a code migration specialist with a migration plan output or a research synthesis specialist with a source-comparison matrix.

## Add a project

Create a folder under the chosen domain's `projects/` and copy the project brief, task, decision, and review templates as needed. Use project IDs in tags and evidence references. Remember that tags do not restrict retrieval inside a domain.

## Add a stricter compartment

The current CLI has fixed scope names. A folder added under `domains/` is not automatically supported. For confidential clients or unrelated owners, start with a separate repository copy and separate permissions. Expanding the scope model in code requires updating validation, routing, tests, and documentation together.

## Add retrieval capabilities

Keep JSON records authoritative. An index must be disposable and rebuildable. Apply scope and classification restrictions before supplying candidates to a model, and recheck them after ranking. Preserve record IDs and evidence in all generated summaries. Evaluate retrieval against known answers before replacing the simple search.

## Add automation

Start with draft-only operations and an allowlist. Separate proposal, review, and execution. Record inputs, outputs, tool evidence, and failure states. Add a queue and writer lock before concurrent writers. Add resource limits, cancellation, and recovery before unattended runs. Prevent role outputs from changing their own permissions.

## Avoid premature complexity

Do not start with a vector database, multi-model router, scheduler, graph store, and dozens of autonomous bots at once. The repository already provides deep definitions; turn on operational complexity only when a concrete workflow requires it and you can test it offline.
