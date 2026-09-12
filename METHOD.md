# 開発手法 V0

## 原則

1. 通常contextには現在状態だけを置く。プロジェクトの正本は `INTENT.md` → 関連する `specs/*.md` → tests → implementation の順とする。
2. 不一致を黙って解消しない。衝突の兆候があるときだけ、対象ファイルに限定してGit履歴と変更理由を調べる。
3. 会話、Orcaのsession・comment・metadataは作業記録であり、永続的な正本にしない。
4. 推測より、プロジェクトが定義するbuild、test、lintなどの決定論的検証を優先する。
5. 開発手法は、実際に観測された摩擦や失敗に対する最小の変更として育てる。予想だけで常時指示や工程を増やさない。

## Projectからの還流

開発projectを手法の実験場、dev-harnessを複数projectから学ぶ上流正本として扱う。project側では観測と証拠をそのprojectに残し、別repositoryの手法正本を直接編集しない。代わりに次を構造化した変更候補として上流へ渡す。

- 摩擦の発生条件、頻度、影響、現在の回避策
- 根拠を確認できるproject内の証拠
- 一般化できる範囲と候補変更
- 成功条件と変更を取り消す条件

上流側は現行手法との整合と証拠を確認し、観測で支持される最小変更だけを正本へ反映する。一時的なhandoff payloadはworkspace間の運搬に使っても、現在状態や変更理由の正本にはしない。

## 変更履歴

`INTENT.md` とspecには現在状態だけを書く。過去の理由が必要な場合は、対象を限定して次を使う。

```console
git log --follow -- <path>
git blame <path>
git show <commit> -- <path>
```

一つの意味的変更を一つの原子的commitにまとめ、文脈が必要な場合だけcommit本文へ次の項目を残す。

```text
Why:
Previous:
Supersedes:
Impact:
```
