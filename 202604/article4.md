# Kotlin 3.0 登場：跨平台開發再突破

## 前言

2026 年 4 月，JetBrains 正式發布 Kotlin 3.0。作為 Kotlin 語言的第三個重大版本，3.0 不僅帶來了語言層面的諸多改進，更在跨平台編譯方面實現了質的飛躍。本文深入探討 Kotlin 3.0 的核心新特性及其對開發生態的影響。

## Kotlin 的十年征程

### 從 JVM 語言到多平台

2016 年 Kotlin 1.0 發布時，它主要是一個「更好的 Java」，運行在 JVM 上。2017 年 Google 宣布 Android 官方支援 Kotlin，使其獲得了爆炸式增長。2023 年 Kotlin Multiplatform 逐漸成熟，Kotlin 開始從 JVM 語言轉變為多平台語言。

Kotlin 3.0 是這一轉變的最終里程碑——它將 Kotlin 定位為「一次編寫，隨處執行」的現代語言。

```
Kotlin 的演進：
2016: Kotlin 1.0 ─── JVM 語言
2017: 1.1 ────────── JavaScript 後端（實驗性）
2019: 1.3 ────────── 協程穩定
2021: 1.5 ────────── 跨平台穩定
2023: 2.0 ────────── K2 編譯器
2024: 2.1 ────────── 效能大幅提升
2026: 3.0 ────────── 四大目標全面穩定！
```

## 跨平台編譯的革命

### 四目標一次建置

Kotlin 3.0 的跨平台編譯器可以將同一份程式碼編譯為四種平台：

```kotlin
// 一份程式碼，四種平台

// build.gradle.kts
kotlin {
    jvm()           // JVM
    js()            // JavaScript
    wasm()          // WebAssembly
    native() {      // 原生（iOS、macOS、Linux、Windows）
        iosArm64()
        iosSimulatorArm64()
        macosArm64()
        linuxX64()
        mingwX64()
    }
    
    sourceSets {
        commonMain {
            dependencies {
                // 共用依賴
            }
        }
    }
}
```

### 共用程式碼範例

```kotlin
// commonMain 中的共用程式碼
// 這個檔案編譯為所有平台！

package com.example.app

import kotlinx.serialization.Serializable
import kotlinx.coroutines.flow.Flow

// 資料模型（所有平台共用）
@Serializable
data class User(
    val id: Long,
    val name: String,
    val email: String,
    val avatar: String? = null,
)

// 業務邏輯（所有平台共用）
class UserRepository(private val api: ApiClient) {
    
    suspend fun getUser(id: Long): Result<User> {
        return try {
            Result.success(api.fetchUser(id))
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
    
    fun searchUsers(query: String): Flow<User> {
        return api.searchUsers(query)
    }
}

// 平台特定實現只需在 expect/actual 中定義
expect class Platform() {
    val name: String
}

// Android、iOS、Web 各自實現 Platform
```

### expect/actual 機制的增強

Kotlin 3.0 對 expect/actual 機制進行了重大改進：

```kotlin
// 3.0 之前的 expect/actual（嚴格一對一匹配）
expect fun randomUUID(): String

actual fun randomUUID(): String = java.util.UUID.randomUUID().toString()

// 3.0 的新 default actual（可選實現）
expect class DefaultHttpClient {
    suspend fun get(url: String): String
}

// 可選的 actual 實現
actual class DefaultHttpClient {
    actual suspend fun get(url: String): String {
        // 平台特定的 HTTP 實現
        return httpClient.request(url)
    }
}

// 或者依賴共用程式碼的預設實現
// 如果沒有提供 actual，使用編譯器生成的預設版本
```

## Context Parameters：依賴注入的語言級支援

### 語法設計

Kotlin 3.0 引入了 Context Parameters——這是一個全新的語言特性，為依賴注入提供了原生支援：

```kotlin
// 傳統方式：將依賴作為參數傳遞
fun saveUser(user: User, db: Database, logger: Logger) {
    db.save(user)
    logger.log("User saved: ${user.id}")
}

// Context Parameters：宣告上下文依賴
fun saveUser(user: User) context(Database, Logger) {
    this@Database.save(user)
    this@Logger.log("User saved: ${user.id}")
}

// 調用時需要提供上下文
fun processUser() context(Database, Logger) {
    val user = User(1, "Alice")
    saveUser(user)  // 自動使用當前上下文
}
```

### 實際應用

```kotlin
// 在 Web 框架中的應用
@Post("/users")
context(Database, Logger, Metrics)
suspend fun createUser(@Body user: CreateUserRequest): User {
    // 自動注入資料庫、日誌、監控
    val saved = database.users.insert(user.toUser())
    logger.info("Created user: ${saved.id}")
    metrics.incrementCounter("users.created")
    return saved
}

// 測試中的應用
@Test
fun testCreateUser() {
    // 提供測試環境的上下文
    withTestDatabase { db ->
        withTestLogger { logger ->
            withTestMetrics { metrics ->
                val handler = UserHandler()
                // 上下文自動傳播
                handler.createUser(CreateUserRequest("Alice"))
            }
        }
    }
}
```

