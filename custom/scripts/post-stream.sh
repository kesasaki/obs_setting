#!/usr/bin/env bash
set -e

BRANCH="stream/$(date '+%Y%m%d-%H%M')"
TITLE="配信後の設定更新 $(date '+%Y-%m-%d %H:%M')"

git checkout -b "$BRANCH"
git add basic/scenes/無題.json
git commit -m "$TITLE"
git push origin "$BRANCH"

gh pr create --title "$TITLE" --body "配信後の自動PR" --base main
gh pr merge --merge --delete-branch --yes

git checkout main
git pull origin main

echo "Done: mainへのマージ完了"
