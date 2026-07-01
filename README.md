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

GitHub CLI (`gh`) を使用して、グローバル環境またはプロジェクトのワークスペースに直接インストールできます。

### 1. すべてのスキルを一括インストールする場合

リポジトリに含まれるすべてのスキルをまとめてインストールするには、リポジトリ名のみを指定します。

#### グローバルインストール

ローカル環境のすべての Antigravity セッションでこれらのスキルを有効にするには、以下を実行します。

```bash
gh skill install asabon/ag-android-developer-skills --agent antigravity
```
*※ `asabon` はご自身のGitHubユーザー名または組織名に置き換えてください。*

#### プロジェクトローカルへのインストール

特定のプロジェクト内のみで本スキルを有効にし、リポジトリに含めてチームで共有したい場合は、プロジェクトのルートディレクトリで以下を実行します。

```bash
gh skill install asabon/ag-android-developer-skills --agent antigravity --scope project
```

### 2. 特定のスキルのみを指定してインストールする場合

リポジトリ内の特定のスキルのみを指定して個別にインストールするには、リポジトリ名の後ろにスキル名（例: `android-build-doctor`）を指定します。

#### グローバルインストール

```bash
gh skill install asabon/ag-android-developer-skills android-build-doctor --agent antigravity
```

#### プロジェクトローカルへのインストール

```bash
gh skill install asabon/ag-android-developer-skills android-build-doctor --agent antigravity --scope project
```

---

## アップデート方法

インストール済みのスキルを最新バージョンに更新するには、以下のコマンドを使用します。

### すべてのスキルを一括で更新する

```bash
gh skill update --all
```

### 対話型で確認しながら更新する

```bash
gh skill update
```

### 特定のスキルを指定して更新する

```bash
gh skill update <skill-name>
```
*※ 例: `gh skill update android-build-doctor`*

---

## ライセンス

[LICENSE](LICENSE) を参照してください。
