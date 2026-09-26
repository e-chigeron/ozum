# ОЗУМ

ОЗУМ（опыт замысла, улучшающего меня）は、Intentを優先し、開発経験と判断の変化を通じて開発手法そのものを改善するメタ開発手法です。このリポジトリはОЗУМの正本であると同時に、ОЗУМ自身を適用するリファレンス実装です。現在の目的、採用している方法、変更理由を分けて管理し、実際の保守・検証・Git履歴を通じて手法を改善します。

このリポジトリは開発手法そのものを扱います。ОЗУМ本体には、ОЗУМ自身を改善するためのメタレベルの目的・判断基準・保守指示も含まれます。

配布する成果物とリファレンス実装は別の対象です。

- `skills/` は、他のプロジェクトでも利用できる必要時だけ読む再利用手順です。
- `templates/project/` は、個別プロジェクトがそのIntentと制約に適応させるための開発手法テンプレートです。
- 個別プロジェクトは固有のIntentと判断を持ち、テンプレートの変更に自動追従しません。

## 構成

- `Intent/`: ОЗУМとそのリファレンス実装に求める現在の目的と制約
- `AGENTS.md`: リファレンス実装を保守する方法と実行指示
- `skills/`: 配布用の必要時だけ読む再利用手順
- `templates/project/`: 新規プロジェクト向けの開発手法テンプレートと、コピー先を保守する `AGENTS.md`
- `orca.yaml`: Orca worktreeのsetup

ОЗУМ本体の `AGENTS.md` はリファレンス実装と配布物の保守を、雛形の `AGENTS.md` はコピー先の製品開発を扱います。各リポジトリの規則はそれぞれの `AGENTS.md` で完結し、共有Skillsは必要時だけ利用します。

Home Managerなどリポジトリ外の旧Profile symlinkは別途設定変更が必要です。Skillsの配布は引き続き必要に応じて管理します。別worktreeの編集やpushだけでは、配布元の作業ツリーは更新されません。

共有Skillは `change-intent` と `review-dev-method` です。

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

プロジェクトで見つかった摩擦は、そのプロジェクト内に証拠を残します。繰り返す摩擦、影響の大きい摩擦、または明示的な手法レビューでは、証拠を参照できる形でОЗУМリポジトリへ渡し、`review-dev-method` で検討します。転送形式や専用ツールは規定しません。

現在の判断は `Intent/` と `AGENTS.md`、変更理由はGit履歴を参照します。

## ライセンス

文書、Skills、配布テンプレートを含むリポジトリ全体の基本ライセンスは[MIT License](LICENSE)です。利用、改変、fork、商用利用、独自派生を許可します。upstreamへの還元を義務化せず、派生物に同一ライセンスを強制しません。コピーまたは実質的な部分を配布するときは、元の著作権表示とMIT License本文を保持してください。

`templates/project/` には単独コピー後も表示を保持できるよう `LICENSE` を同梱しています。ОЗУМのSkillsや文書を個別に取り出して配布するときも、このリポジトリの著作権表示とライセンス本文を添えてください。新しく作成するプロジェクトの独自部分にMIT Licenseを強制するものではありません。

## Contributionとupstream

提案やContribution、第三者による独自の改善を歓迎します。upstreamへの採用はmaintainerがОЗУМのIntent・設計思想・あるべき姿との適合を中心に判断し、採用を保証しません。upstreamはすべてのユースケースを包含することを目標とせず、意図的にopinionatedなリファレンス実装であってよいと考えます。

採用されなかった案についても、prototypeによる検証と結果を伴う再提案、fork、独自派生としての発展を歓迎します。MIT Licenseによる利用許諾とupstreamの採用判断は分離しています。詳しくは[CONTRIBUTING.md](CONTRIBUTING.md)を参照してください。
