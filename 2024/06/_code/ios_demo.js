#!/usr/bin/env node
// ios_demo.js — iOS 開發概念模擬（Node.js）
// 模擬 SwiftUI 狀態管理、導航堆疊、資料持久化

class State {
  constructor(initial) { this._value = initial; this._listeners = []; }
  get value() { return this._value; }
  set value(v) { this._value = v; this._listeners.forEach(fn => fn(v)); }
  watch(fn) { this._listeners.push(fn); }
}

class NavigationStack {
  constructor() { this._stack = []; }
  push(view) { this._stack.push(view); console.log(`[Nav] push: ${view}`); }
  pop() { if (this._stack.length > 1) { const v = this._stack.pop(); console.log(`[Nav] pop: ${v}`); } return this.current; }
  get current() { return this._stack[this._stack.length - 1] || null; }
  get depth() { return this._stack.length; }
}

class Storage {
  constructor() { this._data = {}; }
  set(key, value) { this._data[key] = JSON.stringify(value); }
  get(key) { const v = this._data[key]; return v ? JSON.parse(v) : null; }
  remove(key) { delete this._data[key]; }
  getAll() { return { ...this._data }; }
}

function fetchJSON(url) {
  console.log(`[Network] GET ${url}`);
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({ ok: true, data: { id: 1, name: "iOS App", version: "1.0" } });
    }, 100);
  });
}

// SwiftUI @State 模擬
function useState(initial) {
  const s = new State(initial);
  return [() => s.value, (v) => { s.value = v; }, s];
}

function demo() {
  console.log("=== iOS 開發概念模擬 ===\n");

  // 1. 狀態管理（@State）
  console.log("--- 1. 狀態管理 ---");
  const [getCount, setCount, countState] = useState(0);
  countState.watch(v => console.log(`[Watch] count changed to ${v}`));
  setCount(1); setCount(5); setCount(3);
  console.log(`Final count: ${getCount()}\n`);

  // 2. 導航堆疊
  console.log("--- 2. 導航堆疊 ---");
  const nav = new NavigationStack();
  nav.push("HomeView");
  nav.push("DetailView");
  nav.push("SettingsView");
  console.log(`Depth: ${nav.depth}, Current: ${nav.current}`);
  nav.pop();
  console.log(`After pop: ${nav.current}\n`);

  // 3. 資料持久化（Core Data 風格）
  console.log("--- 3. 資料持久化 ---");
  const store = new Storage();
  store.set("user", { name: "Alice", age: 30 });
  store.set("notes", ["Hello", "World"]);
  console.log("Stored:", JSON.stringify(store.getAll()));
  console.log("Get user:", JSON.stringify(store.get("user")));
  store.remove("notes");
  console.log("After remove:", JSON.stringify(store.getAll()), "\n");

  // 4. 網路請求模擬
  console.log("--- 4. 網路請求 ---");
  fetchJSON("https://api.example.com/app").then(res => {
    console.log("Response:", JSON.stringify(res.data));
    console.log("\n=== 模擬完成 ===");
  });
}

demo();
