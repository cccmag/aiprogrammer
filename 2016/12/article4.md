# Swift 從 Objective-C 到 3.0

## 前言

Swift 3.0 是 Apple 語言發展的重要里程碑，標誌著 Swift 從實驗性語言向成熟、穩定系統的轉變。本文回顧 Swift 的演進並探討 Swift 3.0 的重要改變。

## Objective-C 的遺產

### 兩種語言的融合

```objc
// Objective-C 語法
@interface Person : NSObject
@property (nonatomic, strong) NSString *name;
@property (nonatomic, assign) NSInteger age;
- (void)greet;
@end

@implementation Person
- (void)greet {
    NSLog(@"Hello, %@", self.name);
}
@end
```

```swift
// Swift 等價
class Person {
    var name: String
    var age: Int

    func greet() {
        print("Hello, \(name)")
    }
}
```

## Swift 3.0 的重要改變

### API 命名規範

```swift
// Swift 2.x
UIColor.redColor()
array.removeAtIndex(0)
notificationCenter.postNotificationName("event", object: nil)

// Swift 3.0
UIColor.red
array.remove(at: 0)
notificationCenter.post(name: "event", object: nil)
```

### 枚舉大小寫

```swift
// Swift 2.x
enum Color {
    case Red
    case Green
    case Blue
}

// Swift 3.0
enum Color {
    case red
    case green
    case blue
}
```

## 基本語法演進

### Optional 處理

```swift
// 安全的 Optional 處理
var name: String? = "John"

// if let
if let unwrapped = name {
    print("Name is \(unwrapped)")
}

// guard let
func process(_ name: String?) {
    guard let unwrapped = name else {
        print("No name")
        return
    }
    print("Processing \(unwrapped)")
}

// ?? 運算子
let displayName = name ?? "Anonymous"
```

### 閉包語法

```swift
// Swift 2.x 複雜語法
numbers.sort({ (a: Int, b: Int) -> Bool in
    return a < b
})

// Swift 3.0 簡化
numbers.sort { $0 < $1 }

// 尾隨閉包
numbers.sort { $0 < $1 }
```

## Foundation 重命名

```swift
// Swift 2.x
let date = NSDate()
let formatter = NSDateFormatter()
let string = formatter.stringFromDate(date)

// Swift 3.0
let date = Date()
let formatter = DateFormatter()
let string = formatter.string(from: date)
```

### UIKit 改變

```swift
// Swift 2.x
view.addSubview(subview)
subview.addConstraint(NSLayoutConstraint(...))

// Swift 3.0
view.addSubview(subview)
subview.addConstraint(NSLayoutConstraint(...))
// 更多一致的方法命名
```

## 泛型和協定

### 泛型

```swift
// 泛型函式
func swap<T>(_ a: inout T, _ b: inout T) {
    let temp = a
    a = b
    b = temp
}

// 泛型結構
struct Stack<Element> {
    var items: [Element] = []

    mutating func push(_ item: Element) {
        items.append(item)
    }

    mutating func pop() -> Element? {
        return items.popLast()
    }
}
```

### 協定

```swift
protocol Drawable {
    func draw()
}

protocol Colorable: Drawable {
    var color: String { get set }
    func fill()
}

struct Circle: Colorable {
    var color: String = "red"

    func draw() {
        print("Drawing circle")
    }

    func fill() {
        print("Filling with \(color)")
    }
}
```

## 錯誤處理

```swift
enum NetworkError: Error {
    case noConnection
    case timeout
    case invalidResponse
}

func fetchData() throws -> String {
    // 可能拋出錯誤的程式碼
    throw NetworkError.timeout
}

// 處理錯誤
do {
    let data = try fetchData()
    print(data)
} catch NetworkError.timeout {
    print("Request timed out")
} catch {
    print("Unknown error: \(error)")
}

// try? 和 try!
let result = try? fetchData()
let forced = try! fetchData()
```

## 擴展和衍生型別

### 擴展

```swift
extension String {
    var isBlank: Bool {
        return self.trimmingCharacters(in: .whitespaces).isEmpty
    }

    func toUpperCased() -> String {
        return self.uppercased()
    }
}

"hello".isBlank // false
```

### 衍生型別

```swift
// 衍生型別
enum Direction: String {
    case north = "N"
    case south = "S"
    case east = "E"
    case west = "W"
}

// 關聯值
enum Result {
    case success(Int)
    case failure(String, Error)
}
```

## 遷移指南

### 自動遷移

```bash
# Xcode 提供自動遷移工具
# Edit > Convert > To Current Swift Syntax
```

### 常見遷移模式

```swift
// 枚舉大小寫
Color.Red -> Color.red

// Selector
#selector(MyClass.method) -> #selector(MyClass.method(_:))

// C 函式呼び出し
CGPointMake(x, y) -> CGPoint(x: x, y: y)
```

## 跨平台支援

```swift
// Linux 上使用 Foundation
#if os(Linux)
import Foundation
#else
import Cocoa
#endif

// 平台特定程式碼
#if os(macOS)
let path = "~/Documents"
#elseif os(iOS)
let path = DocumentsDirectory
#endif
```

## 小結

Swift 3.0 代表了 Apple 語言發展的重要階段。透過一致的 API 命名、現代化的語法特性，以及跨平台支援，Swift 從 Objective-C 的基礎上走出了自己的道路。遷移雖然需要時間，但換來的是更清晰、更安全的程式碼。

---

**延伸閱讀**

- [Swift 3.0 Migration Guide](https://www.google.com/search?q=Swift+3+migration+guide)
- [Swift.org Documentation](https://www.google.com/search?q=Swift+official+documentation)
- [Swift Evolution](https://www.google.com/search?q=Swift+evolution+proposals)