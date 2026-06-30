# ag-android-developer-skills

Antigravity (Google's Agent-first development platform) 向けに設計された、Androidアプリ開発を支援するエージェントスキル（Agent Skills）のコレクションです。

## 提供するスキル

### 1. [android-build-doctor](skills/android-build-doctor/SKILL.md)
AndroidアプリのGradleビルドなどでエラーが発生した際、ビルドログやスタックトレースを解析し、原因の特定と具体的なコード・設定の修正提案を行います。
*   JDKバージョンとGradle/Android Gradle Plugin (AGP)の不一致の自動診断
*   依存関係の競合（Dependency resolution errors）の解決提案
*   Manifestの競合（Manifest merger errors）の解消支援

---

## インストール方法

GitHub CLI (`gh`) と `gh-skill` 拡張機能を使用して、グローバル環境またはプロジェクトのワークスペースに直接インストールできます。

### グローバルインストール

ローカル環境のすべての Antigravity セッションでこれらのスキルを有効にするには、以下を実行します。

```bash
gh skill install asabon/ag-android-developer-skills --agent antigravity
```
*※ `<OWNER>` はご自身のGitHubユーザー名または組織名に置き換えてください。*

### プロジェクトローカルへのインストール

特定のプロジェクト内のみで本スキルを有効にし、リポジトリに含めてチームで共有したい場合は、プロジェクトのルートディレクトリで `--scope project` オプションを指定して実行します。

```bash
gh skill install asabon/ag-android-developer-skills --agent antigravity --scope project
```

---

## ライセンス

[LICENSE](LICENSE) を参照してください。
