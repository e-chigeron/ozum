# dev-harness

開発手法自体を改善するメタ開発手法 ОЗУМ（опыт замысла, улучшающего меня）と、その管理対象である開発手法リファレンスの正本です。現在の目的、採用している方法、変更理由を分けて管理し、開発経験から手法自体を改善します。

## 構成

- `Intent/`: ОЗУМと管理対象に求める現在の目的と制約
- `AGENTS.md`: ОЗУМ自身の保守方法と実行指示
- `profiles/codex/AGENTS.md`: 全リポジトリ共通の短い指示
- `skills/`: 必要時だけ読む再利用手順
- `templates/project/`: 配布する開発手法リファレンスを採用する新規プロジェクトの最小雛形
- `orca.yaml`: Orca worktreeのsetup

`profiles/`・`skills/`・`templates/` は配布する開発手法リファレンスです。ОЗУМ自身にも適用する方針はルートの `AGENTS.md` に示します。雛形の指示はコピー先だけで読めるよう、共通指示と一部重複します。

Home Managerは `/path/to/dev-harness` の共通指示とSkillsをout-of-store symlinkで配布します。その配布元への変更はNixOSの再buildなしに新しいCodex sessionへ反映されます。別worktreeの編集やpushだけでは配布元の作業ツリーは更新されません。

共有Skillは `change-intent` と `review-dev-method` です。配布設定で個別列挙している場合はこの2つに合わせ、削除済みの `develop-from-intent` のリンクも除去してください。Home Managerの配布設定はこのリポジトリの管理外です。

## 使い方

このリポジトリ自体を検証します。

```console
devenv tasks run harness:check
```

新しいプロジェクトは雛形をコピーし、`Intent/outcome.md` に具体的な目的を記入して、必要なspecを作成します。Intentは独立して変化する目的が生じたときに分割します。

```console
cp -R templates/project /path/to/new-project
cd /path/to/new-project
git init -b main
devenv tasks run project:verify
```

雛形の `project:verify` は構成と構文のみを検査します。製品のbuild・test・lintは、プロジェクトの `devenv.nix` と `scripts/verify-project` に定義します。共有Skillsは既存の `INTENT.md` を使うプロジェクトにも対応します。

Orcaではbase refを `main` とし、worktreeのsetupは `devenv shell -- true` を行います。worktreeやsessionの管理はOrcaに任せます。

## 手法の改善

プロジェクトで見つかった摩擦は、そのプロジェクト内に証拠を残します。繰り返す摩擦、影響の大きい摩擦、または明示的な手法レビューでは、証拠を参照できる形でdev-harnessへ渡し、`review-dev-method` で検討します。転送形式や専用ツールは規定しません。

現在の判断は `Intent/` と `AGENTS.md`、変更理由はGit履歴を参照します。SQLiteの専用handoff基盤は現行構成に含めません。既存の一時packetを誤って追跡しないよう、`*.aictx` のignoreは維持しています。
