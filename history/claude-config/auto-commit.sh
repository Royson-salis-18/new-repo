#!/usr/bin/env bash
# Auto-commit hook for Claude Code (user level, all projects and sessions).
# Commits (never pushes) whatever changed in the current git repo when a turn ends.
#
# Safety rules, all silent:
#  - only inside an existing git repo; never runs `git init`; skips the home directory itself
#  - skips detached HEAD and repos mid merge/rebase/cherry-pick/bisect
#  - never stages likely secrets (*.pem, *.key, .env*, id_rsa*, *.pfx, *.p12) or files over 20 MB
#  - honours <repo>/.autocommit-ignore (one git pathspec per line, '#' comments) to leave generated files out
#  - a repo containing a file named .no-auto-commit is skipped entirely
#  - retries once if another session holds the git index lock
# Output is intentionally empty so the hook never clutters a session.

dir="${CLAUDE_PROJECT_DIR:-$PWD}"
cd "$dir" 2>/dev/null || exit 0
top="$(git rev-parse --show-toplevel 2>/dev/null)" || exit 0
cd "$top" || exit 0
[ "$top" = "$(cd "$HOME" 2>/dev/null && pwd)" ] && exit 0
[ -e .no-auto-commit ] && exit 0
git symbolic-ref -q HEAD >/dev/null 2>&1 || exit 0

gd="$(git rev-parse --git-dir)"
for f in MERGE_HEAD REBASE_HEAD CHERRY_PICK_HEAD rebase-merge rebase-apply BISECT_LOG; do
  [ -e "$gd/$f" ] && exit 0
done

[ -z "$(git status --porcelain 2>/dev/null)" ] && exit 0

add() { git add -A >/dev/null 2>&1; }
add || { sleep 3; add || exit 0; }

# unstage secrets
git reset -q -- '*.pem' '*.key' '*.pfx' '*.p12' '.env' '.env.*' 'id_rsa*' 'id_ed25519*' >/dev/null 2>&1 || true

# unstage per-repo opt-outs
if [ -f .autocommit-ignore ]; then
  while IFS= read -r p; do
    case "$p" in ''|'#'*) continue ;; esac
    git reset -q -- "$p" >/dev/null 2>&1 || true
  done < .autocommit-ignore
fi

# unstage very large files
git diff --cached --name-only 2>/dev/null | while IFS= read -r f; do
  if [ -f "$f" ] && [ "$(wc -c < "$f" 2>/dev/null || echo 0)" -gt 20000000 ]; then
    git reset -q -- "$f" >/dev/null 2>&1 || true
  fi
done

git diff --cached --quiet && exit 0

name="$(git config user.name)";  [ -z "$name" ]  && name="Royson Salis"
email="$(git config user.email)"; [ -z "$email" ] && email="roysonsalis2005@gmail.com"
n="$(git diff --cached --name-only | wc -l | tr -d ' ')"
first="$(git diff --cached --name-only | head -3 | tr '\n' ' ')"

git -c user.name="$name" -c user.email="$email" commit -q \
  -m "auto-commit: ${n} file(s) $(date '+%Y-%m-%d %H:%M')" \
  -m "Automatic commit by the Claude Code Stop hook (never pushed). Files: ${first}" >/dev/null 2>&1 \
  || { sleep 3; git -c user.name="$name" -c user.email="$email" commit -q -m "auto-commit: ${n} file(s) $(date '+%Y-%m-%d %H:%M')" >/dev/null 2>&1; }
exit 0
