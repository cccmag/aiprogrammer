# Focus 3：行動開發趨勢

## iOS 平台更新

### 側載開放：歷史性變革

2024 年最重大的 iOS 變革是因應歐盟 DMA 法規開放的側載功能。開發者現在可以透過替代應用商店發布 iOS 應用，無需經過 App Store。

### Apple Intelligence

WWDC 2024 發表的 Apple Intelligence 將 AI 直接整合進系統層級。對開發者而言，這意味著：

- **Xcode AI 整合**：程式碼補全、Swift 文件生成
- **On-Device ML**：Core ML 模型最佳化
- **Swift 6**：資料競爭安全檢查編譯層級啟用

## Android 15 亮點

Android 15 專注於隱私保護與 AI 整合。

```javascript
// Android 15 Privacy Sandbox 範例
// 使用 Measurement API 進行廣告歸因
const measurementSource = {
  eventReportWindow: '2024-12-01',
  aggregationKeys: {
    campaignCount: 0x1
  }
};
console.log('Privacy-preserving attribution configured');
```

## Flutter 3.24

Flutter 在 2024 年持續改善 Web 與 Desktop 的穩定度。Dart 3.5 帶來了更強大的巨集支援。

## 跨平台策略

| 方案 | 2024 狀態 | 適合場景 |
|------|-----------|---------|
| Flutter | 3.24，Web/Desktop 穩定 | 跨平台單一程式碼庫 |
| React Native | 0.76，新架構預設 | 需要共用 Web 邏輯 |
| Kotlin Multiplatform | 穩定版釋出 | Android + iOS 共享邏輯 |
| .NET MAUI | 持續改善 | .NET 生態整合 |

2024 年行動開發的關鍵字是「選擇多元化」——不再有單一最佳方案，而是根據專案需求選擇最適合的工具。

> 參考：https://www.google.com/search?q=mobile+development+trends+2024
