# 可選型別 Optional

## Optional 的誕生

在 Objective-C 時代，Nil 指標是程式崩潰的主要原因之一。發送訊息給 nil 物件雖然不會崩潰，但回傳 undefined 的行為讓錯誤難以追蹤。Swift 的設計者為了解決這個問題，引入了一個全新的概念——Optional（可選型別）。

## 什麼是 Optional

Optional 是 Swift 中一種特殊的型別，表示「有一個值」或「沒有值」。它本質上是一個列舉：

```swift
enum Optional<Wrapped> {
    case none           // 沒有值（nil）
    case some(Wrapped)  // 有值
}
```

### 宣告方式

```swift
var name: String? = "Alice"   // Optional<String>
var age: Int? = nil           // 沒有值
```

`String?` 是 `Optional<String>` 的語法糖。

## 為什麼需要 Optional

Optional 強制開發者處理「值可能不存在」的情況：

```swift
func findUser(id: Int) -> User? {
    // 可能找到使用者，也可能找不到
    return database.find(id: id)
}

let user = findUser(id: 42)
// user 的型別是 User?，不是 User
// 編譯器會強制你處理 nil 的情況
```

## Optional Binding

### if let

最安全的使用方式是使用 `if let` 進行繫結：

```swift
if let user = findUser(id: 42) {
    print("Found: \(user.name)")
} else {
    print("User not found")
}
```

### guard let

`guard let` 適合在函式開頭進行檢查：

```swift
func displayUser(id: Int) {
    guard let user = findUser(id: id) else {
        print("User not found")
        return
    }
    // 這裡可以安全使用 user
    print(user.name)
}
```

## 強制解包

使用 `!` 可以強制解包 Optional，但這在值為 nil 時會導致崩潰：

```swift
let user = findUser(id: 42)!
// 危險！如果找不到使用者會崩潰
```

僅在你「確定」值不為 nil 時使用強制解包。

## Nil Coalescing

使用 `??` 運算子提供預設值：

```swift
let name = optionalName ?? "Guest"
```

## 可選鏈（Optional Chaining）

```swift
let street = user?.address?.street
// 任一層為 nil，結果即為 nil
```

可選鏈讓多層 Optional 的存取更加簡潔。

## 隱式解包 Optional

使用 `!` 而非 `?` 宣告的 Optional 會在存取時自動解包：

```swift
var title: String! = "Hello"
print(title)  // 自動解包
```

這主要用於 Interface Builder 的 outlets，但應謹慎使用。

## 實際應用

```swift
struct User {
    let id: Int
    let name: String
    let email: String?
    
    func displayEmail() -> String {
        return email ?? "No email"
    }
}

func parseUser(from json: [String: Any]) -> User? {
    guard let id = json["id"] as? Int,
          let name = json["name"] as? String else {
        return nil
    }
    let email = json["email"] as? String
    return User(id: id, name: name, email: email)
}
```

## 最佳實踐

1. 優先使用 `if let` 和 `guard let` 進行安全解包
2. 少用強制解包 `!`
3. 使用 `??` 提供預設值
4. 只在必要時使用隱式解包

## 延伸閱讀

- [Swift Optional 文檔](https://www.google.com/search?q=Swift+Optional+documentation)
- [Swift Optional 最佳實踐](https://www.google.com/search?q=Swift+Optional+best+practices)
- [Optional 底層實現](https://www.google.com/search?q=Swift+Optional+implementation)

---

*本篇文章為「AI 程式人雜誌 2024 年 6 月號」文章集錦之三。*
