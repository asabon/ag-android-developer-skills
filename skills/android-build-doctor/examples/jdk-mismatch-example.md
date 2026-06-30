# 例：JDKバージョン不整合エラー (Unsupported class file major version)

このファイルは、Android Gradle Plugin (AGP) が要求する JDK バージョンと、実際にビルドで使用されている JDK バージョンが異なる場合に、エージェントが提示すべき解決策の Few-Shot（お手本）です。

## 1. [エラー入力の例]

ユーザーがビルドを実行した際、ターミナルに以下のエラーログが出力された：

```text
FAILURE: Build failed with an exception.

* What went wrong:
An exception occurred applying plugin request [id: 'com.android.application']
> Failed to apply plugin 'com.android.application'.
   > Android Gradle plugin requires Java 17 to run. You are currently using Java 11.
```

または：

```text
* What went wrong:
Could not open settings generic class cache for settings file 'C:\Users\user\Project\settings.gradle' (C:\Users\user\.gradle\caches\8.0\scripts\settings).
> BUG! exception in phase 'semantic analysis' in source unit '_BuildScript_' Unsupported class file major version 61.0
```

---

## 2. [期待されるエージェントの回答・修正手順]

エージェントは以下の通り、原因の解説、解決策の提示、および環境の修正を実施します。

### 回答例

**原因:**
Android Gradle Plugin (AGP) 8.0 以降は、ビルドの実行に **Java 17 (クラスファイルメジャーバージョン 61.0) 以上**を要求します。
現在のビルド環境で使用されている JDK バージョンが Java 11 であるため、ビルドエラーが発生しています。

**解決方法:**
ビルドで使用する JDK バージョンを Java 17 に切り替えてください。

#### ① Android Studio の設定を変更する場合
1. `Settings` (macOS は `Preferences`) > `Build, Execution, Deployment` > `Build Tools` > `Gradle` を開きます。
2. **Gradle JDK** の項目で `JDK 17` (または Android Studio 同梱の `jbr-17`) を選択し、適用します。

#### ② ターミナル（コマンドライン）で切り替える場合
ターミナルで使用される環境変数 `JAVA_HOME` を JDK 17 のパスに変更します。

* **Windows (PowerShell):**
  ```powershell
  $env:JAVA_HOME = "C:\Program Files\Android\Android Studio\jbr"
  ```
  *(Android Studio 同梱の JDK 17 (JetBrains Runtime) を指すパスに設定します)*

* **macOS / Linux:**
  ```bash
  export JAVA_HOME="/Applications/Android Studio.app/Contents/jbr/Contents/Home"
  ```
