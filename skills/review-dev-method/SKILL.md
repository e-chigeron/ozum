---
name: review-dev-method
description: 実際の開発で観測された摩擦や失敗を材料に、dev-harnessの開発手法を見直して最小の改善案を作るときに使う。一般的なbest practiceの追加だけには使わない。
---

# 開発手法を見直す

1. 観測された摩擦を、発生条件、頻度、影響、現在の回避策に分ける。仮説だけの問題は恒久ルールにしない。
2. 開発projectで観測した場合は、そのprojectに証拠を残す。手法の正本が別repositoryにあるときは直接編集せず、証拠の参照、一般化範囲、候補変更、成功条件、取消条件を上流へ渡す。異なるAI・workspaceへ構造化して渡す必要がある場合だけ `.aictx` V0を使い、受信側は `scripts/aictx meta`、`scripts/aictx entrypoints` の順で確認してから `scripts/aictx expand` で関連subgraphだけを読む。元の会話全文は要求せず、packetを正本やGit追跡対象にしない。
3. 上流側で `METHOD.md` と関係する共通指示、Skill、雛形を読み、既存方針で扱えない理由を確認する。
4. 過去の判断理由が必要な箇所だけGit履歴を調べる。会話、Orcaのsessionやcomment、handoff payloadは証拠や運搬に使えても正本にはしない。
5. 問題を解消する最小変更を提案し、常時context、認知負荷、保守対象がどれだけ増えるかを示す。Orca既存機能との重複を避ける。
6. 成功条件と、改善を取り消す条件を示す。実装やcommitは依頼された範囲だけ行う。
