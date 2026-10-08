# ОЗУМ

ОЗУМ（опыт замысла, улучшающего меня）は、Intentを優先し、開発経験と判断の変化を通じて開発手法そのものを改善するメタ開発手法です。このリポジトリはОЗУМの正本であると同時に、ОЗУМ自身を適用するリファレンス実装です。現在の目的、採用している方法、変更理由を分けて管理し、実際の保守・検証・Git履歴を通じて手法を改善します。

このリポジトリは開発手法そのものを扱います。ОЗУМ本体には、ОЗУМ自身を改善するためのメタレベルの目的・判断基準・保守指示も含まれます。

配布する成果物とリファレンス実装は別の対象です。

- `skills/` は、他のプロジェクトでも利用できる必要時だけ読む再利用手順です。
- `templates/project/` は、個別プロジェクトがそのIntentと制約に適応させるための開発手法テンプレートです。
- 個別プロジェクトは固有のIntentと判断を持ち、テンプレートの変更に自動追従しません。

## 構成

- `Intent/`: ОЗУМとそのリファレンス実装に求める現在の目的と制約
- `AGENTS.md`: リファレンス実装の保守方法のFeature Specと実行指示
- `skills/`: 配布用の必要時だけ読む再利用手順
- `templates/project/`: 新規プロジェクト向けの開発手法テンプレートと、コピー先を保守する `AGENTS.md`
- `orca.yaml`: Orca worktreeのsetup

ОЗУМ本体の `AGENTS.md` はリファレンス実装と配布物の保守を、雛形の `AGENTS.md` はコピー先の製品開発を扱います。各リポジトリの規則はそれぞれの `AGENTS.md` で完結し、共有Skillsは必要時だけ利用します。

Home Managerなどリポジトリ外の旧Profile symlinkは別途設定変更が必要です。Skillsの配布は引き続き必要に応じて管理します。別worktreeの編集やpushだけでは、配布元の作業ツリーは更新されません。

共有Skillは `change-intent`、`review-dev-method`、`review-consistency` です。

Feature Specは現在満たすべき仕様・契約の正本です。本体の保守方法は [AGENTS.md](AGENTS.md)、目的・仕様変更の契約は [change-intent](skills/change-intent/SKILL.md)、手法改善の契約は [review-dev-method](skills/review-dev-method/SKILL.md)、検証・環境は [devenv.nix](devenv.nix) と [scripts/check](scripts/check)、worktree setupは [orca.yaml](orca.yaml) から読みます。既存の指示・設定に直接表現された仕様を別文書へ複製しません。コピー先の製品仕様の入口は [templates/project/specs/](templates/project/specs/README.md) です。

仕様のファイル名・見出し・検索と、仕様からIntentへの参照で必要な範囲を辿ります。採用済みの要求と実装状態は区別し、後者は対象の実装・testsで確認します。Dashboard等の状態ビューは必要時に再生成し、正本として保守しません。

## 使い方

このリポジトリ自体を検証します。

```console
devenv tasks run harness:check
```

新しいプロジェクトは雛形をコピーし、`Intent/outcome.md` に具体的な目的を記入して、必要なFeature Specを作成します。配置と責務は雛形の `specs/README.md` を参照してください。Intentは独立して変化する目的が生じたときに分割します。

```console
cp -R templates/project /path/to/new-project
cd /path/to/new-project
git init -b main
devenv tasks run project:verify
```

雛形の `project:verify` は構成と構文のみを検査します。製品のbuild・test・lintは、プロジェクトの `devenv.nix` と `scripts/verify-project` に定義します。共有Skillsは既存の `INTENT.md` を使うプロジェクトにも対応します。

Orcaではbase refを `main` とし、worktreeのsetupは `devenv shell -- true` を行います。worktreeやsessionの管理はOrcaに任せます。

## CIと差分AIレビュー

GitHub Actionsの [機械検証](.github/workflows/check.yml) はpush・PRで `harness:check` を実行します。[AIレビュー](.github/workflows/review-consistency.yml) はPR差分を [review-consistency](skills/review-consistency/SKILL.md) の契約で確認し、独立したjob summaryに参考結果を返します。AIの指摘や接続失敗を機械検証の結果と混ぜず、AI jobをrequired checkにすることは想定していません。

