# iOS 開發概念模擬實作

## 前言

本篇文章使用 Node.js 模擬 iOS 開發中的核心概念，包含 SwiftUI 的狀態管理、導航堆疊、資料持久化與網路請求。雖然 iOS 開發使用 Swift 語言，但我們用 JavaScript 來呈現相同的設計思維，讓尚未熟悉 Swift 的讀者也能掌握這些核心觀念。

---

## 原始碼

完整的 Node.js 實作請參考：[_code/ios_demo.js](_code/ios_demo.js)

```javascript
#!/usr/bin/env node

class State {
  constructor(initial) { this._value = initial; this._listeners = []; }
  get value() { return this._value; }
  set value(v) { this._value = v; this._listeners.forEach(fn => fn(v)); }
  watch(fn) { this._listeners.push(fn); }
}

class NavigationStack {
  constructor() { this._stack = []; }
  push(view) { this._stack.push(view); }
  pop() { if (this._stack.length > 1) return this._stack.pop(); }
  get current() { return this._stack.at(-1); }
}

class Storage {
  constructor() { this._data = {}; }
  set(key, value) { this._data[key] = JSON.stringify(value); }
  get(key) { const v = this._data[key]; return v ? JSON.parse(v) : null; }
  remove(key) { delete this._data[key]; }
}

function fetchJSON(url) {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({ ok: true, data: { id: 1, name: "iOS App", version: "1.0" } });
    }, 100);
  });
}

function demo() {
  // 狀態管理
  const count = new State(0);
  count.watch(v => console.log(`count → ${v}`));
  count.value = 5; // count → 5

  // 導航堆疊
  const nav = new NavigationStack();
  nav.push("Home"); nav.push("Detail");
  console.log(nav.current); // Detail
  nav.pop();
  console.log(nav.current); // Home

  // 資料儲存
  const store = new Storage();
  store.set("user", { name: "Alice" });
  console.log(store.get("user")); // { name: "Alice" }

  // 網路請求
  fetchJSON("https://api.example.com/app").then(console.log);
}
```

---

## SwiftUI 對應概念

### 狀態管理：@State vs State class

SwiftUI 的 `@State` 屬性包裝器會在值改變時自動重新渲染檢視。我們的 `State` 類別透過觀察者模式模擬了相同的行為。

```swift
// SwiftUI
@State private var count = 0
// 當 count 改變時，body 自動重新計算
```

```javascript
// Node.js 模擬
const count = new State(0);
count.watch(v => renderView(v));
```

### 導航堆疊：NavigationStack

```swift
// SwiftUI
NavigationStack {
  List(items) { item in
    NavigationLink(item.name, destination: DetailView(item: item))
  }
}
```

```javascript
// Node.js 模擬
const nav = new NavigationStack();
nav.push("DetailView");
nav.pop();
```

### 資料持久化：Core Data 與 SwiftData

```swift
// SwiftData
@Model class User {
  var name: String
  var age: Int
}
```

### 網路請求：URLSession

```swift
// URLSession + async/await
func fetchUser() async throws -> User {
  let data = try await URLSession.shared.data(from: url).0
  return try JSONDecoder().decode(User.self, from: data)
}
```

---

## 執行結果

```
=== iOS 開發概念模擬 ===

--- 1. 狀態管理 ---
[Watch] count changed to 1
[Watch] count changed to 5
[Watch] count changed to 3
Final count: 3

--- 2. 導航堆疊 ---
[Nav] push: HomeView
[Nav] push: DetailView
[Nav] push: SettingsView
Depth: 3, Current: SettingsView
[Nav] pop: SettingsView
After pop: DetailView

--- 3. 資料持久化 ---
Stored: {"user":"{\"name\":\"Alice\",\"age\":30}","notes":"[\"Hello\",\"World\"]"}
Get user: {"name":"Alice","age":30}
After remove: {"user":"{\"name\":\"Alice\",\"age\":30}"}

--- 4. 網路請求 ---
[Network] GET https://api.example.com/app
Response: {"id":1,"name":"iOS App","version":"1.0"}
```

---

## 核心設計模式

### 觀察者模式

SwiftUI 的狀態綁定本質上是觀察者模式的應用。當狀態值改變時，所有依賴該狀態的檢視都會自動更新。

### 堆疊資料結構

導航堆疊使用後進先出的原則，每個 push 操作對應一個新的畫面，pop 操作回到上一個畫面。

### JSON 序列化

Core Data 的資料儲存涉及物件的序列化與反序列化。我們使用 `JSON.stringify` 和 `JSON.parse` 模擬這個過程。

---

## 延伸閱讀

- [SwiftUI @State 文檔](https://www.google.com/search?q=SwiftUI+%40State+property+wrapper)
- [NavigationStack 官方教學](https://www.google.com/search?q=SwiftUI+NavigationStack+tutorial)
- [Core Data 入門](https://www.google.com/search?q=Core+Data+tutorial)
- [URLSession 使用指南](https://www.google.com/search?q=URLSession+Swift+async+await)

---

*本篇文章為「AI 程式人雜誌 2024 年 6 月號」iOS 開發專題補充文章。*
