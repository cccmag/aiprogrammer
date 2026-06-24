# 本月新知

## 2024 年 5 月程式與 AI 技術動態

### 程式語言與框架

**React Native 0.75 發布新架構**

React Native 團隊於本月推出 0.75 版本，正式將新架構（New Architecture）設為預設值。新架構基於 JSI（JavaScript Interface）而非舊版的 Bridge，大幅提升了 JavaScript 與原生端的通訊效率。Fabric Renderer 和 TurboModules 的整合使畫面渲染效能提升約 40%，特別是在列表滾動和動畫場景中有感升級。

**Expo SDK 52 支援新架構**

Expo 團隊釋出 SDK 52 版本，全面擁抱 React Native 新架構。Expo 現在可以自動偵測並啟用新架構，讓開發者無需手動配置。同時 Expo 更新了 EAS Build 的雲端編譯服務，支援 Apple Silicon Native 建置，二進制檔案體積減少 25%。

**TypeScript 5.5 發布**

微軟發布 TypeScript 5.5 穩定版，主要亮點包括推論型別謂詞（Inferred Type Predicates）、控制流程縮減的陣列過濾增強，以及對 JSDoc `@import` 標籤的支援。這些功能讓開發者在撰寫 React Native 應用時享有更精準的型別檢查體驗。

**Kotlin 2.0 正式登場**

JetBrains 發布 Kotlin 2.0 穩定版，引入基於 FIR 的新編譯器前端，編譯速度提升約 2 倍。Kotlin Multiplatform（KMP）正式達到穩定狀態，意味著 Android 和 iOS 的商業邏輯可以用 Kotlin 共享。這對 React Native 開發者來說是重要的生態系新聞。

### AI 與行動開發

**Apple 發表 Core ML 6**

Apple 在 WWDC 前夕發表 Core ML 6 預覽版，支援更高效能的邊緣 AI 推論。新 SDK 允許在 iPhone 上執行 7B 參數等級的 LLM，為行動端 AI 應用開創全新可能。React Native 開發者可透過原生模組呼叫 Core ML 6 API。

**Google ML Kit 推出即時翻譯 API**

Google 更新 ML Kit 行動 SDK，加入即時語音翻譯功能，支援 50 種語言之間的互譯，全部在裝置端執行。ML Kit 已經提供 React Native 的官方套件，開發者可以幾行程式碼就整合 AI 能力。

**Flutter 3.22 發布**

Flutter 團隊發布 3.22 版本，包含 Impeller 渲染引擎的穩定化和 Dart 3.4 的更新。雖然 Flutter 是 React Native 的競爭對手，但其在遊戲化 UI 和高效能動畫方面的進展，也促使 React Native 社群加速提升自己的動畫能力。

### 開發工具與雲端服務

**Firebase 推出 App Hosting**

Google Firebase 推出 Firebase App Hosting 服務，專為行動和 Web 應用設計的託管平台。支援自動部署、A/B 測試和漸進式推出，與 React Native 的 EAS Build 形成競爭。

**CodePush 被 Microsoft 收購**

Microsoft 收購了 CodePush 背後的團隊，計畫將其整合進 Visual Studio App Center。CodePush 是 React Native 最受歡迎的 OTA（Over-The-Air）更新方案，這項收購意味著微軟在行動開發領域的持續投資。

### 業界動態

- **Meta 開源 react-native-skia**：高效能 2D 繪圖引擎，整合 Skia 圖形庫
- **Shopify 發表 React Native 效能指南**：詳細的最佳化實戰手冊
- **Spotify 將主 App 部分遷移到 React Native**：進一步驗證了 RN 在大型應用的可行性
- **Reanimated 4.0 釋出 alpha**：全新的動畫引擎，基於 JSI 實現真正的 UI 執行緒動畫

### 標準與規範

- **ECMAScript 2024 定案**：正式納入 Grouped Accessors 與 Promise.withResolvers
- **W3C 發布 WebGPU 1.0 草案**：為 Web 高效能圖形運算鋪路
- **Android 15 開發者預覽**：支援 SDS（Satellite Data Service）與更好的摺疊螢幕適配
