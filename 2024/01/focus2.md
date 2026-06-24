# 變數、型別與運算子

## 變數宣告

### var、let、const 的差異

JavaScript 提供三種變數宣告方式，各自有不同的作用域規則：

```javascript
// var：函數作用域，可重複宣告，會被提升
var x = 10;
var x = 20; // 可以重複宣告

// let：區塊作用域，不可重複宣告
let y = 30;
// let y = 40; // SyntaxError

// const：區塊作用域，不可重新賦值
const z = 50;
// z = 60; // TypeError: Assignment to constant variable
```

**作用域比較：**
```javascript
function scopeDemo() {
  if (true) {
    var a = 1;   // 函數作用域
    let b = 2;   // 區塊作用域
    const c = 3; // 區塊作用域
  }
  console.log(a); // 1（var 跳出 if 區塊）
  // console.log(b); // ReferenceError
  // console.log(c); // ReferenceError
}
```

### 變數提升

```javascript
console.log(foo); // undefined（變數被提升但未初始化）
var foo = 'hello';

// let 和 const 也會被提升，但存在暫時性死區
// console.log(bar); // ReferenceError
let bar = 'world';
```

## 基本資料型別

JavaScript 有 7 種基本型別和 1 種複雜型別：

```javascript
// 基本型別（Primitive Types）
const str = '字串';          // string
const num = 42;              // number
const bool = true;           // boolean
const undef = undefined;     // undefined
const nul = null;            // null
const sym = Symbol('id');    // symbol (ES6)
const big = 9007199254740991n; // bigint (ES2020)

// 複雜型別（Object）
const obj = { name: 'Alice' };
const arr = [1, 2, 3];
const func = function() {};
```

### typeof 運算子

```javascript
typeof 'hello';    // 'string'
typeof 42;         // 'number'
typeof true;       // 'boolean'
typeof undefined;  // 'undefined'
typeof null;       // 'object'（歷史遺留問題）
typeof Symbol();   // 'symbol'
typeof function(){}; // 'function'
typeof {};         // 'object'
typeof [];         // 'object'
```

## 型別轉換

### 隱式轉換

JavaScript 是弱型別語言，會在運算時自動轉換型別：

```javascript
'5' - 3;     // 2（字串轉為數字）
'5' + 3;     // '53'（數字轉為字串，+ 有字串連接優先）
+'5';        // 5（一元正號轉數字）
!!'hello';   // true（雙重否定轉布林）

// 比較運算子的陷阱
null == undefined;  // true
null === undefined; // false（嚴格比較）
'0' == false;      // true（都轉為 0）
'0' === false;     // false
```

### 顯式轉換

```javascript
// 轉為字串
String(123);       // '123'
(123).toString();  // '123'

// 轉為數字
Number('123');     // 123
parseInt('123px'); // 123
parseFloat('3.14'); // 3.14

// 轉為布林
Boolean(0);        // false
Boolean('');       // false
Boolean(null);     // false
Boolean(undefined);// false
Boolean(NaN);      // false
Boolean([]);       // true（空陣列為 true）
Boolean({});       // true（空物件為 true）
```

## 運算子一覽

### 算術運算子

```javascript
let a = 10, b = 3;
a + b;   // 13
a - b;   // 7
a * b;   // 30
a / b;   // 3.333...
a % b;   // 1（餘數）
a ** b;  // 1000（指數運算，ES7）
a++;     // 10（後置遞增，回傳原值後加 1）
++a;     // 12（前置遞增，先加 1 再回傳）
```

### 比較運算子

```javascript
// 寬鬆比較（會做型別轉換）
5 == '5';    // true
0 == false;  // true
'' == false; // true

// 嚴格比較（不轉換型別）
5 === '5';   // false
0 === false; // false
null === null; // true

// 其他比較
5 != '5';    // false
5 !== '5';   // true
3 > 2;       // true
3 >= 3;      // true
```

### 邏輯運算子

```javascript
// &&（AND）：短路求值
true && false;   // false
true && true;    // true
'hello' && 42;   // 42（兩個都為 truthy，回傳最後一個）
null && 'ok';    // null（第一個 falsy，短路）

// ||（OR）：短路求值
false || true;   // true
false || 0;      // 0（兩個都 falsy，回傳最後一個）
'hello' || 'world'; // 'hello'（第一個 truthy，短路）

// ??（Nullish 合併，ES2020）
null ?? 'default';    // 'default'
undefined ?? 'default'; // 'default'
0 ?? 'default';       // 0（0 不是 nullish）
'' ?? 'default';      // ''（空字串不是 nullish）

// 可選鏈 ?.（ES2020）
const user = { profile: { name: 'Alice' } };
user?.profile?.name; // 'Alice'
user?.address?.city; // undefined（不會拋錯）
```

### 賦值運算子

```javascript
let x = 10;
x += 5;  // x = 15
x -= 3;  // x = 12
x *= 2;  // x = 24
x /= 4;  // x = 6
x **= 2; // x = 36（ES7）
x %= 5;  // x = 1

// 邏輯賦值運算子（ES2021）
let a = null;
a ||= 'default';   // a = 'default'（a 為 falsy 時賦值）
a &&= 'updated';   // a = 'updated'（a 為 truthy 時賦值）
a ??= 'fallback';  // a = 'fallback'（a 為 nullish 時賦值）
```

## 最佳實踐

1. **優先使用 const**，只在需要重新賦值時用 let
2. **永遠不要使用 var**
3. **使用嚴格比較（===、!==）**避免型別轉換陷阱
4. **使用可選鏈（?.）**代替繁複的 null 檢查
5. **使用 Nullish 合併（??）**代替 || 來處理預設值

---

**延伸閱讀**

- [MDN JavaScript 型別](https://www.google.com/search?q=MDN+JavaScript+types)
- [JavaScript 變數作用域](https://www.google.com/search?q=JavaScript+variable+scope)
- [比較運算子詳解](https://www.google.com/search?q=JavaScript+comparison+operators)
