# useEffect 實戰

## 前言

useEffect 是 React 中用來處理副作用的 Hook。雖然基本用法很簡單，但在實戰中會遇到各種情況需要謹慎處理。本文將從真實世界場景出發，探討 useEffect 的最佳實踐。

## 資料獲取與取消

最常見的場景是從 API 獲取資料。現代瀏覽器支援 AbortController，可以優雅地取消請求：

```javascript
function SearchResults({ query }) {
  const [results, setResults] = useState([])
  const [loading, setLoading] = useState(false)
  
  useEffect(() => {
    const controller = new AbortController()
    
    async function search() {
      setLoading(true)
      try {
        const res = await fetch(`/api/search?q=${query}`, {
          signal: controller.signal,
        })
        const data = await res.json()
        setResults(data)
      } catch (err) {
        if (err.name !== 'AbortError') {
          console.error(err)
        }
      } finally {
        setLoading(false)
      }
    }
    
    search()
    return () => controller.abort()
  }, [query])
  
  return (
    <div>
      {loading ? <Spinner /> :
        <ul>{results.map(r => <li key={r.id}>{r.title}</li>)}</ul>}
    </div>
  )
}
```

當 query 迅速變化時（如輸入搜尋關鍵字），AbortController 確保只有最後一個請求的結果會被處理。

## 事件監聽的清理

```javascript
function useOnlineStatus() {
  const [isOnline, setIsOnline] = useState(navigator.onLine)
  
  useEffect(() => {
    function handleOnline() { setIsOnline(true) }
    function handleOffline() { setIsOnline(false) }
    
    window.addEventListener('online', handleOnline)
    window.addEventListener('offline', handleOffline)
    
    return () => {
      window.removeEventListener('online', handleOnline)
      window.removeEventListener('offline', handleOffline)
    }
  }, [])
  
  return isOnline
}
```

## Debounce 與 Throttle

對於頻繁觸發的副作用（如搜尋建議），可以使用 debounce：

```javascript
function useDebounce(value, delay = 300) {
  const [debouncedValue, setDebouncedValue] = useState(value)
  
  useEffect(() => {
    const id = setTimeout(() => setDebouncedValue(value), delay)
    return () => clearTimeout(id)
  }, [value, delay])
  
  return debouncedValue
}

// 使用
function SearchAutocomplete() {
  const [query, setQuery] = useState('')
  const debouncedQuery = useDebounce(query, 500)
  
  useEffect(() => {
    if (debouncedQuery) {
      fetchSuggestions(debouncedQuery)
    }
  }, [debouncedQuery])
  
  return <input value={query} onChange={e => setQuery(e.target.value)} />
}
```

## 動畫與轉場效果

```javascript
function FadeIn({ children }) {
  const [visible, setVisible] = useState(false)
  const ref = useRef(null)
  
  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setVisible(true)
          observer.disconnect()
        }
      },
      { threshold: 0.1 }
    )
    
    if (ref.current) observer.observe(ref.current)
    return () => observer.disconnect()
  }, [])
  
  return (
    <div
      ref={ref}
      style={{
        opacity: visible ? 1 : 0,
        transition: 'opacity 1s ease-in-out',
      }}
    >
      {children}
    </div>
  )
}
```

## 計時器與輪詢

```javascript
function useInterval(callback, delay) {
  const savedCallback = useRef(callback)
  
  useEffect(() => {
    savedCallback.current = callback
  }, [callback])
  
  useEffect(() => {
    if (delay === null) return
    
    const id = setInterval(() => savedCallback.current(), delay)
    return () => clearInterval(id)
  }, [delay])
}

// 使用
function LiveClock() {
  const [time, setTime] = useState(new Date())
  
  useInterval(() => {
    setTime(new Date())
  }, 1000)
  
  return <p>{time.toLocaleTimeString()}</p>
}
```

## 避免無限循環

useEffect 的依賴陣列是避免無限循環的關鍵：

```javascript
function UserProfile({ userId }) {
  const [user, setUser] = useState(null)
  
  // 錯誤：每次渲染都重新執行
  useEffect(() => {
    fetchUser(userId).then(setUser)
  }) // 缺少依賴陣列
  
  // 正確：僅在 userId 變化時執行
  useEffect(() => {
    fetchUser(userId).then(setUser)
  }, [userId])
  
  // 錯誤：物件/陣列依賴
  useEffect(() => {
    fetchUser(userId).then(setUser)
  }, [{ userId }]) // 每次渲染都建立新物件
  
  return <div>{user?.name}</div>
}
```

## 多個 useEffect 的順序

同一個元件中可以有多個 useEffect，它們按照定義順序執行：

```javascript
function Dashboard() {
  useEffect(() => {
    console.log('第一個 effect')
  }, [])
  
  useEffect(() => {
    console.log('第二個 effect')
  }, [])
  
  // 輸出：第一個 effect → 第二個 effect
}
```

## 結語

useEffect 的實戰關鍵在於依賴陣列的管理、清理函式的正確使用，以及非同步操作的競態條件處理。掌握這些模式，就能寫出可靠的反應式邏輯。

---

## 延伸閱讀

- [useEffect 完整指南](https://www.google.com/search?q=useEffect+complete+guide+React)
- [React 副作用管理](https://www.google.com/search?q=React+side+effects+management)
- [AbortController 與 Fetch](https://www.google.com/search?q=AbortController+fetch+API)

---

*本篇文章為「AI 程式人雜誌 2024 年 4 月號」精選文章之五。*
