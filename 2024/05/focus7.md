# 發布與上架流程

## App 發布的生命週期

從開發完成到使用者下載，App 需要經過簽名、建置、審查和發布四個階段：

```
開發 ──→ 簽名 ──→ 建置 ──→ 審查 ──→ 發布 ──→ 使用者
```

## 證書與簽名

### iOS 證書管理

iOS 應用需要 Apple Developer Program 帳號（年費 $99 USD）。

```bash
# 使用 Xcode 自動管理簽名
# 或在 Project Settings 中手動設定

# 需要的憑證：
# - Development Certificate：開發用
# - Distribution Certificate：發布用
# - Push Notification Certificate：推播用
```

### Android 簽名

Android 使用金鑰庫簽名：

```bash
# 產生 JKS 金鑰庫
keytool -genkey -v \
    -keystore my-release-key.jks \
    -keyalg RSA \
    -keysize 2048 \
    -validity 10000 \
    -alias my-alias

# 設定 gradle.properties
MYAPP_UPLOAD_STORE_FILE=my-release-key.jks
MYAPP_UPLOAD_KEY_ALIAS=my-alias
MYAPP_UPLOAD_STORE_PASSWORD=***
MYAPP_UPLOAD_KEY_PASSWORD=***
```

## Google Play 上架流程

### 建置 AAB

```bash
cd android
./gradlew bundleRelease
# 輸出：android/app/build/outputs/bundle/release/app-release.aab
```

### Google Play Console 步驟

1. 前往 Google Play Console（年費 $25 USD）
2. 建立應用程式
3. 填寫商店資訊：
   - 應用程式名稱與描述
   - 截圖與影片預覽
   - 分類與標籤
   - 評級問卷
4. 上傳 AAB 檔案
5. 設定內容分級
6. 設定發布範圍（內部測試 / 公開測試 / 正式發布）
7. 審查（通常 1-3 天）
8. 發布

### EAS Build（Expo 推薦）

使用 Expo 的開發者可以使用 EAS Build 雲端建置：

```bash
# 安裝 EAS CLI
npm install -g eas-cli

# 登入 Expo 帳號
eas login

# 設定建置配置
eas build:configure

# 建置 Android
eas build --platform android --profile release

# 建置 iOS
eas build --platform ios --profile release
```

```json
// eas.json
{
    "build": {
        "release": {
            "android": {
                "buildType": "app-bundle"
            },
            "ios": {
                "autoIncrement": true
            }
        }
    }
}
```

## App Store 上架流程

### 建置 IPA

```bash
# 方法一：Xcode Archive
# Product > Archive > Distribute App

# 方法二：命令列
xcodebuild -workspace ios/MyApp.xcworkspace \
    -scheme MyApp \
    -sdk iphoneos \
    -configuration Release \
    archive -archivePath build/MyApp.xcarchive

xcodebuild -exportArchive \
    -archivePath build/MyApp.xcarchive \
    -exportOptionsPlist exportOptions.plist \
    -exportPath build/MyApp.ipa
```

### App Store Connect 步驟

1. 登入 App Store Connect
2. 新增 App（Bundle ID 需與專案一致）
3. 填寫應用程式資訊：
   - 名稱、副標題、關鍵字
   - 描述與新功能
   - 截圖（6.7/6.5/5.5 吋）
   - App 預覽影片
4. 上傳建置檔案（透過 Xcode 或 Transporter）
5. 設定價格與銷售範圍
6. 提交審查（通常 1-7 天）
7. 審查通過後手動發布

## OTA 更新（CodePush）

對於 JavaScript 層面的修改，可以使用 CodePush 實現即時更新（無需通過 App Store / Google Play 審查）：

```bash
npm install react-native-code-push

# 註冊應用
appcenter codepush deployment add -a MyApp-ios Staging

# 發布更新
appcenter codepush release-react -a MyApp-ios -d Staging
```

```jsx
import CodePush from "react-native-code-push";

const App = () => {
    // ...
};

export default CodePush({
    checkFrequency: CodePush.CheckFrequency.ON_APP_RESUME,
})(App);
```

### 發布檢查清單

```
發布前檢查項目：
☐ 版本號已更新（app.json / build.gradle / Info.plist）
☐ 所有第三方 SDK 金鑰已設定
☐ App 圖示與啟動畫面已準備
☐ 隱私權政策 URL 已設定
☐ 深層連結（Deep Link）已配置
☐ 推播通知已設定
☐ Analytics 與 Crash Reporting 已啟用
☐ 螢幕截圖已準備
☐ 應用程式描述已撰寫
☐ 測試團隊已完成 QA
```

---

## 延伸閱讀

- [Google Play Console 指南](https://www.google.com/search?q=Google+Play+Console+publishing+guide)
- [App Store Review Guidelines](https://www.google.com/search?q=App+Store+Review+Guidelines)
- [CodePush OTA 更新](https://www.google.com/search?q=CodePush+React+Native+OTA)

---

*本篇文章為「AI 程式人雜誌 2024 年 5 月號」焦點系列之七。*
