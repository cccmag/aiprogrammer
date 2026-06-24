# JavaScript 基礎語法完整實作

## 前言

本期我們將透過一個完整的 Node.js 程式來展示 JavaScript 的核心語法。從變數宣告、函數定義、陣列操作到非同步程式設計，這個範例涵蓋了現代 JavaScript 開發的所有基礎知識。

---

## 原始碼

完整的 Node.js 實作請參考：[_code/js_basics.js](_code/js_basics.js)

```javascript
#!/usr/bin/env node
// JavaScript 基礎語法範例

// ===== 變數與型別 =====
const title = 'JavaScript 基礎';
let year = 2024;
var legacy = '避免使用 var';

const types = {
  string: '文字',
  number: 42,
  boolean: true,
  nullValue: null,
  undefinedValue: undefined,
  array: [1, 2, 3],
  object: { key: 'value' }
};

// ===== 函數與箭頭函數 =====
function add(a, b) {
  return a + b;
}

const multiply = (a, b) => a * b;

function createCounter() {
  let count = 0;
  return () => ++count;
}

// ===== 陣列高階操作 =====
const numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];

const evens = numbers.filter(n => n % 2 === 0);
const doubled = evens.map(n => n * 2);
const sum = doubled.reduce((acc, n) => acc + n, 0);

// ===== Promise 與 async/await =====
function delay(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function fetchData() {
  await delay(500);
  return { id: 1, name: 'Alice' };
}

// ===== 主程式 =====
async function demo() {
  const counter = createCounter();
  counter(); counter();

  console.log('=== JavaScript 基礎語法示範 ===');
  console.log('標題:', title);
  console.log('年份:', year);
  console.log('型別範例:', types);
  console.log('加法:', add(10, 20));
  console.log('乘法:', multiply(6, 7));
  console.log('計數器:', counter());
  console.log('偶數:', evens);
  console.log('加倍:', doubled);
  console.log('總和:', sum);

  const data = await fetchData();
  console.log('非同步資料:', data);

  const { string: str, number: num } = types;
  console.log('解構賦值:', `${str} / ${num}`);

  const more = { ...types, extra: true };
  console.log('展開運算子:', Object.keys(more));
  console.log('=== 示範結束 ===');
}

demo();
```

## 執行結果

```
=== JavaScript 基礎語法示範 ===
標題: JavaScript 基礎
年份: 2024
型別範例: { string: '文字', number: 42, boolean: true, nullValue: null, undefinedValue: undefined, array: [ 1, 2, 3 ], object: { key: 'value' } }
加法: 30
乘法: 42
計數器: 1
偶數: [ 2, 4, 6, 8, 10 ]
加倍: [ 4, 8, 12, 16, 20 ]
總和: 60
非同步資料: { id: 1, name: 'Alice' }
解構賦值: 文字 / 42
展開運算子: [ 'string', 'number', 'boolean', 'nullValue', 'undefinedValue', 'array', 'object', 'extra' ]
=== 示範結束 ===
```

---

## 語法說明

### 變數宣告

JavaScript 提供三種變數宣告方式：

- **const**：常數，不可重新賦值。優先使用
- **let**：可重新賦值的變數。有區塊作用域
- **var**：舊式宣告，有函數作用域。避免使用

### 型別系統

JavaScript 有 7 種基本型別：string、number、boolean、null、undefined、symbol、bigint。加上 object 作為複雜型別。

使用 typeof 操作符可以檢查型別，但要注意 typeof null === 'object' 是歷史遺留 bug。

### 箭頭函數

箭頭函數 (=>) 提供更簡潔的語法，且不綁定自己的 this。使用上要注意：
- 單一參數可省略括號
- 單行表達式可省略 return
- 回傳物件字面需用括號包裹

### 陣列高階函數

- **filter**：過濾出符合條件的元素
- **map**：對每個元素進行轉換
- **reduce**：將所有元素歸納為單一值

這三個函數是函數式程式設計的基礎，串聯使用可以表達複雜的資料處理邏輯。

### 非同步程式設計

Node.js 的非同步模型基於事件循環。從 Callback 到 Promise 再到 async/await，語法越來越直覺：

- **Promise**：代表一個非同步操作的最終結果
- **async/await**：讓非同步程式碼看起來像同步程式碼
- **Promise.all**：並行執行多個非同步操作

---

## 結論

這個範例展示了現代 JavaScript 的核心語法。掌握這些基礎後，讀者可以順利過渡到 React、Vue、Node.js 等框架和執行環境的學習。

完整的可執行程式碼請參考 [_code/js_basics.js](_code/js_basics.js)，建議讀者實際執行並修改程式碼來驗證學習成果。

---

## 延伸閱讀

- [JavaScript 基礎](https://www.google.com/search?q=JavaScript+tutorial+beginner)
- [MDN JavaScript 指南](https://www.google.com/search?q=MDN+JavaScript+guide)
- [Node.js 官方文件](https://www.google.com/search?q=Node.js+documentation)

---

*本篇文章為「AI 程式人雜誌 2024 年 1 月號」補充文章。*
