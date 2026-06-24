# Android SDK 與開發環境架設

## Android SDK 概述

Android SDK（Software Development Kit）是開發 Android 應用程式的必備工具包。2008 年初發布的預覽版提供了完整的開發環境，讓開發者能夠開始 Android 應用程式的開發工作。

### SDK 主要元件

Android SDK 包含以下核心元件：

| 元件 | 說明 |
|------|------|
| Android 函式庫 | 應用程式框架 API |
| 開發工具 | 編譯、打包、除錯工具 |
| 模擬器 | ARM 架構手機模擬器 |
| 文件與範例 | API 文件和範例程式碼 |
| USB 驅動程式 | 連接真實設備 |

## 系統需求

### 支援的作業系統

- **Windows**：XP、Vista
- **Mac OS X**：10.4.8 以上
- **Linux**：Ubuntu 或其他主流發行版

### Java 需求

Android 開發需要 Java Development Kit（JDK）：

```bash
# 檢查 Java 版本
java -version

# 建議使用 Java 5 或 Java 6
```

### 硬體需求

- **處理器**：Pentium 4 或同等級
- **記憶體**：建議 2GB 以上
- **硬碟空間**：建議 10GB 以上
- **螢幕解析度**：建議 1280x800 或更高

## 安裝步驟

### Step 1：下載 SDK

1. 前往 Android 開發者網站
2. 下載對應您作業系統的 SDK
3. 解壓縮到您選擇的位置

```bash
# Linux/Mac 範例
tar -xzf android-sdk-linux_x86-1.0_r1.tgz
mv android-sdk-linux_x86-1.0_r1 ~/android-sdk
```

### Step 2：設定環境變數

將 SDK 的 `tools` 和 `platform-tools` 目錄加入到 PATH：

```bash
# 新增到 ~/.bashrc 或 ~/.profile
export ANDROID_HOME=~/android-sdk
export PATH=$PATH:$ANDROID_HOME/tools
export PATH=$PATH:$ANDROID_HOME/platform-tools
```

### Step 3：驗證安裝

```bash
# 顯示 SDK 版本資訊
android list targets
```

## Eclipse 整合開發環境

### 為什麼使用 Eclipse？

Eclipse 是 Android 開發的主流 IDE，提供了：

- **程式碼編輯**：語法高亮、自動完成
- **視覺化設計**：拖放式 UI 編輯器
- **整合除錯**：完整的除錯工具
- **專案管理**：易於管理專案結構

### 安裝 ADT 擴充套件

ADT（Android Development Tools）是 Eclipse 的擴充套件：

1. 啟動 Eclipse
2. 選擇 Help → Software Updates → Find and Install
3. 新增更新網址：
   ```
   https://dl-ssl.google.com/android/eclipse/
   ```
4. 選擇安裝 Android Development Tools
5. 依照指示完成安裝

### 設定 ADT

安裝完成後，設定 SDK 路徑：

1. 選擇 Window → Preferences
2. 選擇 Android 項目
3. 設定 SDK Location 為您的 SDK 路徑

## 建立第一個專案

### New Android Project 精靈

1. 選擇 File → New → Project
2. 選擇 Android → Android Project
3. 填寫專案資訊：

```
Project Name: HelloAndroid
Build Target: Android 1.0
Application Name: Hello Android
Package Name: com.example.helloandroid
Create Activity: HelloActivity
```

### 專案結構

建立的專案包含以下結構：

```
HelloAndroid/
├── AndroidManifest.xml    # 應用程式設定
├── src/                    # Java 原始碼
│   └── com/example/hello/
│       └── HelloActivity.java
├── res/                    # 資源檔案
│   ├── layout/             # 版面配置
│   │   └── main.xml
│   └── values/             # 字串、色彩等
│       └── strings.xml
└── gen/                    # 自動產生（勿編輯）
    └── com/example/hello/R.java
```

## Android 模擬器

### 啟動模擬器

模擬器讓您無需真實手機即可測試應用程式：

```bash
# 建立 AVD（Android Virtual Device）
android create avd -n my_avd -t 1

# 啟動模擬器
emulator -avd my_avd
```

### 模擬器功能

```
┌──────────────────────────┐
│      模擬器功能           │
├──────────────────────────┤
│  電話功能    ✔           │
│  網路       ✔           │
│  GPS        ✔ (可設定)  │
│  加速計     ✘           │
│  相機       ✘           │
│  藍牙       ✘           │
│  Wi-Fi      ✔           │
│  SD 卡      ✔           │
└──────────────────────────┘
```

### 模擬器限制

模擬器是 ARM 軟體模擬，執行速度比真實設備慢。建議在真實設備上進行效能測試。

## 常用開發工具

### ADB（Android Debug Bridge）

ADB 是與模擬器或設備通訊的命令列工具：

```bash
# 列出已連接的設備
adb devices

# 安裝應用程式
adb install myapp.apk

# 複製檔案到設備
adb push local.txt /sdcard/

# 查看日誌
adb logcat
```

### Dalvik Debug Monitor Service (DDMS)

DDMS 提供了強大的除錯和監控功能：

- **執行緒檢視**：查看執行緒狀態
- **堆積分析**：記憶體使用情況
- **檔案總管**：瀏覽設備檔案系統
- **模擬器控制**：控制模擬器狀態
- **螢幕截圖**：擷取螢幕畫面

### Hierarchy Viewer

視覺化工具用於檢視 UI 元件階層和效能分析。

## 疑難排解

### 常見問題

**SDK 無法啟動**：
- 確認 JAVA_HOME 環境變數已設定
- 確認路徑中包含 Java 的 bin 目錄

**模擬器執行緩慢**：
- 這是正常現象，嘗試使用真實設備
- 增加模擬器記憶體

**看不見 ADT 選項**：
- 確認 ADT 擴充套件已正確安裝
- 重新啟動 Eclipse

---

**延伸閱讀**

- [Android SDK download](https://www.google.com/search?q=Android+SDK+download)
- [Android+development+environment+setup](https://www.google.com/search?q=Android+development+environment+setup)
- [Eclipse+Android+ADT](https://www.google.com/search?q=Eclipse+Android+ADT+installation)