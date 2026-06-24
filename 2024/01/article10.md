# 小專案：待辦事項網頁應用

## 專案概述

在本篇文章中，我們將綜合運用本期所學的 JavaScript 知識，從零開始建立一個完整的待辦事項（Todo List）網頁應用。這個專案涵蓋 DOM 操作、事件處理、localStorage 儲存、陣列操作等核心概念。

## HTML 結構

```html
<!DOCTYPE html>
<html lang="zh-TW">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>待辦事項</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: sans-serif;
      background: #f0f2f5;
      display: flex;
      justify-content: center;
      padding-top: 50px;
    }
    .container {
      width: 500px;
      background: white;
      border-radius: 8px;
      padding: 24px;
      box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    h1 { text-align: center; color: #333; margin-bottom: 20px; }
    .input-area {
      display: flex;
      gap: 8px;
      margin-bottom: 20px;
    }
    .input-area input {
      flex: 1;
      padding: 10px;
      border: 1px solid #ddd;
      border-radius: 4px;
      font-size: 14px;
    }
    .input-area button {
      padding: 10px 20px;
      background: #4a90d9;
      color: white;
      border: none;
      border-radius: 4px;
      cursor: pointer;
    }
    .input-area button:hover { background: #357abd; }
    .filters {
      display: flex;
      gap: 8px;
      margin-bottom: 16px;
    }
    .filters button {
      padding: 6px 12px;
      border: 1px solid #ddd;
      background: white;
      border-radius: 4px;
      cursor: pointer;
    }
    .filters button.active { background: #4a90d9; color: white; }
    ul { list-style: none; }
    li {
      display: flex;
      align-items: center;
      padding: 10px 0;
      border-bottom: 1px solid #eee;
      gap: 8px;
    }
    li.completed span { text-decoration: line-through; color: #999; }
    li span { flex: 1; cursor: pointer; }
    li button { background: #e74c3c; color: white; border: none; border-radius: 4px; padding: 4px 8px; cursor: pointer; }
    .stats { text-align: center; margin-top: 16px; color: #666; font-size: 13px; }
  </style>
</head>
<body>
  <div class="container">
    <h1>待辦事項</h1>
    <div class="input-area">
      <input type="text" id="todoInput" placeholder="輸入新待辦事項...">
      <button id="addBtn">新增</button>
    </div>
    <div class="filters">
      <button class="active" data-filter="all">全部</button>
      <button data-filter="active">進行中</button>
      <button data-filter="completed">已完成</button>
    </div>
    <ul id="todoList"></ul>
    <div class="stats" id="stats"></div>
  </div>
  <script src="app.js"></script>
</body>
</html>
```

## JavaScript 實作

```javascript
// app.js — Todo List 應用邏輯

// ===== 資料層 =====
const STORAGE_KEY = 'todoApp';

function loadTodos() {
  const data = localStorage.getItem(STORAGE_KEY);
  return data ? JSON.parse(data) : [];
}

function saveTodos(todos) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(todos));
}

// ===== 應用狀態 =====
let todos = loadTodos();
let currentFilter = 'all';

// ===== DOM 元素 =====
const todoInput = document.getElementById('todoInput');
const addBtn = document.getElementById('addBtn');
const todoList = document.getElementById('todoList');
const stats = document.getElementById('stats');
const filterBtns = document.querySelectorAll('.filters button');

// ===== 核心功能 =====
function addTodo(text) {
  if (!text.trim()) return;
  const todo = {
    id: Date.now(),
    text: text.trim(),
    completed: false,
    createdAt: new Date().toISOString()
  };
  todos.push(todo);
  saveTodos(todos);
  render();
}

function toggleTodo(id) {
  const todo = todos.find(t => t.id === id);
  if (todo) {
    todo.completed = !todo.completed;
    saveTodos(todos);
    render();
  }
}

function deleteTodo(id) {
  todos = todos.filter(t => t.id !== id);
  saveTodos(todos);
  render();
}

function setFilter(filter) {
  currentFilter = filter;
  filterBtns.forEach(btn => {
    btn.classList.toggle('active', btn.dataset.filter === filter);
  });
  render();
}

function getFilteredTodos() {
  switch (currentFilter) {
    case 'active': return todos.filter(t => !t.completed);
    case 'completed': return todos.filter(t => t.completed);
    default: return todos;
  }
}

// ===== 渲染層 =====
function render() {
  const filtered = getFilteredTodos();
  const total = todos.length;
  const completed = todos.filter(t => t.completed).length;
  const active = total - completed;

  // 渲染列表
  todoList.innerHTML = filtered.map(todo => `
    <li class="${todo.completed ? 'completed' : ''}">
      <input type="checkbox" ${todo.completed ? 'checked' : ''}>
      <span>${escapeHtml(todo.text)}</span>
      <button data-id="${todo.id}">刪除</button>
    </li>
  `).join('');

  // 更新統計
  stats.textContent = `全部 ${total} 項 | 進行中 ${active} 項 | 已完成 ${completed} 項`;

  // 綁定事件
  todoList.querySelectorAll('input[type="checkbox"]').forEach((cb, i) => {
    cb.addEventListener('change', () => toggleTodo(filtered[i].id));
  });

  todoList.querySelectorAll('li span').forEach((span, i) => {
    span.addEventListener('click', () => toggleTodo(filtered[i].id));
  });

  todoList.querySelectorAll('li button').forEach((btn, i) => {
    btn.addEventListener('click', () => deleteTodo(filtered[i].id));
  });
}

function escapeHtml(text) {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}

// ===== 事件綁定 =====
addBtn.addEventListener('click', () => {
  addTodo(todoInput.value);
  todoInput.value = '';
});

todoInput.addEventListener('keypress', (e) => {
  if (e.key === 'Enter') {
    addBtn.click();
  }
});

filterBtns.forEach(btn => {
  btn.addEventListener('click', () => setFilter(btn.dataset.filter));
});

// ===== 初始化 =====
render();
```

## 功能說明

這個待辦事項應用實現了以下功能：

1. **新增待辦事項**：輸入文字後點擊「新增」或按 Enter 鍵
2. **切換完成狀態**：點擊核取方塊或事項文字可標記完成/未完成
3. **刪除事項**：點擊「刪除」按鈕移除事項
4. **篩選檢視**：全部、進行中、已完成三種檢視模式
5. **資料持久化**：使用 localStorage 儲存資料，關閉分頁後重新開啟資料仍在
6. **統計資訊**：顯示全部、進行中和已完成的項目數量

## 執行方式

建立 `index.html` 和 `app.js` 在同一個資料夾中，用瀏覽器打開 `index.html` 即可使用。

## 延伸練習

完成基本功能後，可以嘗試以下改進：

```javascript
// 1. 拖曳排序
// 2. 編輯待辦事項內容
// 3. 設定截止日期
// 4. 優先級標記
// 5. 搜尋功能
// 6. 批量操作
// 7. 資料匯出/匯入
```

## 結語

這個待辦事項應用雖然簡單，卻涵蓋了本期所學的大部分 JavaScript 核心概念。從 DOM 操作到事件處理，從陣列方法到 localStorage 儲存，從函數封裝到模組化思維。將這個應用作為起點，你可以逐步擴展它，加入更多進階功能來鞏固所學知識。

---

**延伸閱讀**

- [MDN localStorage](https://www.google.com/search?q=MDN+localStorage)
- [JavaScript Todo List 教學](https://www.google.com/search?q=JavaScript+Todo+List+tutorial)
- [DOM 操作大全](https://www.google.com/search?q=JavaScript+DOM+manipulation+guide)
