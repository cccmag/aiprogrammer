# 狀態綁定 @State

## 響應式程式設計

SwiftUI 的核心是響應式程式設計。當應用程式的狀態改變時，UI 自動更新以反映最新的狀態。開發者不需要手動更新 UI 元件——只需管理狀態，SwiftUI 處理其餘部分。

## @State 屬性包裝器

`@State` 是 SwiftUI 中最基本的屬性包裝器，用於宣告檢視的本地狀態：

```swift
struct CounterView: View {
    @State private var count = 0
    
    var body: some View {
        VStack {
            Text("Count: \(count)")
                .font(.largeTitle)
            
            Button("Increment") {
                count += 1  // 狀態改變，UI 自動更新
            }
        }
    }
}
```

### 工作原理

當 `@State` 屬性的值改變時，SwiftUI 會：

1. 標記該檢視為「需要更新」
2. 重新計算 `body` 屬性
3. 計算新舊 UI 的差異
4. 只更新變化的部分

這個過程是自動且高效的，開發者不需要介入。

## @State 的生命週期

`@State` 的儲存是由 SwiftUI 管理的，而不是檢視本身。這意味著即使檢視被重新建立，狀態仍然保持：

- 檢視第一次出現時，SwiftUI 分配儲存空間
- 檢視被移除後，儲存空間被釋放
- 檢視重新出現時，重新分配新的儲存

```swift
struct TimerView: View {
    @State private var startTime = Date()
    
    var body: some View {
        Text("Started: \(startTime)")
    }
}
```

## @Binding 雙向繫結

`@Binding` 建立了父子檢視之間的雙向繫結。子檢視可以讀寫父檢視的狀態：

```swift
struct ParentView: View {
    @State private var isOn = false
    
    var body: some View {
        ToggleView(isOn: $isOn)  // 傳入繫結
    }
}

struct ToggleView: View {
    @Binding var isOn: Bool  // 繫結屬性
    
    var body: some View {
        Toggle("Switch", isOn: $isOn)
    }
}
```

使用 `$` 前綴來獲取狀態的 Binding 值。

## @StateObject 與 @ObservedObject

對於更複雜的狀態，使用 ObservableObject：

```swift
class AppModel: ObservableObject {
    @Published var username = ""
    @Published var isLoggedIn = false
}

struct ContentView: View {
    @StateObject private var model = AppModel()
    
    var body: some View {
        Text("User: \(model.username)")
    }
}
```

- `@StateObject`：檢視擁有此物件，生命週期與檢視綁定
- `@ObservedObject`：檢視引用外部物件

## @EnvironmentObject

全域狀態透過 EnvironmentObject 傳遞：

```swift
@main
struct MyApp: App {
    @StateObject private var settings = Settings()
    
    var body: some Scene {
        WindowGroup {
            ContentView()
                .environmentObject(settings)
        }
    }
}

struct DetailView: View {
    @EnvironmentObject var settings: Settings
    
    var body: some View {
        Text("Theme: \(settings.theme)")
    }
}
```

## 狀態管理選擇指南

| 範圍 | 使用 |
|------|------|
| 檢視本地狀態 | @State |
| 父傳子雙向 | @Binding |
| 檢視擁有複雜模型 | @StateObject |
| 引用外部模型 | @ObservedObject |
| 全域共享 | @EnvironmentObject |

## 延伸閱讀

- [SwiftUI 狀態管理](https://www.google.com/search?q=SwiftUI+state+management)
- [@State 文檔](https://www.google.com/search?q=SwiftUI+%40State+documentation)
- [@Binding 使用指南](https://www.google.com/search?q=SwiftUI+%40Binding+guide)

---

*本篇文章為「AI 程式人雜誌 2024 年 6 月號」文章集錦之五。*
