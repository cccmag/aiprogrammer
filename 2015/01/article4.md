# ES6 規範定案：JavaScript 語法大革命

## 前言

ECMAScript 6（又稱 ES2015）在 2015 年 6 月正式定案，這是 JavaScript 語言自 2009 年 ES5 以來最重要的更新。

## 核心新特性

### Arrow Functions

```javascript
// 傳統函式
var sum = function(a, b) {
  return a + b;
};

// Arrow Function
const sum = (a, b) => a + b;

// this 綁定
class Timer {
  constructor() {
    this.seconds = 0;
    setInterval(() => {
      this.seconds++;
    }, 1000);
  }
}
```

### Classes

```javascript
class Animal {
  constructor(name) {
    this.name = name;
  }

  speak() {
    console.log(this.name + ' makes a noise.');
  }

  static create(name) {
    return new Animal(name);
  }
}

class Dog extends Animal {
  constructor(name, breed) {
    super(name);
    this.breed = breed;
  }

  speak() {
    super.speak();
    console.log(this.name + ' barks.');
  }
}
```

### Promises

```javascript
const promise = new Promise((resolve, reject) => {
  setTimeout(() => {
    resolve('成功！');
  }, 1000);
});

promise
  .then(result => console.log(result))
  .catch(error => console.error(error));
```

### Modules

```javascript
// lib.js
export const PI = 3.14159;
export function add(a, b) {
  return a + b;
}
export default class Calculator { }

// app.js
import Calculator, { PI, add } from './lib';

console.log(PI);
console.log(add(1, 2));
```

### Template Literals

```javascript
const name = 'World';
const message = `Hello, ${name}!`;

// 多行
const html = `
  <div>
    <h1>Title</h1>
  </div>
`;
```

### let 和 const

```javascript
// let：區塊作用域
if (true) {
  let x = 10;
}
console.log(x); // ReferenceError

// const：不可重新賦值
const PI = 3.14159;
PI = 3; // TypeError
```

## 瀏覽器支援（2015 年）

```
ES6 支援情況（2015 年）：
──────────────────────────
Chrome 49:  97%
Firefox 45: 95%
Safari 9:   93%
Edge 14:    94%

需要使用 Babel 轉譯以支援舊瀏覽器
```

## 結論

ES6 為 JavaScript 帶來了現代化的語法，大幅提升了開發效率和程式碼可讀性。

---

## 延伸閱讀

- [ES6 規範原文](https://www.google.com/search?q=ECMAScript+2015+ES6+specification)
- [ES6 兼容性表格](https://www.google.com/search?q=ES6+compatibility+table)

---

*本篇文章為「AI 程式人雜誌 2015 年 1 月號」文章之一。*