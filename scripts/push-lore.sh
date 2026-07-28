#!/bin/bash
# push-lore.sh — auto-commit & push Train Lore when the weekly task has written a new tale.
# Mirrors the Gridiron Gazette pusher: the sandbox writes files, THIS script (running on the
# Mac, outside the sandbox) does the git push using a token from the macOS keychain.
#
# It only pushes if something actually changed, so it's safe to run on a timer.

set -euo pipefail

REPO="/Users/kevinsotka/Meatbag_Labs/train_lore"
BRANCH="main"
# Keychain item holding a GitHub Personal Access Token (repo scope). Create once with:
#   security add-generic-password -a "$USER" -s "train_lore_github_token" -w "ghp_xxx"
KEYCHAIN_SERVICE="train_lore_github_token"
GH_USER="kevin-sotka"
GH_REPO="train_lore"

cd "$REPO"

# --- stale-lock guard --------------------------------------------------------
# A git process that crashes mid-commit can leave .git/index.lock behind. With
# `set -e`, the very next run dies at `git add` and every run after it does too,
# silently freezing the site (this once went unnoticed for a month). This job is
# the only scheduled writer to this repo, so a lock older than 2 minutes is
# certainly stale: clear it. A lock younger than that might be a live git
# operation, so skip this run and try again next time rather than clobber it.
LOCK="$REPO/.git/index.lock"
if [ -e "$LOCK" ]; then
  if [ -n "$(find "$LOCK" -mmin +2 2>/dev/null)" ]; then
    echo "$(date '+%Y-%m-%d %H:%M') stale index.lock (>2 min old): removing it"
    rm -f "$LOCK"
  else
    echo "$(date '+%Y-%m-%d %H:%M') fresh index.lock present — another git process may be active; skipping this run"
    exit 0
  fi
fi

# Nothing staged/changed? Exit quietly.
if [ -z "$(git status --porcelain)" ]; then
  echo "$(date '+%Y-%m-%d %H:%M') no changes — nothing to push"
  exit 0
fi

TOKEN=$(security find-generic-password -a "$USER" -s "$KEYCHAIN_SERVICE" -w 2>/dev/null || true)
if [ -z "$TOKEN" ]; then
  echo "ERROR: no GitHub token in keychain (service: $KEYCHAIN_SERVICE)"; exit 1
fi

git add -A
git commit -m "Train Lore: weekly tale + index $(date '+%Y-%m-%d')" || true

# Push over HTTPS with the token, without writing it to disk.
git push "https://${GH_USER}:${TOKEN}@github.com/${GH_USER}/${GH_REPO}.git" "$BRANCH"

echo "$(date '+%Y-%m-%d %H:%M') pushed to $GH_USER/$GH_REPO"
