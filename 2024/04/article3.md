# 函式元件 vs 類別元件

## 前言

React 從一開始就支援兩種定義元件的方式：類別元件和函式元件。在 React 16.8 引入 Hooks 之前，類別元件是唯一能夠管理狀態和使用生命週期的方式。而現在，函式元件加上 Hooks 已經成為官方推薦的寫法。

## 類別元件

類別元件是 ES6 class，繼承自 `React.Component`：

```jsx
class Counter extends React.Component {
  constructor(props) {
    super(props)
    this.state = { count: 0 }
  }
  
  componentDidMount() {
    document.title = `Count: ${this.state.count}`
  }
  
  componentDidUpdate() {
    document.title = `Count: ${this.state.count}`
  }
  
  componentWillUnmount() {
    document.title = 'Goodbye'
  }
  
  render() {
    return (
      <div>
        <p>{this.state.count}</p>
        <button onClick={() => this.setState({ count: this.state.count + 1 })}>
          +1
        </button>
      </div>
    )
  }
}
```

類別元件使用 `this.state` 存取狀態、`this.setState` 更新狀態，並透過生命週期方法（`componentDidMount` 等）管理副作用。

## 同等功能的函式元件

使用 Hooks 後，相同的功能可以用更簡潔的方式實現：

```jsx
function Counter() {
  const [count, setCount] = useState(0)
  
  useEffect(() => {
    document.title = `Count: ${count}`
    return () => { document.title = 'Goodbye' }
  }, [count])

  return (
    <div>
      <p>{count}</p>
      <button onClick={() => setCount(c => c + 1)}>
        +1
      </button>
    </div>
  )
}
```

## 主要差異對比

### 程式碼簡潔度

類別元件需要更多的樣板程式碼：constructor、`this` 綁定、生命週期方法。函式元件則更加直觀。

### this 綁定

類別元件中的 `this` 常造成混淆：

```jsx
class Button extends React.Component {
  // 需要綁定 this
  handleClick = () => {
    this.setState({ clicked: true })
  }
  
  // 或在 constructor 中綁定
  constructor(props) {
    super(props)
    this.handleClick = this.handleClick.bind(this)
  }
}
```

函式元件沒有 `this` 問題，每次渲染都透過閉包捕獲當前 props 和 state。

### 生命週期 vs Hooks

類別元件用多個方法管理生命週期，而 Hooks 用更語義化的方式組合：

| 生命週期方法 | Hooks 對應 |
|------------|-----------|
| componentDidMount | useEffect(fn, []) |
| componentDidUpdate | useEffect(fn, [deps]) |
| componentWillUnmount | useEffect(() => fn, []) 的 cleanup |
| shouldComponentUpdate | React.memo |
| getDerivedStateFromProps | useMemo |

### 程式碼複用

類別元件的邏輯複用依賴 Higher-Order Components（HOC）或 Render Props，會導致巢狀地獄（Wrapper Hell）：

```jsx
// HOC 巢狀
export default withAuth(withRouter(withTheme(MyComponent)))

// Render Props 巢狀
<AuthProvider>
  {auth => (
    <Router>
      {router => (
        <ThemeProvider>
          {theme => <Content ... />}
        </ThemeProvider>
      )}
    </Router>
  )}
</AuthProvider>
```

而 Hooks 的複用方式更簡單：

```jsx
function MyComponent() {
  const { user } = useAuth()
  const { theme } = useTheme()
  const { pathname } = useLocation()
  // ...
}
```

## 函式元件的優勢

1. **更少的程式碼**：減少樣板程式碼約 30-50%
2. **更好的可讀性**：邏輯按功能組織，而非生命週期
3. **沒有 this 困擾**：閉包比 class 的 this 更可預測
4. **邏輯複用**：自訂 Hooks 比 HOC 更簡潔
5. **編譯器優化**：未來 React 編譯器對函式元件的優化空間更大

## 類別元件的適用場景

雖然 Hooks 是未來，但仍有保留類別元件的理由：

- **既有專案**：大型專案全面遷移成本過高
- **Error Boundary**：目前只能用 class 元件實作
- **getSnapshotBeforeUpdate**：某些底層場景需要

```jsx
class ErrorBoundary extends React.Component {
  state = { hasError: false }
  
  static getDerivedStateFromError() {
    return { hasError: true }
  }
  
  componentDidCatch(error, info) {
    logError(error, info)
  }
  
  render() {
    if (this.state.hasError) {
      return this.props.fallback
    }
    return this.props.children
  }
}
```

## 遷移策略

既有類別元件的遷移建議：

1. **新元件一律使用函式元件**
2. **逐步重構**：從簡單的類別元件開始
3. **一次一個 Hook**：逐步用 useEffect 取代生命週期方法
4. **使用 codemod**：社群提供自動遷移工具

## 結語

函式元件搭配 Hooks 是 React 的現在和未來。如果你還在寫類別元件，建議在新專案中開始使用函式元件；既有專案則根據實際情況逐步遷移。

---

## 延伸閱讀

- [React Hooks 官方文件](https://www.google.com/search?q=React+Hooks+documentation)
- [從 class 遷移到 hooks](https://www.google.com/search?q=migrate+from+class+to+hooks+React)
- [Hooks 常見問題](https://www.google.com/search?q=React+Hooks+FAQ)

---

*本篇文章為「AI 程式人雜誌 2024 年 4 月號」精選文章之三。*
