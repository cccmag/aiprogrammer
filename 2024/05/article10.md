# App 上架 Google Play / App Store

## 從開發到發布的完整指南

App 開發完成後，最後一步是上架到應用程式商店。本文詳細介紹 Android（Google Play）和 iOS（App Store）的完整上架流程。

## 上架前檢查清單

### 必要準備

```
☐ 開發者帳號已註冊並付費
   - Apple Developer Program: $99 USD/年
   - Google Play Developer: $25 USD（一次性）

☐ App 圖示已準備
   - iOS: 1024x1024 px（無透明背景）
   - Android: 適配式圖示（前景 108x108，背景 108x108）

☐ 螢幕截圖已準備
   - iOS: 6.7 吋、6.5 吋、5.5 吋
   - Android: 至少 2 張，建議 8 張

☐ 隱私權政策網頁已準備
   - 所有 App 都需要，特別是有帳號系統的 App

☐ 應用程式描述與關鍵字已撰寫
```

## Android：Google Play 上架

### 1. 建置發布版本

```bash
# 產生 AAB（Android App Bundle）
cd android
./gradlew bundleRelease

# 確認 AAB 檔案位置
ls android/app/build/outputs/bundle/release/app-release.aab
```

### 2. Google Play Console 設定

```javascript
// app.json 或 build.gradle 設定
{
    "expo": {
        "version": "1.0.0",
        "android": {
            "package": "com.mycompany.myapp",
            "versionCode": 1,
            "permissions": [
                "CAMERA",
                "ACCESS_FINE_LOCATION",
                "INTERNET"
            ]
        }
    }
}
```

在 Google Play Console 中：

1. 建立應用程式並填寫商店資訊
2. 上傳 AAB 檔案到「正式版本」
3. 完成內容分級問卷
4. 設定定價與發布範圍
5. 提交審查

### 3. Android 自動發布（GitHub Actions）

```yaml
# .github/workflows/android-release.yml
name: Android Release
on:
  push:
    tags: ["v*"]
jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup JDK
        uses: actions/setup-java@v4
        with:
          distribution: "zulu"
          java-version: "17"
      - name: Build AAB
        run: cd android && ./gradlew bundleRelease
      - name: Upload to Google Play
        uses: r0adkll/upload-google-play@v1
        with:
          serviceAccountJson: ${{ secrets.SERVICE_ACCOUNT_JSON }}
          packageName: com.mycompany.myapp
          releaseFiles: android/app/build/outputs/bundle/release/app-release.aab
          track: production
```

## iOS：App Store 上架

### 1. 建置發布版本

```bash
# 使用 Xcode Archive
# 或命令列建置
cd ios
xcodebuild -workspace MyApp.xcworkspace \
    -scheme MyApp \
    -configuration Release \
    -sdk iphoneos \
    archive -archivePath build/MyApp.xcarchive

xcodebuild -exportArchive \
    -archivePath build/MyApp.xcarchive \
    -exportPath build/MyApp.ipa \
    -exportOptionsPlist ExportOptions.plist
```

### 2. App Store Connect 設定

```xml
<!-- ExportOptions.plist -->
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>method</key>
    <string>app-store</string>
    <key>teamID</key>
    <string>YOUR_TEAM_ID</string>
    <key>uploadBitcode</key>
    <true/>
    <key>compileBitcode</key>
    <true/>
</dict>
</plist>
```

### 3. iOS 審查注意事項

iOS 審查比 Android 嚴格，常見被拒原因：

```markdown
1. **登入機制**：如果 App 需要帳號，必須提供「註冊」功能
2. **Apple 登入**：使用第三方登入時，必須同時提供「Sign in with Apple」
3. **隱私權**：必須明確說明資料收集和使用方式
4. **支付**：虛擬商品必須使用 Apple In-App Purchase
5. **測試帳號**：必須提供測試帳號供審查人員使用
```

## 使用 EAS Build（Expo 用戶）

```bash
# 安裝 EAS CLI
npm install -g eas-cli

# 設定建置配置
eas build:configure
```

```json
{
    "cli": { "version": ">= 3.0.0" },
    "build": {
        "production": {
            "android": {
                "buildType": "app-bundle"
            },
            "ios": {
                "autoIncrementBuildNumber": true
            },
            "channel": "production"
        }
    },
    "submit": {
        "production": {
            "android": {
                "serviceAccountKeyPath": "./service-account.json",
                "track": "production"
            },
            "ios": {
                "appleId": "your@email.com",
                "ascAppId": "YOUR_APP_ID",
                "appleTeamId": "YOUR_TEAM_ID"
            }
        }
    }
}
```

```bash
# 建置並提交到商店
eas build --platform all --profile production
eas submit --platform android --profile production
eas submit --platform ios --profile production
```

## 版本管理與更新策略

### 語意化版本號

```javascript
// app.json
{
    "version": "1.2.3",
    // 主版號.次版號.修訂號
    // 1.2.3 → major: 1, minor: 2, patch: 3
}
```

### OTA 更新（Expo Update）

```bash
# 發布 JavaScript 更新（無需商店審查）
eas update --branch production --message "修正登入頁面 bug"
```

---

## 延伸閱讀

- [Google Play Console 說明](https://www.google.com/search?q=Google+Play+Console+help)
- [App Store Review Guidelines](https://www.google.com/search?q=App+Store+Review+Guidelines)
- [EAS Build 文件](https://www.google.com/search?q=Expo+EAS+Build)
