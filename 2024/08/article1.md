# 文章 1：Flutter SDK 安裝

## 系統需求

Flutter SDK 支援 Windows、macOS、Linux 三大平台。安裝前需確認系統符合最低要求。

### macOS 安裝

1. **下載 SDK**：前往 Flutter 官網下載最新穩定版，或使用 Homebrew：
   ```bash
   brew install --cask flutter
   ```

2. **設定路徑**：
   ```bash
   export PATH="$PATH:`pwd`/flutter/bin"
   ```

3. **執行 flutter doctor**：
   ```bash
   flutter doctor
   ```

### Windows 安裝

1. 從官網下載 ZIP 壓縮檔
2. 解壓縮至 `C:\flutter`
3. 將 `C:\flutter\bin` 加入系統 PATH 環境變數
4. 執行 `flutter doctor` 檢查依賴

### Linux 安裝

```bash
sudo snap install flutter --classic
flutter doctor
```

## 必要依賴

flutter doctor 會檢查以下項目：

- **Android Toolchain**：需安裝 Android Studio 並接受 Android SDK 授權
- **Xcode (macOS)**：iOS 開發必備，包含 Command Line Tools
- **Chrome**：網頁開發的除錯瀏覽器
- **Visual Studio Code / IntelliJ**：建議安裝 Flutter / Dart 擴充套件

## 接受授權

```bash
flutter doctor --android-licenses
```

## 建立第一個專案

```bash
flutter create my_first_app
cd my_first_app
flutter run
```

- https://www.google.com/search?q=Flutter+SDK+installation+guide+2024
- https://www.google.com/search?q=flutter+doctor+troubleshooting
