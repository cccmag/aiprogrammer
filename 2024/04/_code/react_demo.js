#!/usr/bin/env node

// ==========================================
// React Simulator — Virtual DOM & Hooks
// No external dependencies
// ==========================================

// --- Virtual DOM ---

function createElement(type, props, ...children) {
  return { type, props: { ...(props || {}), children: children.flat() } }
}

function renderToString(vnode) {
  if (vnode == null || typeof vnode === 'boolean') return ''
  if (typeof vnode === 'string' || typeof vnode === 'number') return String(vnode)
  if (typeof vnode.type === 'function') {
    return renderToString(vnode.type(vnode.props))
  }
  const tag = vnode.type
  const propsStr = Object.entries(vnode.props || {})
    .filter(([k]) => k !== 'children')
    .map(([k, v]) => ` ${k}="${String(v)}"`)
    .join('')
  const children = (vnode.props.children || [])
    .map(renderToString).join('')
  return `<${tag}${propsStr}>${children}</${tag}>`
}

// --- Diff Algorithm ---

function diffProps(prev, next) {
  const changes = []
  const keys = new Set([
    ...Object.keys(prev || {}),
    ...Object.keys(next || {}),
  ])
  for (const key of keys) {
    if (key === 'children') continue
    if (prev?.[key] !== next?.[key]) {
      changes.push({ key, value: next?.[key], prev: prev?.[key] })
    }
  }
  return changes
}

function diff(prev, next) {
  if (typeof prev === 'string' || typeof prev === 'number') {
    if (prev !== next) return [{ type: 'TEXT', prev, next }]
    return []
  }
  if (prev.type !== next.type) {
    return [{ type: 'REPLACE', prev, next }]
  }
  const patches = []
  const propChanges = diffProps(prev.props, next.props)
  if (propChanges.length > 0) {
    patches.push({ type: 'UPDATE_PROPS', changes: propChanges })
  }

  const prevChildren = prev.props?.children || []
  const nextChildren = next.props?.children || []
  const max = Math.max(prevChildren.length, nextChildren.length)
  for (let i = 0; i < max; i++) {
    if (i >= prevChildren.length) {
      patches.push({ type: 'ADD', node: nextChildren[i], index: i })
    } else if (i >= nextChildren.length) {
      patches.push({ type: 'REMOVE', node: prevChildren[i], index: i })
    } else {
      patches.push(...diff(prevChildren[i], nextChildren[i]))
    }
  }
  return patches
}

// --- Hooks ---

let currentRender = null
let hookIndex = 0
const hookStates = []
const cleanupEffects = []

function useState(initial) {
  const idx = hookIndex++
  if (hookStates[idx] === undefined) hookStates[idx] = initial
  const setState = (newVal) => {
    const val = typeof newVal === 'function' ? newVal(hookStates[idx]) : newVal
    if (val !== hookStates[idx]) {
      hookStates[idx] = val
      scheduleRender()
    }
  }
  return [hookStates[idx], setState]
}

function useEffect(cb, deps) {
  const idx = hookIndex++
  const prev = hookStates[idx]
  const changed = !prev || deps === undefined ||
    deps.some((d, i) => d !== prev.deps[i])
  if (changed) {
    if (prev?.cleanup) cleanupEffects.push(prev.cleanup)
    const cleanup = cb()
    hookStates[idx] = { deps, cleanup }
  }
}

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

function useRef(initial) {
  const idx = hookIndex++
  if (hookStates[idx] === undefined) hookStates[idx] = { current: initial }
  return hookStates[idx]
}

// --- Scheduler ---

let pendingRender = false

function scheduleRender() {
  if (pendingRender) return
  pendingRender = true
  if (typeof setImmediate === 'function') {
    setImmediate(runRender)
  } else {
    setTimeout(runRender, 0)
  }
}

function runRender() {
  pendingRender = false
  while (cleanupEffects.length > 0) {
    cleanupEffects.pop()()
  }
  demo()
}

// --- Counter Component ---

