# 文章 5：佈局 Widget — Row、Column、Stack

## Row（水平排列）

Row 將子 Widget 沿水平方向依序排列。常用屬性：
- `mainAxisAlignment`：主軸（水平）對齊
- `crossAxisAlignment`：交叉軸（垂直）對齊

```dart
Row(
  mainAxisAlignment: MainAxisAlignment.spaceEvenly,
  crossAxisAlignment: CrossAxisAlignment.center,
  children: [
    Icon(Icons.star, color: Colors.yellow, size: 40),
    Icon(Icons.favorite, color: Colors.red, size: 40),
    Icon(Icons.thumb_up, color: Colors.blue, size: 40),
  ],
)
```

## Column（垂直排列）

Column 將子 Widget 沿垂直方向依序排列。

```dart
Column(
  mainAxisAlignment: MainAxisAlignment.center,
  children: [
    Text('第一行'),
    Text('第二行'),
    SizedBox(height: 16),
    ElevatedButton(onPressed: () {}, child: Text('按鈕')),
  ],
)
```

## Expanded 與 Flexible

讓子 Widget 填滿剩餘空間，實現自適應佈局。

```dart
Row(
  children: [
    Expanded(flex: 2, child: Container(color: Colors.red)),
    Expanded(flex: 1, child: Container(color: Colors.green)),
  ],
)
```

## Stack（疊加佈局）

Stack 允許子 Widget 疊加在一起。配合 `Positioned` 精確定位。

```dart
Stack(
  children: [
    Container(width: 200, height: 200, color: Colors.blue),
    Positioned(
      top: 10,
      right: 10,
      child: Icon(Icons.close, color: Colors.white, size: 30),
    ),
    Center(child: Text('居中文字', style: TextStyle(color: Colors.white))),
  ],
)
```

## 常用佈局組合技巧

1. **Row + Column 嵌套**：實現複雜的網格結構
2. **Expanded + Flex**：建立比例分配的自適應佈局
3. **Stack + Positioned**：實現重疊效果與浮動元素
4. **AspectRatio**：維持子元件的寬高比
5. **LayoutBuilder**：根據父層尺寸動態調整佈局

## 實例：個人資料卡片

```dart
Card(
  child: Padding(
    padding: EdgeInsets.all(16),
    child: Row(
      children: [
        CircleAvatar(radius: 30, backgroundImage: NetworkImage(url)),
        SizedBox(width: 16),
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text('陳小明', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
              Text('Flutter 開發者', style: TextStyle(color: Colors.grey)),
            ],
          ),
        ),
      ],
    ),
  ),
)
```

- https://www.google.com/search?q=Flutter+Row+Column+Stack+layout+tutorial
- https://www.google.com/search?q=Flutter+Expanded+Flexible+layout
