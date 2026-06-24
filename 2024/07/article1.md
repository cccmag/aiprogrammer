# Android Studio 安裝與專案建立

## 開發環境完整建置流程

### 系統需求

開始 Android 開發前，確保您的電腦滿足最低需求：

| 項目 | 最低要求 | 建議 |
|------|---------|------|
| 記憶體 | 8 GB RAM | 16 GB+ |
| 儲存空間 | 8 GB | 16 GB (SSD) |
| 解析度 | 1280×800 | 1920×1080+ |
| 作業系統 | Windows 10 / macOS 11 / Linux | 最新版 |

### 安裝 Android Studio

Android Studio 是 Google 官方整合開發環境（IDE），基於 IntelliJ IDEA。

**步驟一：下載安裝程式**

前往 [Android Studio 官方下載頁面](https://www.google.com/search?q=Android+Studio+download) 選擇對應作業系統的版本。

**步驟二：執行安裝**

```bash
# macOS：開啟下載的 .dmg，將 Android Studio 拖到 Applications
# Windows/Linux：執行安裝程式，依照指示操作
```

**步驟三：安裝 SDK 元件**

第一次啟動時，Android Studio 會自動引導安裝：

```
Android Studio Setup Wizard:
1. Welcome → Next
2. Install Type → Standard (推薦)
3. SDK Components Setup → 確認包含：
   - Android SDK Platform 34
   - Android SDK Build-Tools 34
   - Android Emulator
   - Android SDK Platform-Tools
4. Accept License → Finish
```

### 建立第一個專案

```bash
# 已在 Android Studio 中操作：
# File → New → New Project

# 選擇範本：Empty Views Activity 或 Empty Compose Activity
```

**專案設定表單：**

| 欄位 | 範例值 |
|------|--------|
| Name | My First App |
| Package Name | com.example.myfirstapp |
| Language | Kotlin |
| Minimum SDK | API 24 (Android 7.0) |
| Build Configuration Language | Kotlin DSL (KTS) |

### 專案結構解析

```
MyFirstApp/
├── app/
│   ├── src/
│   │   ├── main/
│   │   │   ├── java/com/example/myfirstapp/
│   │   │   │   └── MainActivity.kt
│   │   │   ├── res/
│   │   │   │   ├── layout/
│   │   │   │   ├── drawable/
│   │   │   │   ├── values/
│   │   │   │   └── mipmap/
│   │   │   └── AndroidManifest.xml
│   │   └── test/
│   └── build.gradle.kts
├── gradle/
├── build.gradle.kts
└── settings.gradle.kts
```

**重點檔案說明：**

- **MainActivity.kt**：程式進入點，第一個 Activity
- **AndroidManifest.xml**：應用程式宣告檔（權限、元件、進入點）
- **build.gradle.kts**：依賴管理和建置設定
- **res/**：資源資料夾（佈局、圖片、字串、主題）

### Gradle 依賴管理

```kotlin
// app/build.gradle.kts
plugins {
  id("com.android.application")
  id("org.jetbrains.kotlin.android")
  id("org.jetbrains.kotlin.plugin.compose")
}

android {
  namespace = "com.example.myfirstapp"
  compileSdk = 34
  defaultConfig {
    applicationId = "com.example.myfirstapp"
    minSdk = 24
    targetSdk = 34
    versionCode = 1
    versionName = "1.0"
  }
  buildFeatures { compose = true }
}

dependencies {
  implementation("androidx.core:core-ktx:1.12.0")
  implementation("androidx.compose.ui:ui:1.6.0")
  implementation("androidx.compose.material3:material3:1.2.0")
  implementation("androidx.activity:activity-compose:1.8.2")
}
```

### 啟動模擬器

Android Studio 內建模擬器，支援多種裝置設定：

1. 點擊工具列 Device Manager 圖示
2. 點選 Create Device
3. 選擇硬體（建議 Pixel 8 Pro）
4. 下載系統映像（建議 API 34）
5. 點選 Finish

啟動模擬器後，點擊 Run 按鈕（綠色三角形）即可在模擬器上執行應用程式。

### 常見問題與排除

| 問題 | 解決方案 |
|------|---------|
| Gradle 同步失敗 | 檢查網路，或使用 Gradle wrapper 更新 |
| 模擬器無法啟動 | 確認 BIOS 開啟虛擬化技術 |
| AVD 速度慢 | 改用 x86_64 映像，啟用 Quick Boot |
| ADB 找不到裝置 | 重新連接 USB 或執行 `adb kill-server` |

---

## 延伸閱讀

- [Android Studio 官方安裝指南](https://www.google.com/search?q=Android+Studio+installation+guide)
- [建立第一個 Android 應用程式](https://www.google.com/search?q=build+first+Android+app)
- [Gradle 設定基礎](https://www.google.com/search?q=Android+Gradle+configuration)
