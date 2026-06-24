# Expo vs React Native CLI

## 前言

當你決定使用 React Native 開發 App 時，第一個需要做的決定是：使用 Expo 還是 React Native CLI？這兩種工作流程各有優缺，本文將深入比較。

## React Native CLI（裸專案）

React Native CLI 是 Meta 官方維護的命令列工具，提供完整的手機開發體驗。

### 優點

```bash
# 專案初始化
npx @react-native-community/cli init MyApp

# 直接存取所有原生 API
```

- **完全控制**：可以直接修改 android/ 和 ios/ 目錄下的原生程式碼
- **原生模組**：可以集成任何第三方原生 SDK
- **靈活性**：不受 Expo 管理工具的限制

### 缺點

- **環境設定複雜**：需要自行安裝 Xcode、Android Studio、JDK 等工具
- **建置流程手動**：需要自行管理簽名、憑證、建置配置
- **除錯較困難**：沒有 Expo 的整合除錯體驗

## Expo（管理工作流程）

Expo 是一個圍繞 React Native 的管理生態系，提供「設定即完成」的體驗。

### 優點

```bash
# 專案初始化（秒級完成）
npx create-expo-app MyApp

# 啟動開發伺服器
npx expo start
```

- **零配置**：預設包含最佳實踐配置
- **EAS Build**：雲端建置，無需本地 Xcode/Android Studio
- **OTA 更新**：內建 CodePush 類型的更新機制
- **Expo SDK**：統一的 API 封裝，跨平台一致體驗

### Expo SDK 範例

```jsx
import * as ImagePicker from "expo-image-picker";
import { Camera } from "expo-camera";
import * as Location from "expo-location";
import * as Notifications from "expo-notifications";

// Expo 提供的 API 使用方式一致
// 不需要分別處理 iOS 和 Android 的差異
const pickImage = async () => {
    const result = await ImagePicker.launchImageLibraryAsync({
        mediaTypes: ImagePicker.MediaTypeOptions.Images,
        quality: 0.8,
    });
    if (!result.canceled) {
        setImage(result.assets[0].uri);
    }
};
```

### 缺點

- **無法使用部分原生 SDK**：需要自訂原生模組時較困難
- **二進制較大**：Expo 包含較多預設功能的運行時
- **切換到裸專案有成本**：執行 `expo eject` 後無法回到管理工作流程

## 關鍵比較

```
項目                Expo                 React Native CLI
────                ────                 ────────────────
環境設定            開箱即用             需要設定原生環境
原生存取            Expo SDK 提供        完全控制
OTA 更新            內建                 需要 CodePush
建置服務            EAS Build            本機建置
二進制大小          較大（含 SDK）        較小
社群支援            Expo 團隊             Meta + 社群
學習曲線            低                    中
自訂原生模組        受限（需 eject）      完整支援
```

## 如何選擇？

**選擇 Expo 的情況：**
- 新開發者，首次學習 React Native
- 專案不需要複雜的原生功能
- 需要快速迭代和原型開發
- 團隊沒有原生開發人員

**選擇 React Native CLI 的情況：**
- 需要集成特定的原生 SDK
- 對 App 體積有嚴格要求
- 已經有原生的持續集成流程
- 需要完全掌控建置過程

## 第三條路：Expo Dev Client

Expo 提供的 Dev Client 選項可以部分解決兩難。它允許在 Expo 管理工作流程中使用自訂原生模組：

```bash
# 使用 Dev Client
npx create-expo-app MyApp --template blank-typescript
npx expo install expo-dev-client

# 可以在 App 中使用自訂原生模組
# 同時享受 Expo 的開發工具
```

這樣的組合成為許多中型專案的首選方案：開發時使用 Expo 的工具鏈，需要時可以集成自訂原生模組。

## 結語

Expo 和 React Native CLI 不是對立的選擇，而是光譜的兩端。隨著 Expo 生態系的成熟，大部分新專案可以從 Expo 開始，遇到瓶頸時再考慮切換。選擇最適合團隊和專案需求的方案，比追求技術上的「純粹」更重要。

---

## 延伸閱讀

- [Expo 官方文件](https://www.google.com/search?q=Expo+documentation)
- [React Native CLI 指南](https://www.google.com/search?q=React+Native+CLI+guide)
- [Expo vs React Native 比較](https://www.google.com/search?q=Expo+vs+React+Native+CLI+comparison)
