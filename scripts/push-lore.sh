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
