# 本期焦點

## 手機 App 開發導論 — React Native

### 引言

在行動網路時代，手機 App 已經成為人們日常生活不可或缺的一部分。從社群媒體、電子商務到生產力工具，App 的開發效率和品質直接決定了產品的成敗。然而，傳統的行動開發面臨一個根本問題：Android 和 iOS 使用完全不同的技術棧——Java/Kotlin 對比 Swift/Objective-C——這意味著開發團隊需要維護兩套程式碼。

React Native 由 Meta（原 Facebook）於 2015 年開源，提供了一個革命性的解決方案：用 JavaScript/JSX 編寫，同時渲染真正的原生 UI 元件。其核心口號是「Learn once, write anywhere」——學習一次 React 的思維模式，就能夠為任何平台開發應用。

本期雜誌將從零開始，帶領讀者完整了解 React Native 的技術生態系。

---

## 大綱

* [程式：React Native 模擬器](focus_code.md)
   - 元件渲染模擬
   - 導航狀態管理
   - API 請求模擬
* [程式：React Native 模擬器](focus_code.md)

1. [手機 App 開發概論](focus1.md)
   - 行動開發的歷史演進
   - 跨平台方案的比較
   - React Native 的設計哲學

2. [React Native 環境與專案結構](focus2.md)
   - 開發環境建置步驟
   - 專案目錄結構解析
   - Metro Bundler 與打包流程

3. [核心元件：View、Text、ScrollView](focus3.md)
   - View 容器與排版
   - Text 文字渲染
   - ScrollView 滾動容器

4. [導航與頁面切換](focus4.md)
   - React Navigation 入門
   - Stack、Tab、Drawer 導航
   - 參數傳遞與路由管理

5. [狀態管理與資料流](focus5.md)
   - React 狀態管理的演進
   - Context API 與 useReducer
   - Redux Toolkit 與中介軟體

6. [原生模組與 API 串接](focus6.md)
   - 原生模組的運作原理
   - 攝影機與地理位置 API
   - TurboModules 新架構

7. [發布與上架流程](focus7.md)
   - App 簽名與證書管理
   - Google Play 上架流程
   - App Store Connect 審查

8. [結論與展望](focus.md#結論與展望)

---

## 濃縮回顧

### 行動開發的三大時代

**時代一：原生開發（2008-2014）**
iPhone 和 Android 問世後，開發者必須使用平台專屬語言和工具。Objective-C 與 Java 各據山頭，兩套程式碼意味著雙倍的工作量。

**時代二：跨平台框架崛起（2015-2020）**
PhoneGap/Cordova 使用 WebView，但效能不佳。React Native 和 Flutter 相繼出現，提供真正的原生渲染體驗。

**時代三：統一開發體驗（2021-至今）**
React Native 新架構、Expo 管理工具、CodePush OTA 更新，讓開發體驗接近 Web 開發的便利性。

### 為什麼選擇 React Native？

```jsx
// 同一份程式碼，雙平台執行
const App = () => (
  <View style={styles.container}>
    <Text style={styles.text}>Hello, React Native!</Text>
  </View>
);
```

React Native 的核心優勢：
- **程式碼重用**：跨平台共享 90% 以上的程式碼
- **熱更新**：Metro Bundler 支援即時重新載入
- **生態豐富**：npm 上數千個專用套件
- **開發效率**：React 開發者無縫轉換

---

## 結論與展望

React Native 已經從 2015 年的實驗性專案，成長為行動開發的重要選項。新架構（Fabric + TurboModules）的成熟，讓其效能與原生開發的差距進一步縮小。

未來，隨著 AI 在行動端的普及（Core ML、ML Kit）和邊緣運算的發展，React Native 作為跨平台框架的價值將更加凸顯——一次學習，隨處開發，跨平台部署。

---

## 延伸閱讀

- [手機 App 開發概論](focus1.md)
- [React Native 環境與專案結構](focus2.md)
- [核心元件](focus3.md)
- [導航與頁面切換](focus4.md)
- [狀態管理與資料流](focus5.md)
- [原生模組與 API 串接](focus6.md)
- [發布與上架流程](focus7.md)

---

*本期焦點到此結束。下期我們將聚焦另一個影響深遠的主題，敬請期待。*