function Counter(props) {
  const [count, setCount] = useState(props.initial || 0)
  const [step, setStep] = useState(1)

  useEffect(() => {
    if (typeof module !== 'undefined' && module.exports) {
      console.log(`[Effect] Count is now: ${count}`)
    }
    return () => {
      if (typeof module !== 'undefined' && module.exports) {
        console.log(`[Cleanup] Cleaning up effect for count=${count}`)
      }
    }
  }, [count])

  const doubled = useMemo(() => count * 2, [count])
  const increment = useCallback(() => setCount(c => c + step), [step])
  const decrement = useCallback(() => setCount(c => c - step), [step])
  const countRef = useRef(count)
  countRef.current = count

  return createElement('div', { class: 'counter' },
    createElement('h2', {}, `Counter: ${count}`),
    createElement('p', {}, `Doubled: ${doubled}`),
    createElement('p', {}, `Step: ${step}`),
    createElement('button', { onClick: String(increment) }, '+'),
    createElement('button', { onClick: String(decrement) }, '-'),
    createElement('button', { onClick: String(() => setStep(s => s + 1)) }, 'Step+'),
  )
}

// --- Todo Component ---

function TodoApp() {
  const [todos, setTodos] = useState([])
  const [input, setInput] = useState('')

  const addTodo = useCallback(() => {
    if (!input.trim()) return
    setTodos(prev => [...prev, { id: Date.now(), text: input, done: false }])
    setInput('')
  }, [input])

  const toggleTodo = useCallback((id) => {
    setTodos(prev => prev.map(t =>
      t.id === id ? { ...t, done: !t.done } : t
    ))
  }, [])

  const stats = useMemo(() => ({
    total: todos.length,
    done: todos.filter(t => t.done).length,
    pending: todos.filter(t => !t.done).length,
  }), [todos])

  return createElement('div', { class: 'todo-app' },
    createElement('h2', {}, 'Todo App'),
    createElement('div', {},
      createElement('input', {
        value: input,
        placeholder: 'Add todo...',
        onChange: String((e) => setInput(e.target.value)),
      }),
      createElement('button', { onClick: String(addTodo) }, 'Add'),
    ),
    createElement('ul', {},
      ...todos.map(t =>
        createElement('li', {
          key: t.id,
          class: t.done ? 'done' : '',
          onClick: String(() => toggleTodo(t.id)),
        }, `${t.text} ${t.done ? '✓' : '○'}`)
      )
    ),
    createElement('p', { class: 'stats' },
      `Total: ${stats.total} | Done: ${stats.done} | Pending: ${stats.pending}`
    ),
  )
}

// --- Demo function ---

let renderCount = 0

function demo() {
  hookIndex = 0
  renderCount++
  console.log(`\n=== Render #${renderCount} ===`)

  const app = createElement('div', { id: 'app' },
    createElement('h1', {}, `React Simulator — Demo (Render #${renderCount})`),
    createElement(Counter, { initial: 0 }),
    createElement(TodoApp, null),
  )

  const output = renderToString(app)
  console.log(output)

  // Show diff example
  if (renderCount === 1) {
    const prevVDOM = createElement('div', { id: 'app' },
      createElement('h1', {}, 'React Simulator — Demo'),
    )
    const nextVDOM = createElement('div', { id: 'app' },
      createElement('h1', {}, 'React Simulator — Demo (Updated)'),
    )
    const patches = diff(prevVDOM, nextVDOM)
    console.log('\n--- Diff Example ---')
    console.log('Patches:', JSON.stringify(patches, null, 2))
  }

  console.log('\n--- Hook States ---')
  console.log(`Counter state[0] = ${JSON.stringify(hookStates[0])}`)
  console.log(`Step state[1] = ${JSON.stringify(hookStates[1])}`)
  console.log(`Todos state[2] = ${JSON.stringify(hookStates[2])}`)
  console.log(`Input state[3] = ${JSON.stringify(hookStates[3])}`)
}

// --- Run ---

if (typeof require !== 'undefined' && require.main === module) {
  demo()
}

module.exports = {
  createElement,
  renderToString,
  diff,
  diffProps,
  useState,
  useEffect,
  useMemo,
  useCallback,
  useRef,
  demo,
}
