# dev-harness

AIとの共同開発手法 ОЗУМ（опыт замысла, улучшающего меня）の正本です。現在の目的、採用している方法、変更理由を分けて管理し、開発経験から手法自体を改善します。

## 構成

- `Intent/`: 現在の目的と制約
- `AGENTS.md`: 現在採用している方法と保守指示
- `profiles/codex/AGENTS.md`: 全リポジトリ共通の短い指示
- `skills/`: 必要時だけ読む再利用手順
- `templates/project/`: 新規プロジェクトの最小雛形
- `orca.yaml`: Orca worktreeのsetup

Home Managerは `/path/to/dev-harness` の共通指示と3つのSkillをout-of-store symlinkで配布します。その配布元への変更はNixOSの再buildなしに新しいCodex sessionへ反映されます。別worktreeの編集やpushだけでは配布元の作業ツリーは更新されません。

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

プロジェクトで見つかった摩擦は、そのプロジェクトの証拠を参照できる形でdev-harnessへ渡し、`review-dev-method` で検討します。転送形式や専用ツールは規定しません。

現在の判断は `Intent/` と `AGENTS.md`、変更理由はGit履歴を参照します。SQLiteの専用handoff基盤は現行構成に含めません。既存の一時packetを誤って追跡しないよう、`*.aictx` のignoreは維持しています。
