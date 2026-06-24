# 跨平台行動開發 — Flutter

## 為什麼是 Flutter？

行動應用開發在過去十年經歷了巨大變化。從早期的 iOS 與 Android 各自為政，到 React Native 與 Xamarin 的跨平台嘗試，再到如今 Flutter 成為主流選擇，開發者始終在尋找「撰寫一次、隨處運行」的理想方案。

Flutter 是由 Google 開發的開源 UI 框架，使用 Dart 語言，能夠從單一程式碼庫建置高效能的行動、網頁與桌面應用程式。其核心特色包括：

1. **自繪引擎** — Flutter 不依賴平台原生 UI 元件，而是透過 Skia/Impeller 自行繪製每一個像素，確保跨平台一致性。

2. **Widget 哲學** — Flutter 中「萬物皆 Widget」。從結構（Column、Row）到樣式（Padding、Center），從互動（Button、TextField）到佈局（Stack、Flexible），全部以 Widget 組合而成。

3. **高效開發** — Hot Reload 讓開發者在秒級內看到程式碼修改結果，大幅提升迭代速度。

4. **Dart 語言** — 結合 JIT 與 AOT 編譯，開發期享受即時重載，發布時獲得原生級效能。

## 本期內容

本期雜誌將從跨平台開發的整體比較出發，深入 Dart 語言特性、Widget 體系、狀態管理、路由導航、原生通道通訊、以及效能優化與發布等面向。

教學文章則聚焦實際操作，從 SDK 安裝開始，逐步帶領讀者完成 Dart 語法練習、Widget 實作、網路請求、本地資料庫操作，最終建置 APK 與 IPA 發佈檔。

所有範例程式碼收錄於 `_code/flutter_demo.js`，使用 Node.js 模擬 Flutter 的核心機制，讓尚未安裝 Flutter 環境的讀者也能理解其設計理念。

## 關鍵字

Flutter、Dart、跨平台行動開發、Widget、狀態管理、Provider、Riverpod、Navigation、MethodChannel
