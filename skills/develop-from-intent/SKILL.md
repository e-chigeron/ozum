---
name: develop-from-intent
description: リポジトリの現行Intentと仕様に沿って機能実装や修正を行い、プロジェクト定義のtaskで検証するときに使う。Intent自体の変更や開発手法の見直しには使わない。
---

# Intentから開発する

1. リポジトリの指示、`INTENT.md`、依頼に関係するspec、tests、実装の順に必要な範囲だけ読む。
2. 記録同士が一致していれば、現行Intentとspecを受入条件として最小の実装を行う。過去の会話や履歴は通常contextへ加えない。
3. 不一致や意図の衝突を見つけたら黙って選ばず、変更が必要な対象を示す。Intent変更なら `change-intent` の手順へ切り替える。
4. プロジェクトが定義する標準taskで検証し、失敗時は関連する診断だけを調べる。
5. commit権限がなければcommitせず、実装内容、検証結果、必要ならcommit message案を返す。
