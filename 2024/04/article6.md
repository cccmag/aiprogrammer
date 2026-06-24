# 自訂 Hook

## 前言

自訂 Hook 是 React 中最強大的程式碼複用機制。它讓開發者將元件中的邏輯提取為可復用的函式，從而實現「寫一次，到處使用」的目標。本文將從實例出發，展示如何設計和建立自訂 Hook。

## 自訂 Hook 的基本規則

自訂 Hook 是一個以 `use` 開頭的 JavaScript 函式，可以在其中呼叫其他 Hooks：

```javascript
function useDocumentTitle(title) {
  useEffect(() => {
    document.title = title
  }, [title])
}
```

使用時就像任何其他 Hook 一樣：

```jsx
function ProfilePage() {
  useDocumentTitle('User Profile')
  return <div>...</div>
}

function SettingsPage() {
  useDocumentTitle('Settings')
  return <div>...</div>
}
```

## 自訂 Hook 範例

### 1. useLocalStorage

將狀態同步到 localStorage：

```javascript
function useLocalStorage(key, initialValue) {
  const [value, setValue] = useState(() => {
    try {
      const stored = localStorage.getItem(key)
      return stored ? JSON.parse(stored) : initialValue
    } catch {
      return initialValue
    }
  })
  
  useEffect(() => {
    try {
      localStorage.setItem(key, JSON.stringify(value))
    } catch (err) {
      console.error('Failed to save to localStorage:', err)
    }
  }, [key, value])
  
  return [value, setValue]
}

// 使用
function ThemeToggle() {
  const [theme, setTheme] = useLocalStorage('theme', 'light')
  
  return (
    <button onClick={() => setTheme(t => t === 'light' ? 'dark' : 'light')}>
      Current: {theme}
    </button>
  )
}
```

### 2. useFetch

封裝 API 請求邏輯：

```javascript
function useFetch(url) {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  
  useEffect(() => {
    let cancelled = false
    
    async function fetchData() {
      setLoading(true)
      setError(null)
      
      try {
        const res = await fetch(url)
        if (!res.ok) throw new Error(`HTTP ${res.status}`)
        const json = await res.json()
        if (!cancelled) setData(json)
      } catch (err) {
        if (!cancelled) setError(err.message)
      } finally {
        if (!cancelled) setLoading(false)
      }
    }
    
    fetchData()
    return () => { cancelled = true }
  }, [url])
  
  return { data, loading, error }
}

// 使用
function UserList() {
  const { data: users, loading, error } = useFetch('/api/users')
  
  if (loading) return <Spinner />
  if (error) return <ErrorMsg message={error} />
  return <ul>{users.map(u => <li key={u.id}>{u.name}</li>)}</ul>
}
```

### 3. useMediaQuery

響應式設計的自訂 Hook：

```javascript
function useMediaQuery(query) {
  const [matches, setMatches] = useState(
    () => window.matchMedia(query).matches
  )
  
  useEffect(() => {
    const mql = window.matchMedia(query)
    function handler(e) { setMatches(e.matches) }
    
    mql.addEventListener('change', handler)
    return () => mql.removeEventListener('change', handler)
  }, [query])
  
  return matches
}

// 使用
function ResponsiveLayout() {
  const isMobile = useMediaQuery('(max-width: 768px)')
  const isTablet = useMediaQuery('(max-width: 1024px)')
  
  if (isMobile) return <MobileLayout />
  if (isTablet) return <TabletLayout />
  return <DesktopLayout />
}
```

### 4. useToggle

簡化 boolean 狀態操作：

```javascript
function useToggle(initial = false) {
  const [value, setValue] = useState(initial)
  
  const toggle = useCallback(() => setValue(v => !v), [])
  const setTrue = useCallback(() => setValue(true), [])
  const setFalse = useCallback(() => setValue(false), [])
  
  return [value, { toggle, setTrue, setFalse, set: setValue }]
}

// 使用
function ModalExample() {
  const [isOpen, { toggle, setTrue, setFalse }] = useToggle(false)
  
  return (
    <div>
      <button onClick={setTrue}>Open</button>
      {isOpen && <Modal onClose={setFalse} />}
    </div>
  )
}
```

### 5. usePrevious

獲取前一次渲染的值：

```javascript
function usePrevious(value) {
  const ref = useRef()
  
  useEffect(() => {
    ref.current = value
  }, [value])
  
  return ref.current
}

// 使用
function CounterDisplay({ count }) {
  const prevCount = usePrevious(count)
  
  return (
    <p>
      Current: {count} |
      Previous: {prevCount} |
      Direction: {count > prevCount ? 'Up' : count < prevCount ? 'Down' : 'Same'}
    </p>
  )
}
```

## Hook 組合

自訂 Hook 最大的威力來自於組合——一個 Hook 內部可以呼叫其他 Hooks：

```javascript
function useUserData(userId) {
  const { data: user, loading, error } = useFetch(`/api/users/${userId}`)
  const isOnline = useOnlineStatus()
  
  return {
    user,
    loading,
    error,
    isOnline,
    displayName: user ? `${user.name} (${isOnline ? 'Online' : 'Offline'})` : '',
  }
}
```

## Hook 測試

自訂 Hook 可以使用 `renderHook` 測試：

```javascript
import { renderHook, act } from '@testing-library/react'

describe('useToggle', () => {
  it('should toggle value', () => {
    const { result } = renderHook(() => useToggle(false))
    
    expect(result.current[0]).toBe(false)
    
    act(() => result.current[1].toggle())
    expect(result.current[0]).toBe(true)
    
    act(() => result.current[1].toggle())
    expect(result.current[0]).toBe(false)
  })
})
```

## 結語

自訂 Hook 是 React 生態中最優雅的程式碼複用方式。它比 HOC 更簡潔，比 Render Props 更直覺。透過自訂 Hook，可以將複雜的邏輯封裝為可復用的單元，讓元件專注於 UI 渲染。

---

## 延伸閱讀

- [自訂 Hook 官方文件](https://www.google.com/search?q=React+custom+Hooks+documentation)
- [React Hooks 模式](https://www.google.com/search?q=React+Hooks+patterns)
- [實用自訂 Hook 集合](https://www.google.com/search?q=useful+custom+React+hooks)

---

*本篇文章為「AI 程式人雜誌 2024 年 4 月號」精選文章之六。*
