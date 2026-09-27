# Using the repository with a local model

## Runtime-independent setup

The repository supplies instructions and memory; a local runtime supplies inference. Use a model and runtime you already have available and whose license fits your use. The repository makes no assumption about vendor, model name, parameter count, GPU, or operating system. No model was installed as part of this build.

Prepare the runtime, model files, tokenizer, and any required local dependencies before disconnecting. Confirm that a simple prompt works with the network disabled. A desktop interface can still call a remote service even when it looks local; inspect your chosen runtime's configuration and operating-system connections. The repository tools themselves contain no network client.

## Text-only mode

1. Select one domain and one role.
2. Generate a context packet with the CLI, or read the session contract and role card manually.
3. Provide the instructions using the runtime's supported system-instruction field when one exists; supply the task and retrieved records as reference context.
4. Ask for the defined output contract.
5. Save useful output in the selected domain's project folder.
6. Review memory proposals and apply approved changes using the operator-controlled CLI.

Do not assume that attaching a folder makes the model search it correctly or enforce its permissions. Packet generation is the supported bridge supplied here.

## Local tool-enabled mode: later integration

If you add a tool runner later, allowlist the exact operations and paths it needs. Start read-only. Treat a role card as behavioral guidance; actual access must be enforced by the runner or OS. Never give a model an unrestricted shell merely because its role says “Builder.” An inference server on localhost is still an integration that needs its own configuration and testing.

The repository intentionally leaves API adapters and background execution unconfigured. The task and handoff templates are portable contracts you can implement in the platform you choose.

## Context sizing

Start with a modest packet and a few relevant memories. Keep space for output. Character count is portable; token count depends on the tokenizer and language. Measure actual runtime token use before setting a reliable limit. For small context windows, shorten task wording, reduce retrieved records, and use compact role instructions.

## Practical acceptance test

Disconnect networking, start the runtime, ask a simple local question, provide a generated packet, and check that it cites the supplied memory ID. Change an active memory to disputed, generate a new packet, and confirm it disappears. Ask the software role for private personal memory and confirm the packet contains none. The model's refusal alone is not the test; inspect the actual data supplied.

Store runtime-specific settings in `config/local-runtime.example.json` only after copying it to your own local configuration file. The example is descriptive and is not read by the CLI.
