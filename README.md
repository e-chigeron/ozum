# dev-harness

AIとの対話でIntentを実装へ変換し、Gitと決定論的な検証で安全に固定するための最小構成です。Orcaにはworktree、session、diff/review、status hook、usage tracking、model/account切替を任せ、このリポジトリでは再実装しません。

## 構成

- `METHOD.md`: 開発手法の正本
- `profiles/codex/AGENTS.md`: 全リポジトリ共通の短い指示
- `skills/`: 必要時だけ読む再利用手順
- `templates/project/`: 新規プロジェクトの最小雛形
- `orca.yaml`: Orca worktreeのsetup

Home Managerは共通指示と3つのSkillをout-of-store symlinkで配布します。このため、ここでの変更はNixOSの再buildなしに新しいCodex sessionから反映されます。

## 使い方

このリポジトリ自体を検証します。

```console
devenv tasks run harness:check
```

新しいプロジェクトは雛形をコピーしてGitリポジトリにし、`INTENT.md` と必要なspecを現在状態に合わせて編集します。言語固有のtoolchainと検証は、そのプロジェクトの `devenv.nix` と `scripts/verify-project` に追加します。

```console
cp -R templates/project /path/to/new-project
cd /path/to/new-project
git init -b main
devenv tasks run project:verify
```

Orcaではこのリポジトリを登録し、base refを `main` にします。各worktreeのsetupは `devenv shell -- true` のみを行います。標準操作はdevenv taskを正本とし、Quick Commandへ重複させません。

## V0で扱わないもの

Jujutsu、自動Intent conflict hook、会話の永続保存、Context Compiler、常設ADR、Orca orchestration・automations・cloud workspaceは、具体的な不満が観測されるまで追加しません。
