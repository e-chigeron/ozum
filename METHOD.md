# 開発手法 V0

## 原則

1. 通常contextには現在状態だけを置く。プロジェクトの正本は `INTENT.md` → 関連する `specs/*.md` → tests → implementation の順とする。
2. 不一致を黙って解消しない。衝突の兆候があるときだけ、対象ファイルに限定してGit履歴と変更理由を調べる。
3. 会話、Orcaのsession・comment・metadataは作業記録であり、永続的な正本にしない。
4. 推測より、プロジェクトが定義するbuild、test、lintなどの決定論的検証を優先する。
5. 開発手法は、実際に観測された摩擦や失敗に対する最小の変更として育てる。予想だけで常時指示や工程を増やさない。

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
