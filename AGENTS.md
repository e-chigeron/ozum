# ОЗУМリポジトリの保守

このリポジトリはОЗУМの正本かつ自身を適用するリファレンス実装。本書はその保守契約を担う。`skills/` と `templates/project/` は配布物で、その編集にも本書を適用する。テンプレート内のAGENTSはコピー先で働く。

目的は [current-context](Intent/current-context.md)、[decision-traceability](Intent/decision-traceability.md)、[instruction-ownership](Intent/instruction-ownership.md)、[method-evolution](Intent/method-evolution.md)、[publication](Intent/publication.md)。各仕様・設定の所在は [README](README.md#構成) を参照する。

## 判断と情報の責務

- `Intent/` は目的・理由・解を選び直しても守る制約の正本。独立して変わる目的を分け、手段や変更経緯は置かない。固定分類・IDは不要。
- Feature Spec（Spec）は採用した振る舞い・契約・受入条件の正本で、関連Intentへ参照を置く。採用済みでも未実装の場合がある。AGENTS・Skill・設定も対象範囲を明確にしてSpecを兼ねられ、別文書や完全な対応表へ複製しない。実装の事実だけで要求を正当化しない。
- 通常実装では対象Spec・コード・tests・実行指示を読み、検証する。Intentを常時読み直して仕様を変えない。矛盾・不足や目的・仕様の変更では、関連IntentとSpec、必要な履歴・実装へ戻る。Intent間の競合はファイル順で決めず、両立条件か未確定事項を示す。
- 依頼・権限に沿った決定をSpecへ反映し、目的・制約が変わる場合だけIntentを更新する。提案・引用・status表示だけを採用の根拠にせず、決定と反映の差を示す。現在必要な理由は現行文書へ、変更経緯はGit履歴へ残す。
- READMEは入口、Issueは任意の議論・引継ぎ先。Issue・PR・ADRを必須工程にしない。Projection（候補仕様・状態ビュー等）は正本から必要時に再生成するもので、採用判断の効力や同期保守する正本を持たせない。会話・作業環境も正本にしない。

## 変更時に読むもの

- 目的・仕様の変更は `change-intent`。Intent不変の仕様変更も含む。制約の分類・設定と契約の境界はこのSkillで確認する。
- 繰り返す・影響の大きい摩擦（開発の進行・判断・品質を妨げる支障や負担）、または明示的な手法レビューは `review-dev-method`。観測だけで毎回の改善提案は不要。
- 本体の改善は互換性を絶対条件にせず根本的な再設計も選ぶ。この自由を配布先へ強制しない。実行は既存機能を優先し、Orca・GitHub・devenvを手法の必須条件にしない。
- リリース時は [READMEのバージョン節](README.md#バージョン) を読む。

## 変更と共有

- 依頼の範囲でcommit・branch・履歴整理を自律的に行ってよい。他者や既存の未コミット変更を巻き込まず、共有済み履歴の書換えには別途合意を得る。
- 意味のある変更単位にまとめ、日本語のコミットメッセージへ変更理由と以前の判断との関係を残す。squashでも理由を保持し、分割・移動では旧パスと移動先を記す。
- local-only指定がなければ検証と公開確認の後、設定済みupstreamか明示された送信先へpushしてよい。送信対象の全commitの差分・メッセージから一時履歴・秘密情報・非公開情報を除き、公開可否が不明なら確認する。remote・認証・branchを推測せず、送信先不明や失敗は未同期として報告する。

## 検証

- `devenv tasks run harness:check` を実行する。Skill変更はskill-creatorのvalidatorでも検証する。
- 新しい雛形への移行を既存プロジェクトへ強制しない。Jujutsuは導入しない。
