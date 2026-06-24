# Xcode 開發環境

## 認識 Xcode

Xcode 是 Apple 官方的整合開發環境，是所有 iOS、macOS、watchOS 和 tvOS 應用程式的開發起點。Xcode 將編輯器、編譯器、除錯器、模擬器和效能分析工具整合在單一應用程式中，為開發者提供一站式的開發體驗。

## 主要功能區域

### 導航區（Navigator）

Xcode 左側的導航區提供了專案檔案總管、搜尋、原始碼控制、斷點等面板：

- 專案導航（⌘1）：瀏覽和管理專案檔案
- 搜尋導航（⌘3）：在整個專案中搜尋文字
- 原始碼控制導航（⌘5）：查看 Git 變更記錄

### 編輯區（Editor）

Xcode 的編輯器支援多種編輯模式：

- 標準編輯器：撰寫程式碼的主要區域
- 輔助編輯器（⌥⌘↵）：並排顯示相關檔案
- 版本編輯器：檢視程式碼的 Git 差異

### 工具區（Utilities）

右側的工具區包含 Inspector 和 Libraries：

```swift
// Inspector 面板
- File Inspector：檔案屬性和中繼資料
- Quick Help：快速查看 API 文檔
- Attributes Inspector：Storyboard 元件屬性
```

### 除錯區（Debug Area）

底部區域整合了控制台輸出和變數檢查器，用於執行應用程式時的除錯。

## SwiftUI 預覽

Xcode 的 Canvas 提供了 SwiftUI 的即時預覽功能。當你修改程式碼時，預覽會自動更新：

```swift
struct ContentView: View {
    var body: some View {
        VStack {
            Text("Hello, Xcode!")
                .font(.largeTitle)
            Text("SwiftUI Preview is amazing")
                .foregroundColor(.secondary)
        }
    }
}

#Preview {
    ContentView()
}
```

預覽支援不同裝置尺寸、黑暗模式、文字大小等多種變化。

## 程式碼編輯功能

### 自動補全

Xcode 的程式碼自動補全非常強大，不僅補全符號名稱，還會根據上下文推斷最合適的選項。使用 Esc 鍵可以手動觸發補全提示。

### 重構工具

Xcode 支援多種重構操作，包括重新命名、提取方法、轉換為計算屬性等。這些操作會自動更新所有相關引用。

### 即時問題標記

Xcode 在編輯時即時標記語法錯誤、型別錯誤和警告。紅點表示錯誤，黃點表示警告，點擊即可查看具體問題。

## 專案管理

### 專案結構

典型的 iOS 專案結構：

```
MyApp/
├── MyApp.xcodeproj    // 專案設定檔
├── MyApp/              // 原始碼目錄
│   ├── App.swift       // 應用程式入口
│   ├── ContentView.swift
│   ├── Models/         // 資料模型
│   ├── Views/          // 檢視
│   └── ViewModels/     // 檢視模型
├── MyAppTests/         // 單元測試
└── MyAppUITests/       // UI 測試
```

## 鍵盤快捷鍵

常用快捷鍵：

- ⌘B：建置專案
- ⌘R：執行應用程式
- ⌘U：執行測試
- ⌘.：停止執行
- ⌘/：註解/取消註解
- ⌘[ / ⌘]：縮排/反縮排

## 延伸閱讀

- [Xcode 官方文檔](https://www.google.com/search?q=Xcode+user+guide+Apple)
- [Xcode 快捷鍵大全](https://www.google.com/search?q=Xcode+keyboard+shortcuts)
- [Xcode 疑難排解](https://www.google.com/search?q=Xcode+troubleshooting)

---

*本篇文章為「AI 程式人雜誌 2024 年 6 月號」文章集錦之一。*
