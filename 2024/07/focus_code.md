# Android 概念 Node.js 模擬實作

## 前言

本文使用 Node.js 模擬 Android 開發中的核心概念，包括 Lifecycle 狀態機、ViewModel 狀態管理、Navigation 路由、Room 資料庫 CRUD 等。透過 JavaScript 模擬，讓初學者在不需 Android Studio 的情況下理解這些概念。

完整原始碼請參考：[_code/android_demo.js](_code/android_demo.js)

---

## Lifecycle 狀態機

Android 的 Activity 和 Fragment 擁有明確的生命週期。我們用狀態機模擬：

```javascript
const LIFECYCLE_STATES = {
  INITIALIZED: 'INITIALIZED',
  CREATED: 'CREATED',
  STARTED: 'STARTED',
  RESUMED: 'RESUMED',
  PAUSED: 'PAUSED',
  STOPPED: 'STOPPED',
  DESTROYED: 'DESTROYED',
}

class Lifecycle {
  constructor() {
    this.state = LIFECYCLE_STATES.INITIALIZED
    this.listeners = []
  }
  addObserver(fn) { this.listeners.push(fn) }
  transition(newState) {
    const old = this.state
    this.state = newState
    this.listeners.forEach(fn => fn(old, newState))
  }
  onCreate() { this.transition(LIFECYCLE_STATES.CREATED) }
  onStart()  { this.transition(LIFECYCLE_STATES.STARTED) }
  onResume() { this.transition(LIFECYCLE_STATES.RESUMED) }
  onPause()  { this.transition(LIFECYCLE_STATES.PAUSED) }
  onStop()   { this.transition(LIFECYCLE_STATES.STOPPED) }
  onDestroy(){ this.transition(LIFECYCLE_STATES.DESTROYED) }
}
```

---

## ViewModel 狀態管理

ViewModel 在 Android 中負責在配置變更時保留資料：

```javascript
class ViewModel {
  constructor() { this._state = {}; this._observers = [] }
  getState(key) { return this._state[key] }
  setState(key, value) {
    this._state[key] = value
    this.notify(key, value)
  }
  notify(key, value) {
    this._observers.forEach(o => o(key, value))
  }
  observe(fn) { this._observers.push(fn) }
  onCleared() { this._observers = [] }
}
```

---

## Navigation 路由模擬

Navigation Component 管理頁面之間的轉換：

```javascript
class NavController {
  constructor() {
    this.backStack = []
    this.currentRoute = null
  }
  navigate(route, args = {}) {
    if (this.currentRoute) this.backStack.push(this.currentRoute)
    this.currentRoute = { route, args }
  }
  goBack() {
    if (this.backStack.length === 0) return false
    this.currentRoute = this.backStack.pop()
    return true
  }
}
```

---

## Room 資料庫 CRUD 模擬

Room 是 Android 的持久化層。我們用記憶體陣列模擬：

```javascript
class RoomDatabase {
  constructor() { this.tables = {} }
  createTable(name) { this.tables[name] = [] }
  insert(table, record) {
    record.id = Date.now() + Math.random()
    this.tables[table].push(record)
    return record.id
  }
  query(table, predicate = () => true) {
    return this.tables[table].filter(predicate)
  }
  update(table, id, updates) {
    const idx = this.tables[table].findIndex(r => r.id === id)
    if (idx !== -1) Object.assign(this.tables[table][idx], updates)
  }
  delete(table, id) {
    this.tables[table] = this.tables[table].filter(r => r.id !== id)
  }
}
```

---

## 執行結果

```
=== Lifecycle Demo ===
State: INITIALIZED -> CREATED
State: CREATED -> STARTED
State: STARTED -> RESUMED
State: RESUMED -> PAUSED
State: PAUSED -> STOPPED
State: STOPPED -> DESTROYED

=== ViewModel Demo ===
Count set to: 1
Count set to: 2
Count set to: 3

=== Navigation Demo ===
Navigated to: home
Navigated to: profile
Navigated to: settings
Back to: profile
Back to: home

=== Room Demo ===
Inserted user: Alice, id=...
Inserted user: Bob, id=...
All users: 2
Updated Alice to Alice Smith
Found Alice: Alice Smith
Deleted Bob
Remaining: 1
```

---

## 結論

透過這些模擬，我們可以看到 Android 核心概念的運作原理：

1. **Lifecycle** 讓開發者知道何時初始化、釋放資源
2. **ViewModel** 在螢幕旋轉等配置變更時保留狀態
3. **Navigation** 提供統一的路由和返回棧管理
4. **Room** 提供結構化的本地資料持久化方案

這些模式不僅適用於 Android，也廣泛應用於現代前端開發。

---

## 延伸閱讀

- [Android 開發者官方指南](https://www.google.com/search?q=Android+developer+official+guide)
- [Jetpack 架構元件](https://www.google.com/search?q=Android+Jetpack+architecture+components)
- [Node.js 模擬 Android 概念原始碼](_code/android_demo.js)

---

*本篇文章為「AI 程式人雜誌 2024 年 7 月號」技術實作補充文章。*
