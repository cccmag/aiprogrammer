# 函數與箭頭函數

## 函數宣告與表達式

### 函數宣告

函數宣告是最基本的定義方式，具有提升特性：

```javascript
// 函數宣告
function greet(name) {
  return `Hello, ${name}!`;
}

console.log(greet('Alice')); // 'Hello, Alice!'

// 提升特性：宣告可以在呼叫之後
sayHi(); // 'Hi!'
function sayHi() {
  console.log('Hi!');
}
```

### 函數表達式

函數表達式將函數賦值給變數，不具備提升特性：

```javascript
// 匿名函數表達式
const greet = function(name) {
  return `Hello, ${name}!`;
};

// 具名函數表達式
const factorial = function fact(n) {
  if (n <= 1) return 1;
  return n * fact(n - 1);
};
```

### 立即調用函數表達式（IIFE）

```javascript
// IIFE 模式（Immediately Invoked Function Expression）
(function() {
  const secret = '這是私有變數';
  console.log(secret);
})();

// 帶參數的 IIFE
(function(global) {
  global.appName = 'MyApp';
})(window);
```

## 參數處理

### 預設參數

```javascript
// ES6 支援預設參數
function greet(name = '訪客', greeting = 'Hello') {
  return `${greeting}, ${name}!`;
}

greet();              // 'Hello, 訪客!'
greet('Alice');       // 'Hello, Alice!'
greet('Bob', 'Hi');   // 'Hi, Bob!'
```

### Rest 參數

```javascript
// 收集剩餘參數為陣列
function sum(...numbers) {
  return numbers.reduce((total, n) => total + n, 0);
}

sum(1, 2, 3, 4); // 10

// 與其他參數結合使用
function multiply(multiplier, ...nums) {
  return nums.map(n => n * multiplier);
}

multiply(2, 1, 2, 3); // [2, 4, 6]
```

### arguments 物件

```javascript
// 傳統方式（僅在一般函數中可用）
function logAll() {
  for (let i = 0; i < arguments.length; i++) {
    console.log(arguments[i]);
  }
}

// 現代方式：使用 Rest 參數
function logAll(...args) {
  args.forEach(arg => console.log(arg));
}
```

## 箭頭函數

### 基本語法

ES6 引入的箭頭函數提供了更簡潔的寫法：

```javascript
// 無參數
const sayHi = () => console.log('Hi!');

// 單一參數（可省略括號）
const double = x => x * 2;

// 多個參數
const add = (a, b) => a + b;

// 多行函數體需要大括號和 return
const sum = (a, b) => {
  const result = a + b;
  return result;
};

// 回傳物件字面需要括號包裹
const createUser = (name, age) => ({ name, age });
```

### 箭頭函數與 this

箭頭函數最重要特性是它不綁定自己的 `this`：

```javascript
// 傳統函數的問題
const obj = {
  name: 'Alice',
  greet: function() {
    console.log(`Hello, ${this.name}`);

    // 內層函數的 this 指向全域物件
    setTimeout(function() {
      console.log(`Hello, ${this.name}`); // Hello, undefined
    }, 100);
  }
};

// 箭頭函數解決方案
const obj2 = {
  name: 'Alice',
  greet: function() {
    setTimeout(() => {
      console.log(`Hello, ${this.name}`); // Hello, Alice
    }, 100);
  }
};
```

### 箭頭函數的限制

```javascript
// 1. 不能作為建構子
const Person = (name) => { this.name = name; };
// new Person('Alice'); // TypeError

// 2. 沒有 arguments 物件
const test = () => console.log(arguments);
// test(); // ReferenceError

// 3. 不能用於物件方法需要動態 this 的情況
const obj = {
  value: 42,
  getValue: () => this.value // this 指向外層，不是 obj
};
```

## 高階函數

### 什麼是高階函數

高階函數是接受函數作為參數或回傳函數的函數：

```javascript
// 接受函數作為參數
function operate(a, b, callback) {
  return callback(a, b);
}

const result = operate(5, 3, (x, y) => x + y); // 8
```

### 回傳函數

```javascript
// 閉包工廠
function createMultiplier(factor) {
  return function(number) {
    return number * factor;
  };
}

const double = createMultiplier(2);
const triple = createMultiplier(3);

double(5); // 10
triple(5); // 15
```

### 回呼函數

```javascript
// 非同步回呼
function fetchData(callback) {
  setTimeout(() => {
    const data = { id: 1, name: 'Data' };
    callback(null, data);
  }, 1000);
}

fetchData((error, data) => {
  if (error) {
    console.error('錯誤：', error);
    return;
  }
  console.log('資料：', data);
});
```

## 純函數與副作用

### 純函數的條件

```javascript
// 純函數：相同輸入永遠得到相同輸出，無副作用
function add(a, b) {
  return a + b;
}

// 不純函數：依賴外部狀態
let taxRate = 0.05;
function calculatePrice(amount) {
  return amount * (1 + taxRate); // 依賴外部變數
}

// 不純函數：修改外部狀態
let counter = 0;
function increment() {
  counter++; // 副作用
}
```

## 總結

```javascript
// 函數是 JavaScript 中的一等公民
// 可以賦值給變數、作為參數傳遞、作為回傳值

// 現代 JavaScript 開發建議
const preferArrowFunctions = true;

// 使用箭頭函數保持簡潔和正確的 this 綁定
const numbers = [1, 2, 3, 4, 5];
const doubled = numbers.map(n => n * 2);

// 在需要動態 this 時使用一般函數
const button = {
  label: 'Click',
  handleClick: function() {
    console.log(`Clicked ${this.label}`);
  }
};
```

---

**延伸閱讀**

- [MDN 箭頭函數](https://www.google.com/search?q=MDN+arrow+functions)
- [JavaScript 閉包](https://www.google.com/search?q=JavaScript+closures)
- [函數式程式設計](https://www.google.com/search?q=functional+programming+JavaScript)
