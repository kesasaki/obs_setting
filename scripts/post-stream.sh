#!/usr/bin/env bash
set -e

BRANCH="stream/$(date '+%Y%m%d-%H%M')"
TITLE="配信後の設定更新 $(date '+%Y-%m-%d %H:%M')"

DIFF=$(git diff HEAD -- basic/scenes/無題.json)
SUMMARY=$(echo "$DIFF" | claude -p "これはOBSのシーン設定JSONの差分です。変更内容をOBS上のソース表示名を使って日本語の箇条書きで簡潔にまとめてください。ホットキーの追加は省略してください。コードブロックや前置きは不要で箇条書きのみ出力してください。")

git checkout -b "$BRANCH"
git add basic/scenes/無題.json
git commit -m "$TITLE"
git push origin "$BRANCH"

PR_URL=$(gh pr create --title "$TITLE" --body "$SUMMARY" --base main)
PR_NUMBER=$(echo "$PR_URL" | grep -o '[0-9]*$')

REPO=$(gh repo view --json nameWithOwner -q .nameWithOwner)
gh api "repos/$REPO/pulls/$PR_NUMBER/merge" -X PUT -f merge_method=merge -f commit_title="$TITLE"
gh api "repos/$REPO/git/refs/heads/$BRANCH" -X DELETE

git checkout main
git pull origin main

echo "Done: mainへのマージ完了"
