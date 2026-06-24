#!/usr/bin/env node
// JavaScript 基礎語法範例 — AI 程式人雜誌 2024 年 1 月號

// ===== 1. 變數與型別 =====
const title = 'JavaScript 基礎'
let year = 2024
// var 是舊式宣告，避免使用

const types = {
  string: '文字',
  number: 42,
  boolean: true,
  nullValue: null,
  undefinedValue: undefined,
  array: [1, 2, 3],
  object: { key: 'value' }
}

// ===== 2. 函數與箭頭函數 =====
function add(a, b) {
  return a + b
}

const multiply = (a, b) => a * b

function createCounter() {
  let count = 0
  return () => ++count
}

// 高階函數
function operate(a, b, fn) {
  return fn(a, b)
}

// ===== 3. 陣列高階操作 =====
const numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

const evens = numbers.filter(n => n % 2 === 0)
const doubled = evens.map(n => n * 2)
const sum = doubled.reduce((acc, n) => acc + n, 0)

// 解構賦值
const [first, ...rest] = numbers

// ===== 4. Promise 與 async/await =====
function delay(ms) {
  return new Promise(resolve => setTimeout(resolve, ms))
}

async function fetchData() {
  await delay(500)
  return { id: 1, name: 'Alice', role: 'editor' }
}

async function fetchPosts() {
  await delay(300)
  return [
    { id: 101, title: 'JavaScript 基礎' },
    { id: 102, title: 'Promise 教學' }
  ]
}

async function getParallelData() {
  const [user, posts] = await Promise.all([
    fetchData(),
    fetchPosts()
  ])
  return { user, posts }
}

// ===== 5. 字串樣板 =====
function formatUser({ name, role }) {
  return `使用者: ${name} (${role})`
}

// ===== 6. 展開運算子 =====
const defaults = { theme: 'light', lang: 'zh-TW' }
const overrides = { theme: 'dark' }
const config = { ...defaults, ...overrides }

// ===== 7. 主程式 =====
async function demo() {
  console.log('=== JavaScript 基礎語法示範 ===')
  console.log('')

  // 變數與型別
  console.log('--- 變數與型別 ---')
  console.log('標題:', title)
  console.log('年份:', year)
  console.log('型別範例:', types)
  console.log('typeof 檢查:', typeof types.string, typeof types.number)
  console.log('')

  // 函數
  console.log('--- 函數 ---')
  console.log('add(10, 20) =', add(10, 20))
  console.log('multiply(6, 7) =', multiply(6, 7))
  console.log('operate(10, 5, (a,b) => a - b) =', operate(10, 5, (a, b) => a - b))
  console.log('')

  // 閉包
  console.log('--- 閉包 ---')
  const counter = createCounter()
  console.log('counter():', counter())
  console.log('counter():', counter())
  console.log('counter():', counter())
  console.log('')

  // 陣列操作
  console.log('--- 陣列操作 ---')
  console.log('numbers:', numbers)
  console.log('evens:', evens)
  console.log('doubled:', doubled)
  console.log('sum:', sum)
  console.log('first:', first, 'rest:', rest)
  console.log('')

  // 非同步
  console.log('--- 非同步 ---')
  const data = await fetchData()
  console.log('fetchData:', data)
  const parallel = await getParallelData()
  console.log('getParallelData:', JSON.stringify(parallel, null, 2))
  console.log('')

  // 字串樣板
  console.log('--- 字串樣板 ---')
  console.log(formatUser(data))
  console.log(formatUser({ name: 'Bob', role: 'admin' }))
  console.log('')

  // 展開運算子
  console.log('--- 展開運算子 ---')
  console.log('config:', config)
  console.log('')

  console.log('=== 示範結束 ===')
}

demo()
