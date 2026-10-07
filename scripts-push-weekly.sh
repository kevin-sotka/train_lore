#!/bin/zsh
# Weekly auto-commit and push of train_lore to GitHub (run by launchd).
cd /Users/kevinsotka/Meatbag_Labs/train_lore || exit 1
export PATH=/usr/bin:/bin:/usr/local/bin:/opt/homebrew/bin
if [[ -n "$(git status --porcelain)" ]]; then
  git add -A
  git commit -q -m "Train Lore: weekly auto-push $(date +%F)"
fi
git push origin main
