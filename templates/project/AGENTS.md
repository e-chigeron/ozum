# プロジェクト開発ルール

- `Intent/` は目的と制約、`specs/` は現在の仕様、この文書は採用している開発方法を記述する。
- Intent・仕様・tests・実装の不一致を黙って解消しない。競合や変更理由を確認する必要があれば対象のGit履歴を調べる。
- 現行文書には現在の判断を理解するための情報を残し、過去の経緯や未採用案を蓄積しない。
- 言語固有のtoolchainとbuild・test・lintを `devenv.nix` と `scripts/verify-project` に定義する。標準検証は `devenv tasks run project:verify` とする。雛形の検査だけでは製品を検証したことにならない。
- 手法の摩擦はプロジェクト内の証拠を保ち、`review-dev-method` で上流へ変更候補を渡す。
- commitは依頼に含まれる場合だけ行い、それ以外は理由を含むメッセージ案を返す。メッセージは日本語で、重要な変更では以前の判断との関係も残す。
- 依頼・承認されたcommitは、明示的なlocal-only指定がなければ検証後に設定済みupstreamへpushする。remote、認証、対象branchを推測せず、失敗は未同期として報告する。
