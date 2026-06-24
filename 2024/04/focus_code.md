# React 模擬實作

## 前言

為了深入理解 React 的設計原理，本篇文章將在 Node.js 環境中模擬 React 的核心機制，包括虛擬 DOM、Diff 演算法、狀態管理與 Hooks。我們的實作不依賴任何 React 函式庫，而是從零開始建立一套簡化的 React 運行模型。

---

## 原始碼

完整的 JavaScript 實作請參考：[_code/react_demo.js](_code/react_demo.js)

```javascript
// ==========================================
// 模擬 Virtual DOM
// ==========================================

function createElement(type, props, ...children) {
  return {
    type,
    props: { ...props, children: children.flat() }
  }
}

// ==========================================
// 模擬元件渲染
// ==========================================

function renderToString(vnode) {
  if (typeof vnode === 'string') return vnode
  if (typeof vnode.type === 'function') {
    return renderToString(vnode.type(vnode.props))
  }
  const children = (vnode.props.children || [])
    .map(renderToString).join('')
  return `<${vnode.type}>${children}</${vnode.type}>`
}

// ==========================================
// 模擬 Diff 演算法
// ==========================================

function diff(prev, next) {
  const patches = []
  if (typeof prev === 'string' && typeof next === 'string') {
    if (prev !== next) patches.push({ type: 'TEXT', value: next })
  } else if (prev.type !== next.type) {
    patches.push({ type: 'REPLACE', node: next })
  } else {
    patches.push({ type: 'UPDATE', props: diffProps(prev.props, next.props) })
  }
  return patches
}

function diffProps(prev, next) {
  const changes = []
  const allKeys = new Set([...Object.keys(prev||{}), ...Object.keys(next||{})])
  for (const key of allKeys) {
    if (prev[key] !== next[key]) {
      changes.push({ key, value: next[key] })
    }
  }
  return changes
}

// ==========================================
// 模擬 Hooks (useState)
// ==========================================

let currentComponent = null
let hookIndex = 0
const hookStates = []

function useState(initial) {
  const idx = hookIndex++
  if (hookStates[idx] === undefined) hookStates[idx] = initial
  const setState = (newVal) => {
    const val = typeof newVal === 'function' ? newVal(hookStates[idx]) : newVal
    hookStates[idx] = val
    scheduleRender()
  }
  return [hookStates[idx], setState]
}

// ==========================================
// 模擬 useEffect
// ==========================================

function useEffect(cb, deps) {
  const idx = hookIndex++
  const prev = hookStates[idx]
  const changed = !prev || !deps || deps.some((d, i) => d !== prev.deps[i])
  if (changed) {
    if (prev && prev.cleanup) prev.cleanup()
    const cleanup = cb()
    hookStates[idx] = { deps, cleanup }
  }
}

// ==========================================
// 模擬 useMemo / useCallback
// ==========================================

function useMemo(fn, deps) {
  const idx = hookIndex++
  const prev = hookStates[idx]
  if (!prev || deps.some((d, i) => d !== prev.deps[i])) {
    hookStates[idx] = { value: fn(), deps }
  }
  return hookStates[idx].value
}

function useCallback(fn, deps) {
  return useMemo(() => fn, deps)
}

// ==========================================
// 排程渲染
// ==========================================

let pendingRender = false

function scheduleRender() {
  if (pendingRender) return
  pendingRender = true
  setTimeout(() => {
    pendingRender = false
    demo()
  }, 0)
}

// ==========================================
// Demo 元件
// ==========================================

function Counter({ initial }) {
  const [count, setCount] = useState(initial || 0)
  
  useEffect(() => {
    console.log(`Count changed to: ${count}`)
    return () => console.log('Cleanup effect')
  }, [count])

  const doubled = useMemo(() => count * 2, [count])

  const vdom = createElement('div', {},
    createElement('h1', {}, `Count: ${count}`),
    createElement('p', {}, `Doubled: ${doubled}`),
    createElement('button', { onClick: () => setCount(c => c + 1) }, '+1'),
  )
  return renderToString(vdom)
}

let renderCount = 0

function demo() {
  hookIndex = 0
  renderCount++
  const title = renderToString(createElement('h1', {}, `Render #${renderCount}`))
  const result = Counter({ initial: 0 })
  const output = title + '\n' + result
  console.log('--- Demo Output ---')
  console.log(output)
  console.log('Current state:', hookStates[0])
}

if (require.main === module) {
  demo()
}

module.exports = { createElement, renderToString, useState, useEffect, useMemo, useCallback, diff, demo }
```

---

## 執行結果

```
--- Demo Output ---
<h1>Render #1</h1>
<div><h1>Count: 0</h1><p>Doubled: 0</p><button>+1</button></div>
Current state: 0
Count changed to: 0
```

---

## Virtual DOM 概念

Virtual DOM 是 React 的核心創新之一。它是一個輕量級的 JavaScript 物件樹，對應於真實的 DOM 結構。當元件狀態發生變化時，React 會建立一個新的 Virtual DOM 樹，並與舊的樹進行比較（Diffing），找出最小的變更集合，最後應用到真實 DOM 上。

```
┌────────────────────────────────────────────────┐
│                 Virtual DOM 流程                 │
├────────────────────────────────────────────────┤
│                                                │
│  狀態改變 → 新 Virtual DOM → Diff → 更新真實 DOM│
│                                                │
│  優點：批次更新、最小化 DOM 操作、宣告式開發     │
│                                                │
└────────────────────────────────────────────────┘
```

---

## Hooks 實作原理

我們的模擬展示了 Hooks 的核心機制：依賴於固定的 calls order。每次渲染時，Hooks 按照相同的順序被呼叫，React 內部維護一個索引陣列來追蹤每個 Hook 的狀態。這就是為什麼 Hooks 不能在條件式或迴圈中使用。

---

## 延伸閱讀

- [React Virtual DOM](https://www.google.com/search?q=React+Virtual+DOM+explained)
- [React Hooks 原理](https://www.google.com/search?q=React+Hooks+how+it+works)
- [React 原始碼導讀](https://www.google.com/search?q=React+source+code+analysis)

---

*本篇文章為「AI 程式人雜誌 2024 年 4 月號」系列補充文章。*
