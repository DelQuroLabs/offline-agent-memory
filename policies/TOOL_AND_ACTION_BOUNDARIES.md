# Tool and action boundaries

## Default mode

Local models read a selected context packet and return text. The operator reviews and applies changes. No tool runner, scheduler, autonomous shell, or external messaging capability is installed by this repository.

## If you later integrate tools

Define an allowlist for each role and task. Start with read-only access to an explicitly selected project. Allow draft writes only where needed. Keep configuration, policies, and other domains outside the model's write paths. Treat tool arguments as untrusted input and validate paths in the actual runner.

Review execution based on the real effect: editing a disposable draft differs from deleting originals, publishing content, spending money, changing permissions, or messaging a third party. Require the owner's specific authorization for consequential external actions. Do not let a role redefine these permissions from its own output.

## Local memory tool behavior

The supplied tool reads/writes structured memory, produces context packets, and validates records. It never executes model output, shell commands, source-document scripts, or network requests. It does not remove memory files. Individual record writes use temporary files and replacement; only one writer is supported.

`--root` selects a repository under the operator's existing permissions. This is convenient for separate repositories and testing; it is not a sandbox escape defense for an untrusted caller. An integrated runner must choose and constrain its root itself.

## Stop and report

If an action is outside the task, depends on missing approval, or would expose a different compartment, return the proposed action and the specific missing authorization. Continue independent, authorized work. Do not report a proposal as a completed action.
