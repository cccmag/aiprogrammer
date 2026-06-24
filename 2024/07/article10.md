# Android 測試與發布

## 單元測試到 Google Play 上架

### 測試金字塔

```
       ╱  ╲
      ╱ E2E ╲
     ╱  測試  ╲
    ╱───────────╲
   ╱  整合測試   ╲
  ╱────────────────╲
 ╱    單元測試       ╲
╱──────────────────────╲
```

- **底層**：大量快速、穩定的單元測試
- **中層**：適量的整合測試（ViewModel + Repository）
- **頂層**：少量的端對端（E2E）測試

### 單元測試

測試 ViewModel 和 Repository 的業務邏輯：

```kotlin
// build.gradle.kts
dependencies {
  testImplementation("junit:junit:4.13.2")
  testImplementation("org.jetbrains.kotlinx:kotlinx-coroutines-test:1.7.3")
  testImplementation("app.cash.turbine:turbine:1.0.0")  // Flow 測試
}

// ViewModel 測試
class CounterViewModelTest {
  private lateinit var viewModel: CounterViewModel

  @Before
  fun setup() {
    viewModel = CounterViewModel()
  }

  @Test
  fun `increment increases count by 1`() = runTest {
    viewModel.increment()
    val count = viewModel.count.first()
    assertEquals(1, count)
  }

  @Test
  fun `multiple increments accumulate`() = runTest {
    repeat(5) { viewModel.increment() }
    val count = viewModel.count.first()
    assertEquals(5, count)
  }
}
```

### UI 測試（Compose）

```kotlin
// build.gradle.kts
androidTestImplementation("androidx.compose.ui:ui-test-junit4:1.6.0")
debugImplementation("androidx.compose.ui:ui-test-manifest:1.6.0")

@RunWith(AndroidJUnit4::class)
class CounterScreenTest {

  @get:Rule
  val composeTestRule = createComposeRule()

  @Test
  fun `counter starts at zero`() {
    composeTestRule.setContent { CounterScreen() }
    composeTestRule.onNodeWithText("Count: 0").assertExists()
  }

  @Test
  fun `increment button works`() {
    composeTestRule.setContent { CounterScreen() }
    composeTestRule.onNodeWithText("+").performClick()
    composeTestRule.onNodeWithText("Count: 1").assertExists()
  }
}
```

### 測試涵蓋範圍

```kotlin
class ViewModelIntegrationTest {
  private lateinit var viewModel: NoteViewModel
  private lateinit var db: AppDatabase

  @Before
  fun setup() {
    val context = ApplicationProvider.getApplicationContext<Context>()
    db = Room.inMemoryDatabaseBuilder(context, AppDatabase::class.java).build()
    viewModel = NoteViewModel(/* 使用測試用的db */)
  }

  @After
  fun teardown() {
    db.close()
  }

  @Test
  fun `add note and verify in database`() = runTest {
    viewModel.addNote("Test Title", "Test Content")
    val notes = viewModel.allNotes.first()
    assertEquals(1, notes.size)
    assertEquals("Test Title", notes[0].title)
  }
}
```

### 應用程式簽署

```gradle
// app/build.gradle.kts
android {
  signingConfigs {
    create("release") {
      storeFile = file("keystore.jks")
      storePassword = System.getenv("KEYSTORE_PASSWORD")
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

### 建置簽署版本

```bash
# 產生 App Bundle
./gradlew bundleRelease

# 產生 APK
./gradlew assembleRelease

# 輸出位置：
# app/build/outputs/bundle/release/app-release.aab
# app/build/outputs/apk/release/app-release.apk
```

### 上架到 Google Play

**步驟一：建立開發者帳號**

前往 Google Play Console 註冊（一次性 25 美元費用）。

**步驟二：建立應用程式**

1. 點選「建立應用程式」
2. 選擇應用程式名稱和預設語言
3. 選擇是應用程式還是遊戲

**步驟三：填寫商店資訊**

| 區塊 | 內容 |
|------|------|
| 簡短描述 | 80 字元內，吸引使用者 |
| 完整描述 | 4000 字元內，詳細功能說明 |
| 螢幕截圖 | 至少 2 張，建議 8 張 |
| 圖示 | 512×512 適配 Adaptive Icon |
| 分類 | 選擇正確的應用程式分類 |
| 標籤 | 最多 5 個關鍵字 |

**步驟四：設定內容評級**

填寫問卷以獲得 PEGI/ESRB 年齡分級。

**步驟五：定價與發布範圍**

選擇免費或付費，以及發布國家/地區。

**步驟六：發布前檢查**

```text
☑ Android App Bundle (AAB) 上傳成功
☑ 版本號正確（versionCode 遞增）
☑ 商店資訊完整
☑ 隱私權政策連結
☑ 內容評級完成
☑ 測試人員帳號設定（可選）
```

### 階段性發布

Google Play 支援多層測試管道：

```
內部測試 → 封閉測試 → 開放測試 → 正式發布
  │          │          │           │
  開發者     邀請測試    公開註冊    全部使用者
  (最多100人)  (最多100人)
```

```kotlin
// 加入內部測試追蹤
class PlayCoreManager(private val context: Context) {
  fun showInAppUpdate() {
    val appUpdateManager = AppUpdateManagerFactory.create(context)
    val task = appUpdateManager.appUpdateInfo
    task.addOnSuccessListener { info ->
      if (info.updateAvailability() == UpdateAvailability.UPDATE_AVAILABLE) {
        appUpdateManager.startUpdateFlow(
          info, context,
          InAppUpdateActivity::class.java,
          AppUpdateType.IMMEDIATE
        )
      }
    }
  }
}
```

### 發布後監控

```kotlin
// Firebase Crashlytics（崩潰監控）
class MyApplication : Application() {
  override fun onCreate() {
    super.onCreate()
    FirebaseCrashlytics.getInstance().apply {
      setCustomKey("build_version", BuildConfig.VERSION_NAME)
      log("Application started")
    }
  }
}

// Google Play Console 提供：
// - 崩潰與 ANR 報告
// - 評分與評論
// - 下載與營收統計
// - 測試實驗室結果
```

### 持續整合

```yaml
# .github/workflows/android_ci.yml
name: Android CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up JDK 17
        uses: actions/setup-java@v4
        with:
          java-version: '17'
      - name: Unit Tests
        run: ./gradlew testDebugUnitTest
      - name: Build Debug APK
        run: ./gradlew assembleDebug
```

---

## 總結

從單元測試到 Google Play 發布，每個環節都影響著應用程式的品質和使用者體驗。建立完整的測試習慣、正確的簽署流程和階段性發布策略，是成功發布 Android 應用的關鍵。

---

## 延伸閱讀

- [Android 測試指南](https://www.google.com/search?q=Android+testing+guide)
- [Google Play 上架流程](https://www.google.com/search?q=Google+Play+publish+process)
- [Android CI/CD 最佳實踐](https://www.google.com/search?q=Android+CI+CD+best+practices)
