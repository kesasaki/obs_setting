# OBS設定リポジトリ

## 配信後の作業

配信終了後に「配信後」「post stream」「PRやって」など配信後の処理を頼まれたら、以下を実行する：

```bash
bash scripts/post-stream.sh
```

このスクリプトは `basic/scenes/無題.json` の変更を自動でブランチ→PR→mainマージまで行う。
