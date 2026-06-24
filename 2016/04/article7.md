# 函式式 React：前端開發新範式

## React 的宣告式設計

React 是 Facebook 於 2013 年開源的前端框架，其核心思想與函式式程式設計高度吻合：

- **宣告式 UI**：描述「應該是什麼」，而非「如何變更」
- **元件是純函式**：相同輸入產生相同輸出
- **不可變狀態**：狀態更新創建新物件，而非修改

## JSX：語法擴展

JSX 允許你在 JavaScript 中編寫類似 HTML 的語法：

```jsx
// 宣告式元件
function Greeting({ name }) {
    return <div>Hello, {name}!</div>;
}

// 條件渲染
function Conditional({ show }) {
    return show && <div>Shown!</div>;
}

// 列表渲染
function List({ items }) {
    return (
        <ul>
            {items.map(item => (
                <li key={item.id}>{item.name}</li>
            ))}
        </ul>
    );
}
```

## 純元件

React 元件應該是純函式——相同的 props 產生相同的輸出：

```jsx
// 純元件：無副作用，只根據 props 渲染
function UserCard({ name, email, avatar }) {
    return (
        <div className="user-card">
            <img src={avatar} alt={name} />
            <h3>{name}</h3>
            <p>{email}</p>
        </div>
    );
}
```

## Redux：函式式狀態管理

Redux 是 React 生態中最流行的狀態管理庫，其設計完全遵循函式式原則：

### 三大原則

1. **單一真相來源**：整個應用的狀態存在單一 store
2. **狀態唯讀**：狀態只能透過 action 觸發變更
3. **純函式 Reducer**：Reducer 是純函式，接收舊狀態和 action，返回新狀態

### Reducer 是純函式

```javascript
// 純函式 Reducer
const todoApp = (state = { todos: [], filter: 'ALL' }, action) => {
    switch (action.type) {
        case 'ADD_TODO':
            return {
                ...state,  // 淺拷貝，不修改原狀態
                todos: [...state.todos, {
                    id: action.id,
                    text: action.text,
                    completed: false
                }]
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
};
```

### 不可變更新模式

```javascript
// 巢狀更新的不可變方式
const updateNestedState = (state, path, value) => {
    return {
        ...state,
        user: {
            ...state.user,
            profile: {
                ...state.user.profile,
                [path]: value
            }
        }
    };
};

// 使用 reduce 组合多個更新
const updatePath = (state, updates) =>
    updates.reduce((s, { path, value }) =>
        updateNestedState(s, path, value), state);
```

## 時間旅行調試

因為 Reducer 是純函式，Redux 可以儲存每個狀態的快照，實現時間旅行調試：

```javascript
// Redux DevTools 允许你：
// 1. 檢視每個 action 前後的狀態
// 2. 往前/往後跳轉到任意時間點
// 3. 重放任意時間點之後的所有 action
```

## React Hooks：函式式元件增強

React 16.8 引入的 Hooks 使得函式式元件更加強大：

```jsx
import { useState, useEffect, useMemo } from 'react';

// useState：狀態管理
function Counter() {
    const [count, setCount] = useState(0);
    return (
        <div>
            <p>Count: {count}</p>
            <button onClick={() => setCount(c => c + 1)}>Increment</button>
        </div>
    );
}

// useEffect：副作用（原 componentDidMount, componentDidUpdate）
function UserProfile({ userId }) {
    const [user, setUser] = useState(null);

    useEffect(() => {
        fetchUser(userId).then(setUser);
    }, [userId]);

    return user ? <div>{user.name}</div> : <div>Loading...</div>;
}

// useMemo：記憶化計算
function SortedList({ items, sortKey }) {
    const sorted = useMemo(
        () => items.sort((a, b) => a[sortKey] - b[sortKey]),
        [items, sortKey]
    );
    return sorted.map(item => <div key={item.id}>{item.name}</div>);
}
```

## 未來：React 的方向

React 持續演進，未來可能包括：

- **Concurrent Mode**：非阻塞渲染
- **Server Components**：服務端元件
- **Suspense**：更好的非同步載入體驗

延伸閱讀：
- [Google 搜尋：React functional components](https://www.google.com/search?q=React+functional+components)
- [Google 搜尋：Redux functional programming](https://www.google.com/search?q=Redux+functional+programming)