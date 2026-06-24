# Android 平台架構

## 從 Linux 核心到應用層

Android 採用分層架構設計，從底層的 Linux 核心到上層的系統應用，每一層都扮演著關鍵角色。理解這個架構是成為優秀 Android 開發者的第一步。

---

## 系統架構四層次

```
┌─────────────────────────────────────────────┐
│           系統應用層                          │
│  電話 · 聯絡人 · 瀏覽器 · 設定 · 相機       │
├─────────────────────────────────────────────┤
│           應用框架層 (Java API)              │
│  Activity Manager · Window Manager          │
│  Content Providers · View System            │
│  Package Manager · Telephony Manager        │
├─────────────────────────────────────────────┤
│           系統執行層                          │
│  Android Runtime (ART) · Native libs        │
│  HAL (硬體抽象層)                           │
├─────────────────────────────────────────────┤
│           Linux 核心層                       │
│  行程管理 · 記憶體管理 · 驅動程式            │
│  網路堆疊 · 電源管理                        │
└─────────────────────────────────────────────┘
```

### 第一層：Linux 核心

Android 基於 Linux 核心（目前使用 LTS 版本），提供：

- **行程管理**：每個應用程式運行在獨立行程中
- **記憶體管理**：低記憶體時自動終止背景行程
- **驅動程式**：顯示、相機、音訊、Wi-Fi、藍牙等硬體驅動
- **電源管理**：電池最佳化與喚醒鎖（Wake Lock）
- **Binder IPC**：跨行程通訊機制

安全性是核心的重要考量。Android 使用 Linux 的使用者與群組模型隔離應用程式，每個應用程式以獨立使用者的身分運行。

### 第二層：HAL 與原生函式庫

硬體抽象層（HAL）定義了硬體廠商需實作的標準介面：

```cpp
// HAL 範例：Camera 模組
typedef struct camera_module {
  hw_module_t common;
  int (*get_number_of_cameras)(void);
  int (*get_camera_info)(int id, camera_info *info);
} camera_module_t;
```

重要的原生函式庫包括：

- **WebKit**：網頁渲染引擎
- **OpenMAX**：多媒體編解碼
- **OpenGL ES / Vulkan**：3D 圖形渲染
- **SSL**：網路安全傳輸

### 第三層：Android Runtime (ART)

ART 取代了早期的 Dalvik VM，在 Android 5.0 之後成為正式執行環境：

- **AOT 編譯**：應用程式安裝時編譯為原生機器碼
- **JIT 編譯**：熱點程式碼即時編譯
- **垃圾回收**：改良的並行 GC 減少暫停時間
- **記憶體最佳化**：壓縮 GC 與物件共用

ART 執行 DEX（Dalvik Executable）位元碼，這是從 Java/Kotlin 原始碼編譯而來的中間表示。

### 第四層：應用框架層

這層是開發者最常接觸的 API，提供：

```
┌──────────────────────────────────┐
│  Activity Manager               │
│  管理 Activity 生命週期和返回棧   │
├──────────────────────────────────┤
│  Content Provider               │
│  跨應用程式資料共享              │
├──────────────────────────────────┤
│  View System                    │
│  按鈕、文字、列表等 UI 元件      │
├──────────────────────────────────┤
│  Notification Manager           │
│  通知顯示與管理                  │
├──────────────────────────────────┤
│  Package Manager                │
│  應用程式安裝與權限管理          │
└──────────────────────────────────┘
```

### 第五層：系統應用層

Android 出廠時預裝一系列系統應用，包括電話、聯絡人、瀏覽器、相機、設定等。這些應用使用與第三方應用相同的 API。

---

## 應用程式元件

Android 應用由四大元件構成：

### Activity

Activity 提供使用者可互動的畫面。每個 Activity 相當於一個「頁面」：

```kotlin
class MainActivity : AppCompatActivity() {
  override fun onCreate(savedInstanceState: Bundle?) {
    super.onCreate(savedInstanceState)
    setContentView(R.layout.activity_main)
  }
}
```

### Service

Service 在背景執行長時間操作：

```kotlin
class MyService : Service() {
  override fun onStartCommand(intent: Intent, flags: Int, id: Int): Int {
    // 執行背景工作
    return START_STICKY
  }
}
```

### BroadcastReceiver

接收系統或應用發送的廣播：

```kotlin
class BootReceiver : BroadcastReceiver() {
  override fun onReceive(context: Context, intent: Intent) {
    if (intent.action == Intent.ACTION_BOOT_COMPLETED) {
      // 開機完成後執行
    }
  }
}
```

### ContentProvider

管理應用程式資料的共享存取：

```kotlin
class MyProvider : ContentProvider() {
  override fun query(uri: Uri, proj: Array<String>?, sel: String?,
    args: Array<String>?, sort: String?): Cursor? { /* ... */ }
}
```

---

## 總結

Android 平台的四層架構設計，從 Linux 核心的穩定基礎到應用框架的豐富 API，為開發者提供了強大有彈性的開發環境。理解各層的職責和互動方式，有助於寫出高效能、穩定的應用程式。

---

## 延伸閱讀

- [Android 平台架構官方文件](https://www.google.com/search?q=Android+platform+architecture)
- [Android 應用程式元件](https://www.google.com/search?q=Android+app+components)
- [Android Runtime (ART) 介紹](https://www.google.com/search?q=Android+Runtime+ART)
