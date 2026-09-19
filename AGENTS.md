# dev-harness の保守

このリポジトリは、AIと共同開発するときの最小共通手法、共通指示、Skill、プロジェクト雛形の正本である。

## 判断の順序

- 現行の判断は `METHOD.md` を正本とする。
- 共通指示は `profiles/codex/AGENTS.md`、再利用する手順は `skills/`、新規プロジェクトの契約は `templates/project/` に置く。
- Orcaのsession、comment、履歴、usage情報は運用補助であり、Intentや設計判断の正本にしない。
- 観測された摩擦がない限り、手順や常時contextを増やさない。

## 変更と検証

- このリポジトリに限り、AIは意味のある実装、修正、判断変更が生じた時点でcommitできる。作業全体の完成や操作ごとの承認を待つ必要はない。commit、branch、rebase、squashなどの進め方はAIが判断する。Jujutsuは導入しない。
- commitはIntentに沿って独立に説明できる変更単位にし、同じ目的の機械的修正はまとめる。commit数や形式は固定しない。
- 問題を見つけた場合は原則として追加commitで修正する。採用を撤回する場合も、履歴を消すより変更を取り消すcommitを優先する。履歴の書換えは必要な場合に限り、自分の未共有の作業履歴で行う。
- commitの差分とメッセージから、重要なIntentの変更、設計判断、採用理由を追えるようにする。必要な場合は本文に `Why:`、`Previous:`、`Supersedes:`、`Impact:` を残す。
- 未完成または未検証のcommitは許容する。その場合はcommit本文に状態と残る検証を記録し、検証済みの状態と区別する。未完成・未検証のcommitを本流へ統合または外部へ公開するかは、AIが作業の範囲、検証結果、対象branchを確認して別途判断する。
- 既存の未コミット変更、他者の変更、共有済み履歴を巻き込まない。共有済み履歴を変更するには別途合意を得る。
- 検証済みのcommitは、明示的なlocal-only指定がない限り、AIが設定済みupstreamへのpushを判断してよい。remote、認証、対象branchを推測せず、失敗は未同期として報告する。
- `devenv tasks run harness:check` を標準検証とする。
- Skillを変更したらskill-creatorのvalidatorでも検証する。
