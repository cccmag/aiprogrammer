# App Store 上架流程

## 從開發到發布

開發完成一個 iOS 應用程式只是第一步。要讓使用者可以下載你的應用，你需要通過 Apple 的審查並將應用發布到 App Store。這個過程涉及多個步驟，從開發者帳號申請到最終的審查提交。

## 開發者帳號申請

### 個人與組織帳號

加入 Apple Developer Program 需要準備：

1. Apple ID（建議使用專屬開發用 ID）
2. 信用卡或簽帳金融卡（年費 99 美元）
3. 個人或組織資訊

組織帳號需要額外的 D-U-N-S 編號來驗證公司身份。台灣的企業可以透過經濟部工商登記資料取得 D-U-N-S 編號。

### 帳號啟用流程

申請後需要等待 Apple 的審核，通常 24-48 小時內完成。帳號啟用後，你可以在 App Store Connect 中管理應用程式。

## 應用程式簽名

### 簽名機制

iOS 應用程式必須經過數位簽署才能在真機上執行。簽名機制確保：

- 應用程式的來源可信
- 應用程式未被篡改
- 開發者身份已被驗證

### Xcode 自動簽名

Xcode 提供自動簽名管理功能，開發者只需選擇 Team 和 Bundle Identifier：

```swift
// Xcode 專案設定
// Signing & Capabilities 分頁
// Team: 你的開發者團隊
// Bundle Identifier: com.example.myapp
```

簽名所需的憑證和描述檔都會由 Xcode 自動管理。

## App Store Connect

### 應用程式建立

在 Xcode 中歸檔（Archive）應用程式後，上傳到 App Store Connect：

1. 選擇 Product → Archive
2. 在 Organizer 中選擇上傳
3. 填寫應用程式資訊（名稱、描述、關鍵字等）
4. 上傳截圖和預覽影片

### 應用程式資訊

```swift
// 必要的應用程式資訊
- 名稱（30 字元內）
- 副標題（30 字元內）
- 描述（4000 字元內）
- 關鍵字（100 字元內）
- 支援的語言
- 年齡分級
- 價格與銷售範圍
```

## 應用審查

### 審查流程

Apple 的審查團隊會檢查應用的功能、內容和穩定性：

1. 功能性檢查：應用能否正常啟動和操作
2. 內容審查：是否違反 App Store 規範
3. 效能評估：載入速度和記憶體使用
4. 隱私檢查：資料收集和權限使用

### 常見拒絕原因

- 應用 Crash 或 Bug
- 使用者介面不符合 HIG
- 隱私描述不完整
- 使用私有 API
- 應用內容重複

### 加快審查

- 提供測試帳號和示範資料
- 明確說明應用的功能和用途
- 確保所有連結都可正常訪問
- 避免在審查期間上傳更新版本

## TestFlight

### Beta 測試

在正式發布前，使用 TestFlight 進行 Beta 測試：

- 內部測試：最多 100 名團隊成員
- 外部測試：最多 10,000 名測試者（需經過 Beta 審查）

TestFlight 讓開發者可以在正式發布前收集回饋、發現問題。

## 版本更新與維護

### 應用程式更新

發布後仍需持續維護：

- 修復 Bug 和安全性問題
- 支援新的 iOS 版本
- 根據使用者回饋改進功能
- 更新應用程式描述和截圖

### 審查加速

對於緊急修復，Apple 提供加速審查申請，通常在 24 小時內完成。

## 延伸閱讀

- [App Store Review Guidelines](https://www.google.com/search?q=App+Store+Review+Guidelines)
- [App Store Connect 使用指南](https://www.google.com/search?q=App+Store+Connect+guide)
- [TestFlight 幫助](https://www.google.com/search?q=TestFlight+beta+testing)
- [iOS 簽名與發布](https://www.google.com/search?q=iOS+code+signing+distribution)

---

*本篇文章為「AI 程式人雜誌 2024 年 6 月號」iOS 開發入門系列之七。*
