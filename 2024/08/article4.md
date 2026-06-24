# 文章 4：常用 Material Widget

## AppBar

頁面頂部的應用程式列，包含標題、導航按鈕與操作選單。

```dart
AppBar(
  title: Text('我的應用'),
  leading: IconButton(icon: Icon(Icons.menu), onPressed: () {}),
  actions: [
    IconButton(icon: Icon(Icons.search), onPressed: () {}),
    IconButton(icon: Icon(Icons.more_vert), onPressed: () {}),
  ],
)
```

## Card

Material Design 的卡片元件，用於呈現相關資訊區塊。

```dart
Card(
  elevation: 4,
  margin: EdgeInsets.all(8),
  child: Padding(
    padding: EdgeInsets.all(16),
    child: Column(
      children: [
        Text('卡片標題', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
        SizedBox(height: 8),
        Text('這是卡片內容，可以包含文字、圖片或其他 Widget。'),
      ],
    ),
  ),
)
```

## Switch

開關元件，常用於設定頁面的啟用/停用選項。

```dart
Switch(
  value: _isNotificationsEnabled,
  onChanged: (value) {
    setState(() => _isNotificationsEnabled = value);
  },
)
```

## TextField

文字輸入框，支援各種輸入類型與裝飾。

```dart
TextField(
  decoration: InputDecoration(
    labelText: '電子郵件',
    hintText: '請輸入 Email',
    prefixIcon: Icon(Icons.email),
    border: OutlineInputBorder(),
  ),
  keyboardType: TextInputType.emailAddress,
)
```

## ElevatedButton

浮起按鈕，Material Design 的主要按鈕樣式。

```dart
ElevatedButton(
  onPressed: () => print('按下了！'),
  child: Text('確認'),
)
```

## Chip

標籤元件，用於顯示分類、標籤或聯絡人資訊。

```dart
Wrap(
  children: [
    Chip(label: Text('Flutter')),
    Chip(label: Text('Dart')),
    Chip(label: Text('行動開發')),
  ],
)
```

## Dialog

對話框用於顯示重要資訊或要求使用者確認。

```dart
showDialog(
  context: context,
  builder: (context) => AlertDialog(
    title: Text('確認刪除？'),
    content: Text('此操作無法復原。'),
    actions: [
      TextButton(onPressed: () => Navigator.pop(context), child: Text('取消')),
      TextButton(onPressed: () => /* 刪除 */, child: Text('確認')),
    ],
  ),
)
```

- https://www.google.com/search?q=Flutter+Material+Widgets+list
- https://www.google.com/search?q=Flutter+AppBar+Card+TextField+tutorial
