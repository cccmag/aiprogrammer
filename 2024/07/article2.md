# Kotlin 變數與函數

## 從變數宣告到 Lambda 表達式

Kotlin 融合了物件導向與函數式程式設計的精華。本文將從最基本的變數宣告開始，逐步深入函數的各種用法。

### 變數宣告

Kotlin 使用 `val` 與 `var` 區分唯讀與可變：

```kotlin
val name = "Alice"      // 唯讀 (類似 Java 的 final)
var age = 30            // 可變
var count: Int = 0      // 明確指定型別
```

**型別推斷**：Kotlin 編譯器可從初始值推斷型別，無需明確指定。

### 基本型別

```kotlin
val intVal: Int = 42
val longVal: Long = 42L
val floatVal: Float = 3.14f
val doubleVal: Double = 3.14
val boolVal: Boolean = true
val charVal: Char = 'A'
val stringVal: String = "Hello"
```

### 字串模板

字串模板讓變數嵌入更方便：

```kotlin
val user = "Alice"
val age = 30
println("User: $user, Age: $age")           // User: Alice, Age: 30
println("Next year: ${age + 1}")           // Next year: 31
println("Name length: ${user.length}")     // Name length: 5
```

### 可空型別

Kotlin 透過 `?` 區分可空與不可空型別：

```kotlin
val nonNull: String = "Hello"
val nullable: String? = null

// nonNull.length     // 安全
// nullable.length    // 編譯錯誤！
nullable?.length       // 安全呼叫：如果為 null 則回傳 null
nullable?.length ?: 0  // Elvis 運算子：如果為 null 則使用預設值 0
```

### 函數宣告

```kotlin
// 完整語法
fun add(a: Int, b: Int): Int {
  return a + b
}

// 單表達式函數
fun multiply(a: Int, b: Int) = a * b

// 無回傳值
fun greet(name: String) {
  println("Hello, $name!")
}
```

### 預設與具名參數

```kotlin
fun createUser(
  name: String,
  age: Int = 18,           // 預設值
  email: String = "none@example.com"
) = "$name ($age) - $email"

createUser("Alice")                       // 使用預設值
createUser("Bob", 25)                     // 指定年齡
createUser(email = "bob@test.com", name = "Bob", age = 30)  // 具名參數
```

### Lambda 表達式

Lambda 是 Kotlin 函數式程式設計的核心：

```kotlin
// 基本 Lambda
val sum = { a: Int, b: Int -> a + b }
println(sum(3, 4))  // 7

// Lambda 作為參數
fun operate(x: Int, y: Int, op: (Int, Int) -> Int): Int = op(x, y)
operate(5, 3, { a, b -> a + b })   // 8
operate(5, 3) { a, b -> a * b }    // 15 (trailing lambda)

// 使用 it（單參數隱式名稱）
val numbers = listOf(1, 2, 3, 4, 5)
numbers.filter { it % 2 == 0 }     // [2, 4]
numbers.map { it * 2 }             // [2, 4, 6, 8, 10]
```

### 匿名函數

```kotlin
val square = fun(x: Int): Int = x * x
println(square(5))  // 25

numbers.filter(fun(x: Int): Boolean { return x > 3 })  // [4, 5]
```

### 高階函數實例

```kotlin
fun <T> List<T>.customFilter(predicate: (T) -> Boolean): List<T> {
  val result = mutableListOf<T>()
  for (item in this) {
    if (predicate(item)) result.add(item)
  }
  return result
}

val words = listOf("apple", "banana", "cherry", "date")
val longWords = words.customFilter { it.length > 5 }
// [banana, cherry]
```

### 擴充函數

Kotlin 允許為現有類別添加新函數：

```kotlin
fun String.reverse(): String = this.reversed()
fun Int.isEven(): Boolean = this % 2 == 0

println("Hello".reverse())   // olleH
println(42.isEven())         // true
```

### 中綴函數

```kotlin
infix fun Int.plus(x: Int): Int = this + x
println(5 plus 3)  // 8

// 自定義 Pair 建立
infix fun <A, B> A.to(that: B): Pair<A, B> = Pair(this, that)
val pair = "key" to "value"  // (key, value)
```

### 解構宣告

```kotlin
val (x, y) = Pair(3, 4)           // x=3, y=4
val (name, age) = User("Alice", 30)  // 需有 componentN() 函數

data class Point(val x: Int, val y: Int)
val point = Point(10, 20)
val (px, py) = point               // px=10, py=20
```

---

## 總結

掌握變數宣告、空安全、Lambda 和擴充函數，就掌握了 Kotlin 最核心的日常用法。這些特性讓程式碼更簡潔、更安全、更具表達力。

---

## 延伸閱讀

- [Kotlin 語法參考](https://www.google.com/search?q=Kotlin+syntax+reference)
- [Kotlin 慣用寫法](https://www.google.com/search?q=Kotlin+idioms)
- [Kotlin 函數式程式設計](https://www.google.com/search?q=Kotlin+functional+programming)
