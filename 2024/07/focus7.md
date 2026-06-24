# Google Play 上架

## 發布流程與最佳實踐

完成應用程式開發後，最後一步就是發布到 Google Play 商店。本文將介紹從開發者帳號申請到應用程式更新的完整流程。

---

## 開發者帳號申請

### 建立 Play Console 帳號

1. 前往 [Google Play Console](https://www.google.com/search?q=Google+Play+Console) 註冊
2. 支付一次性註冊費（約 25 美元）
3. 填寫開發者資訊
4. 同意開發者條款

### 帳號類型

| 類型 | 說明 |
|------|------|
| 個人帳號 | 個人開發者，適合獨立開發者 |
| 組織帳號 | 公司或團隊，需提供組織文件 |

---

## 應用程式簽署

Android 要求所有應用程式使用數位憑證簽署。

### App Signing by Google Play

推薦使用 Google Play 的應用簽署功能：

```gradle
// app/build.gradle.kts
android {
  signingConfigs {
    create("release") {
      storeFile = file("release-keystore.jks")
      storePassword = System.getenv("STORE_PASSWORD")
      keyAlias = System.getenv("KEY_ALIAS")
      keyPassword = System.getenv("KEY_PASSWORD")
    }
  }
  buildTypes {
    release {
      isMinifyEnabled = true
      isShrinkResources = true
      proguardFiles(
        getDefaultProguardFile("proguard-android-optimize.txt"),
        "proguard-rules.pro"
      )
      signingConfig = signingConfigs.getByName("release")
    }
  }
}
```

### 產生金鑰庫

```bash
keytool -genkey -v -keystore release-keystore.jks \
  -keyalg RSA -keysize 2048 -validity 10000 \
  -alias my-key-alias
```

---

## App Bundle（AAB）

Google Play 推薦使用 Android App Bundle (AAB) 格式取代 APK：

```bash
./gradlew bundleRelease
```

AAB 會根據使用者的裝置設定（螢幕密度、CPU 架構、語言）動態生成最佳化的 APK。

---

## 商店列表最佳化

### 必要資訊

| 欄位 | 說明 |
|------|------|
| 應用程式名稱 | 最多 50 字元，需反映 App 功能 |
| 簡短描述 | 最多 80 字元，一句話吸引使用者 |
| 完整描述 | 最多 4000 字元，詳細說明功能與特性 |
| 螢幕截圖 | 至少 2 張，建議 8 張，解析度為 1080p |
| 特色圖片 | 1024×500 像素 |
| 圖示 | 512×512 像素（適配 Adaptive Icon） |
| 分類 | 選擇合適的應用程式分類 |

### 最佳化技巧

```text
🔹 在描述中使用關鍵字（但不過度堆砌）
🔹 提供多語言商店列表
🔹 定期更新截圖
🔹 使用 A/B 測試不同圖示和描述
🔹 加入應用內瀏覽預覽功能
```

---

## 評分與評論管理

### 監控使用者反饋

```kotlin
// 使用 In-App Review API 詢問評分
class ReviewHelper {
  fun requestReview(activity: Activity) {
    ReviewManagerFactory.create(activity).apply {
      requestReviewFlow().addOnCompleteListener { task ->
        if (task.isSuccessful) {
          launchReviewFlow(activity, task.result)
        }
      }
    }
  }
}
```

### 回覆評論

- 在 7 天內回覆使用者評論
- 對負面評論專業且友善地回應
- 將常見問題轉化為 FAQ

---

## 更新策略

### 版本命名

```gradle
android {
  defaultConfig {
    versionCode = 7         // 內部版本號（遞增整數）
    versionName = "1.2.3"   // 使用者可見版本名稱
  }
}
```

### 階段性發布

```text
1. 內部測試（Internal Testing）：僅限開發者
2. 封閉測試（Closed Testing）：邀請測試者（最多 100 人）
3. 開放測試（Open Testing）：開放註冊
4. 正式發布（Production）：向所有使用者發布
```

### 更新注意事項

- **資料庫遷移**：Room 架構變更時使用 Migration
- **向下相容**：使用 minSdkVersion 和 targetSdkVersion 管理
- **灰度發布**：先向 1% - 5% 使用者發布，監控錯誤率

---

## 收入與獲利

### 獲利選項

| 模式 | 說明 |
|------|------|
| 付費應用 | 下載前付費 |
| 應用內購買 | 數位商品或解鎖功能 |
| 訂閱 | 定期收費 |
| 廣告 | Google AdMob 整合 |
| Freemium | 免費 + 付費解鎖 |

---

## 總結

發布應用程式到 Google Play 不僅是技術過程，也涉及市場行銷和使用者經營。透過 App Signing、AAB 格式、商店列表最佳化和階段性發布策略，開發者可以確保應用程式的成功發布和持續成長。

---

## 延伸閱讀

- [Google Play Console 使用指南](https://www.google.com/search?q=Google+Play+Console+guide)
- [Android App Bundle 介紹](https://www.google.com/search?q=Android+App+Bundle)
- [Google Play 政策中心](https://www.google.com/search?q=Google+Play+policy+center)
