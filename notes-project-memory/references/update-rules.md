# Update Rules

## Before Writing

- Read the target file first if it exists.
- Preserve user-written sections and wording unless they are obsolete or contradicted by verified facts.
- Prefer section-level edits over full rewrites.
- Avoid duplicate bullets; merge related facts.

## Fact Quality

- Mark a command as verified only when it was actually run or the user explicitly says it is verified.
- If a fact is inferred from source files or documentation, word it as an observation, not an absolute guarantee.
- Include dates for status changes, verified commands, major decisions, and investigation results.
- Update or remove stale guidance as soon as it is discovered.

## Safety

- Do not store secrets, credentials, access tokens, private keys, or personal data unrelated to the project.
- Do not store temporary scratch notes unless the user asks to preserve them as durable project context.
- If the notes workspace is a git repo, do not commit by default. Report changed paths and git status.

## Reporting

After a write, tell the user:

- Which project folder was used.
- Which note files changed.
- Whether the content was created, updated, or only read.
- Any ambiguity that remains, such as an inferred project slug or unverified command.
