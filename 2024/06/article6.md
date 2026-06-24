# 列表與導航

## List 元件

List 是 SwiftUI 中最基礎的列表容器，用於顯示可滾動的資料行。它相當於 UIKit 中的 UITableView，但使用起來更簡單。

### 基本用法

```swift
struct ContentView: View {
    let items = ["Apple", "Banana", "Cherry", "Date"]
    
    var body: some View {
        List(items, id: \.self) { item in
            Text(item)
        }
    }
}
```

### 使用 Identifiable 資料

對於自訂資料型別，讓它遵循 Identifiable 協定：

```swift
struct Item: Identifiable {
    let id = UUID()
    let name: String
    let emoji: String
}

let items = [
    Item(name: "Apple", emoji: "🍎"),
    Item(name: "Banana", emoji: "🍌"),
    Item(name: "Cherry", emoji: "🍒")
]

List(items) { item in
    Label(item.name, systemImage: item.emoji)
}
```

### 列表樣式

```swift
List {
    Section("Fruits") {
        Text("Apple")
        Text("Banana")
    }
    Section("Vegetables") {
        Text("Carrot")
        Text("Broccoli")
    }
}
.listStyle(.insetGrouped)
```

## 滑動操作

在行上實現滑動刪除和操作：

```swift
List {
    ForEach(items) { item in
        Text(item.name)
            .swipeActions(edge: .trailing) {
                Button("Delete", role: .destructive) {
                    delete(item)
                }
                Button("Pin") { pin(item) }
                    .tint(.yellow)
            }
    }
}
```

## NavigationStack 整合

將 List 與 NavigationStack 結合實現導航：

### 基礎導航

```swift
NavigationStack {
    List(items) { item in
        NavigationLink(item.name, value: item)
    }
    .navigationTitle("Items")
    .navigationDestination(for: Item.self) { item in
        DetailView(item: item)
    }
}
```

### 動態導航

有時需要根據條件決定導航目標：

```swift
NavigationStack {
    List {
        NavigationLink("Profile", destination: ProfileView())
        NavigationLink("Settings", destination: SettingsView())
    }
    .navigationTitle("Menu")
}
```

## 可搜尋列表

iOS 15 以上的 `.searchable` 修飾器：

```swift
@State private var searchText = ""

var filteredItems: [String] {
    items.filter { searchText.isEmpty || $0.localizedCaseInsensitiveContains(searchText) }
}

NavigationStack {
    List(filteredItems, id: \.self) { item in
        Text(item)
    }
    .searchable(text: $searchText, prompt: "Search...")
    .navigationTitle("Items")
}
```

## 可重新排序列表

```swift
@State private var items = ["A", "B", "C"]

List {
    ForEach(items, id: \.self) { item in
        Text(item)
    }
    .onMove { from, to in
        items.move(fromOffsets: from, toOffset: to)
    }
}
.toolbar { EditButton() }
```

## 下拉重新整理

```swift
List(items, id: \.self) { item in
    Text(item)
}
.refreshable {
    // 執行非同步重新整理
    try? await Task.sleep(nanoseconds: 2_000_000_000)
    await loadItems()
}
```

## 效能考量

對於大量資料，使用 LazyVStack 來實現懶加載：

```swift
ScrollView {
    LazyVStack {
        ForEach(items) { item in
            ItemRow(item: item)
        }
    }
}
```

## 延伸閱讀

- [SwiftUI List 文檔](https://www.google.com/search?q=SwiftUI+List+documentation)
- [NavigationStack 指南](https://www.google.com/search?q=SwiftUI+NavigationStack+guide)
- [List 效能最佳化](https://www.google.com/search?q=SwiftUI+List+performance)

---

*本篇文章為「AI 程式人雜誌 2024 年 6 月號」文章集錦之六。*
