# React Native 環境與專案結構

## 開發環境建置步驟

### 前置需求

開始 React Native 開發前，需要在電腦上安裝以下工具：

```
必要工具：
├── Node.js （>= 18 LTS）
├── Watchman （Facebook 檔案監控）
├── Xcode （macOS，iOS 開發）
├── Android Studio （Android 開發）
└── Java Development Kit （JDK 17）
```

### 兩種開發工作流程

React Native 提供兩種開發方式：

**React Native CLI（裸專案）：**
```bash
npx react-native init MyApp --template react-native-template-typescript
cd MyApp
npx react-native run-ios
```

**Expo CLI（管理專案）：**
```bash
npx create-expo-app MyApp --template blank-typescript
cd MyApp
npx expo start
```

### 專案目錄結構解析

無論使用哪種 CLI，產生的專案結構類似：

```
MyApp/
├── android/        # Android 原生專案（Gradle）
├── ios/            # iOS 原生專案（Xcode）
├── node_modules/   # npm 套件
├── src/            # 原始碼（開發者主要工作目錄）
│   ├── components/ # 可複用元件
│   ├── screens/    # 頁面元件
│   ├── navigation/ # 導航設定
│   ├── store/      # 狀態管理
│   ├── services/   # API 服務
│   └── utils/      # 工具函式
├── App.tsx         # 應用程式入口
├── package.json    # 套件依賴
├── tsconfig.json   # TypeScript 設定
├── metro.config.js # Metro Bundler 設定
└── babel.config.js # Babel 設定
```

### Metro Bundler 打包流程

React Native 使用 Metro Bundler 作為 JavaScript 打包工具：

```
源碼 ──→ Babel 轉換 ──→ 模組解析 ──→ 打包（Bundle） ──→ 載入裝置
```

```javascript
// metro.config.js 基本配置
const { getDefaultConfig } = require("@react-native/metro-config");

module.exports = (() => {
    const config = getDefaultConfig(__dirname);
    const { transformer, resolver } = config;
    config.transformer = {
        ...transformer,
        babelTransformerPath: require.resolve("react-native-svg-transformer"),
    };
    config.resolver = {
        ...resolver,
        assetExts: resolver.assetExts.filter((ext) => ext !== "svg"),
        sourceExts: [...resolver.sourceExts, "svg"],
    };
    return config;
})();
```

### App.tsx 入口檔案解析

```jsx
import React from "react";
import { SafeAreaView, StatusBar, StyleSheet } from "react-native";
import { NavigationContainer } from "@react-navigation/native";
import RootNavigator from "./src/navigation/RootNavigator";

const App = () => {
    return (
        <SafeAreaView style={styles.container}>
            <StatusBar barStyle="dark-content" />
            <NavigationContainer>
                <RootNavigator />
            </NavigationContainer>
        </SafeAreaView>
    );
};

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: "#fff",
    },
});

export default App;
```

### 開發流程循環

React Native 的開發循環極具效率：

1. **編寫程式碼**：在編輯器中修改 JS/TS 檔案
2. **自動重新載入**：Metro Bundler 偵測變更，透過 HMR 更新
3. **即時預覽**：在模擬器或實體裝置上看到結果
4. **Debug**：使用 Chrome DevTools 或 Flipper

### 疑難排解

常見問題與解決方案：

```bash
# 清除 Metro 快取
npx react-native start --reset-cache

# 清除 npm 快取
npm cache clean --force

# 重新安裝原生依賴（iOS）
cd ios && pod install && cd ..

# 重新安裝原生依賴（Android）
cd android && ./gradlew clean && cd ..
```

---

## 延伸閱讀

- [React Native 環境設定指南](https://www.google.com/search?q=React+Native+environment+setup)
- [Metro Bundler 文件](https://www.google.com/search?q=Metro+Bundler+documentation)
- [Expo 開發工具](https://www.google.com/search?q=Expo+CLI+development+tools)

---

*本篇文章為「AI 程式人雜誌 2024 年 5 月號」焦點系列之二。*
