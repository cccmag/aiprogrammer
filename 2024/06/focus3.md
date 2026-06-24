# SwiftUI 宣告式 UI

## 從 UIKit 到 SwiftUI

在 SwiftUI 出現之前，iOS 開發者使用 UIKit 建立使用者介面。UIKit 是命令式的——你需要告訴系統「建立一個按鈕」、「設定它的位置」、「為它加入事件處理」。這種方式雖然靈活，但隨著 UI 複雜度的增加，程式碼也變得難以維護。

SwiftUI 於 2019 年問世，它引入了一種全新的宣告式編程模式。你不再需要描述「如何」建立 UI，而是「宣告」UI 應該是什麼樣子，系統自動處理其餘部分。

## View 協定

在 SwiftUI 中，所有 UI 元件都遵循 `View` 協定。一個檢視只需要實作一個計算屬性 `body`：

```swift
struct ContentView: View {
    var body: some View {
        Text("Hello, SwiftUI!")
    }
}
```

`some View` 是 Swift 的不透明回傳型別語法，表示這個屬性回傳某個符合 View 協定的型別。

## 宣告式 vs 命令式

對比 UIKit 和 SwiftUI 的差異：

### UIKit（命令式）

```swift
// UIKit
let label = UILabel()
label.text = "Hello"
label.textColor = .blue
label.textAlignment = .center
view.addSubview(label)
```

### SwiftUI（宣告式）

```swift
// SwiftUI
Text("Hello")
    .foregroundColor(.blue)
    .multilineTextAlignment(.center)
```

SwiftUI 的程式碼更簡潔，也更接近 UI 的「最終狀態」描述。

## 修飾器（Modifier）

修飾器是 SwiftUI 的核心概念之一。每個修飾器回傳一個新的檢視，這使得我們可以串聯多個修飾器：

```swift
Text("Welcome")
    .font(.title)
    .fontWeight(.bold)
    .foregroundColor(.primary)
    .padding()
    .background(Color.yellow.opacity(0.3))
    .cornerRadius(10)
```

修飾器的順序很重要。例如先 `padding` 再 `background`，與先 `background` 再 `padding` 會產生不同的視覺效果。

## 佈局系統

SwiftUI 提供了三種核心佈局容器：

### VStack（垂直排列）

```swift
VStack(alignment: .leading, spacing: 20) {
    Text("Title")
    Text("Subtitle").font(.caption)
}
```

### HStack（水平排列）

```swift
HStack {
    Image(systemName: "star")
    Text("Favorites")
}
```

### ZStack（疊加排列）

```swift
ZStack {
    Color.blue
    Text("Overlay").foregroundColor(.white)
}
```

## 預覽功能

SwiftUI 的即時預覽是開發效率的一大提升。你可以在 Xcode 的 Canvas 中即時看到 UI 的變化，無需每次編譯和執行：

```swift
#Preview {
    ContentView()
}
```

預覽支援不同的裝置尺寸、黑暗模式、甚至動態字型大小。開發者可以一次檢視多種配置下的 UI 呈現。

## 常用內建檢視

- `Text`：顯示文字
- `Image`：顯示圖片
- `Button`：可點擊的按鈕
- `TextField`：文字輸入框
- `Slider`：滑桿選擇器
- `Toggle`：開關切換
- `List`：列表顯示
- `Form`：表單容器

這些檢視可以自由組合，建構出複雜的使用者介面。

## 延伸閱讀

- [SwiftUI 官方教學](https://www.google.com/search?q=SwiftUI+tutorial+Apple)
- [SwiftUI 修飾器參考](https://www.google.com/search?q=SwiftUI+modifier+reference)
- [SwiftUI 佈局系統](https://www.google.com/search?q=SwiftUI+layout+system)

---

*本篇文章為「AI 程式人雜誌 2024 年 6 月號」iOS 開發入門系列之三。*
