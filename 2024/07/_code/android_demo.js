#!/usr/bin/env node
/**
 * android_demo.js
 * Android 核心概念 Node.js 模擬
 * 模擬：Lifecycle, ViewModel, Navigation, Room
 */

// ─── Lifecycle 狀態機 ───

const LIFECYCLE_STATES = {
  INITIALIZED: 'INITIALIZED',
  CREATED: 'CREATED',
  STARTED: 'STARTED',
  RESUMED: 'RESUMED',
  PAUSED: 'PAUSED',
  STOPPED: 'STOPPED',
  DESTROYED: 'DESTROYED',
}

class Lifecycle {
  constructor() {
    this.state = LIFECYCLE_STATES.INITIALIZED
    this.listeners = []
  }
  addObserver(fn) { this.listeners.push(fn) }
  transition(newState) {
    const old = this.state
    this.state = newState
    this.listeners.forEach(fn => fn(old, newState))
  }
  onCreate() { this.transition(LIFECYCLE_STATES.CREATED) }
  onStart()  { this.transition(LIFECYCLE_STATES.STARTED) }
  onResume() { this.transition(LIFECYCLE_STATES.RESUMED) }
  onPause()  { this.transition(LIFECYCLE_STATES.PAUSED) }
  onStop()   { this.transition(LIFECYCLE_STATES.STOPPED) }
  onDestroy(){ this.transition(LIFECYCLE_STATES.DESTROYED) }
}

// ─── ViewModel ───

class ViewModel {
  constructor() {
    this._state = {}
    this._observers = []
  }
  getState(key) { return this._state[key] }
  setState(key, value) {
    this._state[key] = value
    this.notify(key, value)
  }
  notify(key, value) {
    this._observers.forEach(o => o(key, value))
  }
  observe(fn) { this._observers.push(fn) }
  onCleared() { this._observers = [] }
}

// ─── Navigation ───

class NavController {
  constructor() {
    this.backStack = []
    this.currentRoute = null
  }
  navigate(route, args = {}) {
    if (this.currentRoute) this.backStack.push(this.currentRoute)
    this.currentRoute = { route, args }
  }
  goBack() {
    if (this.backStack.length === 0) return false
    this.currentRoute = this.backStack.pop()
    return true
  }
}

// ─── Room Database ───

class RoomDatabase {
  constructor() { this.tables = {} }
  createTable(name) { this.tables[name] = [] }
  insert(table, record) {
    record.id = Date.now() + Math.random()
    this.tables[table].push(record)
    return record.id
  }
  query(table, predicate = () => true) {
    return this.tables[table].filter(predicate)
  }
  update(table, id, updates) {
    const idx = this.tables[table].findIndex(r => r.id === id)
    if (idx !== -1) Object.assign(this.tables[table][idx], updates)
  }
  delete(table, id) {
    this.tables[table] = this.tables[table].filter(r => r.id !== id)
  }
}

// ─── Demo ───

function lifecycleDemo() {
  console.log('=== Lifecycle Demo ===')
  const lc = new Lifecycle()
  lc.addObserver((old, now) => console.log(`State: ${old} -> ${now}`))
  lc.onCreate()
  lc.onStart()
  lc.onResume()
  lc.onPause()
  lc.onStop()
  lc.onDestroy()
  console.log()
}

function viewModelDemo() {
  console.log('=== ViewModel Demo ===')
  const vm = new ViewModel()
  vm.observe((key, value) => console.log(`${key} set to: ${value}`))
  vm.setState('count', 1)
  vm.setState('count', 2)
  vm.setState('count', 3)
  console.log()
}

function navigationDemo() {
  console.log('=== Navigation Demo ===')
  const nav = new NavController()
  console.log(`Navigated to: home`); nav.navigate('home')
  console.log(`Navigated to: profile`); nav.navigate('profile')
  console.log(`Navigated to: settings`); nav.navigate('settings')
  nav.goBack(); console.log(`Back to: ${nav.currentRoute.route}`)
  nav.goBack(); console.log(`Back to: ${nav.currentRoute.route}`)
  console.log()
}

function roomDemo() {
  console.log('=== Room Demo ===')
  const db = new RoomDatabase()
  db.createTable('users')

  const id1 = db.insert('users', { name: 'Alice', email: 'alice@example.com' })
  const id2 = db.insert('users', { name: 'Bob', email: 'bob@example.com' })
  console.log(`Inserted user: Alice, id=${id1}`)
  console.log(`Inserted user: Bob, id=${id2}`)

  const all = db.query('users')
  console.log(`All users: ${all.length}`)

  db.update('users', id1, { name: 'Alice Smith' })
  const found = db.query('users', u => u.id === id1)[0]
  console.log(`Updated Alice to ${found.name}`)
  console.log(`Found Alice: ${found.name}`)

  db.delete('users', id2)
  const remaining = db.query('users')
  console.log(`Deleted Bob`)
  console.log(`Remaining: ${remaining.length}`)
}

function demo() {
  lifecycleDemo()
  viewModelDemo()
  navigationDemo()
  roomDemo()
}

if (require.main === module) {
  demo()
}

module.exports = { Lifecycle, LIFECYCLE_STATES, ViewModel, NavController, RoomDatabase, demo }
