# 狀態管理：useState

## React 的狀態哲學

在前端應用中，「狀態」指的是隨著時間變化的資料。使用者的輸入、伺服器回應、介面的開關狀態——這些都是狀態。

React 的核心哲學之一是 UI 是狀態的函式：`UI = f(state)`。當狀態改變時，UI 自動重新渲染，開發者不需要手動操作 DOM。

## useState 的基本用法

`useState` 是 React 中最基本的 Hook，用於在函式元件中宣告狀態變數：

```javascript
import { useState } from 'react'

function Counter() {
  const [count, setCount] = useState(0)
  
  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount(count + 1)}>+1</button>
    </div>
  )
}
```

`useState` 接受一個初始值作為參數，回傳一個陣列，包含當前狀態值和更新該狀態的函式。

## 狀態的非同步更新

React 的狀態更新是非同步的。當你呼叫 `setState` 時，React 會將更新加入佇列，並在後續的 re-render 中處理：

```javascript
function AsyncExample() {
  const [count, setCount] = useState(0)
  
  function handleClick() {
    setCount(count + 1)
    console.log(count) // 仍然是舊值
    setCount(count + 1)
    console.log(count) // 仍然是舊值，兩次設定結果只 +1
  }
  
  return <button onClick={handleClick}>{count}</button>
}
```

如果需要基於前一個狀態來更新，應該使用函式形式的 `setState`：

```javascript
function handleClick() {
  setCount(prev => prev + 1)
  setCount(prev => prev + 1) // 現在會正確地 +2
}
```

## 多個狀態變數

同一個元件可以有多個狀態變數：

```javascript
function Form() {
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [age, setAge] = useState(0)
  
  return (
    <form>
      <input value={name} onChange={e => setName(e.target.value)} />
      <input value={email} onChange={e => setEmail(e.target.value)} />
      <input type="number" value={age} onChange={e => setAge(Number(e.target.value))} />
    </form>
  )
}
```

## 使用物件狀態

當狀態是物件時，更新時必須遵守不可變性原則：

```javascript
function UserProfile() {
  const [user, setUser] = useState({ name: '', age: 0, email: '' })
  
  function updateName(name) {
    // 錯誤：直接修改物件
    // user.name = name
    
    // 正確：建立新物件
    setUser({ ...user, name })
  }
  
  return (
    <div>
      <p>{user.name}, {user.age}</p>
      <input value={user.name} onChange={e => updateName(e.target.value)} />
    </div>
  )
}
```

展開運算子 `...` 是建立物件拷貝的常用方式，但如果巢狀層次較深，可以考慮使用 Immer 套件。

## 狀態提升

當多個元件需要共享同一份狀態時，可以將狀態提升到它們的共同父元件：

```javascript
function Parent() {
  const [sharedValue, setSharedValue] = useState('')
  
  return (
    <div>
      <ChildA value={sharedValue} onChange={setSharedValue} />
      <ChildB value={sharedValue} />
    </div>
  )
}
```

這就是 React 單向資料流的體現：狀態由父元件管理，透過 props 傳遞給子元件。

## 常見陷阱

### 初始值為函式

如果初始值需要經過複雜計算，應該傳入一個函式而非直接執行計算：

```javascript
// 不好：每次渲染都執行一次計算
const [data] = useState(expensiveComputation())

// 好：只在初始渲染時執行一次
const [data] = useState(() => expensiveComputation())
```

### State 與 Props 的區別

State 是元件內部的資料，由元件自己管理；Props 是從父元件傳入的資料，子元件不能修改。

## 結語

useState 是 React Hooks 的基礎，也是最常使用的 Hook。掌握了 useState，就掌握了 React 狀態管理的根本。記住不可變性、非同步更新和狀態提升這三個關鍵概念，就能寫出可靠的 React 元件。

---

## 延伸閱讀

- [React useState 文件](https://www.google.com/search?q=React+useState+documentation)
- [React 狀態管理哲學](https://www.google.com/search?q=React+state+management+philosophy)
- [React 不可變性](https://www.google.com/search?q=React+immutability+state)

---

*本篇文章為「AI 程式人雜誌 2024 年 4 月號」焦點系列之三。*
