# this 關鍵字全解析

## this 的基礎概念

this 是 JavaScript 中最容易混淆的概念之一。它的值不是在定義時決定的，而是在函數被調用時動態綁定。

### 全域環境中的 this

```javascript
// 瀏覽器
console.log(this === window); // true

// Node.js（模組中）
console.log(this === module.exports); // true

// 一般函數中的 this（非嚴格模式）
function showThis() {
  console.log(this); // 瀏覽器：window，Node.js：global
}

// 嚴格模式
function showThisStrict() {
  'use strict';
  console.log(this); // undefined
}
```

## this 綁定規則

JavaScript 有五種 this 綁定規則，優先級從低到高。

### 1. 預設綁定

```javascript
function greet() {
  console.log(`Hello, ${this.name}`);
}

const name = 'Global';

// 非嚴格模式：this 指向全域物件
greet(); // Hello, Global

// 嚴格模式：this 為 undefined
```

### 2. 隱式綁定

當函數作為物件的方法被調用時，this 指向該物件：

```javascript
const user = {
  name: 'Alice',
  greet() {
    console.log(`Hello, ${this.name}`);
  },
  profile: {
    name: 'Bob',
    greet() {
      console.log(`Hello, ${this.name}`);
    }
  }
};

user.greet();       // Hello, Alice（this 指向 user）
user.profile.greet(); // Hello, Bob（this 指向 profile）

// 隱式綁定丟失
const greetFn = user.greet;
greetFn(); // Hello, undefined（this 指向全域）

// 回呼函數中的丟失
setTimeout(user.greet, 1000); // Hello, undefined
```

### 3. 顯式綁定

使用 call、apply、bind 強制指定 this：

```javascript
function introduce(language, level) {
  console.log(`${this.name} 使用 ${language}（${level}）`);
}

const alice = { name: 'Alice' };
const bob = { name: 'Bob' };

// call：立即執行，參數列表
introduce.call(alice, 'JavaScript', '進階');
introduce.call(bob, 'Python', '中級');

// apply：立即執行，參數陣列
introduce.apply(alice, ['JavaScript', '進階']);

// bind：建立新函數，不立即執行
const aliceIntro = introduce.bind(alice);
aliceIntro('JavaScript', '進階');
aliceIntro('TypeScript', '初學');
```

### 4. new 綁定

使用 new 關鍵字時，this 指向新建立的物件：

```javascript
function Person(name, age) {
  // this = {}（由 new 建立）
  this.name = name;
  this.age = age;
  // return this（隱含）
}

const alice = new Person('Alice', 30);
console.log(alice.name); // 'Alice'

// 箭頭函數不能作為建構子
// const PersonArrow = (name) => { this.name = name; };
// new PersonArrow('Alice'); // TypeError
```

### 5. 箭頭函數綁定

箭頭函數沒有自己的 this，它繼承外層作用域的 this：

```javascript
const obj = {
  name: 'Alice',
  traditional: function() {
    console.log('傳統:', this.name);

    setTimeout(function() {
      console.log('傳統內層:', this.name); // undefined
    }, 100);
  },
  arrow: function() {
    console.log('箭頭外層:', this.name);

    setTimeout(() => {
      console.log('箭頭內層:', this.name); // 'Alice'
    }, 100);
  }
};

obj.traditional();
// 傳統: Alice
// 傳統內層: undefined

obj.arrow();
// 箭頭外層: Alice
// 箭頭內層: Alice
```

## 常見場景解析

### DOM 事件處理

```javascript
const button = document.querySelector('#myButton');

// 一般函數：this 指向觸發事件的元素
button.addEventListener('click', function() {
  console.log(this); // button 元素
  this.classList.toggle('active');
});

// 箭頭函數：this 繼承外層
button.addEventListener('click', () => {
  console.log(this); // window（或外層的 this）
});

// 如果需要同時存取 event 和 this
button.addEventListener('click', function(event) {
  console.log(this);          // button
  console.log(event.target);  // button
});
```

### 物件方法

```javascript
const counter = {
  count: 0,
  increment() {
    this.count++;
    return this;
  },
  decrement() {
    this.count--;
    return this;
  },
  getCount() {
    return this.count;
  }
};

// 鏈式調用（回傳 this）
counter.increment().increment().decrement();
console.log(counter.getCount()); // 1
```

### 類別中的 this

```javascript
class Timer {
  constructor(seconds) {
    this.seconds = seconds;
  }

  start() {
    // 箭頭函數確保 this 指向 Timer 實例
    this.intervalId = setInterval(() => {
      this.seconds--;
      console.log(this.seconds);

      if (this.seconds <= 0) {
        this.stop();
      }
    }, 1000);
  }

  stop() {
    clearInterval(this.intervalId);
    console.log('計時結束');
  }
}

const timer = new Timer(5);
timer.start();
```

## 實用技巧

### 安全的 this

```javascript
// 方法 1：箭頭函數
class SafeClass {
  constructor() {
    this.name = 'Safe';
  }
  method() {
    const inner = () => {
      console.log(this.name); // 'Safe'
    };
    inner();
  }
}

// 方法 2：bind
class BindClass {
  constructor() {
    this.name = 'Bind';
    this.method = this.method.bind(this);
  }
  method() {
    console.log(this.name);
  }
}

// 方法 3：保存引用
class SaveClass {
  constructor() {
    this.name = 'Save';
    const self = this;
    setTimeout(function() {
      console.log(self.name);
    }, 100);
  }
}
```

## this 優先級總結

1. **new 綁定** > 顯式綁定 > 隱式綁定 > 預設綁定
2. 箭頭函數不遵循以上規則，繼承外層 this
3. 箭頭函數不能被 new 調用

```javascript
function priorityTest() {
  console.log(this.name);
}

const obj1 = { name: 'Obj1', test: priorityTest };
const obj2 = { name: 'Obj2' };

// 隱式綁定
obj1.test();             // Obj1

// 顯式綁定優先於隱式綁定
obj1.test.call(obj2);    // Obj2

// new 綁定優先於顯式綁定
new priorityTest();      // undefined（新的空物件）

// bind 不能與 new 一起使用
// const Bound = priorityTest.bind(obj1);
// new Bound(); // 仍然指向新物件
```

## 結語

this 的混亂源於 JavaScript 的動態綁定機制。理解五種綁定規則後，大部分 this 相關的 bug 都可以避免。建議在專案中統一使用箭頭函數或 .bind() 來管理 this 的指向。

---

**延伸閱讀**

- [MDN this](https://www.google.com/search?q=MDN+this+keyword)
- [JavaScript this 詳解](https://www.google.com/search?q=JavaScript+this+keyword+explained)
- [箭頭函數與 this](https://www.google.com/search?q=arrow+function+this)
