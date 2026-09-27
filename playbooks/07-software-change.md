# Software: a bounded engineering change

Coordinator defines the behavior to change. Architect records design constraints when needed. Builder inspects the local code and implements the change if tool access is enabled. Debugger investigates observed failures. Reviewer evaluates relevant behavior, failure modes, and actual validation results.

Deliverables: the change or patch, a concise rationale, meaningful test evidence, and remaining limitations. A text-only model can return a proposed patch but must not claim it applied or tested it.

Memory candidates: a verified root cause, a system invariant, a repeatable validation procedure, or a consequential design decision. Keep temporary logs in sources and redact secrets before adding them to context.
