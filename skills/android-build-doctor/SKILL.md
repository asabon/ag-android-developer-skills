---
name: android-build-doctor
description: Androidアプリ開発におけるGradleビルドエラーや環境設定エラーのログ（Kotlinコンパイルエラー、依存関係の競合、SDK/JDKミスマッチ、Manifestマージ失敗など）を解析し、具体的な解決策と修正コードを提供します。
---

# Android Build Doctor

このスキルは、Androidアプリのビルドエラーやテスト失敗が発生した際に、ビルドログやシステム構成を解析し、最も効率的かつ安全な解決策を提示するためのガイドラインです。

## トリガー条件

以下のファイルやログにビルドエラー、コンパイルエラー、または設定エラーが含まれている場合、本スキルがアクティブになります。

*   ターミナル出力またはログファイル内の Gradle ビルドエラー (`* What went wrong:`, `BUILD FAILED`)
*   Kotlin / Java コンパイルエラー (`Unresolved reference:`, `Symbol not found`)
*   依存関係解決エラー (`Could not resolve all dependencies`, `Failed to resolve:`)
*   Android SDK / JDK 互換性エラー (`Unsupported class file major version`, `Minimum supported Gradle version is...`)
*   Manifest マージエラー (`Manifest merger failed with multiple errors`)
*   マルチデクス / 重複クラスエラー (`Duplicate class found in modules`)

---

## 解析手順

ビルドエラーを検知した場合、以下のステップに従って解析を行います。

### 1. エラー情報の収集
*   エラーログの**スタックトレース**および Gradle が出力した原因メッセージ (`* What went wrong:`) を特定します。
*   可能であれば、以下のプロジェクト構成ファイルを読み取り、現在のバージョン関係を把握します。
    *   [gradle-wrapper.properties](file:///e:/work/ag-android-build-doctor/gradle/wrapper/gradle-wrapper.properties)（Gradleのバージョン）
    *   ルートの [build.gradle](file:///e:/work/ag-android-build-doctor/build.gradle) または [build.gradle.kts](file:///e:/work/ag-android-build-doctor/build.gradle.kts)（Android Gradle Plugin (AGP) や Kotlin のバージョン）
    *   モジュールごとの `build.gradle`（`compileSdk`, `targetSdk`, `minSdk` および依存関係ライブラリ）

### 2. 根本原因の分類
エラーを以下のいずれかに分類し、解決のアプローチを決定します。

| エラーカテゴリ | 主なキーワード | 調査対象ファイル |
| :--- | :--- | :--- |
| **JDK/Gradle 互換性** | `Unsupported class file major version`, `Minimum supported Gradle version` | `gradle-wrapper.properties`, Java実行環境のバージョン |
| **依存関係解決** | `Could not resolve all files`, `Failed to resolve:` | 各モジュールの `build.gradle`, `settings.gradle` のリポジトリ設定 |
| **コンパイル/シンボル** | `Unresolved reference:`, `Cannot find symbol` | エラーが発生しているソースコード (`.kt`, `.java`) |
| **Manifest マージ** | `Manifest merger failed`, `Attribute ... is also present at` | `AndroidManifest.xml`, マージされたマニフェスト報告ファイル |
| **重複クラス/D8** | `Duplicate class ... found in`, `DexArchiveMergerException` | 依存関係ツリー、Jetpack（AndroidX）移行設定 |

### 3. 解決策の提示
ユーザーに対し、以下のフォーマットに沿って明快な改善案を提示します。回答の組み立てに際しては、`examples/` ディレクトリ内の事例（例: [jdk-mismatch-example.md](file:///e:/work/ag-android-build-doctor/skills/android-build-doctor/examples/jdk-mismatch-example.md)）を参考にし、同様のトーンと構成で回答を生成してください。

#### ① 原因の解説
なぜこのエラーが発生したのか、背景（例: 「Gradle 8.0 は JDK 17 以上を要求しますが、現在は JDK 11 が使用されています」など）を簡潔に説明します。

#### ② 具体的な修正方法
可能な限り、自動で実行できるコマンドや、書き換えるべき具体的なコードの差分（Diff形式）を提示します。

*   **ファイル書き換えの例 (build.gradle.kts の修正など):**
    ```diff
    dependencies {
    -    implementation("com.example:library:1.0.0")
    +    implementation("com.example:library:1.2.0") // バージョン競合を解消
    }
    ```

*   **環境構築の修正が必要な場合:**
    OS（Windows / macOS / Linux）ごとの設定変更コマンドや手順を示します。

---

## 注意事項

*   **破壊的変更の回避**: ライブラリのメジャーバージョンアップを行う場合は、他の依存関係やコードに影響が出るリスクがあることを必ず警告してください。
*   **キャッシュのクリア**: ビルド環境がクリーンでないことが原因と疑われる場合は、`./gradlew clean` や Gradleキャッシュの削除（`--no-build-cache` や `.gradle/` ディレクトリの削除）を段階的に試すよう案内してください。

---

## 新しい解決パターンの自動フィードバック

既存の `examples/` に存在しない新規のエラーパターンの解決に成功した場合は、以下の手順で自動フィードバックを実行してください。

1. **フィードバックの提案**:
   ユーザーに対して、「今回のエラー解決事例はまだ共有リポジトリに登録されていません。共通リポジトリ（`asabon/ag-android-developer-skills`）へ Issue として自動で登録（共有）してもよろしいですか？」と確認してください。
2. **GitHub CLI による Issue 作成**:
   ユーザーの承諾が得られた場合、GitHub CLI (`gh` コマンド) を呼び出して、以下のような Issue を自動的に作成してください。
   * **コマンド例**:
     ```bash
     gh issue create --repo asabon/ag-android-developer-skills --title "[New Example] <エラーの概要>" --body "<エラーログと解決手順のMarkdown>"
     ```
   * **Issue本文のMarkdown構造**:
     * `# エラー内容`（発生したビルドログの抜粋）
     * `# 解決方法`（具体的な修正コードの Diff や実行した手順の解説）
