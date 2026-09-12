---
name: change-intent
description: 製品のあるべき姿や仕様を変更し、現行文書を更新して変更理由をGit履歴へ残すときに使う。現行Intent内の通常実装だけには使わない。
---

# Intentを変更する

1. 変更対象の `INTENT.md`、関連spec、tests、実装を必要な範囲だけ読む。
2. 現行記述と依頼が衝突する、または変更理由の確認が必要な場合だけ、対象pathを限定して `git log --follow -- <path>`、`git blame <path>`、`git show <commit> -- <path>` を使う。
3. 新しい判断が既存の理由を無効化するか、両立するかを明示する。不明な重要事項は推測で確定しない。
4. `INTENT.md` とspecには変更履歴を追記せず、合意した現在状態だけが残るように更新する。必要なtestsと実装も整合させる。
5. 一つの意味的変更にまとめ、必要な項目だけを使ってcommit messageを準備する。

```text
<要約>

Why: <変更する理由>
Previous: <置き換える以前の判断>
Supersedes: <対象commitや判断>
Impact: <影響範囲>
```

commitは依頼に含まれる場合だけ行う。含まれない場合はmessage案として返す。
