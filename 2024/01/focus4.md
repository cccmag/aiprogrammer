# 物件與陣列操作

## 物件字面語法

### 建立物件

物件是 JavaScript 中最基本的資料結構，使用鍵值對儲存資料：

```javascript
// 基本物件字面語法
const person = {
  name: 'Alice',
  age: 30,
  'full-name': 'Alice Wang',
  greet() {
    return `Hello, ${this.name}`;
  }
};

// 屬性縮寫（ES6）
const name = 'Bob';
const age = 25;
const user = { name, age }; // { name: 'Bob', age: 25 }

// 計算屬性名稱（ES6）
const dynamicKey = 'email';
const config = {
  [dynamicKey]: 'alice@example.com',
  [`get${dynamicKey.toUpperCase()}`]() {
    return this[dynamicKey];
  }
};
```

### 屬性存取

```javascript
const obj = { name: 'Alice', age: 30 };

// 點記法
obj.name; // 'Alice'

// 括號記法（可以用變數或特殊字元）
obj['age']; // 30
const key = 'name';
obj[key]; // 'Alice'
obj['full-name']; // 用點記法無法存取

// 刪除屬性
delete obj.age;
console.log(obj); // { name: 'Alice' }

// 檢查屬性是否存在
'name' in obj; // true
obj.hasOwnProperty('name'); // true
obj.toString !== undefined; // true（來自原型鏈）
```

### 物件方法

```javascript
const obj = { a: 1, b: 2, c: 3 };

// 取得鍵、值、條目
Object.keys(obj);   // ['a', 'b', 'c']
Object.values(obj); // [1, 2, 3]
Object.entries(obj); // [['a', 1], ['b', 2], ['c', 3]]

// 合併物件
const target = { a: 1 };
const source1 = { b: 2 };
const source2 = { c: 3 };
Object.assign(target, source1, source2);
// target: { a: 1, b: 2, c: 3 }

// 展開運算子（更現代的寫法）
const merged = { ...source1, ...source2 };
const clone = { ...obj };

// 凍結物件（不可變）
const frozen = Object.freeze({ x: 1 });
// frozen.x = 2; // 嚴格模式下會拋錯
```

## 陣列操作大全

### 建立與存取

```javascript
// 建立陣列
const arr1 = [1, 2, 3, 4, 5];
const arr2 = new Array(5); // 長度為 5 的空陣列
const arr3 = Array.from('hello'); // ['h', 'e', 'l', 'l', 'o']
const arr4 = Array.of(1, 2, 3); // [1, 2, 3]

// 存取元素
arr1[0]; // 1
arr1[arr1.length - 1]; // 5

// 新增/刪除元素
arr1.push(6);     // 尾部新增：[1,2,3,4,5,6]
arr1.pop();       // 尾部移除：[1,2,3,4,5]
arr1.unshift(0);  // 頭部新增：[0,1,2,3,4,5]
arr1.shift();     // 頭部移除：[1,2,3,4,5]
arr1.splice(2, 1); // 刪除索引 2 的元素
arr1.splice(2, 0, 'a'); // 在索引 2 插入
```

### 遍歷陣列

```javascript
const numbers = [1, 2, 3, 4, 5];

// forEach：遍歷
numbers.forEach(num => console.log(num));

// for...of：遍歷（ES6）
for (const num of numbers) {
  console.log(num);
}

// 傳統 for 迴圈
for (let i = 0; i < numbers.length; i++) {
  console.log(numbers[i]);
}
```

### 高階陣列方法

```javascript
const numbers = [1, 2, 3, 4, 5];

// map：轉換每個元素
const doubled = numbers.map(n => n * 2); // [2, 4, 6, 8, 10]

// filter：過濾元素
const evens = numbers.filter(n => n % 2 === 0); // [2, 4]

// reduce：歸納
const sum = numbers.reduce((acc, n) => acc + n, 0); // 15

// find：找第一個符合條件的元素
const firstEven = numbers.find(n => n % 2 === 0); // 2

// findIndex：找符合條件的索引
const firstEvenIndex = numbers.findIndex(n => n % 2 === 0); // 1

// some：是否有元素符合條件
numbers.some(n => n > 4); // true

// every：所有元素是否符合條件
numbers.every(n => n > 0); // true

// includes：是否包含特定值
numbers.includes(3); // true

// flat：扁平化巢狀陣列
[[1, 2], [3, [4]]].flat(2); // [1, 2, 3, 4]

// flatMap：map 後再 flat
['hello world', 'foo bar'].flatMap(s => s.split(' '));
// ['hello', 'world', 'foo', 'bar']
```

## 解構賦值

### 陣列解構

```javascript
const arr = [1, 2, 3, 4, 5];

// 基本解構
const [first, second] = arr;
// first = 1, second = 2

// 跳過元素
const [first, , third] = arr;
// first = 1, third = 3

// Rest 模式
const [head, ...tail] = arr;
// head = 1, tail = [2, 3, 4, 5]

// 預設值
const [a, b, c = 0] = [1, 2];
// a = 1, b = 2, c = 0

// 交換變數（經典用法）
let x = 1, y = 2;
[x, y] = [y, x];
// x = 2, y = 1
```

### 物件解構

```javascript
const user = {
  id: 1,
  name: 'Alice',
  email: 'alice@example.com',
  address: { city: 'Taipei', zip: '100' }
};

// 基本解構
const { name, email } = user;

// 重新命名
const { name: userName, email: userEmail } = user;

// 預設值
const { phone = 'N/A' } = user;

// 巢狀解構
const { address: { city } } = user;
// city = 'Taipei'

// Rest 屬性
const { id, ...rest } = user;
// rest = { name: 'Alice', email: 'alice@example.com', address: {...} }
```

### 函數參數解構

```javascript
// 參數解構非常實用
function createUser({ name, age, email = 'N/A' }) {
  return { name, age, email };
}

const user = createUser({
  name: 'Bob',
  age: 25,
  email: 'bob@example.com'
});
```

## 綜合範例

```javascript
// 一個完整的資料處理範例
const users = [
  { name: 'Alice', age: 28, active: true },
  { name: 'Bob', age: 22, active: false },
  { name: 'Charlie', age: 35, active: true },
  { name: 'David', age: 19, active: true },
];

// 取得所有活躍使用者的名稱（大寫）
const activeNames = users
  .filter(u => u.active)
  .map(u => u.name.toUpperCase());
// ['ALICE', 'CHARLIE', 'DAVID']

// 計算平均年齡
const averageAge = users
  .reduce((sum, u) => sum + u.age, 0) / users.length;
// 26
```

---

**延伸閱讀**

- [MDN 物件](https://www.google.com/search?q=MDN+JavaScript+objects)
- [MDN 陣列](https://www.google.com/search?q=MDN+JavaScript+arrays)
- [解構賦值](https://www.google.com/search?q=JavaScript+destructuring)
