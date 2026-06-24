# 焦點 1：跨平台開發比較

## 跨平台開發的演進

行動開發領域長期存在「一次開發，多平台部署」的追求。從早期的 PhoneGap / Cordova（WebView 包裝），到 React Native（JavaScript 橋接原生），再到 Flutter（自繪引擎），技術路線不斷進化。

## 主流方案對比

### 原生開發 (Swift / Kotlin)

- 優點：完全存取平台 API、最佳效能、最新平台特性
- 缺點：雙倍開發成本、程式碼無法共享
- 適用：高度依賴平台特性的應用

### React Native

- 優點：JavaScript 生態系豐富、Hot Reload、大量社群套件
- 缺點：JavaScript Bridge 效能瓶頸、除錯困難
- 架構：Virtual DOM → Native Widget 橋接
- 適用：需要快速迭代的 MVP 產品

### Flutter

- 優點：高效能（Impeller 引擎）、一致的 UI、Hot Reload、單一程式碼庫
- 缺點：App 體積較大、平台特定功能需插件
- 架構：Widget → Skia/Impeller → 像素渲染
- 適用：重視 UI 一致性與效能的產品

### Kotlin Multiplatform (KMP)

- 優點：共享業務邏輯、保留原生 UI、型別安全
- 缺點：UI 層仍需各平台實作、較新的生態系
- 適用：已有原生團隊、希望共享邏輯的專案

## 選擇建議

選擇框架時應考慮：團隊技術棧、專案時間線、效能需求、平台特定功能比例。

若團隊已熟悉 JavaScript 且需要快速原型，React Native 是合理選擇。若追求 UI 一致性與高效能，Flutter 更具優勢。若已有原生開發團隊且希望逐步共享邏輯，KMP 值得考慮。

## 未來趨勢

2024 年跨平台開發呈現融合趨勢：Flutter 支援更多平台（Web、Desktop），KMP 強化 UI 共享能力，React Native 新架構縮小效能差距。開發者應根據專案現實需求做出選擇，而非盲目跟隨潮流。

- https://www.google.com/search?q=Flutter+vs+React+Native+vs+Kotlin+Multiplatform+2024
- https://www.google.com/search?q=cross-platform+mobile+development+comparison+2024
