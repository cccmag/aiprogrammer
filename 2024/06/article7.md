# TabView 與多頁面

## 分頁導航的應用場景

TabView 是 iOS 應用中最常見的導航模式之一。它將應用程式的主要功能分類為數個分頁，使用者可以透過底部的 Tab Bar 快速切換。社群媒體（首頁、搜尋、發布、通知、個人檔案）、工具類應用（功能 A、功能 B、設定）等都廣泛使用 TabView。

## 基本用法

```swift
struct ContentView: View {
    var body: some View {
        TabView {
            HomeView()
                .tabItem {
                    Label("Home", systemImage: "house")
                }
            
            SearchView()
                .tabItem {
                    Label("Search", systemImage: "magnifyingglass")
                }
            
            ProfileView()
                .tabItem {
                    Label("Profile", systemImage: "person")
                }
        }
    }
}
```

## 分頁與導航的組合

最常見的架構是每個 Tab 包含一個獨立的 NavigationStack：

```swift
TabView {
    NavigationStack {
        HomeView()
    }
    .tabItem { Label("Home", systemImage: "house") }
    
    NavigationStack {
        SettingsView()
    }
    .tabItem { Label("Settings", systemImage: "gear") }
}
```

## 選中分頁的控制

使用 `@State` 控制和監聽當前選中的分頁：

```swift
@State private var selectedTab = 0

TabView(selection: $selectedTab) {
    HomeView()
        .tabItem { Label("Home", systemImage: "house") }
        .tag(0)
    
    ProfileView()
        .tabItem { Label("Profile", systemImage: "person") }
        .tag(1)
}
.onChange(of: selectedTab) { oldTab, newTab in
    print("Switched from \(oldTab) to \(newTab)")
}
```

## Badge 與通知

在 Tab Item 上顯示標記數字：

```swift
MessagesView()
    .tabItem {
        Label("Messages", systemImage: "message")
    }
    .badge(unreadCount)
```

當 `unreadCount` 為 0 時，Badge 自動隱藏。

## 自訂 Tab Bar

雖然 SwiftUI 的 TabView 功能完整，但有時你需要自訂 Tab Bar 的外觀：

```swift
UITabBar.appearance().backgroundColor = UIColor.systemBackground
UITabBar.appearance().unselectedItemTintColor = UIColor.secondaryLabel
```

或者完全自訂 Tab Bar：

```swift
struct CustomTabView: View {
    @State private var selected = 0
    
    var body: some View {
        VStack(spacing: 0) {
            TabContent(selected: $selected)
            
            HStack {
                TabButton(icon: "house", label: "Home", tag: 0, selected: $selected)
                TabButton(icon: "heart", label: "Favorites", tag: 1, selected: $selected)
                TabButton(icon: "gear", label: "Settings", tag: 2, selected: $selected)
            }
            .padding()
            .background(.ultraThinMaterial)
        }
    }
}
```

## 多頁面頁籤（Page TabView）

TabView 也可以用作內容頁面的滑動切換：

```swift
TabView {
    OnboardingView1()
    OnboardingView2()
    OnboardingView3()
}
.tabViewStyle(.page)
.indexViewStyle(.page(backgroundDisplayMode: .always))
```

這種樣式常用於引導頁或輪播圖。

## 隱藏 Tab Bar

在某些頁面需要隱藏 Tab Bar：

```swift
// 在全螢幕檢視中隱藏 Tab Bar
DetailView()
    .toolbar(.hidden, for: .tabBar)
```

## 最佳實踐

1. 分頁數量控制在 3-5 個
2. 使用系統提供的 SF Symbols 作為圖標
3. 每個分頁的導航應獨立管理
4. 避免在 Tab Bar 中使用過多的視覺效果

## 延伸閱讀

- [TabView 文檔](https://www.google.com/search?q=SwiftUI+TabView+documentation)
- [SF Symbols 參考](https://www.google.com/search?q=SF+Symbols+Apple)
- [TabView 設計指南](https://www.google.com/search?q=iOS+tab+bar+design+guidelines)

---

*本篇文章為「AI 程式人雜誌 2024 年 6 月號」文章集錦之七。*
