# React 核心概念：元件與 JSX

## 元件化思想

React 的核心是「元件化」——將使用者介面拆解為獨立、可復用的小區塊。每個元件封裝了自己的結構、樣式和行為，開發者像堆積木一樣組裝出完整的頁面。

元件化的好處：

- **可復用**：同一個元件可以在多個地方使用
- **可維護**：每個元件的程式碼量小，易於理解和修改
- **可組合**：小元件可以組成更大的元件
- **獨立性**：元件之間低耦合、高內聚

```jsx
// 導航列元件
function Navbar() {
  return (
    <nav>
      <Logo />
      <MenuItems />
      <UserAvatar />
    </nav>
  )
}
```

## 什麼是 JSX

JSX（JavaScript XML）是 React 的一個語法擴展，讓開發者可以在 JavaScript 中直接撰寫類似 HTML 的標記語言。JSX 不是模板引擎——它會被編譯為 JavaScript 函式呼叫。

```jsx
const element = <h1>Hello, World!</h1>
```

經過 Babel 編譯後，上面的 JSX 程式碼會變成：

```javascript
const element = React.createElement('h1', null, 'Hello, World!')
```

而 `createElement` 函式的回傳值是一個普通的 JavaScript 物件——這就是 Virtual DOM 的節點。

## JSX 的基本規則

使用 JSX 時有幾個重要的規則需要遵守：

### 單一根元素

JSX 表達式必須有單一根元素。如果不想多餘的 DOM 節點，可以使用 Fragment：

```jsx
function App() {
  return (
    <>
      <h1>Title</h1>
      <p>Content</p>
    </>
  )
}
```

### JavaScript 表達式

在 JSX 中使用大括弧嵌入 JavaScript 表達式：

```jsx
function Greeting({ name, age }) {
  return (
    <div>
      <p>Hello, {name.toUpperCase()}!</p>
      <p>Next year you'll be {age + 1}</p>
    </div>
  )
}
```

### 屬性使用 camelCase

JSX 中的 HTML 屬性使用 JavaScript 的命名慣例（camelCase）：

```jsx
// HTML: class, onclick, tabindex
// JSX: className, onClick, tabIndex

<button className="btn" onClick={handleClick} tabIndex={0}>
  Click me
</button>
```

### 條件渲染

JSX 支援多種條件渲染方式：

```jsx
function Status({ isLoggedIn }) {
  return (
    <div>
      {isLoggedIn ? <UserPanel /> : <LoginButton />}
      {isLoggedIn && <Dashboard />}
    </div>
  )
}
```

### 列表渲染

渲染列表時需要提供唯一的 key 屬性：

```jsx
function TodoList({ items }) {
  return (
    <ul>
      {items.map(item => (
        <li key={item.id}>{item.text}</li>
      ))}
    </ul>
  )
}
```

## 宣告式 UI

React 的關鍵創新在於宣告式 UI。傳統的命令式程式碼需要詳細描述每一步操作：

```javascript
// 命令式
const app = document.getElementById('app')
const h1 = document.createElement('h1')
h1.textContent = 'Hello'
app.appendChild(h1)
```

而在 React 中，開發者只需宣告 UI 應該如何呈現：

```jsx
// 宣告式
function App() {
  return <h1>Hello</h1>
}
```

當狀態發生變化時，React 自動計算出需要更新的部分，並套用到真實 DOM。

## 元件類型

React 中有兩種定義元件的方式：函式元件和類別元件。在 React 16.8 引入 Hooks 後，函式元件成為主流。

```jsx
// 函式元件（現代寫法）
function Welcome({ name }) {
  return <h1>Hello, {name}</h1>
}

// 類別元件（傳統寫法）
class Welcome extends React.Component {
  render() {
    return <h1>Hello, {this.props.name}</h1>
  }
}
```

## 結語

元件與 JSX 是 React 的兩大基石。元件化思想讓 UI 開發變得有條理、可維護，而 JSX 提供了一種直覺的方式來描述 UI 結構。理解了這兩個概念，就掌握了 React 的第一把鑰匙。

---

## 延伸閱讀

- [React JSX 完整介紹](https://www.google.com/search?q=React+JSX+introduction)
- [React 元件與 Props](https://www.google.com/search?q=React+components+and+props)
- [JSX 原理與編譯](https://www.google.com/search?q=how+JSX+works+React)

---

*本篇文章為「AI 程式人雜誌 2024 年 4 月號」焦點系列之二。*
