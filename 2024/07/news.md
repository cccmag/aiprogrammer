# 本月新知

## 2024 年 7 月 Android 技術動態

### Android 15 Beta 4 發布

Google 於 7 月發布 Android 15 Beta 4，這是正式版前的最後一個測試版本。新特性包括：

- **隱私沙盒（Privacy Sandbox）**：進一步限制廣告追蹤
- **衛星通訊 API**：支援 MOTS（Mobile Originated Termination Solicited）
- **應用程式封存（App Archiving）**：保留資料的卸載機制
- **更強大的多工處理**：分割畫面支援視窗固定
- **Health Connect 增強**：新的健身和健康資料類型

正式版預計在 8 月推送給 Pixel 裝置。

### Kotlin 2.0 正式發布

JetBrains 於 2024 年 5 月發布 Kotlin 2.0，7 月迎來首個重大更新（2.0.10），主要改進包括：

- **K2 編譯器穩定**：編譯速度快 2 倍以上
- **Power Assert**：測試失敗時顯示詳細的表達式值
- **Explicit backing fields**：屬性後端欄位更明確的控制
- **多平台最佳化**：Wasm 目標平台支援持續改善

Kotlin 2.0 相容 Kotlin 1.9 的程式碼，升級風險低。

### Jetpack Compose 1.6 與 Compose Compiler 1.5

Compose 最新版本帶來了多項改善：

- **Shared Element Transitions**：跨頁面動畫轉場
- **Compose Compiler 1.5**：與 Kotlin 2.0 K2 編譯器完整整合
- **Lazy Layout 效能最佳化**：Item 回收機制改善
- **基本手勢增強**：`detectTransformGestures` 支援多指操作
- **Text 元件改進**：行高與文字溢出處理

### Gemini Nano 端側 AI 支援

Android 15 將內建 Gemini Nano，這是 Google 的裝置端 AI 模型：

- **Smart Reply**：通知欄的智慧回覆
- **On-Device Summarization**：網頁和文件摘要
- **Photo Picker 智慧選擇**：AI 輔助照片選擇
- **開發者 API**：透過 `OnDeviceInferenceManager` 呼叫

開發者可以在 Android 15 上體驗端側 AI 的潛力。

### Material 3 Adaptive Layout

Google 推出了自適應佈局指南，幫助開發者適配不同螢幕尺寸：

- **Canonical Layouts**：列表-詳細、支撐-詳細等模式
- **Navigation Suit**：導航抽屜、底部導航、導航欄自動切換
- **Window Size Classes**：Compact / Medium / Expanded 三種尺寸

這些模式使得 Android 應用可以無縫適配手機、平板和折疊裝置。

### 其他重要動態

- **Firebase 65% 折扣**：Google 調整 Firebase 定價
- **Flutter 3.22 發布**：Impeller 渲染引擎在 Android 上穩定
- **Gradle 8.7**：建構速度提升 15%
- **Android Studio Koala**：新的 IDE 版本，整合 Gemini 助手
- **ProGuard Rules 自動化**：R8 全模式成為預設

### SDK 與工具更新

- **Room 2.6**：支援 Kotlin 2.0 與 KSP
- **Retrofit 2.11**：OkHttp 4.12 整合
- **Coil 3.0**：純 Kotlin 協程的圖片載入庫
- **Hilt 1.2**：Dagger 依賴注入的 Android 最佳化版本

### 研討會與活動

- **Google I/O 2024**（5 月）：宣布了上述多項更新
- **Android Developer Summit**（9 月）：將討論 Android 16 初步規劃
- **KotlinConf 2024**（5 月）：JetBrains 展示 Kotlin 未來路線圖

### 業界趨勢

2024 年 Android 開發生態系的主要趨勢包括：

1. **AI 整合**：端側 AI 從 Gemini Nano 開始普及
2. **大螢幕適配**：折疊裝置和平板的開發優先級提升
3. **Kotlin Multiplatform**：跨平台開發方案日益成熟
4. **Jetpack Compose 主流化**：新專案多數直接使用 Compose
5. **效能與安全**：隱私沙盒和 R8 最佳化持續加強
