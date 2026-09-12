# dev-harness の保守

このリポジトリは、AIと共同開発するときの最小共通手法、共通指示、Skill、プロジェクト雛形の正本である。

## 判断の順序

- 現行の判断は `METHOD.md` を正本とする。
- 共通指示は `profiles/codex/AGENTS.md`、再利用する手順は `skills/`、新規プロジェクトの契約は `templates/project/` に置く。
- Orcaのsession、comment、履歴、usage情報は運用補助であり、Intentや設計判断の正本にしない。
- 観測された摩擦がない限り、手順や常時contextを増やさない。

## 変更と検証

- 変更は一つの意味単位にまとめ、必要ならcommit本文に `Why:`、`Previous:`、`Supersedes:`、`Impact:` を残す。
- commitは依頼に含まれる場合だけ行う。含まれない場合はcommit message案を返す。
- `devenv tasks run harness:check` を標準検証とする。
- Skillを変更したらskill-creatorのvalidatorでも検証する。
