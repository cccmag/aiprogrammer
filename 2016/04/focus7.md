# 主題七：函式式反應式程式設計

## 什麼是 FRP？

函式式反應式程式設計（Functional Reactive Programming，FRP）是一種處理**隨時間變化的值**的宣告式方法。在 FRP 中，你不是寫「當 X 發生時，更新 Y」，而是定義「Y 表達式是 Z 隨著時間的變化」。

傳統的命令式方式：

```javascript
// 命令式：手動管理狀態和更新
let result = 0;
let inputValue = 0;

input.addEventListener('change', (e) => {
    inputValue = parseInt(e.target.value);
    result = inputValue * 2;
    display.textContent = result;
});
```

FRP 方式：

```javascript
// 宣告式：表達值之間的關係
const inputValue$ = fromEvent(input, 'change')
    .map(e => parseInt(e.target.value));

const result$ = inputValue$.map(x => x * 2);

result$.subscribe(value => {
    display.textContent = value;
});
```

## 核心概念

### Observable（可觀察對象）

Observable 是一個隨時間發送值的來源。它類似於一個時間序列，可以被訂閱和處理。

```javascript
// 從事件創建 Observable
const clicks$ = fromEvent(button, 'click');

// 從計時器創建 Observable
const interval$ = interval(1000);

// 從陣列創建 Observable（立即發送所有值然後完成）
const numbers$ = from([1, 2, 3, 4, 5]);
```

### 運算子（Operators）

Observable 提供豐富的運算子來轉換和組合流：

```javascript
// map：轉換每個值
const squares$ = numbers$.pipe(map(x => x * x));

// filter：只允許滿足條件的值通過
const evens$ = numbers$.pipe(filter(x => x % 2 === 0));

// debounceTime：降低更新頻率
const searchInput$ = fromEvent(searchInput, 'input').pipe(
    debounceTime(300),
    map(e => e.target.value)
);

// switchMap：取消前一個 Observable，切換到新的
const result$ = searchInput$.pipe(
    switchMap(query => searchAPI(query))
);
```

### 組合多個 Observable

```javascript
// 合併多個流
const combined$ = combineLatest(
    name$.pipe(startWith('')),
    email$.pipe(startWith(''))
).pipe(
    map(([name, email]) => ({ name, email, valid: name && email }))
);

// 等待所有 Observable 完成
const result$ = forkJoin({
    user: fetchUser(),
    posts: fetchPosts()
}).pipe(
    map(({ user, posts }) => ({ user, postCount: posts.length }))
);
```

## RxJS：JavaScript 的 FRP 庫

RxJS 是最受歡迎的 JavaScript FRP 庫，Angular 2 採用它作為內建的響應式程式庫。

### 基本使用

```javascript
import { fromEvent, interval } from 'rxjs';
import { map, filter, take, reduce } from 'rxjs/operators';

// 從 DOM 事件創建 Observable
const clicks$ = fromEvent(document, 'click');

// 轉換和處理
const coordinate$ = clicks$.pipe(
    map(click => ({ x: click.clientX, y: click.clientY })),
    take(5)  // 只取前 5 個
);

// 訂閱
clicks$.subscribe({
    next: pos => console.log(`Clicked at ${pos.x}, ${pos.y}`),
    complete: () => console.log('Done!'),
    error: err => console.error(err)
});
```

### 實際應用：自動完成搜索

```javascript
import { fromEvent } from 'rxjs';
import { debounceTime, distinctUntilChanged, switchMap, map } from 'rxjs/operators';

const searchInput = document.querySelector('#search');
const results = document.querySelector('#results');

fromEvent(searchInput, 'input').pipe(
    map(e => e.target.value),           // 提取輸入值
    filter(text => text.length >= 2),    // 至少 2 個字元
    debounceTime(300),                  // 等待 300ms
    distinctUntilChanged(),             // 避免重複請求
    switchMap(query => fetch(`/api/search?q=${query}`)),  // 取消舊請求
    map(response => response.json())
).subscribe(data => {
    results.innerHTML = renderResults(data);
});
```

## React 與 Redux：前端的 FRP 思想

雖然 Redux 不是嚴格意義上的 FRP，但它體現了函式式反應式程式的核心思想：

### 單向資料流

```
Action → Dispatcher → Store → View
              ↑                    |
              └────────────────────┘
```

### Reducer：純函式

```javascript
// Reducer 是純函式，接收舊狀態和 action，返回新狀態
function todoApp(state = { todos: [], visibilityFilter: 'SHOW_ALL' }, action) {
    switch (action.type) {
        case 'ADD_TODO':
            return {
                ...state,
                todos: [
                    ...state.todos,
                    {
                        id: action.id,
                        text: action.text,
                        completed: false
                    }
                ]
            };
        case 'TOGGLE_TODO':
            return {
                ...state,
                todos: state.todos.map(todo =>
                    todo.id === action.id
                        ? { ...todo, completed: !todo.completed }
                        : todo
                )
            };
        default:
            return state;
    }
}
```

### 時間旅行調試

因為 Reducer 是純函式， Redux 可以記錄每次狀態變更，實現時間旅行調試——你可以往前或往後檢視應用程式狀態。

## Cycle.js：真正的 FRP 前端框架

Cycle.js 是一個完全基於 FRP 理念的前端框架：

```javascript
import { run } from '@cycle/core';
import { div, label, input, p } from '@cycle/dom';

function main(sources) {
    const name$ = sources.DOM.select('.name').events('input')
        .map(e => e.target.value)
        .startWith('');

    const vtree$ = name$.map(name =>
        div([
            label('Name:'),
            input('.name', { type: 'text' }),
            p(`Hello, ${name || 'World'}!`)
        ])
    );

    return {
        DOM: vtree$
    };
}

run(main, {
    DOM: makeDOMDriver('#app')
});
```

## Bacon.js：另一個 FRP 庫

Bacon.js 提供類似 RxJS 的功能性響應式程式設計：

```javascript
import * as Bacon from 'baconjs';

const name = Bacon.fromEvent(document.querySelector('#name'), 'input')
    .map(e => e.target.value)
    .startWith('');

const email = Bacon.fromEvent(document.querySelector('#email'), 'input')
    .map(e => e.target.value)
    .startWith('');

const submit = Bacon.fromEvent(document.querySelector('#submit'), 'click');

const formData = Bacon.combineWith({ name, email }, (n, e) => ({ name: n, email: e }));

const validSubmit = submit.sampledBy(formData).filter(form => form.name && form.email);

// 處理提交
validSubmit.onValue(form => console.log('Submit:', form));
```

## 未來趨勢：Async/Await 與 FRP 的融合

ES2017 引入的 async/await 為非同步程式設計帶來了更簡潔的語法：

```javascript
// async/await 讓非同步程式看起來像同步
async function search(query) {
    const response = await fetch(`/api/search?q=${query}`);
    const data = await response.json();
    return data;
}

// 結合 FRP 運算子
const results$ = fromEvent(searchInput, 'input').pipe(
    debounceTime(300),
    distinctUntilChanged(),
    switchMap(query => from(search(query)))
);
```

## 小結

函式式反應式程式設計（FRP）提供了一種優雅的方式來處理隨時間變化的資料和事件。透過宣告式而非命令式的表達，我們可以：

- 更清晰地表達資料之間的關係
- 更容易組合和轉換事件流
- 更好地處理非同步和並發
- 實現時間旅行調試等強大功能

從 RxJS 到 Redux，從 Cycle.js 到 Bacon.js，FRP 的思想已經深刻影響了現代前端開發。理解這些概念，將使你成為更優秀的開發者。