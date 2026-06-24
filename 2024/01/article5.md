# 閉包與作用域

## 什麼是作用域

作用域決定了變數的可見性和生命週期。JavaScript 使用詞法作用域（Lexical Scoping），即函數的作用域在定義時決定：

```javascript
// 全域作用域
const globalVar = '全域';

function outer() {
  // 函數作用域
  const outerVar = '外部';

  function inner() {
    // 內部函數可以訪問外層變數
    console.log(globalVar); // '全域'
    console.log(outerVar);  // '外部'
  }

  inner();
}
```

### 作用域鏈

當訪問一個變數時，JavaScript 會沿著作用域鏈向上查找：

```javascript
const x = 'global';

function level1() {
  const x = 'level1';

  function level2() {
    const x = 'level2';

    function level3() {
      console.log(x); // 'level2'（最近的作用域）
    }

    level3();
  }

  level2();
}

level1();
```

## 閉包（Closure）

### 什麼是閉包

閉包是函數與其詞法環境的組合。即使外部函數已經返回，內部函數仍然可以訪問外部函數的變數：

```javascript
function createCounter() {
  let count = 0; // 被閉包捕獲的變數

  return function() {
    count++;
    return count;
  };
}

const counter = createCounter();
console.log(counter()); // 1
console.log(counter()); // 2
console.log(counter()); // 3
```

### 閉包的經典應用

**1. 私有變數**

```javascript
function createBankAccount(initialBalance) {
  let balance = initialBalance;

  return {
    deposit(amount) {
      balance += amount;
      return `存入 ${amount}，餘額 ${balance}`;
    },
    withdraw(amount) {
      if (amount > balance) return '餘額不足';
      balance -= amount;
      return `提領 ${amount}，餘額 ${balance}`;
    },
    getBalance() {
      return balance;
    }
  };
}

const account = createBankAccount(1000);
console.log(account.deposit(500));  // 存入 500，餘額 1500
console.log(account.withdraw(200)); // 提領 200，餘額 1300
// console.log(account.balance); // undefined（無法直接訪問）
```

**2. 工廠函數**

```javascript
function createMultiplier(factor) {
  return (number) => number * factor;
}

const double = createMultiplier(2);
const triple = createMultiplier(3);

console.log(double(5));  // 10
console.log(triple(5));  // 15
```

**3. 事件監聽器**

```javascript
function setupButtons() {
  const buttons = document.querySelectorAll('button');

  for (let i = 0; i < buttons.length; i++) {
    // 使用 let 會為每次迭代建立獨立的作用域
    buttons[i].addEventListener('click', () => {
      console.log(`按鈕 ${i} 被點擊`);
    });
  }
}
```

### 閉包與迴圈的陷阱

```javascript
// 常見錯誤：使用 var
for (var i = 0; i < 5; i++) {
  setTimeout(() => {
    console.log(i); // 全部輸出 5
  }, i * 1000);
}

// 解決方案 1：使用 let
for (let i = 0; i < 5; i++) {
  setTimeout(() => {
    console.log(i); // 0, 1, 2, 3, 4
  }, i * 1000);
}

// 解決方案 2：使用 IIFE 建立閉包
for (var i = 0; i < 5; i++) {
  (function(j) {
    setTimeout(() => {
      console.log(j); // 0, 1, 2, 3, 4
    }, j * 1000);
  })(i);
}
```

## 作用域類型

### 全域作用域

```javascript
// 瀏覽器中的全域物件是 window
var globalVar = '全域';
console.log(window.globalVar); // '全域'

// 在 Node.js 中全域物件是 global
// global.globalVar = '全域';
```

### 函數作用域

```javascript
function scopeTest() {
  if (true) {
    var functionScoped = '我是 var';
    let blockScoped = '我是 let';
  }

  console.log(functionScoped); // '我是 var'
  // console.log(blockScoped); // ReferenceError
}
```

### 區塊作用域（ES6）

```javascript
{
  const a = 'const 也是區塊作用域';
  let b = 'let 當然也是';
  var c = 'var 不是區塊作用域';
}

// console.log(a); // ReferenceError
// console.log(b); // ReferenceError
console.log(c); // 'var 不是區塊作用域'
```

## 記憶體管理

閉包會保持對外部變數的引用，可能導致記憶體洩漏：

```javascript
function createLargeData() {
  const largeData = new Array(1000000).fill('data');

  return function() {
    // 這個閉包持有 largeData 的引用
    console.log(largeData.length);
  };
}

// 即使不再需要 largeData，它仍然存在於記憶體中
const closure = createLargeData();
// 當確實不再需要時，可以釋放
// closure = null;
```

## 實用範例

### 記憶化（Memoization）

```javascript
function memoize(fn) {
  const cache = {};

  return function(...args) {
    const key = JSON.stringify(args);

    if (key in cache) {
      console.log('從快取返回');
      return cache[key];
    }

    const result = fn(...args);
    cache[key] = result;
    return result;
  };
}

const expensiveCalc = memoize((n) => {
  console.log('執行耗時計算');
  return n * n;
});

console.log(expensiveCalc(5)); // 執行耗時計算，25
console.log(expensiveCalc(5)); // 從快取返回，25
```

### 柯里化

```javascript
function curry(fn) {
  return function curried(...args) {
    if (args.length >= fn.length) {
      return fn(...args);
    }
    return (...more) => curried(...args, ...more);
  };
}

const add = (a, b, c) => a + b + c;
const curriedAdd = curry(add);

console.log(curriedAdd(1)(2)(3)); // 6
console.log(curriedAdd(1, 2)(3)); // 6
```

## 結語

閉包是 JavaScript 中最核心也最難掌握的概念之一。理解了閉包，就理解了 JavaScript 的作用域機制、模組模式和函數式程式設計的基礎。

---

**延伸閱讀**

- [MDN 閉包](https://www.google.com/search?q=MDN+closures)
- [JavaScript 作用域深入](https://www.google.com/search?q=JavaScript+scope+explained)
- [閉包與記憶體](https://www.google.com/search?q=JavaScript+closure+memory+leak)
