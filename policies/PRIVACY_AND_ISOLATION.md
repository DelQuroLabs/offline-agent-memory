# Privacy and isolation

## Four classifications

| Class | Intended handling | Default retrieval |
|---|---|---|
| public | Suitable for intentional public disclosure; still do not publish automatically | Included if otherwise eligible |
| internal | Ordinary repository-owner working material | Included if otherwise eligible |
| private | Sensitive material limited to its domain and necessary tasks | Excluded unless `--include-private` |
| restricted | Highly sensitive material kept out of model context | Always excluded |

Do not store passwords, API tokens, private keys, or recovery codes in this repository. Restricted classification is a retrieval exclusion, not a vault. Keep secrets in an appropriate separate protected store and record only a non-secret locator if necessary.

## Scope matrix

| Current session | Readable memory | Other domains |
|---|---|---|
| personal | personal + shared | excluded |
| software | software + shared | excluded |
| business | business + shared | excluded |
| shared | shared only | excluded |

The CLI enforces this matrix for its retrieval and packet commands. Raw filesystem access, backup archives, manually copied prompts, and external model tools are outside that boundary. Do not give a model broad filesystem access and expect a prompt to constrain it reliably.

## Practical compartmentalization

Use OS permissions to restrict who can open each repository. If multiple people or clients need different access, use separate repositories rather than tags in one domain. Protect backups and context packets with the same sensitivity as their contents. Avoid automatic cloud sync for material intended to remain local.

Shared memory accepts only public/internal records. Cross-domain copying is explicit and reviewed. Review source excerpts, titles, and local path names as well as bodies; metadata can reveal confidential information.

## Minimal disclosure

Give a role the minimum relevant evidence. A planning role usually needs commitments and constraints, not an entire journal. A content role needs approved claims, not full client records. A debugger often needs a redacted failure trace, not production secrets.

The repository does not configure encryption, OS accounts, network firewalls, or a sandbox. Document your actual controls in a local operator note rather than claiming these controls exist because the policy names them.
