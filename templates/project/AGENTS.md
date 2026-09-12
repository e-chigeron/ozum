# プロジェクト開発ルール

- 正本の優先順は `INTENT.md` → 関連する `specs/*.md` → tests → implementation とする。
- `INTENT.md` とspecには現在状態だけを書き、変更履歴を蓄積しない。
- 不一致を黙って解消しない。衝突の兆候がある場合だけ、対象pathのGit履歴を調べる。
- 言語固有のtoolchainと検証は `devenv.nix` と `scripts/verify-project` に定義する。
- 標準検証は `devenv tasks run project:verify` とする。
- 一つの意味的変更を一つのcommitにまとめる。commitは依頼に含まれる場合だけ行う。
