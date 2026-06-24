# 陣列高階函數：map、filter、reduce

## 為什麼需要高階函數

傳統的 for 迴圈雖然功能強大，但存在可讀性差、容易出錯（索引越界）等問題。陣列高階函數用宣告式的方式描述「做什麼」，而非「怎麼做」：

```javascript
const numbers = [1, 2, 3, 4, 5];

// 命令式（Imperative）
const doubled1 = [];
for (let i = 0; i < numbers.length; i++) {
  doubled1.push(numbers[i] * 2);
}

// 宣告式（Declarative）
const doubled2 = numbers.map(n => n * 2);
```

## map：轉換每個元素

map 建立一個新陣列，對每個元素執行提供的函數：

```javascript
const numbers = [1, 2, 3, 4, 5];

// 基本用法
const squared = numbers.map(n => n * n);
// [1, 4, 9, 16, 25]

// 使用索引
const indexed = numbers.map((n, i) => `${i}: ${n}`);
// ['0: 1', '1: 2', '2: 3', '3: 4', '4: 5']

// 物件轉換
const users = [
  { firstName: 'Alice', lastName: 'Wang' },
  { firstName: 'Bob', lastName: 'Chen' }
];

const fullNames = users.map(u =>
  `${u.firstName} ${u.lastName}`
);
// ['Alice Wang', 'Bob Chen']

// 鏈式調用
const result = [1, 2, 3]
  .map(n => n * 2)
  .map(n => n + 1);
// [3, 5, 7]
```

## filter：過濾元素

filter 建立一個新陣列，只包含通過測試的元素：

```javascript
const numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];

// 基本用法
const evens = numbers.filter(n => n % 2 === 0);
// [2, 4, 6, 8, 10]

const bigNumbers = numbers.filter(n => n > 5);
// [6, 7, 8, 9, 10]

// 去除 falsy 值
const mixed = [0, 'hello', '', null, 42, undefined, false];
const truthy = mixed.filter(Boolean);
// ['hello', 42]

// 物件過濾
const products = [
  { name: 'iPhone', price: 30000, inStock: true },
  { name: 'iPad', price: 15000, inStock: false },
  { name: 'MacBook', price: 50000, inStock: true }
];

const inStock = products.filter(p => p.inStock);
const affordable = products.filter(p => p.price < 40000);
```

## reduce：歸納為單一值

reduce 是最強大的高階函數，可以實現 map 和 filter 的功能：

```javascript
const numbers = [1, 2, 3, 4, 5];

// 基本用法：加總
const sum = numbers.reduce((acc, n) => acc + n, 0);
// 15

// 找出最大值
const max = numbers.reduce((acc, n) =>
  n > acc ? n : acc, -Infinity
);
// 5

// 計算出現次數
const fruits = ['蘋果', '香蕉', '蘋果', '橘子', '香蕉', '蘋果'];
const count = fruits.reduce((acc, fruit) => {
  acc[fruit] = (acc[fruit] || 0) + 1;
  return acc;
}, {});
// { 蘋果: 3, 香蕉: 2, 橘子: 1 }

// 陣列扁平化
const nested = [[1, 2], [3, 4], [5, 6]];
const flat = nested.reduce((acc, arr) => [...acc, ...arr], []);
// [1, 2, 3, 4, 5, 6]

// 分組
const people = [
  { name: 'Alice', age: 25 },
  { name: 'Bob', age: 30 },
  { name: 'Charlie', age: 25 }
];

const groupedByAge = people.reduce((acc, person) => {
  const key = person.age;
  if (!acc[key]) acc[key] = [];
  acc[key].push(person);
  return acc;
}, {});
// { 25: [Alice, Charlie], 30: [Bob] }
```

## 實戰組合

### 資料處理管線

```javascript
const transactions = [
  { category: 'food', amount: 150, date: '2024-01-01' },
  { category: 'transport', amount: 50, date: '2024-01-02' },
  { category: 'food', amount: 200, date: '2024-01-03' },
  { category: 'entertainment', amount: 300, date: '2024-01-04' },
  { category: 'food', amount: 100, date: '2024-01-05' }
];

// 取得食品類的總花費
const foodTotal = transactions
  .filter(t => t.category === 'food')
  .map(t => t.amount)
  .reduce((sum, amount) => sum + amount, 0);
// 450

// 各類別花費統計
const categoryTotals = transactions
  .reduce((acc, { category, amount }) => {
    acc[category] = (acc[category] || 0) + amount;
    return acc;
  }, {});
// { food: 450, transport: 50, entertainment: 300 }
```

### 用 reduce 實現 map 和 filter

```javascript
// 自定義 map
function myMap(arr, fn) {
  return arr.reduce((acc, item, index) => {
    acc.push(fn(item, index));
    return acc;
  }, []);
}

// 自定義 filter
function myFilter(arr, fn) {
  return arr.reduce((acc, item, index) => {
    if (fn(item, index)) acc.push(item);
    return acc;
  }, []);
}
```

## 效能與注意事項

```javascript
// 避免過度鏈式調用
const data = [1, 2, 3, 4, 5];

// 每個方法都會建立新陣列，若資料量極大需注意
const result = data
  .filter(n => n > 2)     // 建立新陣列 [3, 4, 5]
  .map(n => n * 2)        // 建立新陣列 [6, 8, 10]
  .reduce((a, b) => a + b); // 單一值 24

// 改用 reduce 一次完成
const optimized = data.reduce((acc, n) => {
  if (n > 2) acc.push(n * 2);
  return acc;
}, []).reduce((a, b) => a + b);
```

## 結語

map、filter、reduce 是函數式程式設計的三大支柱。掌握它們不僅能寫出更簡潔的 JavaScript 程式碼，更是理解其他框架（如 React 的 JSX 渲染）的基礎。

---

**延伸閱讀**

- [MDN Array 方法](https://www.google.com/search?q=MDN+Array+methods)
- [JavaScript 函數式程式設計](https://www.google.com/search?q=functional+JavaScript+tutorial)
- [陣列方法大全](https://www.google.com/search?q=JavaScript+array+methods+guide)
