'use strict';

// ============================================================
// Flutter 模擬器 — 在 Node.js 中展示 Flutter/Dart 核心概念
// 包含：Widget 樹、狀態管理 (Provider)、路由導航
// ============================================================

// ---- 1. 基底 Widget ----
class Widget {
  build(context) { throw new Error('build() 須由子類實作'); }
}

// ---- 2. BuildContext 模擬 ----
class BuildContext {
  constructor(state) { this.state = state; this.routes = new Map(); }
}

// ---- 3. Provider 狀態管理 ----
class Provider {
  static _container = new Map();
  static provide(key, value) { Provider._container.set(key, value); }
  static of(key) { return Provider._container.get(key); }
}

// ---- 4. 基礎 Widget ----
class Text extends Widget {
  constructor(text, style = {}) { super(); this.text = text; this.style = style; }
  build() { return { type: 'Text', props: { text: this.text, style: this.style } }; }
}

class Column extends Widget {
  constructor(children) { super(); this.children = children; }
  build() {
    return { type: 'Column', props: { children: this.children.map(c => c.build()) } };
  }
}

class Row extends Widget {
  constructor(children) { super(); this.children = children; }
  build() {
    return { type: 'Row', props: { children: this.children.map(c => c.build()) } };
  }
}

class Center extends Widget {
  constructor(child) { super(); this.child = child; }
  build() { return { type: 'Center', props: { child: this.child.build() } }; }
}

class Padding extends Widget {
  constructor({ padding, child }) { super(); this.padding = padding; this.child = child; }
  build() { return { type: 'Padding', props: { padding: this.padding, child: this.child.build() } }; }
}

class ElevatedButton extends Widget {
  constructor({ onPressed, child }) { super(); this.onPressed = onPressed; this.child = child; }
  build() { return { type: 'ElevatedButton', props: { child: this.child.build() } }; }
  press() { if (this.onPressed) this.onPressed(); }
}

class Scaffold extends Widget {
  constructor({ appBar, body, floatingActionButton }) {
    super();
    this.appBar = appBar;
    this.body = body;
    this.floatingActionButton = floatingActionButton;
  }
  build() {
    return {
      type: 'Scaffold',
      props: {
        appBar: this.appBar?.build(),
        body: this.body?.build(),
        fab: this.floatingActionButton?.build()
      }
    };
  }
}

// ---- 5. StatefulWidget 生命週期模擬 ----
class StatefulWidget extends Widget {
  createState() { throw new Error('createState() 須由子類實作'); }
}

class State {
  constructor(widget) { this.widget = widget; this._mounted = true; }
  setState(updater) {
    Object.assign(this, updater);
    if (this._mounted) this._render();
  }
  _render() { /* 觸發重新 build */ }
  dispose() { this._mounted = false; }
  initState() { /* 初始化 */ }
  build() { throw new Error('build() 須由子類實作'); }
}

// ---- 6. 計數器 App (示範 StatefulWidget) ----
class CounterWidget extends StatefulWidget {
  createState() { return new CounterState(this); }
}

class CounterState extends State {
  constructor(widget) { super(widget); this.count = 0; }
  increment() { this.setState({ count: this.count + 1 }); }
  build() {
    const btn = new ElevatedButton({
      onPressed: () => this.increment(),
      child: new Text('點我 +1')
    });
    return new Scaffold({
      appBar: new Text('Flutter 計數器'),
      body: new Column([
        new Text(`點擊次數: ${this.count}`, { fontSize: 28 }),
        btn
      ])
    });
  }
}

// ---- 7. 導航路由 ----
class Navigator {
  constructor() { this._routes = new Map(); this._history = []; }
  define(name, widgetFactory) { this._routes.set(name, widgetFactory); }
  push(name) {
    if (!this._routes.has(name)) throw new Error(`路由 '${name}' 不存在`);
    this._history.push(name);
    return this._routes.get(name)();
  }
  pop() {
    if (this._history.length === 0) return null;
    return this._history.pop();
  }
  current() {
    if (this._history.length === 0) return null;
    const name = this._history[this._history.length - 1];
    return this._routes.get(name)();
  }
  canPop() { return this._history.length > 1; }
}

// ---- 8. Provider 進階：ChangeNotifier ----
class ChangeNotifier {
  constructor() { this._listeners = []; }
  addListener(fn) { this._listeners.push(fn); }
  removeListener(fn) {
    this._listeners = this._listeners.filter(l => l !== fn);
  }
  notifyListeners() { this._listeners.forEach(fn => fn()); }
}

class TodoModel extends ChangeNotifier {
  constructor() { super(); this.todos = []; }
  add(text) { this.todos.push({ id: Date.now(), text, done: false }); this.notifyListeners(); }
  toggle(id) {
    const item = this.todos.find(t => t.id === id);
    if (item) { item.done = !item.done; this.notifyListeners(); }
  }
}

// ---- 9. 主展示函式 ----
function demo() {
  console.log('=== Flutter 模擬器 ===\n');

  // 9a. Provider 展示
  console.log('--- 狀態管理: Provider ---');
  const todoModel = new TodoModel();
  Provider.provide('todos', todoModel);
  todoModel.addListener(() => {
    const pending = todoModel.todos.filter(t => !t.done).length;
    console.log(`待辦更新 — 總數: ${todoModel.todos.length}, 未完成: ${pending}`);
  });
  todoModel.add('學習 Flutter');
  todoModel.add('研究 Provider');
  todoModel.toggle(todoModel.todos[0].id);

  // 9b. Widget 樹建置
  console.log('\n--- Widget 樹 (JSON) ---');
  const counterApp = new CounterWidget();
  const state = counterApp.createState();
  state.initState();
  const tree = state.build().build();
  console.log(JSON.stringify(tree, null, 2));

  // 9c. 路由導航
  console.log('\n--- 路由導航 ---');
  const nav = new Navigator();
  nav.define('home', () => new Scaffold({ appBar: new Text('首頁'),
    body: new Text('歡迎來到 Flutter 模擬器！') }));
  nav.define('settings', () => new Scaffold({ appBar: new Text('設定'),
    body: new Center(new Text('設定頁面')) }));
  nav.define('about', () => new Scaffold({ appBar: new Text('關於'),
    body: new Center(new Text('AI 程式人雜誌 202408')) }));

  nav.push('home');
  nav.push('settings');
  console.log('當前路由:', JSON.stringify(nav.current().build()));
  nav.pop();
  console.log('返回後:', JSON.stringify(nav.current().build()));
  nav.push('about');
  console.log('前往關於:', JSON.stringify(nav.current().build()));

  // 9d. Widget 組合展示
  console.log('\n--- 複雜佈局 (Column + Row) ---');
  const complex = new Column([
    new Row([new Text('姓名'), new Text(':'), new Text('陳小明')]),
    new Row([new Text('年齡'), new Text(':'), new Text('28')]),
    new Row([new Text('城市'), new Text(':'), new Text('台北')]),
  ]).build();
  console.log(JSON.stringify(complex, null, 2));

  console.log('\n=== Demo 完成 ===');
}

const isMain = require.main === module;
if (isMain) demo();

module.exports = {
  Widget, Text, Column, Row, Center, Padding,
  ElevatedButton, Scaffold, StatefulWidget, State,
  Navigator, Provider, ChangeNotifier, TodoModel, demo
};
