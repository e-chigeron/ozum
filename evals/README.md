# ОЗУМ本体のIntent摩擦検証

目的は [method-evolution](../Intent/method-evolution.md)、[current-context](../Intent/current-context.md)、[instruction-ownership](../Intent/instruction-ownership.md) に沿って、ある目的のための変更が別の目的を損なわないかを確かめること。この文書は本体の検証契約を担う。Issue #9の実証用で、汎用テスト形式の採用や有効性の実証済み宣言ではない。

## 適用範囲と責務

自動検証・明示的な検証実行のみに適用する。通常開発の読み方は変更しない。本体の手法変更のレビューでは小さい本体Intent集合を全て確認し、他の文書・実装は差分起点で絞る。これは全リポジトリの一括投入ではない。

配布Skill・テンプレートの内容も本体の成果物として検査するが、この検証基盤をコピー先へ導入しない。テンプレートの変更は不要。実証後に、指針・事例、テスト作成Skill、実行補助のどれを配布するかを判断する。「各プロジェクトのAIにテストを作らせる」は候補であって確定方針ではない。

| 層 | 責務 | 成功の意味 |
| --- | --- | --- |
| `harness:check` | 構文、リンク、入力準備処理のテスト | 機械的条件を満たす。Intent整合の証明ではない |
| [変更レビュー](review.md) | Specとの一致に加え、別Intentへの影響、重複、過剰、適用範囲を読む | 確認範囲内の根拠付き所見 |
| シナリオ実行 | 同じ課題を変更前後の指示で実行し、成果物と行動を観測 | 実行完了と評価上の妥当性は別 |
| [結果評価](grade.md) | ログ・成果物を事前観点で比較する | 一つの正解文や多数決でなく性質を評価 |

Issue #11は摩擦への対処方式（単独、調査委任、複数視点＋統合等）の比較実験。本体変更を検証する#9とは目的を分け、ケース・初期状態・観測を共用できる。#11の方式をそのまま唯一の採点者にしない。専用daemon、DB、依存グラフ、独自オーケストレーターは設けない。

## 変更レビュー

[prepare.py](prepare.py)はGitの明示したcommit範囲を資料へ変換する。実行するスクリプトとreview.mdは信頼済みのcheckoutから選ぶ。レビュー対象のheadから起動指示を取得しない。資料は番号付きtxtと元パスのmanifestに変換するため、対象のAGENTS・Skill・プロバイダ設定は自動読込されない。実行可能な対象コードも起動しない。

```console
# 信頼済みcheckoutで実行。出力はソースrepoの外の未作成ディレクトリ。
python3 evals/prepare.py review --repo /path/to/ozum --base BASE_SHA --head HEAD_SHA --out /tmp/ozum-review-01
cd /tmp/ozum-review-01
codex exec --skip-git-repo-check --sandbox read-only --json --output-last-message answer.md - < prompt.md > events.jsonl
```

PRではmerge-baseからheadを指定する。CLIは指定SHA間をそのまま比較し、範囲を推測しない。未commit変更はこの補助の対象外なので、必要ならローカルの一時commitを作り送信前に履歴整理する。CLI・認証・モデルの利用可否は実行環境に委ねる。レビュー実行にも時間制限を設定する。

[Actions](../.github/workflows/review-consistency.yml)はbase側の検証方針を使い、headを資料として扱う。同一repoの非draft PRのみ。Secret `OPENAI_API_KEY` とVariable `AI_REVIEW_ENABLED=true` が必要で、`AI_REVIEW_MODEL` は任意。未設定時は未実行。初回導入PRではbaseに方針がないため自動的にheadへフォールバックせず、bootstrap-requiredと表示する。初回は採用する方針を明示して上記のローカル検証を行う。

読み取り専用・drop-sudo、10分上限、同PRの古い実行取消を使い、報告は別jobのsummaryだけに返す。AIチェックはrequired checkに設定しない。実行失敗はログ上失敗として残し、成功に偽装しない。指摘による自動修正・自動merge・PRコメント送信は行わない。無効化するにはAI_REVIEW_ENABLEDを外す。