### 與傳統 DI 框架的比較

```kotlin
// Spring/Koin 方式
class UserService(
    private val db: Database,
    private val logger: Logger,
) {
    fun saveUser(user: User) {
        db.save(user)
        logger.log("Saved: ${user.id}")
    }
}

// Kotlin 3.0 Context Parameters 方式
fun saveUser(user: User) context(Database, Logger) {
    this@Database.save(user)
    this@Logger.log("Saved: ${user.id}")
}

// Context Parameters 的優勢：
// 1. 不需要建立包裝類（減少 boilerplate）
// 2. 編譯期類型安全
// 3. 沒有執行時反射開銷
// 4. 更好的 IDE 支援
```

## 效能提升

### K2 編譯器的持續改進

Kotlin 3.0 基於 K2 編譯器，帶來了顯著的效能提升：

| 指標 | Kotlin 2.0 | Kotlin 3.0 | 提升 |
|------|-----------|-----------|------|
| 編譯速度（中型專案） | 45 秒 | 28 秒 | 38% |
| 編譯速度（大型專案） | 3.2 分 | 1.8 分 | 44% |
| APK 大小（Android） | 8.2 MB | 6.8 MB | 17% |
| 執行效能 | 基準 | +15% | 15% |
| IDE 反應速度 | 基準 | +30% | 30% |

### 內聯增強

```kotlin
// Kotlin 3.0 的智能內聯
inline fun <reified T> createInstance(): T {
    // reified 型別參數的內聯更加智能
    return when (T::class) {
        String::class -> "default" as T
        Int::class -> 0 as T
        else -> T::class.constructors.first().call()
    }
}
```

## 語言特性增強

### 新的模式匹配語法

```kotlin
// Kotlin 3.0 的模式匹配增強
fun describe(value: Any): String = when (value) {
    is String if value.length > 10 -> "長字串"
    is String -> "短字串"
    is Int && > 0 -> "正數"
    is Int && < 0 -> "負數"
    is Int && == 0 -> "零"
    is Pair<String, Int> -> "配對: ${value.first}, ${value.second}"
    else -> "其他"
}
```

### 不可變集合的增強

```kotlin
// 新的不可變集合操作
val numbers = persistentListOf(1, 2, 3, 4, 5)

val result = numbers
    .filter { it % 2 == 0 }
    .map { it * it }
    .toPersistentList()  // 返回不可變列表

// 高效的結構共享
val modified = result.add(36)
// result 仍然是 [4, 16]
// modified 是 [4, 16, 36]
// 兩者共用大部份記憶體！
```

## 生態系統

### 跨平台 UI 框架

Kotlin 3.0 發布時，JetBrains 也推出了 Compose Multiplatform 1.0 穩定版：

```kotlin
// 跨平台 UI：同一份 Compose 程式碼
@Composable
fun UserProfile(user: User) {
    Column(modifier = Modifier.padding(16.dp)) {
        AsyncImage(
            model = user.avatar,
            contentDescription = "${user.name}'s avatar",
            modifier = Modifier.size(64.dp).clip(CircleShape)
        )
        
        Text(
            text = user.name,
            style = MaterialTheme.typography.h5
        )
        
        Text(
            text = user.email,
            style = MaterialTheme.typography.body2,
            color = MaterialTheme.colorScheme.onSurfaceVariant
        )
    }
}

// 這份程式碼可以直接在以下平台使用：
// - Android（原生效能）
// - iOS（原生效能）
// - Desktop（macOS、Windows、Linux）
// - Web（Canvas/WebGL）
```

### 協程的跨平台標準化

```kotlin
// 統一的協程 API
fun <T> asyncOperation(): Flow<T> = flow {
    // 在所有平台上使用相同的 API
    // Kotlin 3.0 統一了各平台的協程調度器
    
    emit(loadData())
}

// iOS/JavaScript/Swift 互操作
// Kotlin 3.0 可以將 Flow 導出為：
// - iOS: AsyncSequence
// - JS: AsyncIterable
// - Swift: AsyncSequence
```

## 結語

Kotlin 3.0 是 JetBrains 對「一次編寫，隨處執行」願景的終極實現。Context Parameters 為語言帶來了創新的依賴注入機制；跨平台編譯器的成熟使得 Android、iOS、Web 和後端共用程式碼成為現實；Compose Multiplatform 的穩定則讓 UI 層也能跨平台共用。對於考慮跨平台開發的團隊，Kotlin 3.0 已經成為一個極具競爭力的選擇。

---

**延伸閱讀**

- [Kotlin 3.0 What's New](https://www.google.com/search?q=Kotlin+3.0+whats+new)
- [Context Parameters KEEP](https://www.google.com/search?q=Kotlin+context+parameters+design)
- [Compose Multiplatform 1.0](https://www.google.com/search?q=Compose+Multiplatform+1.0+release)
