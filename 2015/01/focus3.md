# JavaScript ES6 新語法：Arrow Function、Promise、Class、Template Literal

## 前言

ECMAScript 6（ES6，又稱 ES2015）在 2015 年 6 月正式定案，是 JavaScript 語言史上最重要的更新。本篇介紹 2015 年初已可在部分瀏覽器使用的關鍵特性。

## Arrow Function 箭頭函式

### 基本語法

```javascript
// 傳統函式
function sum(a, b) {
  return a + b;
}

// Arrow Function
const sum = (a, b) => a + b;

// 單一參數可省略括號
const double = x => x * 2;

// 多行程式碼需要大括號和 return
const greet = (name) => {
  const message = `Hello, ${name}!`;
  return message;
};
```

### 與傳統函式的關鍵差異

```javascript
// 1. this 的綁定
function Timer() {
  this.seconds = 0;

  // 傳統函式：this 指向實例
  setInterval(function() {
    this.seconds++;  // this 是 window/undefined（strict mode）
  }, 1000);

  // Arrow Function：this 繼承外部作用域
  setInterval(() => {
    this.seconds++;  // this 指向 Timer 實例
  }, 1000);
}

// 2. arguments 物件
function traditional() {
  console.log(arguments);  // 有 arguments
}

const arrow = () => {
  console.log(arguments);  // 報錯！arguments 未定義
};

// 3. 不能作為建構函式
const Person = (name) => {
  this.name = name;  // 無法使用 new
};

// new Person('John');  // 報錯
```

### 常見用法

```javascript
// Array.prototype 方法
const numbers = [1, 2, 3, 4, 5];

numbers.map(x => x * 2);              // [2, 4, 6, 8, 10]
numbers.filter(x => x > 2);           // [3, 4, 5]
numbers.reduce((acc, x) => acc + x);  // 15

// 排序
numbers.sort((a, b) => a - b);         // 數字排序

// promise chain
fetch('/api/data')
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error(error));
```

## Promise 與非同步編程

### Promise 基本概念

```javascript
// 建立 Promise
const promise = new Promise((resolve, reject) => {
  setTimeout(() => {
    resolve('成功！');
    // 或 reject(new Error('失敗'));
  }, 1000);
});

// 處理結果
promise
  .then(result => console.log(result))
  .catch(error => console.error(error))
  .finally(() => console.log('完成'));
```

### Promise 鏈

```javascript
// 傳統回調地獄
getData(function(a) {
  getMoreData(a, function(b) {
    getEvenMoreData(b, function(c) {
      console.log(c);
    });
  });
});

// Promise 鏈
getData()
  .then(a => getMoreData(a))
  .then(b => getEvenMoreData(b))
  .then(c => console.log(c))
  .catch(error => console.error(error));
```

### Promise.all 與 Promise.race

```javascript
// 並行執行多個 Promise
Promise.all([
  fetch('/api/users'),
  fetch('/api/posts'),
  fetch('/api/comments')
])
  .then(([users, posts, comments]) => {
    console.log(users, posts, comments);
  });

// 任一個完成就繼續
Promise.race([
  fetch('/api/fast'),
  new Promise((_, reject) =>
    setTimeout(() => reject(new Error('Timeout')), 5000)
  )
])
  .then(result => console.log(result))
  .catch(error => console.error(error));
```

### fetch API 範例

```javascript
// 基本 GET 請求
fetch('/api/users')
  .then(response => response.json())
  .then(users => console.log(users))
  .catch(error => console.error(error));

// POST 請求
fetch('/api/users', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({ name: 'John', email: 'john@example.com' })
})
  .then(response => response.json())
  .then(user => console.log('Created:', user))
  .catch(error => console.error(error));

// 錯誤處理
fetch('/api/users')
  .then(response => {
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.json();
  })
  .then(data => console.log(data))
  .catch(error => console.error(error));
```

## Class 類別語法

### 基本類別定義

```javascript
// ES5 構造函式
function Person(name, age) {
  this.name = name;
  this.age = age;
}

Person.prototype.greet = function() {
  return `Hello, I'm ${this.name}`;
};

// ES6 Class
class Person {
  constructor(name, age) {
    this.name = name;
    this.age = age;
  }

  greet() {
    return `Hello, I'm ${this.name}`;
  }

  static create(name) {
    return new Person(name, 0);
  }
}

