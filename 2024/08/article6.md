# 文章 6：列表與網格

## ListView

ListView 是 Flutter 中最常用的可滑動列表元件。

### 基本用法

```dart
ListView(
  children: [
    ListTile(title: Text('項目 1'), leading: Icon(Icons.star)),
    ListTile(title: Text('項目 2'), leading: Icon(Icons.favorite)),
    Divider(),
    ListTile(title: Text('項目 3'), leading: Icon(Icons.thumb_up)),
  ],
)
```

### ListView.builder（高效）

只建構可見項目的 Widget，適合長列表。

```dart
ListView.builder(
  itemCount: 1000,
  itemBuilder: (context, index) {
    return ListTile(
      title: Text('項目 #$index'),
      subtitle: Text('這是第 $index 個項目的說明'),
    );
  },
)
```

### ListView.separated

在項目之間插入分隔元件。

```dart
ListView.separated(
  itemCount: items.length,
  separatorBuilder: (context, index) => Divider(),
  itemBuilder: (context, index) => ListTile(title: Text(items[index])),
)
```

## GridView

GridView 以網格方式排列子元件。

### GridView.count

指定列數的網格。

```dart
GridView.count(
  crossAxisCount: 2,          // 兩列
  crossAxisSpacing: 8,       // 水平間距
  mainAxisSpacing: 8,        // 垂直間距
  children: List.generate(20, (index) {
    return Card(
      child: Center(child: Text('網格 $index')),
    );
  }),
)
```

### GridView.builder

使用 builder 模式建立大型網格。

```dart
GridView.builder(
  gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
    crossAxisCount: 3,
    childAspectRatio: 1,  // 正方形
  ),
  itemCount: images.length,
  itemBuilder: (context, index) => Image.network(images[index], fit: BoxFit.cover),
)
```

## 效能最佳化

1. **使用 Builder 模式**：ListView.builder / GridView.builder
2. **避免過度重建**：將列表項抽取為獨立 StatelessWidget
3. **使用 const**：列表項目盡量使用 const 建構
4. **圖片快取**：使用 cached_network_image 套件
5. **項目高度固定**：設定 itemExtent 讓 ListView 預先計算滾動範圍

```dart
ListView.builder(
  itemExtent: 80,  // 每項固定 80 像素高
  itemCount: 500,
  itemBuilder: (context, index) => ListTile(title: Text('項目 $index')),
)
```

- https://www.google.com/search?q=Flutter+ListView+builder+tutorial
- https://www.google.com/search?q=Flutter+GridView+example+2024