AI接続は未設定です。利用する場合はGitHubのSettings → Secrets and variables → Actionsで次を設定します。キーのダミー文字列を登録する必要はありません。

| 設定 | 値 |
| --- | --- |
| Secret `OPENAI_API_KEY` | `<利用するOpenAI APIキー>` |
| Variable `AI_REVIEW_ENABLED` | `true`（未設定なら実行しない） |
| Variable `AI_REVIEW_MODEL` | `<利用可能なモデルID>`（任意、未設定ならCodex既定値） |

実行には[公式Codex GitHub Action](https://developers.openai.com/codex/github-action/)を使います。同一リポジトリのdraftではないPRを対象に、merge-baseからPR headまでを読み取り専用でレビューします。Action自身のユーザー権限チェックも適用されます。fork PR、未設定時は未実行を表示します。10分のjob制限と同じPRの古い実行の取消で遅延・重複を抑えます。Secret設定後のAPI接続、モデルの利用可否、費用、誤検出率は実運用で確認が必要です。

Orca内のcoding agentや別CIでも、比較範囲を指定してSkillを読み、同じレビューを実行できます。GitHub非使用の未commit変更なら、たとえばCodex CLIで次を実行します。CLIのインストール・認証は利用環境に委ねます。

```console
codex exec --sandbox read-only 'skills/review-consistency/SKILL.mdを読み、未commit変更（staged・unstaged・未追跡）を意味的整合レビューしてください。変更せず結果だけ返してください。'
```

コピー先では共有Skillを利用可能にするか、雛形の `AGENTS.md` のレビュー規則をcoding agentへ渡します。GitHub ActionsやCodexをテンプレートの必須依存にはしません。

変更差分から文脈を絞る規則はCI・差分AIレビュー専用で、ОЗУМ全体の方針ではありません。対応表・独自daemon・DB・状態同期は追加しません。費用・遅延・誤検出に見合う便益がない場合は `AI_REVIEW_ENABLED` を外し、機械検証と必要時のローカルレビューへ戻せます。確認範囲の妥当性、指摘の有用性、実行時間・API使用量を実運用で評価し、常時読む規則や仕組みを増やす前に見直します。

## 手法の改善

プロジェクトで見つかった摩擦は、そのプロジェクト内に証拠を残します。繰り返す摩擦、影響の大きい摩擦、または明示的な手法レビューでは、証拠を参照できる形でОЗУМリポジトリへ渡し、`review-dev-method` で検討します。転送形式や専用ツールは規定しません。

現在の目的は `Intent/`、仕様と実装時の読み方は `AGENTS.md` および対象のFeature Spec、変更理由は対象仕様・実装のGit履歴を参照します。

## ライセンス

文書、Skills、配布テンプレートを含むリポジトリ全体の基本ライセンスは[MIT License](LICENSE)です。利用、改変、fork、商用利用、独自派生を許可します。upstreamへの還元を義務化せず、派生物に同一ライセンスを強制しません。コピーまたは実質的な部分を配布するときは、元の著作権表示とMIT License本文を保持してください。

`templates/project/` には単独コピー後も表示を保持できるよう `LICENSE` を同梱しています。ОЗУМのSkillsや文書を個別に取り出して配布するときも、このリポジトリの著作権表示とライセンス本文を添えてください。新しく作成するプロジェクトの独自部分にMIT Licenseを強制するものではありません。

## Contributionとupstream

提案やContribution、第三者による独自の改善を歓迎します。upstreamへの採用はmaintainerがОЗУМのIntent・設計思想・あるべき姿との適合を中心に判断し、採用を保証しません。upstreamはすべてのユースケースを包含することを目標とせず、意図的にopinionatedなリファレンス実装であってよいと考えます。

採用されなかった案についても、prototypeによる検証と結果を伴う再提案、fork、独自派生としての発展を歓迎します。MIT Licenseによる利用許諾とupstreamの採用判断は分離しています。詳しくは[CONTRIBUTING.md](CONTRIBUTING.md)を参照してください。