const john = new Person('John', 30);
console.log(john.greet());  // "Hello, I'm John"
const baby = Person.create('Baby');  // 靜態方法
```

### 繼承

```javascript
class Animal {
  constructor(name) {
    this.name = name;
  }

  speak() {
    console.log(`${this.name} makes a noise`);
  }
}

class Dog extends Animal {
  constructor(name, breed) {
    super(name);  // 呼叫父類別建構函式
    this.breed = breed;
  }

  speak() {
    super.speak();  // 呼叫父類別方法
    console.log(`${this.name} barks`);
  }
}

const dog = new Dog('Rex', 'German Shepherd');
dog.speak();
// "Rex makes a noise"
// "Rex barks"
```

### Getter 和 Setter

```javascript
class Circle {
  constructor(radius) {
    this._radius = radius;
  }

  get diameter() {
    return this._radius * 2;
  }

  set diameter(value) {
    this._radius = value / 2;
  }

  get area() {
    return Math.PI * this._radius ** 2;
  }
}

const circle = new Circle(5);
console.log(circle.diameter);  // 10
console.log(circle.area);      // 78.54
circle.diameter = 20;
console.log(circle._radius);   // 10
```

## Template Literal 模板字串

### 基本用法

```javascript
// 傳統字串連接
const greeting = 'Hello, ' + name + '! Today is ' + date + '.';

// Template Literal
const greeting = `Hello, ${name}! Today is ${date}.`;

// 多行字串
const html = `
  <div class="card">
    <h2>${title}</h2>
    <p>${content}</p>
  </div>
`;
```

### 表達式支援

```javascript
const a = 5;
const b = 10;

console.log(`a + b = ${a + b}`);           // "a + b = 15"
console.log(`a * b = ${a * b}`);           // "a * b = 50"

const status = 'active';
console.log(`User is ${status ? 'online' : 'offline'}`);

// 巢狀模板
const items = ['apple', 'banana', 'orange'];
const list = `
  <ul>
    ${items.map(item => `<li>${item}</li>`).join('')}
  </ul>
`;
```

### 標籤模板（Tagged Templates）

```javascript
function highlight(strings, ...values) {
  let result = '';
  strings.forEach((str, i) => {
    result += str;
    if (i < values.length) {
      result += `<strong>${values[i]}</strong>`;
    }
  });
  return result;
}

const name = 'John';
const age = 30;
const bio = highlight`My name is ${name} and I am ${age} years old.`;
// "My name is <strong>John</strong> and I am <strong>30</strong> years old."
```

## 其他 ES6 特性

### 解構賦值

```javascript
// 陣列解構
const [a, b, c] = [1, 2, 3];

// 物件解構
const { name, age } = { name: 'John', age: 30 };

// 函式參數解構
function greet({ name, age }) {
  return `Hello, ${name}! You are ${age}.`;
}

// 預設值
const { x = 10, y = 20 } = { x: 5 };
```

### 展開運算子

```javascript
// 陣列展開
const arr1 = [1, 2, 3];
const arr2 = [...arr1, 4, 5];  // [1, 2, 3, 4, 5]

// 物件展開
const obj1 = { a: 1, b: 2 };
const obj2 = { ...obj1, c: 3 };  // { a: 1, b: 2, c: 3 }

// 函式參數
const numbers = [1, 2, 3, 4, 5];
console.log(Math.max(...numbers));  // 5
```

### let 和 const

```javascript
// var：函式作用域，可重複宣告
var x = 10;

// let：區塊作用域，不可重複宣告
let y = 20;

// const：區塊作用域，必須初始化，不可重新賦值
const PI = 3.14159;
// PI = 3;  // 報錯

// const 物件可以修改屬性
const user = { name: 'John' };
user.name = 'Jane';  // 允許
```

## 結語

ES6 為 JavaScript 帶來了現代化語法，大幅提升了開發效率。Arrow Function 簡化了函式寫法、Promise 改善了非同步編程、Class 提供了清晰的 OOP 語法、Template Literal 讓字串處理更直觀。

---

## 延伸閱讀

- [ES6 完整教程](https://www.google.com/search?q=ES6+JavaScript+tutorial+arrow+function+promise)
- [Promise 詳解](https://www.google.com/search?q=JavaScript+Promise+async+await+tutorial)
- [ES6 Class 指南](https://www.google.com/search?q=ES6+class+inheritance+JavaScript)

---

*本篇文章為「AI 程式人雜誌 2015 年 1 月號」歷史回顧系列之一。*