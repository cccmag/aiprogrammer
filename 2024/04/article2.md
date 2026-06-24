# JSX 語法深入

## 前言

JSX 是 React 的語法糖，表面上寫起來像 HTML，但實際上它經過 Babel 編譯後變成 JavaScript 函式呼叫。理解 JSX 的底層機制，有助於寫出更高效、更安全的程式碼。

## JSX 的編譯過程

當你寫下這段 JSX：

```jsx
const element = (
  <div className="container">
    <h1>Hello</h1>
    <p>World</p>
  </div>
)
```

Babel 會將它編譯為：

```javascript
const element = React.createElement(
  'div',
  { className: 'container' },
  React.createElement('h1', null, 'Hello'),
  React.createElement('p', null, 'World')
)
```

而 `React.createElement` 回傳的是這樣一個物件：

```javascript
{
  type: 'div',
  props: {
    className: 'container',
    children: [
      { type: 'h1', props: { children: 'Hello' } },
      { type: 'p', props: { children: 'World' } },
    ]
  }
}
```

這就是 Virtual DOM 節點的本質——一個描述 UI 的普通 JavaScript 物件。

## 沒有 React 的 JSX

在 React 17+ 中，引入了新的 JSX 轉換方式，不再需要在檔案頂部 `import React`：

```jsx
// React 17 之前：需要 import React
import React from 'react'

// React 17+：自動從 react/jsx-runtime 引入
function App() {
  return <h1>Hello</h1>
}
```

這是由 Babel 的 `@babel/plugin-transform-react-jsx` 和 TypeScript 4.0+ 從底層支援的。

## JSX 中的表達式

JSX 的大括弧可以嵌入任何 JavaScript 表達式：

```jsx
function Welcome({ user, items }) {
  const now = new Date()
  
  return (
    <div>
      <h1>{user.name.toUpperCase()}</h1>
      <p>{items.length > 0 ? 'Has items' : 'Empty'}</p>
      <p>Time: {now.toLocaleString()}</p>
      <p>Sum: {items.reduce((a, b) => a + b.value, 0)}</p>
    </div>
  )
}
```

但不能使用 `if/else`、`for` 迴圈等語句——這些不是表達式，不會回傳值。

## JSX 的條件渲染

### 三元運算子

```jsx
function Status({ isLoading, error }) {
  return (
    <div>
      {isLoading ? <Spinner /> :
       error ? <ErrorMsg message={error} /> :
       <Content />}
    </div>
  )
}
```

### 邏輯 AND 運算子

```jsx
function Notification({ message }) {
  return (
    <div>
      {message && <Alert text={message} />}
    </div>
  )
}
```

注意：`0 && <Component />` 會渲染出 `0`，因為 JavaScript 會回傳 falsy 值本身。

### IIFE（立即執行函式）

```jsx
function ComplexCondition({ user, role }) {
  return (
    <div>
      {(() => {
        if (role === 'admin') return <AdminPanel user={user} />
        if (role === 'editor') return <EditorPanel user={user} />
        return <ViewerPanel user={user} />
      })()}
    </div>
  )
}
```

## JSX 中的列表渲染

```jsx
function ItemList({ items }) {
  return (
    <ul>
      {items.map((item, index) => (
        <li key={item.id || index}>
          {item.name}
        </li>
      ))}
    </ul>
  )
}
```

Key 的選擇非常重要：

- 優先使用唯一 ID：`key={item.id}`
- 避免使用索引：除非列表靜態且不會重新排序
- 確保 key 在同層兄弟間唯一

## JSX 中的 Fragment

`<></>` 是 `React.Fragment` 的簡寫，用於分組多個元素而不新增額外 DOM 節點：

```jsx
function Table() {
  return (
    <table>
      <tbody>
        <tr>
          <>
            <td>Cell 1</td>
            <td>Cell 2</td>
          </>
        </tr>
      </tbody>
    </table>
  )
}
```

Fragment 可以接受 `key` 屬性，但簡寫語法不支援。

## Props Spread

可以使用展開運算子將物件作為 props 傳遞：

```jsx
function App() {
  const userProps = { name: 'Alice', age: 25, role: 'admin' }
  
  return <UserCard {...userProps} />
}
```

但要小心：過度使用 Props Spread 會讓程式碼難以追蹤。

## JSX 的潛在危險

### XSS 防護

React 會自動對 JSX 內容進行跳脫（escape），防止 XSS 攻擊：

```jsx
const userContent = '<img onerror="stealCookies()" src="x" />'

// React 會將其渲染為文字，而非 HTML
<div>{userContent}</div>
```

但使用 `dangerouslySetInnerHTML` 時要格外小心：

```jsx
<div dangerouslySetInnerHTML={{ __html: sanitize(userContent) }} />
```

## 結語

JSX 看似簡單，但其底層的編譯機制、表達式處理和安全性設計都值得深入了解。掌握 JSX 的進階用法，能夠寫出更優雅、更安全的 React 程式碼。

---

## 延伸閱讀

- [JSX 深入指南](https://www.google.com/search?q=React+JSX+in+depth)
- [JSX 編譯原理](https://www.google.com/search?q=how+does+Babel+compile+JSX)
- [React 條件渲染模式](https://www.google.com/search?q=React+conditional+rendering+patterns)

---

*本篇文章為「AI 程式人雜誌 2024 年 4 月號」精選文章之二。*
