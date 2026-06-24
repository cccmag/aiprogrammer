# Compose 基本元件

## Text、Button、Image 等基礎元件

### 什麼是 Composable

在 Jetpack Compose 中，UI 元件由 `@Composable` 函數定義。這些函數描述 UI 的外觀，而非如何建構它。

### Text 元件

Text 是最基本的顯示元件：

```kotlin
@Composable
fun TextExamples() {
  Column(modifier = Modifier.padding(16.dp)) {
    // 基本文字
    Text("Hello, Compose!")

    // 樣式設定
    Text(
      text = "Styled Text",
      color = Color.Blue,
      fontSize = 24.sp,
      fontWeight = FontWeight.Bold,
      fontStyle = FontStyle.Italic
    )

    // 行數限制
    Text(
      text = "This is a very long text that should be truncated after two lines...",
      maxLines = 2,
      overflow = TextOverflow.Ellipsis
    )

    // 使用 Material Theme
    Text(
      text = "Headline",
      style = MaterialTheme.typography.headlineLarge
    )
    Text(
      text = "Body text",
      style = MaterialTheme.typography.bodyMedium
    )
  }
}
```

### Button 元件

```kotlin
@Composable
fun ButtonExamples() {
  Column(modifier = Modifier.padding(16.dp)) {
    // 基本按鈕
    Button(onClick = { /* 點擊處理 */ }) {
      Text("Click Me")
    }

    // Outlined Button
    OutlinedButton(onClick = { /* */ }) {
      Text("Outlined")
    }

    // Text Button
    TextButton(onClick = { /* */ }) {
      Text("Text Only")
    }

    // 帶圖示的按鈕
    Button(onClick = { /* */ }) {
      Icon(Icons.Default.Add, contentDescription = null)
      Spacer(modifier = Modifier.width(8.dp))
      Text("Add Item")
    }

    // 禁用按鈕
    Button(onClick = { /* */ }, enabled = false) {
      Text("Disabled")
    }
  }
}
```

### Image 元件

```kotlin
@Composable
fun ImageExamples() {
  Column(modifier = Modifier.padding(16.dp)) {
    // 從資源載入
    Image(
      painter = painterResource(id = R.drawable.sample),
      contentDescription = "Sample image",
      modifier = Modifier
        .size(200.dp)
        .clip(CircleShape),
      contentScale = ContentScale.Crop
    )

    // 從網路載入（需 Coil 套件）
    // AsyncImage(
    //   model = "https://example.com/image.jpg",
    //   contentDescription = "Network image",
    //   modifier = Modifier.fillMaxWidth()
    // )

    // 圖示
    Icon(
      imageVector = Icons.Default.Home,
      contentDescription = "Home",
      tint = Color.Red,
      modifier = Modifier.size(48.dp)
    )
  }
}
```

### TextField 輸入框

```kotlin
@Composable
fun TextFieldExamples() {
  var text by remember { mutableStateOf("") }

  Column(modifier = Modifier.padding(16.dp)) {
    OutlinedTextField(
      value = text,
      onValueChange = { text = it },
      label = { Text("Name") },
      placeholder = { Text("Enter your name") },
      leadingIcon = { Icon(Icons.Default.Person, null) },
      trailingIcon = {
        if (text.isNotEmpty()) {
          IconButton(onClick = { text = "" }) {
            Icon(Icons.Default.Clear, null)
          }
        }
      },
      modifier = Modifier.fillMaxWidth(),
      singleLine = true
    )

    // 密碼輸入
    var password by remember { mutableStateOf("") }
    var showPassword by remember { mutableStateOf(false) }

    OutlinedTextField(
      value = password,
      onValueChange = { password = it },
      label = { Text("Password") },
      visualTransformation = if (showPassword) VisualTransformation.None
        else PasswordVisualTransformation(),
      trailingIcon = {
        IconButton(onClick = { showPassword = !showPassword }) {
          Icon(
            if (showPassword) Icons.Default.VisibilityOff
            else Icons.Default.Visibility, null
          )
        }
      }
    )
  }
}
```

### 其他常用元件

```kotlin
@Composable
fun OtherComponents() {
  Column(modifier = Modifier.padding(16.dp)) {
    // Checkbox
    var checked by remember { mutableStateOf(false) }
    Row(verticalAlignment = Alignment.CenterVertically) {
      Checkbox(checked = checked, onCheckedChange = { checked = it })
      Text("Remember me")
    }

    // Switch
    var switchOn by remember { mutableStateOf(false) }
    Row(verticalAlignment = Alignment.CenterVertically) {
      Switch(checked = switchOn, onCheckedChange = { switchOn = it })
      Spacer(modifier = Modifier.width(8.dp))
      Text(if (switchOn) "Enabled" else "Disabled")
    }

    // RadioButton
    val options = listOf("Option A", "Option B", "Option C")
    var selected by remember { mutableStateOf(options[0]) }
    options.forEach { option ->
      Row(verticalAlignment = Alignment.CenterVertically) {
        RadioButton(
          selected = option == selected,
          onClick = { selected = option }
        )
        Text(option)
      }
    }

    // Progress Indicator
    LinearProgressIndicator(modifier = Modifier.fillMaxWidth())
    Spacer(modifier = Modifier.height(8.dp))
    CircularProgressIndicator()
  }
}
```

### Card 卡片元件

```kotlin
@Composable
fun CardExamples() {
  Card(
    modifier = Modifier
      .fillMaxWidth()
      .padding(16.dp),
    shape = RoundedCornerShape(12.dp),
    elevation = CardDefaults.cardElevation(defaultElevation = 4.dp)
  ) {
    Column(modifier = Modifier.padding(16.dp)) {
      Text("Card Title", style = MaterialTheme.typography.titleMedium)
      Spacer(modifier = Modifier.height(8.dp))
      Text("This is the card body content. Cards are used to group related information.")
      Spacer(modifier = Modifier.height(12.dp))
      Row(horizontalArrangement = Arrangement.End) {
        TextButton(onClick = { /* */ }) { Text("Cancel") }
        Spacer(modifier = Modifier.width(8.dp))
        Button(onClick = { /* */ }) { Text("Save") }
      }
    }
  }
}
```

### AlertDialog 對話框

```kotlin
@Composable
fun AlertDialogExample() {
  var showDialog by remember { mutableStateOf(false) }

  Button(onClick = { showDialog = true }) {
    Text("Show Dialog")
  }

  if (showDialog) {
    AlertDialog(
      onDismissRequest = { showDialog = false },
      title = { Text("Confirm Deletion") },
      text = { Text("Are you sure you want to delete this item?") },
      confirmButton = {
        Button(onClick = { showDialog = false }) { Text("Delete") }
      },
      dismissButton = {
        TextButton(onClick = { showDialog = false }) { Text("Cancel") }
      }
    )
  }
}
```

---

## 總結

Compose 提供了一組完整的基本元件，涵蓋了常見的 UI 需求。從文字顯示、按鈕操作、輸入表單到對話框，開發者可以透過組合這些元件快速建立功能完整的介面。

---

## 延伸閱讀

- [Compose 元件列表](https://www.google.com/search?q=Jetpack+Compose+components+list)
- [Material 3 元件指南](https://www.google.com/search?q=Material+3+components+Compose)
- [Compose API 參考](https://www.google.com/search?q=Compose+API+reference)
