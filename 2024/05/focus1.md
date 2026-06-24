# 手機 App 開發概論

## 行動開發的歷史演進

### 原生時代（2008-2014）

2008 年，Apple 發布 iPhone 3G 和 App Store，同年 Google 推出 Android Market（現 Google Play）。從那一刻起，手機 App 開發成為一個全新的產業。

原生開發要求開發者使用平台專屬的語言和工具。iOS 使用 Objective-C（後來是 Swift）和 Xcode；Android 使用 Java（後來是 Kotlin）和 Android Studio。兩套完全不同的技術棧意味著：

```
iOS 技術棧       Android 技術棧
────────────     ────────────
Swift/Obj-C      Kotlin/Java
UIKit             Android SDK
Xcode             Android Studio
CocoaPods         Gradle
```

### Web 技術混合時代（2010-2016）

PhoneGap（後來的 Apache Cordova）首先嘗試用 Web 技術開發 App。開發者用 HTML/CSS/JavaScript 編寫，然後透過 WebView 渲染。這個方案雖然實現了跨平台，但存在嚴重的效能問題：

```javascript
// Cordova 範例：透過 JS Bridge 呼叫原生功能
document.addEventListener("deviceready", () => {
    navigator.camera.getPicture(
        (imageData) => console.log("Photo taken"),
        (err) => console.error(err)
    );
});
```

WebView 渲染缺乏原生應有的流暢感，特別是在列表滾動和動畫場景中，使用者體驗明顯打折。

### 跨平台框架崛起（2015-2020）

2015 年，Facebook 開源 React Native，Google 在 2017 年發布 Flutter。它們的核心區別在於：

```javascript
// React Native：JavaScript -> 原生 UI 元件
<View style={styles.container}>
  <Text>這是原生的 UILabel / android.widget.TextView</Text>
</View>
```

React Native 將 JavaScript 元件映射為真正的原生 UI 元件，解決了 WebView 的效能問題。

### React Native 的設計哲學

#### Learn Once, Write Anywhere

React Native 的核心設計理念是「學習一次，隨處編寫」。這與「一次編寫，到處運行」有本質區別：

- **一次編寫，到處運行**（Write Once, Run Anywhere）：Java 的哲學，但通常意味著最低共同標準
- **學習一次，隨處編寫**（Learn Once, Write Anywhere）：React Native 的哲學，學習 React 思維後，為每個平台編寫最佳體驗

```jsx
// iOS 和 Android 上的按鈕表現不同
// 但開發者使用同一套 API
const MyButton = () => (
    <TouchableOpacity onPress={handlePress}>
        <Text>點我</Text>
    </TouchableOpacity>
);
```

#### 宣告式 UI

React Native 繼承了 React 的宣告式 UI 哲學。開發者描述「UI 應該長什麼樣子」，而不是「如何建立 UI」：

```jsx
// 宣告式：描述 UI 的狀態驅動結果
const Greeting = ({ name }) => (
    <Text>Hello, {name}!</Text>
);
```

### 選擇 React Native 的考量

**適合場景：**
- 社交媒體 App（Facebook、Instagram 使用 RN）
- 電子商務 App（Shopify、Walmart 使用 RN）
- 商業工具 App
- 原型與 MVP 開發

**不適合場景：**
- 高效能遊戲（需要 Unity/Unreal）
- 複雜的 3D 渲染應用
- 系統層級應用（啟動器、設定）

### 生態系統總覽

React Native 生態包含：
- **核心函式庫**：react-native
- **開發工具**：Expo CLI、React Native CLI
- **導航**：React Navigation
- **狀態管理**：Redux Toolkit、Zustand、Jotai
- **UI 元件庫**：NativeBase、React Native Elements
- **動畫**：React Native Reanimated、Animatable

---

## 延伸閱讀

- [React Native 官方文件](https://www.google.com/search?q=React+Native+official+documentation)
- [跨平台開發比較](https://www.google.com/search?q=cross+platform+app+development+comparison)
- [React 設計哲學](https://www.google.com/search?q=React+design+philosophy)

---

*本篇文章為「AI 程式人雜誌 2024 年 5 月號」焦點系列之一。*
