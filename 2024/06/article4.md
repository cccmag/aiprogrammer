# SwiftUI 檢視與修飾器

## View 協定

SwiftUI 中所有 UI 元件都遵循 `View` 協定。這個協定的要求非常簡單——只需要實作一個 `body` 屬性：

```swift
protocol View {
    associatedtype Body: View
    @ViewBuilder var body: Self.Body { get }
}
```

實際上你不需要直接遵循這個協定，因為 SwiftUI 提供的所有內建元件都已經遵循了。

## 內建檢視

### Text

顯示文字是應用程式中最基本的操作：

```swift
Text("Hello, SwiftUI!")
    .font(.largeTitle)
    .fontWeight(.bold)
    .foregroundColor(.blue)
    .multilineTextAlignment(.center)
```

### Image

顯示圖片，支援 SF Symbols 和自訂圖片：

```swift
Image(systemName: "star.fill")
    .resizable()
    .frame(width: 50, height: 50)
    .foregroundColor(.yellow)
```

### Button

按鈕接受一個動作閉包和一個標籤檢視：

```swift
Button(action: { print("Tapped!") }) {
    Label("Tap Me", systemImage: "hand.tap")
        .padding()
        .background(Color.blue)
        .foregroundColor(.white)
        .cornerRadius(10)
}
```

### TextField

文字輸入框使用繫結來讀取和寫入值：

```swift
@State private var text = ""

TextField("Enter text", text: $text)
    .textFieldStyle(.roundedBorder)
    .padding()
```

## 修飾器（Modifier）

修飾器是 SwiftUI 最具特色的設計模式。每個修飾器都是一個方法，回傳一個新的、修改過的檢視。

### 常見修飾器

```swift
Text("Styled Text")
    .font(.headline)           // 字型
    .foregroundColor(.primary) // 前景色
    .padding(.horizontal)      // 水平內距
    .background(Color.gray.opacity(0.1))  // 背景
    .cornerRadius(8)           // 圓角
    .shadow(color: .black.opacity(0.1), radius: 4)  // 陰影
    .padding()                 // 外層內距
```

### 修飾器順序

修飾器的應用順序會影響最終結果：

```swift
// 順序不同，結果不同
Text("Hello")
    .padding()          // 先加內距
    .background(.yellow) // 黃色背景包含內距區域

Text("Hello")
    .background(.yellow) // 先加背景
    .padding()          // 再加內距（背景不包含內距區域）
```

## 容器檢視

### Group

Group 對其子檢視進行分組，但不引入額外的佈局：

```swift
Group {
    Text("Line 1")
    Text("Line 2")
}
.font(.body)  // 同時應用於所有子檢視
```

### Section

在 List 或 Form 中建立分組：

```swift
Section("Section Title") {
    Text("Content")
}
```

## 自訂修飾器

當你需要重複使用一組修飾器時，可以建立自訂的 `ViewModifier`：

```swift
struct CardStyle: ViewModifier {
    func body(content: Content) -> some View {
        content
            .padding()
            .background(Color.white)
            .cornerRadius(12)
            .shadow(radius: 4)
    }
}

extension View {
    func cardStyle() -> some View {
        modifier(CardStyle())
    }
}

// 使用
Text("Card").cardStyle()
```

## 延伸閱讀

- [SwiftUI View 文檔](https://www.google.com/search?q=SwiftUI+View+protocol)
- [SwiftUI 修飾器大全](https://www.google.com/search?q=SwiftUI+modifiers+list)
- [自訂 ViewModifier](https://www.google.com/search?q=SwiftUI+custom+ViewModifier)

---

*本篇文章為「AI 程式人雜誌 2024 年 6 月號」文章集錦之四。*
