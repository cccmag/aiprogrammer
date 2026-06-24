# 空安全與擴充函數

## Kotlin 最有價值的兩項特性

### 空安全（Null Safety）

空指標異常（NullPointerException）是 Java 中最常見的錯誤來源。Kotlin 透過型別系統在編譯時期解決這個問題。

### 可空與不可空型別

```kotlin
var name: String = "Alice"    // 不可空 → 永遠不能為 null
// name = null               // 編譯錯誤！

var nullableName: String? = null  // 可空 → 可以為 null
```

**強制轉換為可空**：

```kotlin
val text: String? = nullableName ?: "Fallback"  // Elvis 運算子
val length: Int = text?.length ?: 0             // 安全呼叫 + Elvis
```

### 安全呼叫運算子（?.）

```kotlin
data class Address(val street: String?)
data class User(val address: Address?)

fun getUserStreet(user: User?): String? {
  return user?.address?.street   // 任一層 null 則回傳 null
}

fun getUserStreetSafe(user: User?): String {
  return user?.address?.street ?: "Unknown"
}
```

### Elvis 運算子（?:）

```kotlin
fun getLength(str: String?): Int = str?.length ?: 0

// 也可以與 return/throw 合用
fun checkNotNull(str: String?): String {
  return str ?: throw IllegalArgumentException("str cannot be null")
}
```

### 非空斷言（!!）

```kotlin
val nullable: String? = "Hello"
val nonNull: String = nullable!!  // 強制非空

// 如果 nullable 為 null，會拋出 KotlinNullPointerException
// 謹慎使用：只在 100% 確定非空時使用
```

### let 與 run

```kotlin
fun processUser(user: User?) {
  // let：在非空時執行
  user?.let { u ->
    println(u.name)
    println(u.age)
  }

  // 可以簡化為
  user?.let {
    println(it.name)
    println(it.age)
  }
}

// run：執行並回傳 Lambda 結果
val fullName = nullableName?.run {
  "$this Smith"    // this 指向 nullableName
} ?: "Unknown"
```

### 安全轉型（as?）

```kotlin
val obj: Any = "Hello World"
val str: String? = obj as? String    // 成功："Hello World"
val num: Int? = obj as? Int          // 失敗：null（不會拋出 ClassCastException）
```

### 可空擴充

Kotlin 的 `?.` 可與擴充函數結合：

```kotlin
fun String?.isEmptyOrNull(): Boolean {
  return this == null || this.isEmpty()
}

val a: String? = null
val b: String? = ""
val c: String? = "Hello"

println(a.isEmptyOrNull())  // true
println(b.isEmptyOrNull())  // true
println(c.isEmptyOrNull())  // false
```

---

### 擴充函數（Extension Functions）

擴充函數可以在不繼承的情況下為既有類別添加方法。

### 基本語法

```kotlin
// 為 String 添加擴充函數
fun String.addExclamation(): String = "$this!"

// 使用
println("Hello".addExclamation())  // Hello!

// 為 List<Int> 添加擴充
fun List<Int>.sumOfSquares(): Int = this.sumOf { it * it }
println(listOf(1, 2, 3).sumOfSquares())  // 14
```

### 擴充屬性

```kotlin
val String.isEmail: Boolean
  get() = this.contains("@")

println("user@example.com".isEmail)  // true
println("hello".isEmail)             // false
```

### 泛型擴充

```kotlin
fun <T> List<T>.secondOrNull(): T? {
  return if (size >= 2) this[1] else null
}

fun <T> List<T>.lastTwo(): List<T> {
  return if (size >= 2) this.takeLast(2) else this
}

println(listOf(1, 2, 3).secondOrNull())  // 2
println(listOf(1).secondOrNull())        // null
```

### 可空接收者擴充

```kotlin
fun String?.toDefault(default: String = ""): String {
  return this ?: default
}

val nullStr: String? = null
println(nullStr.toDefault("N/A"))  // N/A
```

### 實例：String 工具擴充

```kotlin
fun String.isValidPassword(): Boolean {
  return this.length >= 8 &&
    this.any { it.isDigit() } &&
    this.any { it.isUpperCase() } &&
    this.any { it.isLowerCase() }
}

fun String.isValidPhone(): Boolean {
  return this.matches(Regex("^09\\d{8}$"))
}

fun String.truncate(maxLength: Int, suffix: String = "..."): String {
  return if (length <= maxLength) this
    else take(maxLength) + suffix
}

println("HelloWorld123".isValidPassword())  // true
println("0912345678".isValidPhone())       // true
println("Hello, World!".truncate(8))      // Hello, W...
```

### 擴充泛型類別

```kotlin
// 為 Map 添加擴充
fun <K, V> Map<K, V>.getOrThrow(key: K, message: String = "Key not found: $key"): V {
  return this[key] ?: throw NoSuchElementException(message)
}

val map = mapOf("a" to 1, "b" to 2)
println(map.getOrThrow("a"))     // 1
// map.getOrThrow("c")           // 拋出 NoSuchElementException
```

### 標準庫常用擴充

Kotlin 標準庫包含大量實用的擴充函數：

```kotlin
// 集合
listOf(3, 1, 4, 1, 5).sorted()          // [1, 1, 3, 4, 5]
listOf(1, 2, 3).joinToString(",")       // "1,2,3"

// 字串
"  hello  ".trim()                       // "hello"
"abc".repeat(3)                          // "abcabcabc"

// 檔案
File("test.txt").readText()              // 讀取所有文字
File("log.txt").appendText("new line")   // 附加內容

// 序列
(1..100).filter { it % 2 == 0 }.take(5).toList()  // [2, 4, 6, 8, 10]
```

---

## 總結

空安全讓 Kotlin 在編譯時期消滅了 NullPointerException，而擴充函數則讓程式碼更具表達力和重用性。這兩個特性相輔相成，是 Kotlin 最受歡迎的原因之一。

---

## 延伸閱讀

- [Kotlin 空安全指南](https://www.google.com/search?q=Kotlin+null+safety)
- [Kotlin 擴充函數](https://www.google.com/search?q=Kotlin+extension+functions)
- [Kotlin 慣用寫法進階](https://www.google.com/search?q=Kotlin+idioms+advanced)
