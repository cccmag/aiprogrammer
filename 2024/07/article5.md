# 狀態與重組

## Compose 的狀態驅動 UI 更新機制

### 宣告式 UI 的核心概念

在傳統的 View 系統中，開發者需要手動更新 UI：

```kotlin
// 命令式：手動更新
textView.text = "新文字"
button.isEnabled = false
```

在 Compose 中，UI 是狀態的函數：

```kotlin
// 宣告式：描述 UI 應有的樣子
@Composable
fun Greeting(name: String) {
  Text("Hello, $name!")
}
```

當 `name` 改變時，Compose 會自動「重組」（Recompose）UI。

### 狀態的基礎：mutableStateOf

`mutableStateOf` 建立 Compose 可觀察的狀態：

```kotlin
@Composable
fun Counter() {
  val count = remember { mutableStateOf(0) }

  Column {
    Text("Count: ${count.value}")
    Button(onClick = { count.value++ }) {
      Text("Increment")
    }
  }
}
```

**關鍵概念**：
- `mutableStateOf` 建立一個可觀察的狀態容器
- `remember` 讓狀態在重組時保留（不是每次重組都重新初始化）
- 當 `.value` 改變時，Compose 排程重組

### 委派屬性語法

使用 Kotlin 的委派屬性讓語法更簡潔：

```kotlin
@Composable
fun CounterDelegate() {
  var count by remember { mutableStateOf(0) }

  Column {
    Text("Count: $count")
    Button(onClick = { count++ }) {
      Text("Increment")
    }
  }
}
```

`by` 關鍵字允許直接使用 `count` 而非 `count.value`。

### 狀態提升（State Hoisting）

將狀態移到呼叫端，使元件無狀態（stateless）且可重用：

```kotlin
// 低階元件：無狀態
@Composable
fun CounterDisplay(
  count: Int,
  onIncrement: () -> Unit,
  onDecrement: () -> Unit
) {
  Row(verticalAlignment = Alignment.CenterVertically) {
    Button(onClick = onDecrement) { Text("-") }
    Text("$count", modifier = Modifier.padding(horizontal = 16.dp))
    Button(onClick = onIncrement) { Text("+") }
  }
}

// 高階元件：持有狀態
@Composable
fun CounterScreen() {
  var count by remember { mutableStateOf(0) }

  CounterDisplay(
    count = count,
    onIncrement = { count++ },
    onDecrement = { count-- }
  )
}
```

### 狀態容器：remember vs rememberSaveable

```kotlin
@Composable
fun StateComparison() {
  // 僅在重組時保留（螢幕旋轉時丟失）
  val lost on Rotation = remember { mutableStateOf("") }

  // 在行程重建時也保留（透過 Bundle）
  val saved = rememberSaveable { mutableStateOf("") }
}
```

### derivedStateOf

從其他狀態推導出新狀態，避免不必要的重組：

```kotlin
@Composable
fun ShoppingCart(items: List<String>) {
  val itemCount by remember(items.size) {
    derivedStateOf { items.size }
  }

  val hasItems by remember(items.isEmpty()) {
    derivedStateOf { items.isNotEmpty() }
  }

  Text("Items: $itemCount")
  if (hasItems) {
    Button(onClick = { /* 結帳 */ }) {
      Text("Checkout")
    }
  }
}
```

### 集合狀態

對於列表等集合，使用 `mutableStateListOf`：

```kotlin
@Composable
fun TodoList() {
  val todos = remember { mutableStateListOf<String>() }
  var input by remember { mutableStateOf("") }

  Column {
    Row {
      OutlinedTextField(
        value = input,
        onValueChange = { input = it }
      )
      Button(onClick = {
        if (input.isNotBlank()) {
          todos.add(input)
          input = ""
        }
      }) {
        Text("Add")
      }
    }

    LazyColumn {
      items(todos) { todo ->
        Text(todo, modifier = Modifier.padding(8.dp))
      }
    }
  }
}
```

### 重組的時機與最佳化

Compose 會在以下情況排程重組：

1. 狀態值改變
2. 輸入參數改變
3. 父元件重組

**最佳化技巧**：

```kotlin
// 使用 derivedStateOf 減少重組範圍
@Composable
fun ExpensiveList(items: List<String>, query: String) {
  val filteredItems by remember(items, query) {
    derivedStateOf {
      items.filter { it.contains(query, ignoreCase = true) }
    }
  }

  LazyColumn {
    items(filteredItems) { item ->
      ListItem(headlineContent = { Text(item) })
    }
  }
}

// 使用 key 幫助 LazyColumn 追蹤
LazyColumn {
  items(items, key = { it.id }) { item ->
    ListItem(headlineContent = { Text(item.name) })
  }
}
```

### 副作用（Side Effects）

```kotlin
@Composable
fun SideEffectExamples() {
  // LaunchedEffect：在 Composable 進入組合時執行協程
  LaunchedEffect(Unit) {
    val data = api.fetchData()
    // 更新狀態
  }

  // DisposableEffect：清理資源
  DisposableEffect(Unit) {
    val observer = LifecycleObserver()
    lifecycle.addObserver(observer)
    onDispose {
      lifecycle.removeObserver(observer)
    }
  }
}
```

### 狀態持有者模式

對於複雜邏輯，建立自訂的狀態持有者類別：

```kotlin
class CounterState {
  var count by mutableStateOf(0)
  var maxReached by mutableStateOf(false)
    private set

  fun increment() {
    count++
    if (count >= 100) maxReached = true
  }

  fun reset() {
    count = 0
    maxReached = false
  }
}

@Composable
fun rememberCounterState(): CounterState {
  return remember { CounterState() }
}
```

---

## 總結

Compose 的狀態與重組機制讓 UI 開發變得宣告式且直覺。掌握 `remember`、`mutableStateOf`、狀態提升和 `derivedStateOf`，就能有效管理 UI 狀態並最佳化重組效能。

---

## 延伸閱讀

- [Compose 狀態管理指南](https://www.google.com/search?q=Compose+state+management+guide)
- [Compose 重組與效能](https://www.google.com/search?q=Compose+recomposition+performance)
- [Compose 副作用文檔](https://www.google.com/search?q=Compose+side+effects)
