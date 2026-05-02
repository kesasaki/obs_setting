#!/usr/bin/env bash
set -e

BRANCH="stream/$(date '+%Y%m%d-%H%M')"
TITLE="配信後の設定更新 $(date '+%Y-%m-%d %H:%M')"

git checkout -b "$BRANCH"
git add basic/scenes/無題.json
git commit -m "$TITLE"
git push origin "$BRANCH"

PR_URL=$(gh pr create --title "$TITLE" --body "配信後の自動PR" --base main)
PR_NUMBER=$(echo "$PR_URL" | grep -o '[0-9]*$')

REPO=$(gh repo view --json nameWithOwner -q .nameWithOwner)
gh api "repos/$REPO/pulls/$PR_NUMBER/merge" -X PUT -f merge_method=merge -f commit_title="$TITLE"
gh api "repos/$REPO/git/refs/heads/$BRANCH" -X DELETE

git checkout main
git pull origin main

echo "Done: mainへのマージ完了"
