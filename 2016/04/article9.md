# Swift 與函式式程式設計

## Swift：Apple 的現代語言

Swift 由 Apple 於 2014 年發布，作為 Objective-C 的繼承者，Swift 從一開始就設計了大量函式式特性。2016 年 Swift 2.2 的發布進一步強化了這些功能。

## 選代項（Optional）與模式匹配

Swift 的 Optional 類型體現了函式式思想：

```swift
// Optional 使用
var name: String? = "Alice"

if let unwrapped = name {
    print("Hello, \(unwrapped)")
} else {
    print("No name")
}

// Optional chaining
let length = name?.count ?? 0

// map 和 flatMap
let maybeNumber: Int? = 5
let squared = maybeNumber.map { $0 * $0 }  // Optional(25)
let incremented = maybeNumber.flatMap { $0 + 1 }  // Optional(6)
```

## 閉包語法

Swift 的閉包簡潔優雅：

```swift
// 基本閉包
let add = { (a: Int, b: Int) -> Int in
    return a + b
}

// 推斷類型
let addInferred = { a, b in a + b }

// 單一表達式閉包（隱式返回）
let square = { $0 * $0 }

// 作為參數
numbers.map { $0 * 2 }
numbers.filter { $0 > 5 }
numbers.reduce(0) { $0 + $1 }
```

## 高階函式

Swift 的 Collection 类型支援豐富的高階函式：

```swift
let numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

// map：轉換
let squares = numbers.map { $0 * $0 }

// filter：篩選
let evens = numbers.filter { $0 % 2 == 0 }

// reduce：聚合
let sum = numbers.reduce(0) { $0 + $1 }

// 組合
let result = numbers
    .filter { $0 % 2 == 0 }
    .map { $0 * $0 }
    .reduce(0) { $0 + $1 }

// flatMap：扁平化
let nested = [[1, 2], [3, 4], [5]]
let flat = nested.flatMap { $0 }
```

## 枚舉與代數資料類型

Swift 的枚舉支持關聯值，相當於代數資料類型：

```swift
enum Result<T> {
    case success(T)
    case failure(Error)
}

enum Tree<T> {
    case leaf(T)
    case node(Tree<T>, Tree<T>)
}

// 使用模式匹配
func sum(tree: Tree<Int>) -> Int {
    switch tree {
    case .leaf(let value):
        return value
    case .node(let left, let right):
        return sum(tree: left) + sum(tree: right)
    }
}
```

## 函數式錯誤處理

Swift 的錯誤處理可以與函式式風格結合：

```swift
// 定義錯誤
enum MathError: Error {
    case divisionByZero
    case invalidInput
}

// throwing 函式
func safeDivide(_ a: Double, _ b: Double) throws -> Double {
    guard b != 0 else { throw MathError.divisionByZero }
    return a / b
}

// 使用 map 和 flatMap 處理 Result
let result = try? safeDivide(10, 2)
    .map { $0 * 2 }
```

## 協定導向設計

Swift 的協定（Protocol）提供了強大的抽象機制：

```swift
// 定義協定
protocol Monoid {
    static var identity: Self { get }
    static func combine(_ a: Self, _ b: Self) -> Self
}

// 實現
extension Int: Monoid {
    static var identity: Int { 0 }
    static func combine(_ a: Int, _ b: Int) -> Int { a + b }
}

extension Array: Monoid {
    static var identity: Array { [] }
    static func combine(_ a: Array, _ b: Array) -> Array { a + b }
}
```

## 2016 年的 Swift

2016 年 Swift 持續快速迭代：

- Swift 2.2 支援更多平臺
- Swift 正式開放原始碼（2015年12月）
- Linux 版 Swift 持續改進

Swift 的開放原始碼讓更多人能夠參與語言的發展，也為伺服器端程式設計打開了大門。

延伸閱讀：
- [Google 搜尋：Swift functional programming](https://www.google.com/search?q=Swift+functional+programming)
- [Google 搜尋：Swift optional handling](https://www.google.com/search?q=Swift+optional+handling)