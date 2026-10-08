---
name: auto-commit-hook
description: User-level Stop/SessionEnd hook that auto-commits (never pushes) in every git repo; how it works and how to opt out
metadata:
  node_type: memory
  type: reference
  originSessionId: 8673308d-c568-4b54-9362-2ac060cc6404
  modified: 2026-10-07T10:07:08.147Z
---

On 2026-10-07 the user asked for auto-commit across all projects and chats. Implemented as a user-level hook:
- `C:\Users\MITE\.claude\settings.json` registers `Stop` and `SessionEnd` hooks that run `bash "$HOME/.claude/hooks/auto-commit.sh"`.
- The script commits all changes in the current git repo (never pushes, never `git init`, uses the user's name/email via `-c` because no global git identity exists).
- Guards: skips non-repos, home dir, detached HEAD, merge/rebase in progress, `.no-auto-commit`; never stages `*.pem *.key .env* id_rsa* *.pfx *.p12` or files over 20 MB; honours `<repo>/.autocommit-ignore` (git pathspecs).
- Repos known: `microservice-mapper` (main; has `.autocommit-ignore` for `server/data/` and `*.log`) and `final project (short and sweet)` (master; `projects/`, `samples/`, `litdb/pdfs`, `litdb/texts`, `config.yaml` are gitignored). `royson-paper` is not a repo.
- Sessions already open when the settings file was created may need a restart to load the hook; run the script manually until then.

**Why:** the user wants work saved automatically across all chats (including child sessions).
**How to apply:** don't add extra manual commits just to save work; still make deliberate commits when asked. If a repo should be skipped, add `.no-auto-commit`. Sessions that commit by hand will race with the hook only harmlessly (the hook retries on index.lock).
