# 副作用與 useEffect

## 什麼是副作用

在 React 中，元件的主要職責是根據狀態和 Props 渲染 UI。但現實應用還需要執行 API 請求、操作 DOM、設定計時器、註冊事件監聽等操作——這些統稱為「副作用」（Side Effects）。

副作用是元件與外部世界互動的唯一方式，但它們也帶來了複雜性：時機管理、資源清理、依賴追蹤。

## useEffect 的基本用法

`useEffect` 是 React 提供的副作用處理 Hook，讓開發者可以在函式元件中執行副作用操作：

```javascript
import { useEffect } from 'react'

function DataFetcher() {
  useEffect(() => {
    // 副作用邏輯
    console.log('Component mounted or updated')
    
    // 清理函式（可選）
    return () => {
      console.log('Cleanup before next effect or unmount')
    }
  }, []) // 依賴陣列
}
```

`useEffect` 接受兩個參數：

1. **副作用函式**：執行副作用的函式
2. **依賴陣列**（可選）：控制副作用何時執行

## 依賴陣列機制

依賴陣列決定 useEffect 何時執行：

```javascript
// 1. 無依賴陣列：每次渲染後都執行
useEffect(() => {
  console.log('Runs after every render')
})

// 2. 空陣列：只在初次掛載時執行
useEffect(() => {
  console.log('Runs only once on mount')
}, [])

// 3. 有依賴值：當依賴值變化時執行
const [count, setCount] = useState(0)
useEffect(() => {
  console.log('Runs when count changes:', count)
}, [count])
```

依賴陣列的機制是 React 避免無限循環的關鍵。如果副作用中修改了某個狀態，但該狀態不在依賴陣列中，就可能導致意料之外的行為。

## 常見的副作用場景

### API 資料獲取

```javascript
function UserList() {
  const [users, setUsers] = useState([])
  const [loading, setLoading] = useState(true)
  
  useEffect(() => {
    let cancelled = false
    
    async function fetchUsers() {
      const res = await fetch('/api/users')
      const data = await res.json()
      if (!cancelled) setUsers(data)
      setLoading(false)
    }
    
    fetchUsers()
    return () => { cancelled = true }
  }, [])
  
  if (loading) return <p>Loading...</p>
  return <ul>{users.map(u => <li key={u.id}>{u.name}</li>)}</ul>
}
```

使用 `cancelled` flag 可以避免元件卸載後更新狀態的錯誤。在 React 18 之後，也可以使用 `useEffect` 的 cleanup 機制搭配 AbortController。

### 事件監聽與訂閱

```javascript
function WindowSize() {
  const [width, setWidth] = useState(window.innerWidth)
  
  useEffect(() => {
    function handleResize() {
      setWidth(window.innerWidth)
    }
    
    window.addEventListener('resize', handleResize)
    return () => window.removeEventListener('resize', handleResize)
  }, [])
  
  return <p>Window width: {width}px</p>
}
```

清理函式確保在元件卸載時移除事件監聽，避免記憶體洩漏。

### 計時器

```javascript
function Timer() {
  const [seconds, setSeconds] = useState(0)
  
  useEffect(() => {
    const id = setInterval(() => {
      setSeconds(s => s + 1)
    }, 1000)
    
    return () => clearInterval(id)
  }, [])
  
  return <p>Elapsed: {seconds}s</p>
}
```

## useEffect 的生命週期對應

useEffect 組合了類別元件中的三個生命週期方法：

| 類別元件 | useEffect 對應 |
|---------|--------------|
| componentDidMount | useEffect(fn, []) |
| componentDidUpdate | useEffect(fn, [dep1, dep2]) |
| componentWillUnmount | useEffect(() => fn, []) 的 cleanup |

## 常見錯誤

### 忘記依賴

```javascript
const [count, setCount] = useState(0)

useEffect(() => {
  const id = setInterval(() => {
    setCount(count + 1) // 使用閉包中的 count
  }, 1000)
  return () => clearInterval(id)
}, []) // 錯誤：count 不變，永遠顯示 1
```

修正方式：使用函式更新或加入正確的依賴。

### 副作用中的狀態更新

如果副作用中更新了狀態，而該狀態在依賴陣列中，要小心避免無限循環：

```javascript
const [count, setCount] = useState(0)

useEffect(() => {
  setCount(count + 1) // 更新 count
}, [count]) // count 變化 → 觸發 effect → count 變化 → ...
```

## 結語

useEffect 是 React 中最強大的 Hook 之一，也是學習曲線最陡峭的一個。理解副作用的概念、依賴陣列的運作機制和清理的重要性，是寫出穩定 React 應用的關鍵。

---

## 延伸閱讀

- [React useEffect 文件](https://www.google.com/search?q=React+useEffect+documentation)
- [useEffect 完整指南](https://www.google.com/search?q=useEffect+complete+guide)
- [同步 vs 生命週期](https://www.google.com/search?q=React+useEffect+vs+lifecycle)

---

*本篇文章為「AI 程式人雜誌 2024 年 4 月號」焦點系列之四。*
