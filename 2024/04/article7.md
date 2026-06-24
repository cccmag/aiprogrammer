# Context API 與全域狀態

## 前言

當 React 應用的規模成長到一定程度，元件間的狀態共享成為一個必須面對的問題。Props Drilling 讓程式碼變得冗長，而全域狀態管理方案則提供了更優雅的解決方案。Context API 是 React 內建的全域狀態方案，簡單而強大。

## Context API 的核心

Context API 由三個部分組成：

1. **createContext**：建立一個 Context 物件
2. **Provider**：提供資料給所有子元件
3. **useContext**：消費 Context 中的資料

```jsx
import { createContext, useContext, useState } from 'react'

// 1. 建立 Context
const ThemeContext = createContext('light')

// 2. Provider
function App() {
  const [theme, setTheme] = useState('light')
  
  return (
    <ThemeContext.Provider value={{ theme, setTheme }}>
      <Header />
      <MainContent />
      <Footer />
    </ThemeContext.Provider>
  )
}

// 3. Consumer（使用 useContext）
function Header() {
  const { theme, setTheme } = useContext(ThemeContext)
  
  return (
    <header className={`header-${theme}`}>
      <button onClick={() => setTheme(t => t === 'light' ? 'dark' : 'light')}>
        Toggle Theme
      </button>
    </header>
  )
}
```

## 多個 Context

一個應用可能有多個全域狀態，建議將它們拆分為不同的 Context：

```jsx
function App({ children }) {
  return (
    <AuthProvider>
      <ThemeProvider>
        <NotificationProvider>
          {children}
        </NotificationProvider>
      </ThemeProvider>
    </AuthProvider>
  )
}
```

這樣做的好處是：每個 Context 的更新只會觸發消費該 Context 的元件重新渲染。

## Context + useReducer

對於複雜的狀態邏輯，可以搭配 `useReducer`：

```jsx
import { createContext, useContext, useReducer } from 'react'

const AuthContext = createContext(null)
const AuthDispatchContext = createContext(null)

function authReducer(state, action) {
  switch (action.type) {
    case 'LOGIN':
      return { ...state, user: action.user, isAuthenticated: true }
    case 'LOGOUT':
      return { ...state, user: null, isAuthenticated: false }
    case 'SET_LOADING':
      return { ...state, loading: action.loading }
    default:
      return state
  }
}

function AuthProvider({ children }) {
  const [state, dispatch] = useReducer(authReducer, {
    user: null,
    isAuthenticated: false,
    loading: false,
  })
  
  return (
    <AuthContext.Provider value={state}>
      <AuthDispatchContext.Provider value={dispatch}>
        {children}
      </AuthDispatchContext.Provider>
    </AuthContext.Provider>
  )
}

function useAuth() {
  return useContext(AuthContext)
}

function useAuthDispatch() {
  return useContext(AuthDispatchContext)
}

// 使用
function LoginButton() {
  const dispatch = useAuthDispatch()
  const { loading } = useAuth()
  
  async function handleLogin() {
    dispatch({ type: 'SET_LOADING', loading: true })
    const user = await loginAPI()
    dispatch({ type: 'LOGIN', user })
    dispatch({ type: 'SET_LOADING', loading: false })
  }
  
  return <button onClick={handleLogin} disabled={loading}>Login</button>
}
```

## Context vs Props

什麼時候使用 Context，什麼時候使用 Props？

- **Props**：單層或少層傳遞、元件專屬的資料
- **Context**：多層傳遞、多個元件共享的資料、全域設定

```jsx
// Props 適合
<UserCard user={user} onEdit={handleEdit} />

// Context 適合
// 主題、語系、認證資訊、通知
```

## 效能優化

Context 的效能問題主要來自於：Provider 的 value 變化時，所有消費者都會重新渲染。

### 使用 useMemo

```jsx
function ThemeProvider({ children }) {
  const [theme, setTheme] = useState('light')
  
  const value = useMemo(() => ({ theme, setTheme }), [theme])
  
  return (
    <ThemeContext.Provider value={value}>
      {children}
    </ThemeContext.Provider>
  )
}
```

### 拆分 Context

將經常變化的和穩定的資料分開：

```jsx
// 穩定資料
const ConfigContext = createContext({ locale: 'zh-TW', version: '1.0' })

// 經常變化的資料
const UserContext = createContext(null)

function App() {
  const [user, setUser] = useState(null)
  
  return (
    <ConfigContext.Provider value={{ locale: 'zh-TW', version: '1.0' }}>
      <UserContext.Provider value={{ user, setUser }}>
        <Dashboard />
      </UserContext.Provider>
    </ConfigContext.Provider>
  )
}
```

## 與外部狀態管理比較

| 特性 | Context | Redux | Zustand |
|-----|---------|-------|--------|
| 內建 | 是 | 否 | 否 |
| 學習曲線 | 低 | 高 | 低 |
| 中間件支援 | 無 | 豐富 | 有限 |
| DevTools | 基本 | 強大 | 支援 |
| 複雜狀態 | 需搭配 useReducer | 內建 | 支援 |

## 實戰：多語言支援

```jsx
const I18NContext = createContext(null)

const translations = {
  zh: { hello: '你好', goodbye: '再見' },
  en: { hello: 'Hello', goodbye: 'Goodbye' },
}

function I18NProvider({ children }) {
  const [locale, setLocale] = useState('zh')
  
  const t = useCallback((key) => translations[locale][key] || key, [locale])
  
  const value = useMemo(() => ({ locale, setLocale, t }), [locale, t])
  
  return <I18NContext.Provider value={value}>{children}</I18NContext.Provider>
}

function useI18N() {
  return useContext(I18NContext)
}
```

## 結語

Context API 是 React 內建的全域狀態管理方案，對於中等規模的應用來說已經足夠。搭配 useReducer 和 useMemo，可以解決大多數的狀態管理需求。

---

## 延伸閱讀

- [Context API 文件](https://www.google.com/search?q=React+Context+API+documentation)
- [useReducer 搭配 Context](https://www.google.com/search?q=useReducer+with+Context+React)
- [Context 效能優化](https://www.google.com/search?q=React+Context+performance+optimization)

---

*本篇文章為「AI 程式人雜誌 2024 年 4 月號」精選文章之七。*
