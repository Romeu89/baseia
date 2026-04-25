#!/usr/bin/env bash
# Sandbox bootstrap for remote agent runs on Romeu89/baseia.
#
# Purpose: make a fresh Anthropic remote-agent sandbox commit-and-push capable
# in seconds, so the agent's wall-clock time budget goes to deliverables instead
# of environment discovery.
#
# Idempotent. Run from the repo root. The final stdout line is the result:
#   BOOTSTRAP OK push_mode=<mode> gh=<mode> user=<email>
#   BOOTSTRAP FAIL: <reason>
# The remote agent greps for "BOOTSTRAP OK" / "BOOTSTRAP FAIL" to branch.

set -euo pipefail

REPO_URL="https://github.com/Romeu89/baseia.git"
USER_EMAIL="romeuhrechdan@gmail.com"
USER_NAME="Romeu Hungria Rechdan"

fail() {
  echo "BOOTSTRAP FAIL: $1" >&2
  exit 1
}

# 1. Must be inside a git work tree.
git rev-parse --is-inside-work-tree >/dev/null 2>&1 \
  || fail "not inside a git work tree"

# 2. Configure origin if missing. If origin already exists (e.g. the harness
#    cloned with a remote), leave it alone — do not overwrite the harness setup.
if ! git remote get-url origin >/dev/null 2>&1; then
  git remote add origin "$REPO_URL" \
    || fail "could not add origin remote"
fi

# 3. Repo-scoped identity. Sandbox snapshots discard .git/config, so this MUST
#    re-apply on every run even if a prior run set it.
git config user.email "$USER_EMAIL"
git config user.name "$USER_NAME"

# 4. Auth strategy.
#    If GITHUB_TOKEN is injected by the remote-agent harness, rewrite the
#    origin URL to embed it (x-access-token user, PAT/installation token in
#    password slot). Token lives only in the ephemeral .git/config.
#    If absent, leave origin as-is. Pushes will fail; agent keeps committing
#    locally so work survives until manual pull. No halt.
PUSH_MODE="local-only"
if [[ -n "${GITHUB_TOKEN:-}" ]]; then
  TOKEN_URL="https://x-access-token:${GITHUB_TOKEN}@github.com/Romeu89/baseia.git"
  git remote set-url origin "$TOKEN_URL"
  PUSH_MODE="token-injected"
fi

# 5. Connectivity probe. Fetch must succeed for the agent to be useful.
git fetch origin --prune >/dev/null 2>&1 \
  || fail "git fetch origin failed (push_mode=$PUSH_MODE)"

# 6. gh availability. Missing gh is NOT a halt — the brief has a fallback
#    path that emits the PR command for manual execution.
GH_MODE="absent"
if command -v gh >/dev/null 2>&1; then
  if gh auth status >/dev/null 2>&1; then
    GH_MODE="authenticated"
  else
    GH_MODE="installed-no-auth"
  fi
fi

echo "BOOTSTRAP OK push_mode=$PUSH_MODE gh=$GH_MODE user=$(git config user.email)"