## シナリオの準備と実行

[cases](cases/)には6つの合成事例を置く。実際に観測された失敗とは区別する。taskとinputは作業AI用、expectationsは評価者用。評価者の観点に特定の回答文や唯一の解法を要求しない。

```console
python3 evals/prepare.py scenario --base BASE_SHA --head HEAD_SHA --case evals/cases/value-judgment --out /tmp/ozum-trial-01
python3 evals/run.py /tmp/ozum-trial-01/before --model MODEL_ID --timeout 600
python3 evals/run.py /tmp/ozum-trial-01/after --model MODEL_ID --timeout 600
```

prepareは同じtask/inputを二つの独立コピーへ渡し、評価観点・検証コード・tests・CI・プロバイダ設定をコピーしない。AGENTSと配布Skillは評価対象として保持し、taskが必要なSkillを読むよう指示する。コピーには初期状態だけのGit履歴がありremoteはない。検証基盤を省略するため、この試行ではharness:checkを作業AIの実行対象から外す。製品のbuild/test能力は測っていない。過去履歴の検索能力を試すケースにはこの方式は使えない。#11で履歴依存ケースを追加する際は、評価用答案を含まない履歴を別途準備する。

runはインストール・認証済みCodexを一回だけ起動し、モデル、CLI版、コマンド、時間、終了状態、JSONイベント、最終回答、変更差分を保存する。新規未追跡ファイルはstatusとworkspace本体から確認する。再試行は新しい出力先を使う。終了コード0は意味的な合格ではない。質問待ちは適切な対処であり得るが実装完了とは別。対話で回答を与えて続行する実験は既存Harnessで行い、回答も記録する。

このコピー作成はOSのセキュリティ境界ではない。厳密に答案・別試行の結果を隠す比較では、各actorのworkspace/taskだけを別コンテナ等へ渡す。評価者資料、別試行ログ、元repoをマウントしない。グローバル指示・追加Skill・MCP・設定も条件間で揃えて記録し、未隔離なら限界として報告する。自動的なインストール、API接続、反復課金は行わない。

## 評価・受入条件

初回は少数の代表例で入力・観測が成立するか確認する。先に主要なケースと観点を決め、結果に合わせて勝敗を変えない。重要な事例は複数回実行する。盲検化できるなら前後ラベルを伏せて採点し、少数例から一般的な優位性を断定しない。

- 変更レビュー：契約と成果物の証拠を示し、別Intentの侵害・設計とSkillのずれ・組合せの重複を見つける。未実装や正当なトレードオフを一律に違反にしない。
- シナリオ：重大な無断判断・根拠の捏造・必要な相談の欠落を、速度や少ない質問で相殺しない。不要な質問・工程・手戻り、独立作業の進行を別に評価する。
- 評価者：自己申告だけでなくログと成果物を確認する。指摘なし・部分確認・未実行・失敗を区別し、実測できない費用は不明にする。
- 再現性：比較SHA、方針/ケースのhash、モデル・Harness・設定・反復数を残す。入力準備の回帰検証は [test_evals.py](../tests/test_evals.py)。AIの検出力はこれでは検証されない。

最初の採用判断では、明確な違反ケースを見つけ、両立可能・承認済みの負担増ケースを誤って落とさないかを確認する。許容できる費用・遅延は実測を見てmaintainerが判断する。数字が未設定の段階で自動合否にしない。基準の不備は別に記録し、全ての判定を総合点へ潰さない。

実証記録は [validation.md](validation.md)。実行ログはGitHub artifactsか実験用の外部ディレクトリへ保存し、短い結論から証拠へ辿れるようにする。生ログを恒久的な仕様や同期Dashboardにしない。公開前にログ・成果物の情報を確認する。有効性が示せなければAI自動実行を止め、機械検証と必要時の手動検証へ戻す。
