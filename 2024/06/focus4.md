# 導航與頁面架構

## iOS 導航的核心概念

在使用者介面設計中，導航決定使用者如何在應用程式的不同頁面之間移動。iOS 提供了幾種主要的導航模式，每種模式適用於不同的場景。選擇正確的導航結構對使用者體驗至關重要。

## NavigationStack

NavigationStack 是 SwiftUI 中主要的層級導航容器。它以堆疊的方式管理頁面——新頁面推入堆疊頂部，返回時從頂部彈出：

```swift
struct ContentView: View {
    var body: some View {
        NavigationStack {
            List(items) { item in
                NavigationLink(item.name, value: item)
            }
            .navigationTitle("Items")
            .navigationDestination(for: Item.self) { item in
                DetailView(item: item)
            }
        }
    }
}
```

### NavigationLink

NavigationLink 是觸發導航的按鈕。使用者點擊它時，目標檢視會被推入導航堆疊。導航欄會自動顯示返回按鈕。

### navigationDestination

`safeNavigationDestination` 修飾器將資料型別與目標檢視關聯。這種型別安全的導航機制避免了傳統 Segue 的字串識別符問題。

### 程式化導航

有時需要透過程式碼控制導航，例如表單提交後自動跳轉：

```swift
@State private var showDetail = false

Button("Go to Detail") {
    showDetail = true
}
.navigationDestination(isPresented: $showDetail) {
    DetailView()
}
```

## TabView

TabView 實現分頁導航，適合用於應用程式的主要功能分類：

```swift
TabView {
    HomeView()
        .tabItem {
            Label("Home", systemImage: "house")
        }
    SearchView()
        .tabItem {
            Label("Search", systemImage: "magnifyingglass")
        }
    SettingsView()
        .tabItem {
            Label("Settings", systemImage: "gear")
        }
}
```

每個 Tab 可以包含自己的 NavigationStack，形成巢狀導航結構。

### Badge 與客製化

TabView 支援在圖標上顯示標記數字：

```swift
.tabItem { Label("Messages", systemImage: "message") }
.badge(unreadCount)
```

## Modal 與 Sheet

Sheet 是一種模態呈現方式，通常用於表單或臨時性任務：

```swift
@State private var showSheet = false

Button("Show Sheet") {
    showSheet = true
}
.sheet(isPresented: $showSheet) {
    FormView()
}
```

### 全螢幕覆蓋

對於需要完整畫面的場景，使用 `.fullScreenCover`：

```swift
.fullScreenCover(isPresented: $showFullScreen) {
    CameraView()
}
```

## 導航架構模式

### 簡潔型

單一 NavigationStack 配合 List，適合工具類應用。

### 分頁型

TabView + NavigationStack 組合，每頁獨立導航，適合社群或內容類應用。

### 側邊欄型

NavigationSplitView 提供三欄佈局，適合 iPad 和 Mac 的多工場景：

```swift
NavigationSplitView {
    List // 側邊欄
} content: {
    List // 內容欄
} detail: {
    DetailView() // 詳細欄
}
```

## 導航最佳實踐

1. 避免導航層級過深（建議不超過 5 層）
2. TabView 的數量保持在 3-5 個
3. 使用 Sheet 而非推入式導航來處理表單
4. 在 iPad 上考慮使用 NavigationSplitView

## 延伸閱讀

- [NavigationStack 文檔](https://www.google.com/search?q=SwiftUI+NavigationStack+documentation)
- [TabView 使用指南](https://www.google.com/search?q=SwiftUI+TabView+guide)
- [iOS 導航設計規範](https://www.google.com/search?q=iOS+navigation+design+guidelines)

---

*本篇文章為「AI 程式人雜誌 2024 年 6 月號」iOS 開發入門系列之四。*
