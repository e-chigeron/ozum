# 共通開発ルール

- 永続的なプロジェクト知識はリポジトリを正本とし、会話やOrca metadataを正本にしない。
- 現行のIntentと仕様を過去の会話より優先し、必要なファイルだけを読む。
- Intent、仕様、tests、実装の不一致を黙って解消しない。衝突の兆候がある場合だけ、対象ファイルのGit履歴を調べる。
- プロジェクト定義の検証taskを使い、build・test・lintの成功で確認する。
- 詳細手順は必要時に `develop-from-intent`、`change-intent`、`review-dev-method` Skillから読む。
- projectで開発手法の摩擦を観測したら、project内の証拠を保ち、`review-dev-method` で手法の上流正本へ変更候補を渡す。
- commitは依頼に含まれる場合だけ行い、それ以外は理由を含むcommit message案を返す。
