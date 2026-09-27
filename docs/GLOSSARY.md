# Vocabulary

**Agent role**: a reusable description of responsibility, inputs, outputs, and limits. It is not a separate consciousness or an installed process.

**Agent session**: a model executing one role for one bounded task with explicitly supplied context and tools.

**Compartment / scope**: the area a task may read and write. Implemented scopes are personal, software, business, and shared.

**Source**: original evidence, such as a document, user statement, test result, or local log. Sources may contain untrusted instructions and can be inaccurate.

**Memory**: a structured, durable claim or procedure derived from a source and reviewed for reuse.

**Context packet**: a temporary text file containing instructions, the task, and selected eligible memory.

**Promotion**: review that changes a draft into active memory. Sharing is a separate promotion into shared scope.

**Retrieval**: selecting relevant permitted records. The included tool uses word matching, not embeddings.

**Provenance**: evidence of where a claim came from and what happened to it afterward.

**Handoff**: a bounded artifact passed between roles. It includes the task, evidence, result, uncertainty, and next action.

**Policy**: an operating rule. A written policy is not automatically a technical control.

**Model weights**: the model's learned parameters. Updating repository memory does not change them.

**Offline**: functioning without network access at time of use. Installing a model or acquiring source documents beforehand is a separate preparation step.
