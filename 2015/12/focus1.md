# Web 技術發展回顧

## 前言

2015 年是 Web 技術發展的重要一年。從 JavaScript 框架的激烈競爭到 ES6 標準的正式發布，從 React 的崛起到 WebAssembly 的進展，Web 開發正在經歷深刻的變革。

## JavaScript 框架競合

### 2015 年框架態勢

```
┌─────────────────────────────────────────────────────────────┐
│                 JavaScript 框架勢力圖（2015）               │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   React ★★★★★     ────>  Facebook 主導                    │
│   Angular ★★★★      ────>  Google 主導                    │
│   Vue.js ★★★        ────>  社群驅動                       │
│   Ember ★★★        ────>  穩健但小眾                      │
│   Backbone ★★       ────>  逐步退場                       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### React 的崛起

React 在 2015 年獲得了爆發式增長：

- **Facebook 持續投入**：React 0.14 發布，DOM 分離
- **社群採用加速**：Netflix、Airbnb、Instagram 等大站使用
- **React Native 發布**：用 React 開發原生行動應用
- **React DevTools**：除錯工具成熟

### Angular 2 的演進

Angular 2 從 Alpha 到 Beta，功能逐漸完善：

- **TypeScript 支援**：Angular 2 全面採用 TypeScript
- **Component-based**：完全組件化的架構
- **效能優化**：更快的變更偵測
- **行動優先**：專為行動應用優化

### Vue.js 的興起

Vue.js 在 2015 年獲得了顯著關注：

- **簡單易學**：學習曲線平緩
- **漸進式採用**：可以只使用核心功能
- **中文文件**：在華語圈快速傳播
- **Laravel 採用**：Taylor Otwell 的背書

## ECMAScript 2015（ES6）

### 重要新特性

#### 類別（Class）

```javascript
class Person {
  constructor(name, email) {
    this.name = name;
    this.email = email;
  }

  greet() {
    return `Hello, I'm ${this.name}`;
  }

  static create(name, email) {
    return new Person(name, email);
  }
}

class Student extends Person {
  constructor(name, email, grade) {
    super(name, email);
    this.grade = grade;
  }
}
```

#### 箭頭函數（Arrow Functions）

```javascript
// 傳統函數
const add = function(a, b) {
  return a + b;
};

// 箭頭函數
const add = (a, b) => a + b;

// 閉包
const numbers = [1, 2, 3, 4, 5];
const doubled = numbers.map(n => n * 2);
```

#### Promise

```javascript
const fetchData = () => {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      resolve({ data: "Hello" });
    }, 1000);
  });
};

fetchData()
  .then(result => console.log(result))
  .catch(error => console.error(error));
```

#### 模組（Modules）

```javascript
// math.js
export const PI = 3.14159;

export function add(a, b) {
  return a + b;
}

export default class Calculator {
  // ...
}

// main.js
import { add, PI } from './math';
import Calculator from './math';
```

#### 解構賦值（Destructuring）

```javascript
const { name, email } = user;
const [first, second, ...rest] = array;
const { data: result } = response;
```

#### Template Literals

```javascript
const greeting = `Hello, ${name}!`;
const html = `
  <div>
    <h1>${title}</h1>
    <p>${content}</p>
  </div>
`;
```

#### Let 和 Const

```javascript
let count = 0;  // 區塊作用域
const MAX = 100;  // 常量，不可重新賦值

if (true) {
  let blockScoped = "only in this block";
  const alsoBlockScoped = "same";
}
```

### 瀏覽器支援

| 功能 | Chrome | Firefox | Safari | Edge |
|------|--------|---------|--------|------|
| Classes | 49 | 44 | 9 | 13 |
| Arrow Functions | 49 | 44 | 9 | 13 |
| Promises | 32 | 29 | 7.1 | 12 |
| Modules | ✗ | ✗ | ✗ | ✗ |
| async/await | 55 | 52 | 10 | 15 |

## WebAssembly 進展

### 什麼是 WebAssembly？

WebAssembly（簡稱 WASM）是一種低層級的位元組碼格式，可以在瀏覽器中以接近原生的速度執行：

- **效能**：接近原生程式碼執行速度
- **可移植**：支援多種語言編譯
- **安全**：在沙盒環境中執行
- **高效**：位元組碼格式，解析快速

### 2015 年里程碑

- 初步規範制定完成
- Firefox Nightly 支援
- Emscripten 工具鏈成熟
- 越來越多專案開始支援

### 範例

```rust
// Rust 程式碼
#[no_mangle]
pub extern "C" fn add(a: i32, b: i32) -> i32 {
    a + b
}
```

編譯為 WebAssembly 後可以在瀏覽器中呼叫。

## 開發工具演進

### 建構工具

| 工具 | 特點 | 2015 年狀態 |
|------|------|-------------|
| Webpack | 功能完整、擴展性強 | v1.13 發布 |
| Rollup | 專為 ES6 模組優化 | v0.25 發布 |
| Browserify | 簡單易用 | 社群驅動 |
| Parcel | 零配置 | 即將發布 |

### 轉譯器

| 工具 | 用途 | 2015 年狀態 |
|------|------|-------------|
| Babel | ES6 → ES5 | v6.0 發布 |
| TypeScript | JS 超集 | v1.6/1.7 |
| CoffeeScript | Python-like JS | v2.0 開發中 |

### 除錯工具

- **Chrome DevTools**：持續改進
- **React DevTools**：發布 Beta
- **Vue DevTools**：發布 v1.0

## 未來展望

### 2016 年預期

1. **ES6 全面支援**：主流瀏覽器完整支援
2. **WebAssembly 可用**：正式進入瀏覽器
3. **HTTP/2 普及**：改變資源載入方式
4. **Service Workers**：離線應用成標準
5. **GraphQL vs REST**：新的 API 範式競爭

## 小結

2015 年是 Web 技術發展的重要一年：

- **JavaScript 框架成熟**：React、Angular、Vue 形成三強鼎立
- **ES6 開啟新時代**：現代 JavaScript 特性全面可用
- **WebAssembly 接近現實**：高效 Web 應用的未來
- **開發工具現代化**：建構和除錯工具大幅改進

---

## 延伸閱讀

- [ES6 Tutorial](https://www.google.com/search?q=ES6+tutorial+beginners)
- [React vs Angular vs Vue](https://www.google.com/search?q=React+vs+Angular+vs+Vue+2015)
- [WebAssembly Guide](https://www.google.com/search?q=WebAssembly+guide)