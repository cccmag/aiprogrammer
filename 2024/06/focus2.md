# Swift 語言基礎

## 語言的誕生

Swift 由 Chris Lattner 於 2010 年開始設計，2014 年在 WWDC 上首次公開。它的設計目標是取代 Objective-C，成為 Apple 生態系的主要開發語言。Swift 融合了現代語言的特性—型別安全、型別推論、函數式編程模式，同時保持了與 Objective-C 的互操作性。

## 變數與常數

Swift 使用 `var` 宣告變數，`let` 宣告常數。型別可透過推論自動判斷：

```swift
var count = 10        // Int
let name = "Alice"    // String，常數不可修改
var price: Double = 99.99  // 明確指定型別
```

Swift 是強型別語言，所有變數在編譯時期就確定型別，這有助於減少執行時期錯誤。

## 基本資料型別

### 數值型別

```swift
let int: Int = 42
let float: Float = 3.14
let double: Double = 3.1415926535
let bool: Bool = true
```

### 字串與字元

```swift
let greeting = "Hello, iOS!"
let emoji: Character = "🚀"
let multiline = """
這是多行字串
在 Swift 中非常方便
"""
```

### 集合型別

```swift
let array: [String] = ["A", "B", "C"]
var dictionary: [String: Int] = ["apple": 1, "banana": 2]
let set: Set<Int> = [1, 2, 3, 3]  // 重複元素自動去除
```

## 函式

Swift 的函式使用 `func` 關鍵字，支援外部參數名稱和預設值：

```swift
func greet(to person: String, with message: String = "Hello") -> String {
    return "\(message), \(person)!"
}
print(greet(to: "World"))  // Hello, World!
```

### 閉包

閉包是 Swift 中的一等公民，類似於 JavaScript 的箭頭函式：

```swift
let numbers = [3, 1, 4, 1, 5]
let sorted = numbers.sorted { $0 < $1 }
```

## 結構體與類別

### 結構體（Struct）

結構體是值型別，賦值時會複製：

```swift
struct User {
    var name: String
    var age: Int
    
    func description() -> String {
        return "\(name) (\(age))"
    }
}
```

### 類別（Class）

類別是參考型別，賦值時共享同一實例：

```swift
class Counter {
    var value = 0
    
    func increment() { value += 1 }
}
```

## 協定（Protocol）

協定類似於其他語言的介面，定義了型別必須實作的方法和屬性：

```swift
protocol Drivable {
    var speed: Double { get set }
    func drive()
}

struct Car: Drivable {
    var speed: Double = 0
    
    func drive() {
        print("Driving at \(speed) km/h")
    }
}
```

Swift 的協定還可以透過 extension 提供預設實作，並支援協定組合。

## 錯誤處理

Swift 使用 `do-catch` 和 `throws` 處理錯誤：

```swift
enum FileError: Error {
    case notFound
    case permissionDenied
}

func readFile(_ path: String) throws -> String {
    guard path.hasPrefix("/") else {
        throw FileError.notFound
    }
    return "file content"
}

do {
    let content = try readFile("/data")
} catch {
    print("Error: \(error)")
}
```

## 延伸學習

- [Swift 官方文檔](https://www.google.com/search?q=Swift+programming+language)
- [Swift 風格指南](https://www.google.com/search?q=Swift+style+guide)
- [Swift 演進提案](https://www.google.com/search?q=Swift+evolution+proposal)

---

*本篇文章為「AI 程式人雜誌 2024 年 6 月號」iOS 開發入門系列之二。*
