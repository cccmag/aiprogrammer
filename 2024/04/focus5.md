# 元件間通訊：props 與 context

## Props 的單向資料流

在 React 中，資料從父元件流向子元件——這就是單向資料流。父元件透過 `props`（properties 的簡稱）將資料傳遞給子元件：

```jsx
function Parent() {
  const user = { name: 'Alice', age: 25 }
  return <Child name={user.name} age={user.age} />
}

function Child({ name, age }) {
  return <p>{name} is {age} years old</p>
}
```

Props 是唯讀的，子元件不應該直接修改 props。如果要改變資料，必須從父元件更新狀態。

## Props 的預設值與驗證

可以為 props 設定預設值，確保元件在缺少某些 prop 時仍能正常運作：

```jsx
function Button({ label, variant = 'primary', disabled = false }) {
  return (
    <button className={`btn btn-${variant}`} disabled={disabled}>
      {label}
    </button>
  )
}
```

在開發階段也可以使用 PropTypes 進行型別驗證：

```javascript
import PropTypes from 'prop-types'

Button.propTypes = {
  label: PropTypes.string.isRequired,
  variant: PropTypes.oneOf(['primary', 'secondary', 'danger']),
  disabled: PropTypes.bool,
}
```

## Props Drilling 問題

當元件樹很深時，從頂層元件傳遞資料到深層元件需要經過多層中間元件，這就是 Props Drilling：

```jsx
function App() {
  const [user, setUser] = useState(null)
  return <Header user={user} setUser={setUser} />
}

function Header({ user, setUser }) {
  return <nav><UserMenu user={user} setUser={setUser} /></nav>
}

function UserMenu({ user, setUser }) {
  return <Avatar user={user} setUser={setUser} />
}
```

中間的 Header 元件本身不需要 user 資料，但為了傳遞給子元件，不得不接收這些 props。這會導致耦合度增加和程式碼冗餘。

## Context API 解決方案

Context API 是 React 內建的全域狀態管理方案，可以避免 Props Drilling：

```jsx
import { createContext, useContext } from 'react'

// 1. 建立 Context
const AuthContext = createContext(null)

// 2. Provider 提供資料
function App() {
  const [user, setUser] = useState(null)
  
  return (
    <AuthContext.Provider value={{ user, setUser }}>
      <Header />
      <MainContent />
    </AuthContext.Provider>
  )
}

// 3. Consumer 消費資料
function Avatar() {
  const { user, setUser } = useContext(AuthContext)
  
  if (!user) return <LoginButton onLogin={setUser} />
  return <UserProfile user={user} />
}
```

直接使用 `useContext` Hook 讀取 context 的值，比傳統的 `Context.Consumer` 寫法更簡潔。

## Context 的效能注意事項

使用 Context 時需要注意：

```jsx
function App() {
  const [user, setUser] = useState(null)
  
  // 每次 App 重新渲染，都會建立新的物件
  return (
    <AuthContext.Provider value={{ user, setUser }}>
      <HeavyComponent />
    </AuthContext.Provider>
  )
}
```

當 Provider 的 value 變化時，所有消費該 Context 的元件都會重新渲染。可以使用 `useMemo` 來優化：

```jsx
const value = useMemo(() => ({ user, setUser }), [user])

return (
  <AuthContext.Provider value={value}>
    <HeavyComponent />
  </AuthContext.Provider>
)
```

## 組合（Composition）模式

有時候，元件間通訊最好的方式不是 props 或 context，而是組合：

```jsx
function Layout({ sidebar, main }) {
  return (
    <div className="layout">
      <aside>{sidebar}</aside>
      <main>{main}</main>
    </div>
  )
}

function App() {
  return (
    <Layout
      sidebar={<Sidebar />}
      main={<MainContent />}
    />
  )
}
```

這種模式讓 Layout 元件不需要關心其內容的具體實現，減少了 props 的傳遞。

## Context vs Redux

當應用規模增大時，開發者常面臨 Context 和 Redux 的選擇：

- **Context**：React 內建、輕量、適合中等規模的狀態共享
- **Redux**：功能完整、中樞式 store、適合大型應用的狀態管理

## 結語

React 的元件間通訊遵循從簡單到複雜的策略：優先使用 props，遇到 Props Drilling 時使用 Context，對於大型應用則考慮 Redux 等外部狀態管理方案。

---

## 延伸閱讀

- [React Context API 文件](https://www.google.com/search?q=React+Context+API+documentation)
- [Props Drilling vs Context](https://www.google.com/search?q=Props+drilling+vs+Context+API)
- [React 組合模式](https://www.google.com/search?q=React+composition+pattern)

---

*本篇文章為「AI 程式人雜誌 2024 年 4 月號」焦點系列之五。*
