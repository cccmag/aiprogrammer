# 效能最佳化：memo、useMemo

## 前言

React 的宣告式渲染模型讓開發者專注於「要做什麼」而非「怎麼做」，但這種便利性可能帶來不必要的重複渲染。當元件的渲染成本較高時，效能最佳化就變得重要了。本文將探討 React 提供的三大效能工具：React.memo、useMemo 和 useCallback。

## React 的渲染機制

在深入最佳化之前，需要理解 React 何時重新渲染一個元件：

1. **State 變化**：元件的 state 更新
2. **Props 變化**：父元件傳入的 props 變化
3. **Context 變化**：使用的 Context 值變化
4. **父元件重新渲染**：父元件重新渲染時，子元件也跟著重新渲染

當父元件重新渲染時，所有子元件都會重新渲染，即使它們的 props 沒有變化：

```jsx
function App() {
  const [count, setCount] = useState(0)
  
  return (
    <div>
      <button onClick={() => setCount(c + 1)}>{count}</button>
      <ExpensiveComponent /> {/* 每次 count 變化都重新渲染 */}
    </div>
  )
}
```

## React.memo

`React.memo` 是一個高階元件，它會對 props 進行淺比較（shallow compare），如果 props 沒有變化，就跳過重新渲染：

```jsx
import { memo } from 'react'

const ExpensiveList = memo(function ExpensiveList({ items, onItemClick }) {
  console.log('ExpensiveList rendered')
  
  return (
    <ul>
      {items.map(item => (
        <li key={item.id} onClick={() => onItemClick(item.id)}>
          {item.name}
        </li>
      ))}
    </ul>
  )
})
```

使用 memo 後，只有當 `items` 或 `onItemClick` 變化時，元件才會重新渲染。

### memo 的比較函式

預設使用淺比較，也可以自訂比較函式：

```jsx
const Item = memo(
  ({ item, isSelected }) => {
    return <div className={isSelected ? 'selected' : ''}>{item.name}</div>
  },
  (prevProps, nextProps) => {
    return prevProps.item.id === nextProps.item.id &&
           prevProps.isSelected === nextProps.isSelected
  }
)
```

## useMemo

`useMemo` 用於快取計算結果。當計算成本較高時，可以避免在每次渲染時重新計算：

```jsx
import { useMemo } from 'react'

function Dashboard({ transactions, filter }) {
  // 複雜的過濾和計算邏輯
  const filteredData = useMemo(() => {
    console.log('Computing filtered data...')
    return transactions
      .filter(t => t.type === filter.type)
      .filter(t => t.date >= filter.startDate)
      .map(t => ({
        ...t,
        total: t.amount * t.quantity,
        tax: t.amount * t.quantity * 0.05,
      }))
      .sort((a, b) => b.date - a.date)
  }, [transactions, filter])
  
  // 統計總和
  const totals = useMemo(() => ({
    totalAmount: filteredData.reduce((sum, t) => sum + t.total, 0),
    totalTax: filteredData.reduce((sum, t) => sum + t.tax, 0),
    count: filteredData.length,
  }), [filteredData])
  
  return (
    <div>
      <SummaryCard totals={totals} />
      <TransactionList items={filteredData} />
    </div>
  )
}
```

## useCallback

`useCallback` 是 `useMemo` 的特殊形式，專門用於快取函式：

```jsx
import { useCallback } from 'react'

function TodoList() {
  const [todos, setTodos] = useState([])
  
  // 沒有 useCallback：每次渲染都建立新函式
  const handleAdd = useCallback((text) => {
    setTodos(prev => [...prev, { id: Date.now(), text, done: false }])
  }, [])
  
  const handleToggle = useCallback((id) => {
    setTodos(prev => prev.map(t =>
      t.id === id ? { ...t, done: !t.done } : t
    ))
  }, [])
  
  const handleDelete = useCallback((id) => {
    setTodos(prev => prev.filter(t => t.id !== id))
  }, [])
  
  return (
    <div>
      <AddTodo onAdd={handleAdd} />
      <TodoItems items={todos} onToggle={handleToggle} onDelete={handleDelete} />
    </div>
  )
}
```

為什麼需要 `useCallback`？因為如果 `handleAdd` 每次渲染都重新建立，傳遞給 `memo(AddTodo)` 時，memo 的淺比較會認為 props 變化了。

## 實際案例：虛擬列表

虛擬列表是效能優化的典型應用：

```jsx
function VirtualList({ items, itemHeight, containerHeight }) {
  const [scrollTop, setScrollTop] = useState(0)
  
  const visibleItems = useMemo(() => {
    const start = Math.floor(scrollTop / itemHeight)
    const end = Math.min(start + Math.ceil(containerHeight / itemHeight) + 1, items.length)
    return items.slice(start, end).map((item, i) => ({
      ...item,
      index: start + i,
    }))
  }, [items, scrollTop, itemHeight, containerHeight])
  
  const handleScroll = useCallback((e) => {
    setScrollTop(e.target.scrollTop)
  }, [])
  
  return (
    <div style={{ height: containerHeight, overflow: 'auto' }} onScroll={handleScroll}>
      <div style={{ height: items.length * itemHeight }}>
        {visibleItems.map(item => (
          <div key={item.id} style={{
            position: 'absolute',
            top: item.index * itemHeight,
            height: itemHeight,
          }}>
            <MemoizedItem data={item} />
          </div>
        ))}
      </div>
    </div>
  )
}
```

## 何時不該最佳化

過早的最佳化是萬惡之源。以下情況不需要使用 memo/useMemo：

- 元件渲染非常快（單純的 div 和文字）
- 元件在所有渲染中都會被重新建立
- 父元件很少重新渲染
- props 幾乎總是變化

Profiling 優先於猜測：

```jsx
import { Profiler } from 'react'

function onRender(id, phase, actualDuration) {
  console.log(`${id} (${phase}): ${actualDuration}ms`)
}

<Profiler id="TodoList" onRender={onRender}>
  <TodoList />
</Profiler>
```

## 結語

React.memo、useMemo 和 useCallback 是 React 效能優化的三大利器。但最佳化是有代價的——記憶體消耗和比較的開銷。建議先以 Profiler 測量效能瓶頸，再針對性地進行優化。

---

## 延伸閱讀

- [React.memo 文件](https://www.google.com/search?q=React+memo+documentation)
- [useMemo 與 useCallback](https://www.google.com/search?q=React+useMemo+useCallback+guide)
- [React Profiler](https://www.google.com/search?q=React+Profiler+performance)

---

*本篇文章為「AI 程式人雜誌 2024 年 4 月號」精選文章之九。*
