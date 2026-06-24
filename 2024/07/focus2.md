# Kotlin 語言基礎

## 現代語言的優雅語法

Kotlin 是 Google 在 2017 年宣布成為 Android 官方開發語言的現代靜態型別語言。它由 JetBrains 公司開發，結合了 Java 的穩定性和現代語言的簡潔表達力。

---

## 變數與型別

### 宣告方式

Kotlin 使用 `val`（唯讀）和 `var`（可變）宣告變數：

```kotlin
val name: String = "Alice"  // 不可變（類似 final）
var age: Int = 30           // 可變
```

型別可以省略（型別推斷）：

```kotlin
val message = "Hello"       // 自動推斷為 String
var count = 42              // 自動推斷為 Int
```

### 基本型別

Kotlin 的型別系統完全物件化：

| 型別 | 大小 | 範例 |
|------|------|------|
| `Byte` | 8 位元 | `val b: Byte = 127` |
| `Short` | 16 位元 | `val s: Short = 32767` |
| `Int` | 32 位元 | `val i = 100` |
| `Long` | 64 位元 | `val l = 100L` |
| `Float` | 32 位元 | `val f = 3.14f` |
| `Double` | 64 位元 | `val d = 3.14` |
| `Boolean` | — | `val b = true` |
| `Char` | 16 位元 | `val c = 'A'` |
| `String` | — | `val s = "Hello"` |

### 字串模板

```kotlin
val name = "Alice"
println("Hello, $name!")        // Hello, Alice!
println("Length: ${name.length}") // Length: 5
```

---

## 函數

### 基本語法

```kotlin
fun add(a: Int, b: Int): Int {
  return a + b
}

// 單表達式函數（可省略回傳型別）
fun multiply(a: Int, b: Int) = a * b
```

### 預設參數

```kotlin
fun greet(name: String, prefix: String = "Hello") {
  println("$prefix, $name!")
}

greet("Alice")              // Hello, Alice!
greet("Bob", "Hi")          // Hi, Bob!
```

### 具名參數

```kotlin
fun createUser(name: String, age: Int, email: String) { /* ... */ }

createUser(age = 30, name = "Alice", email = "alice@example.com")
```

---

## Lambda 與高階函數

Lambda 是 Kotlin 的核心特性：

```kotlin
val sum = { a: Int, b: Int -> a + b }
println(sum(3, 4))  // 7

// trailing lambda 語法
val numbers = listOf(1, 2, 3, 4, 5)
val doubled = numbers.map { it * 2 }  // [2, 4, 6, 8, 10]
val evens = numbers.filter { it % 2 == 0 }  // [2, 4]
```

`it` 是單參數 Lambda 的隱式名稱。

### 高階函數

```kotlin
fun operate(a: Int, b: Int, op: (Int, Int) -> Int): Int {
  return op(a, b)
}

val result = operate(5, 3) { x, y -> x + y }  // 8
```

---

## 資料類別（Data Class）

資料類別自動生成 `equals()`、`hashCode()`、`toString()`、`copy()`：

```kotlin
data class User(
  val id: Long,
  val name: String,
  val email: String
)

val user1 = User(1, "Alice", "alice@example.com")
val user2 = user1.copy(email = "alice@new.com")
println(user1)  // User(id=1, name=Alice, email=alice@example.com)
```

---

## 密封類別（Sealed Class）

密封類別定義有限集合的子類型，常用於狀態表示：

```kotlin
sealed class Result<out T> {
  data class Success<T>(val data: T) : Result<T>()
  data class Error(val message: String) : Result<Nothing>()
}

fun handle(result: Result<String>) = when (result) {
  is Result.Success -> println("Data: ${result.data}")
  is Result.Error -> println("Error: ${result.message}")
}
```

---

## 協程簡介

Kotlin 協程簡化非同步程式設計：

```kotlin
suspend fun fetchUser(): User {
  return withContext(Dispatchers.IO) {
    // 模擬網路請求
    delay(1000)
    User(1, "Alice", "alice@example.com")
  }
}

// 在 ViewModel 中呼叫
fun loadUser() {
  viewModelScope.launch {
    val user = fetchUser()
    _userState.value = user
  }
}
```

---

## 總結

Kotlin 的現代語法特性——空安全、Lambda、資料類別、協程——大幅提升了 Android 開發效率和程式碼可讀性。掌握這些基礎後，就可以順利進入 Jetpack Compose 的世界。

---

## 延伸閱讀

- [Kotlin 官方文檔](https://www.google.com/search?q=Kotlin+official+documentation)
- [Kotlin 協程指南](https://www.google.com/search?q=Kotlin+coroutines+guide)
- [Kotlin 慣用寫法](https://www.google.com/search?q=Kotlin+idioms)
