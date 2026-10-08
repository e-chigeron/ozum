# ОЗУМリポジトリの保守

このリポジトリは、開発手法を改善するメタ開発手法ОЗУМの正本であり、ОЗУМ自身を適用するリファレンス実装である。この文書は、そのリファレンス実装の保守に適用する。

## 目的と方法

- `Intent/` は現在有効な目的、望む理由、必要な制約・達成状態の正本。実現手段や変更経緯を置かず、手段だけの変更では更新しない。
- Feature Specは、現在満たすべき振る舞い・契約、必要な制約、検証可能な受入条件の正本。関連Intentへの参照を置き、Intent側の逆リンクや完全な対応表は要求しない。採用済みの要求と実装済みの事実は区別する。
- この文書は保守方法のFeature Specと実行指示を兼ねる。特定作業の契約は `skills/*/SKILL.md`、検証・環境は `devenv.nix` と `scripts/check`、worktree setupは `orca.yaml` に直接表現する。仕様を担う既存文書・設定を別Markdownへ複製しない。
- READMEは公開入口と正本への導線、実装・testsは仕様の実現と検証、Git履歴は採用した変更と理由を担う。Issueは任意の議論・引継ぎ先とし、Issue・PR・ADR作成を必須工程にしない。参照や要約を別の正本として同期保守しない。
- `skills/` と `templates/project/` は配布物であり、リファレンス実装そのものではない。テンプレート内を保守するときもこの文書に従い、配布後の `templates/project/AGENTS.md` はコピー先のプロジェクトで働く。
- Intentには独立して変わる目的を分けて置く。固定の分類やIDは設けない。

## 現在の判断

この保守方法は [current-context](Intent/current-context.md)、[decision-traceability](Intent/decision-traceability.md)、[instruction-ownership](Intent/instruction-ownership.md)、[method-evolution](Intent/method-evolution.md)、[publication](Intent/publication.md) を実現する。

- 検討時は関連Intentと現行Feature Specを読み、必要なIssue・Git履歴・実装を確認する。Intent同士の競合はファイル順で決めず、現在の両立条件または未確定の判断を明示する。
- 決定時は採用内容をFeature Specへ反映し、目的・制約が変わる場合だけIntentも更新する。
- 通常の実装時は対象のFeature Spec、対象コード・tests、この文書等の実装指示を読み、受入条件を満たすよう実装し、プロジェクト定義のtaskで検証する。Intentを通常の実装コンテキストに含めず、仕様を再解釈して変更しない。矛盾・不足を発見した場合は黙って補わず、関連Intentへ戻って検討する。
- 現行文書には現在の判断を理解するための情報を置く。未採用案や過去の変更経緯は通常の指示として蓄積しない。引用やNOTEは採用の証拠にしない。
- 矛盾の解消や変更理由の確認が必要な場合に、Intentだけでなく関連仕様・実装を対象にGit履歴を調べる。会話やOrca metadataは永続的な正本にしない。
- Dashboard・Current State・候補仕様・Next Actions等のProjectionは必要時にIntent・Feature Spec・Git・Issue・実装から生成する一時的なビュー。削除しても正本を失わず再生成でき、人間が同期保守しないものとする。恒久ディレクトリや生成ファイルを必須化しない。
- 目的や仕様を変更するときは `change-intent` を使う。
- 手法の改善は観測された摩擦を起点とし、証拠、一般化できる範囲、成功条件と取消条件を `review-dev-method` で検討する。
- 改善対象がОЗУМのメタ開発手法、リファレンス実装、開発手法テンプレート、Skillsのどれかを区別する。ОЗУМ自身に別の手法上流への提案を課さない。

## 変更と履歴

- 依頼の範囲でローカルのcommit・branch・履歴整理を自律的に行ってよい。既存の未コミット変更や他者の変更を巻き込まない。履歴の書換えは自分の未共有履歴に限り、共有済み履歴の書換えには別途合意を得る。Jujutsuは導入しない。
- 重要な変更では、変更理由と以前の判断との関係を日本語のコミットメッセージに残す。squashしても必要な理由を引き継ぎ、文書の分割・移動では旧パスと移動先を記す。
- 明示的なlocal-only指定がなければ、検証と公開確認の後、設定済みupstreamまたは明示された送信先へpushしてよい。remote・認証・対象branchを推測せず、送信先不明や失敗は未同期として報告する。
- push前に送信対象の全commitの差分・メッセージを確認し、一時的な作業履歴、秘密情報、非公開情報が含まれないようにする。公開branchを変えても履歴は公開される。判断できない情報があればその公開を保留して確認する。

## 保守と検証

- 標準検証は `devenv tasks run harness:check` とする。Skillを変更したらskill-creatorのvalidatorでも検証する。
- 配布用のSkillsとテンプレートは既存プロジェクトでも使われる。新しい雛形の構成を既存プロジェクトへ強制しない。
