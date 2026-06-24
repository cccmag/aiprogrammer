# Jetpack Compose 宣告式 UI

## 宣告式 vs 命令式 UI

傳統 Android 開發使用 XML 定義佈局，再透過 `findViewById` 操作視圖。這種「命令式 UI」需要開發者手動控制每個 UI 元件的狀態和更新。

Jetpack Compose 採用「宣告式 UI」範式，開發者只需描述 UI 應有的樣子，框架自動處理更新：

```
命令式：    findViewById<TextView>(R.id.text).text = "Hello"
宣告式：    Text("Hello")  // Compose 自動管理
```

---

## Composable 函數

Composable 函數是 Compose 的建構單元。使用 `@Composable` 註解標記：

```kotlin
@Composable
fun Greeting(name: String) {
  Text(text = "Hello, $name!")
}
```

### 組合與重組

當 `name` 參數改變時，Compose 會自動「重組」UI：

```kotlin
@Composable
fun Counter() {
  var count by remember { mutableStateOf(0) }

  Column {
    Text("You clicked $count times")
    Button(onClick = { count++ }) {
      Text("Click me")
    }
  }
}
```

`remember` 讓狀態在重組時保留，`mutableStateOf` 讓 Compose 觀察狀態變化。

---

## 佈局元件

Compose 提供多種佈局元件：

### Column 與 Row

```kotlin
@Composable
fun ProfileCard(name: String, age: Int) {
  Column(modifier = Modifier.padding(16.dp)) {
    Row(verticalAlignment = Alignment.CenterVertically) {
      Icon(Icons.Default.Person, contentDescription = null)
      Spacer(modifier = Modifier.width(8.dp))
      Text(name, style = MaterialTheme.typography.headlineSmall)
    }
    Text("Age: $age", style = MaterialTheme.typography.bodyMedium)
  }
}
```

### Box

Box 類似 FrameLayout，允許元件疊放：

```kotlin
@Composable
fun BadgedIcon() {
  Box {
    Icon(Icons.Default.Home, contentDescription = "Home")
    Badge(modifier = Modifier.align(Alignment.TopEnd)) {
      Text("3")
    }
  }
}
```

### LazyColumn（類似 RecyclerView）

```kotlin
@Composable
fun ItemList(items: List<String>) {
  LazyColumn {
    items(items) { item ->
      ListItem(
        headlineContent = { Text(item) },
        leadingContent = { Icon(Icons.Default.Done, null) }
      )
    }
  }
}
```

---

## 修飾符（Modifier）

修飾符是 Compose 的風格和行為配置方式，可鏈式調用：

```kotlin
@Composable
fun StyledButton(text: String, onClick: () -> Unit) {
  Button(
    onClick = onClick,
    modifier = Modifier
      .fillMaxWidth()
      .padding(horizontal = 16.dp, vertical = 8.dp)
      .clip(RoundedCornerShape(8.dp))
  ) {
    Text(text)
  }
}
```

常見修飾符包括 `padding`、`size`、`fillMaxWidth`、`clip`、`background`、`clickable` 等。

---

## Material 3 主題

Compose 內建 Material 3 設計系統：

```kotlin
@Composable
fun MyApp(content: @Composable () -> Unit) {
  MaterialTheme(
    colorScheme = lightColorScheme(
      primary = Color(0xFF6200EE),
      secondary = Color(0xFF03DAC5),
      background = Color(0xFFFFFFFF)
    ),
    typography = Typography(
      headlineLarge = TextStyle(fontSize = 32.sp, fontWeight = FontWeight.Bold)
    )
  ) {
    Surface(modifier = Modifier.fillMaxSize()) {
      content()
    }
  }
}
```

### 自訂主題

```kotlin
data class MyColors(
  val primary: Color,
  val secondary: Color,
  val background: Color
)

val LocalColors = compositionLocalOf {
  MyColors(Color.Blue, Color.Cyan, Color.White)
}

@Composable
fun MyTheme(content: @Composable () -> Unit) {
  CompositionLocalProvider(LocalColors provides MyColors(
    primary = Color(0xFF1976D2),
    secondary = Color(0xFF03A9F4),
    background = Color(0xFFFAFAFA)
  )) {
    content()
  }
}
```

---

## 總結

Compose 的宣告式 UI 大幅簡化了 Android 介面開發。透過 Composable 函數組合、狀態驅動重組、以及豐富的佈局和修飾符系統，開發者可以用更少的程式碼建立更優質的使用者介面。

---

## 延伸閱讀

- [Jetpack Compose 官方指南](https://www.google.com/search?q=Jetpack+Compose+tutorial)
- [Compose 佈局基礎](https://www.google.com/search?q=Compose+layout+basics)
- [Material 3 設計系統](https://www.google.com/search?q=Material+3+design+system)
