# 函數式程式設計興起

## 為什麼函數式？

2015 年，函數式程式設計概念在主流語言中迅速普及：

- **React/Redux**：前端函數式
- **Lambdas**：Java 8、Python
- **RxJS**：響應式程式設計

## 核心概念

### 不可變性

```javascript
// 不好：可變狀態
const user = { name: 'John' };
user.name = 'Jane';

// 好：不可變更新
const user = { name: 'John' };
const updatedUser = { ...user, name: 'Jane' };
```

### 高階函數

```javascript
// 陣列操作
const numbers = [1, 2, 3, 4, 5];

const doubled = numbers.map(n => n * 2);
const evens = numbers.filter(n => n % 2 === 0);
const sum = numbers.reduce((acc, n) => acc + n, 0);
```

### 組合

```javascript
// 函數組合
const compose = (f, g) => x => f(g(x));
const toUpperCase = s => s.toUpperCase();
const addExclamation = s => s + '!';

const shout = compose(addExclamation, toUpperCase);
shout('hello');  // 'HELLO!'
```

## 在 React 中的應用

```javascript
// Redux 的函數式思想
const reducer = (state, action) => {
  switch (action.type) {
    case 'ADD':
      return [...state, action.payload];
    case 'REMOVE':
      return state.filter((_, i) => i !== action.payload);
    default:
      return state;
  }
};
```

## 響應式程式設計

```javascript
// RxJS
const { fromEvent } = require('rxjs');
const { debounceTime, distinctUntilChanged } = require('rxjs/operators');

fromEvent(input, 'input').pipe(
  debounceTime(300),
  distinctUntilChanged()
).subscribe(value => {
  console.log(value);
});
```

## 小結

函數式程式設計提高了程式碼的可測試性和可維護性。

---

## 延伸閱讀

- [Functional Programming Guide](https://www.google.com/search?q=functional+programming+javascript+guide)
- [Redux Guide](https://www.google.com/search?q=Redux+functional+programming)