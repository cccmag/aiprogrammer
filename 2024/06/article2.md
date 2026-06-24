# Swift 變數與型別

## 型別系統概覽

Swift 是一門強型別語言，這意味著每個變數和常數都有一個明確的型別，且編譯器會檢查型別的一致性。強型別系統有助於在編譯時期捕獲錯誤，減少執行時期的意外崩潰。

## 變數與常數

### var 與 let

Swift 使用 `var` 宣告可變變數，`let` 宣告不可變常數：

```swift
var score = 0       // 可變
score += 10         // OK

let maxScore = 100  // 不可變
// maxScore = 200   // 編譯錯誤！
```

常數 `let` 的使用不只為了防止意外修改，也幫助編譯器進行最佳化。

### 型別推論

Swift 編譯器可以從賦值自動推斷變數的型別：

```swift
let name = "Alice"        // String
let count = 42            // Int
let pi = 3.14             // Double（預設浮點數型別）
let isActive = true       // Bool
```

你仍可以明確指定型別：

```swift
let price: Double = 99    // 99.0
let value: Float = 3.14   // Float 而非預設的 Double
```

## 基本型別

### 數值型別

```swift
let int8: Int8 = 127
let uint: UInt = 42
let hex = 0xFF          // 255
let binary = 0b1010     // 10
let octal = 0o77        // 63
let scientific = 1.5e5  // 150000.0
```

Swift 不允許不同數值型別的隱式轉換，需要使用建構子顯式轉換：

```swift
let x: Int = 3
let y: Double = Double(x) + 0.5
```

### 字串

```swift
var greeting = "Hello"
greeting += ", Swift!"   // Hello, Swift!
let count = greeting.count  // 13
let hasPrefix = greeting.hasPrefix("Hello")

// 字串插值
let age = 30
let message = "Age: \(age)"
```

### 布林值

```swift
let isSwift = true
if isSwift {
    print("This is Swift!")
}
```

## 集合型別

### 陣列

```swift
var fruits: [String] = ["Apple", "Banana"]
fruits.append("Cherry")
let first = fruits[0]           // Apple
let sorted = fruits.sorted()
```

### 字典

```swift
var scores: [String: Int] = [:]
scores["Alice"] = 95
scores["Bob"] = 87
let aliceScore = scores["Alice"] ?? 0
```

### 集合

```swift
let unique: Set<Int> = [1, 2, 3, 1, 2]
// {1, 2, 3} — 重複元素自動去除
```

## 型別安全與型別推論的優勢

Swift 的型別安全機制避免了許多常見的程式設計錯誤：

```swift
// 編譯錯誤：不能將 String 賦值給 Int
var number: Int = 0
// number = "hello"

// 編譯錯誤：Int 和 Double 需要顯式轉換
let result = Double(number) + 0.5
```

這些檢查讓 Bug 在開發階段就被發現，而不是等到使用者回報。

## 型別別名

使用 `typealias` 可以為既有型別建立別名：

```swift
typealias JSON = [String: Any]
let data: JSON = ["name": "Swift"]
```

## 延伸閱讀

- [Swift 型別文檔](https://www.google.com/search?q=Swift+types+documentation)
- [Swift 型別安全](https://www.google.com/search?q=Swift+type+safety)
- [Swift 集合型別](https://www.google.com/search?q=Swift+collection+types)

---

*本篇文章為「AI 程式人雜誌 2024 年 6 月號」文章集錦之二。*
