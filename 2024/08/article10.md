# 文章 10：建置 APK 與 IPA

## Android 建置

### 設定應用程式簽署

編輯 `android/app/build.gradle`：

```gradle
android {
  signingConfigs {
    release {
      storeFile file('my-release-key.jks')
      storePassword '密碼'
      keyAlias 'my-key'
      keyPassword '密碼'
    }
  }
  buildTypes {
    release {
      signingConfig signingConfigs.release
    }
  }
}
```

### 產生簽署金鑰

```bash
keytool -genkey -v -keystore my-release-key.jks \
  -keyalg RSA -keysize 2048 -validity 10000 -alias my-key
```

### 建置 APK

```bash
flutter build apk --split-per-abi
```

此命令產生三個 APK（arm64-v8a、armeabi-v7a、x86_64），各平台只需安裝對應版本。

### 建置 App Bundle

Google Play 從 2021 年 8 月起要求新上架應用使用 Android App Bundle（AAB）。

```bash
flutter build appbundle
```

產生的 AAB 位於 `build/app/outputs/bundle/release/app-release.aab`。

## iOS 建置

### 前置準備

1. 加入 Apple Developer Program（年費 $99 USD）
2. 在 Xcode 中設定 Team 與 Bundle Identifier

### 建置 IPA

```bash
flutter build ios --release
```

然後在 Xcode 中：

1. 開啟 `ios/Runner.xcworkspace`
2. 選擇 Product → Archive
3. 在 Organizer 中點選 Distribute App
4. 選擇 App Store Connect 或 Ad Hoc 等方式

### 版本號管理

編輯 `pubspec.yaml`：

```yaml
version: 1.0.0+1    # 版本名稱+版本代碼
```

或分別設定 Android 與 iOS：

- Android：編輯 `android/app/build.gradle` 中的 `versionCode` 與 `versionName`
- iOS：在 Xcode 專案設定中修改 Version 與 Build

## 發布前檢查清單

- [ ] 移除所有 debug 標誌與除錯輸出
- [ ] 確認網路權限宣告正確
- [ ] 測試所有第三方登入功能
- [ ] 檢查應用圖示與啟動畫面
- [ ] 驗證深層連結設定
- [ ] 執行 ProGuard/R8 程式碼混淆

## CI/CD 自動化

使用 GitHub Actions 或 Codemagic 自動化建置流程：

```yaml
# .github/workflows/flutter-build.yml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: subosito/flutter-action@v2
      - run: flutter pub get
      - run: flutter build appbundle
```

- https://www.google.com/search?q=Flutter+build+APK+release+2024
- https://www.google.com/search?q=Flutter+build+iOS+IPA+App+Store+Connect
