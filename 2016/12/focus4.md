# 主題四：Swift 3.0

## Swift 簡介

Swift 是 Apple 開發的程式語言，於 2014 年 WWDC 首次發布，用於取代 Objective-C。Swift 3.0 於 2016 年 9 月發布，是首個開源版本的重要里程碑。

### Swift 3.0 的重要改變

```swift
// Swift 2.x vs Swift 3.0 API 命名
// Swift 2.x
UIColor.redColor()
array.removeAtIndex(0)
notificationCenter.postNotificationName("event", object: nil)

// Swift 3.0
UIColor.red
array.remove(at: 0)
notificationCenter.post(name: "event", object: nil)
```

### Swift 的核心特點

```python
swift_features = {
    '安全': 'Optional types, type safety',
    '快速': '高效能，編譯優化',
    '現代': '閉包、元組、泛型、擴展',
    '互動': 'Playgrounds 即時反饋',
    '開源': 'Linux 支援，社群驅動',
}
```

## 基本語法

### Hello World

```swift
print("Hello, Swift!")
```

### 變數和常數

```swift
// 變數
var greeting = "Hello"
greeting = "Hello, World"

// 常數
let pi = 3.14159
let appName = "MyApp"

// 型別註釋
var score: Int = 100
var temperature: Double = 36.5
var isActive: Bool = true
```

### 字串

```swift
var name = "Swift"
let greeting = "Hello, \(name)!"
let multiline = """
    This is a
    multiline
    string
"""

// 字串操作
let upper = name.uppercased()
let length = name.count
let prefix = name.hasPrefix("Sw")
```

### 集合

```swift
// Array
var numbers = [1, 2, 3, 4, 5]
numbers.append(6)
let first = numbers[0]
numbers.remove(at: 0)

// Dictionary
var ages = ["Alice": 30, "Bob": 25]
ages["Charlie"] = 35
let aliceAge = ages["Alice"]
for (name, age) in ages {
    print("\(name) is \(age)")
}

// Set
var uniqueNumbers = Set([1, 2, 3, 2, 1])
uniqueNumbers.insert(4)
```

### 控制流

```swift
// if-else
let score = 85
if score >= 90 {
    print("A")
} else if score >= 80 {
    print("B")
} else {
    print("C")
}

// switch
let grade = "A"
switch grade {
case "A": print("Excellent")
case "B": print("Good")
case "C": print("Fair")
default: print("Try harder")
}

// for-in
for i in 1...5 {
    print(i)
}

for name in ["Alice", "Bob", "Charlie"] {
    print(name)
}

// while
var counter = 0
while counter < 5 {
    counter += 1
}
```

## 函式

```swift
func greet(name: String) -> String {
    return "Hello, \(name)!"
}

// 參數標籤
func greet(to person: String, and other: String) -> String {
    return "Hello, \(person) and \(other)!"
}

greet(to: "Alice", and: "Bob")

// 預設參數值
func log(_ message: String, level: String = "INFO") {
    print("[\(level)] \(message)")
}

log("User logged in")
log("Failed login", level: "ERROR")

// 可變參數
func sum(_ numbers: Int...) -> Int {
    return numbers.reduce(0, +)
}

sum(1, 2, 3, 4, 5)

// 巢狀函式
func outer() -> () {
    func inner() {
        print("Inner")
    }
    inner()
}
```

## 閉包

```swift
// 基本語法
let add: (Int, Int) -> Int = { (a, b) in
    return a + b
}

// 簡化
let addSimple = { $0 + $1 }

// 使用
let result = addSimple(2, 3)

// Map, Filter, Reduce
let numbers = [1, 2, 3, 4, 5]
let doubled = numbers.map { $0 * 2 }
let evens = numbers.filter { $0 % 2 == 0 }
let sum = numbers.reduce(0) { $0 + $1 }
```

## Optional

```swift
// 宣告
var name: String? = "Swift"
var empty: String? = nil

// 展開
// 方法 1: if let
if let unwrapped = name {
    print("Name is \(unwrapped)")
}

// 方法 2: guard let
func process(_ name: String?) {
    guard let unwrapped = name else {
        print("No name")
        return
    }
    print("Processing \(unwrapped)")
}

// 方法 3: ?? 運算子
let displayName = name ?? "Anonymous"

// 方法 4: 可選鏈
let length = name?.count
```

## 列舉

```swift
enum Direction {
    case north
    case south
    case east
    case west
}

enum Status {
    case success(Int)
    case failure(String, Error)
}

enum Planet {
    case mercury, venus, earth, mars
    var description: String {
        switch self {
        case .mercury: return "Mercury"
        case .venus: return "Venus"
        case .earth: return "Earth"
        case .mars: return "Mars"
        }
    }
}

let status = Status.success(200)
switch status {
case .success(let code): print("Success: \(code)")
case .failure(let error): print("Error: \(error)")
}
```

## 結構體和類別

```swift
// 結構體（值型別）
struct Point {
    var x: Double
    var y: Double

    func distance(to other: Point) -> Double {
        let dx = x - other.x
        let dy = y - other.y
        return sqrt(dx * dx + dy * dy)
    }
}

// 類別（參考型別）
class Person {
    var name: String
    var age: Int

    init(name: String, age: Int) {
        self.name = name
        self.age = age
    }

    func greet() {
        print("Hello, I'm \(name)")
    }
}
```

## 協定

```swift
protocol Drawable {
    func draw()
}

protocol Colorful {
    var color: String { get }
}

struct Circle: Drawable, Colorful {
    var color: String = "red"

    func draw() {
        print("Drawing circle")
    }
}

extension Int: Colorful {
    var color: String { return "blue" }
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
    // 模擬網路請求
    throw NetworkError.timeout
}

do {
    let data = try fetchData()
    print(data)
} catch NetworkError.timeout {
    print("Request timed out")
} catch {
    print("Unknown error: \(error)")
}

// try? 簡化
let result = try? fetchData()

// try! 強制展開
let forced = try! fetchData()
```

## 泛型

```swift
func swap<T>(_ a: inout T, _ b: inout T) {
    let temp = a
    a = b
    b = temp
}

struct Stack<Element> {
    var items: [Element] = []

    mutating func push(_ item: Element) {
        items.append(item)
    }

    mutating func pop() -> Element? {
        return items.popLast()
    }
}

var stack = Stack<Int>()
stack.push(1)
stack.push(2)
print(stack.pop() ?? 0)
```

## 小結

Swift 3.0 是 Swift 語言發展的重要里程碑。通過一致的 API 命名、跨平台支援和更現代的語法，Swift 成為一個更成熟、更實用的程式語言。從 iOS/macOS 開發到伺服器端程式，Swift 的應用範圍正在不斷擴大。

---

**延伸閱讀**

- [Swift Official Documentation](https://www.google.com/search?q=Swift+official+documentation)
- [Swift Programming Language Guide](https://www.google.com/search?q=Swift+programming+language+guide)
- [Swift 3.0 Migration Guide](https://www.google.com/search?q=Swift+3+migration+guide)