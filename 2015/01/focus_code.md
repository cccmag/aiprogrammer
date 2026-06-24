# JavaScript 與 DOM 操作實務

## 概述

本期實作將展示 JavaScript 與 DOM 操作的核心技術，包括 DOM 查詢與遍歷、事件處理機制、以及 AJAX 與 Fetch API 的實際應用。

## DOM 查詢與操作

### 基本查詢方法

```javascript
// 根據 ID 查詢（最快）
const header = document.getElementById('header');

// 根據類別查詢
const items = document.getElementsByClassName('item');

// 根據標籤查詢
const paragraphs = document.getElementsByTagName('p');

// 查詢選擇器（支援 CSS 選擇器）
const firstCard = document.querySelector('.card');
const allButtons = document.querySelectorAll('button.btn');
```

### 元素操作

```javascript
// 建立元素
const newDiv = document.createElement('div');
newDiv.textContent = '新元素';
newDiv.className = 'new-element';

// 插入元素
parent.appendChild(newDiv);           // 末尾插入
parent.insertBefore(newDiv, reference); // 指定位置插入

// 移除元素
parent.removeChild(child);
child.remove(); // 現代方法

// 修改元素內容
element.textContent = '新文字';
element.innerHTML = '<strong>HTML</strong> 內容';

// 修改屬性
element.setAttribute('data-id', '123');
element.getAttribute('data-id');
element.removeAttribute('data-id');

// 修改樣式
element.style.color = 'blue';
element.style.backgroundColor = '#f0f0f0';
element.classList.add('active');
element.classList.remove('hidden');
element.classList.toggle('expanded');
```

### 事件處理

```javascript
// 基本事件監聽
element.addEventListener('click', function(event) {
  console.log('點擊了', event.target);
});

// 箭頭函式
element.addEventListener('click', (e) => {
  console.log('座標:', e.clientX, e.clientY);
});

// 事件監聽器選項
element.addEventListener('click', handler, {
  capture: false,    // 捕獲階段
  once: true,        // 只觸發一次
  passive: false     // 不調用 preventDefault
});

// 移除監聽
element.removeEventListener('click', handler);

// 事件委託
document.querySelector('.list').addEventListener('click', (e) => {
  if (e.target.matches('.list-item')) {
    console.log('點擊了:', e.target.textContent);
  }
});
```

### 常見事件類型

```javascript
// 滑鼠事件
element.addEventListener('click', handler);
element.addEventListener('dblclick', handler);
element.addEventListener('mouseenter', handler);
element.addEventListener('mouseleave', handler);
element.addEventListener('mousemove', handler);
element.addEventListener('mousedown', handler);
element.addEventListener('mouseup', handler);

// 鍵盤事件
document.addEventListener('keydown', (e) => {
  console.log('按鍵:', e.key);
  console.log('代碼:', e.code);
});
document.addEventListener('keyup', handler);

// 表單事件
form.addEventListener('submit', (e) => {
  e.preventDefault(); // 阻止預設提交
});
input.addEventListener('focus', handler);
input.addEventListener('blur', handler);
input.addEventListener('change', handler);
input.addEventListener('input', handler);

// 視窗事件
window.addEventListener('resize', handler);
window.addEventListener('scroll', handler);
window.addEventListener('load', handler);
document.addEventListener('DOMContentLoaded', handler);
```

## Fetch API 實戰

### 基本 GET 請求

```javascript
async function fetchUsers() {
  try {
    const response = await fetch('/api/users');
    const users = await response.json();
    console.log(users);
    return users;
  } catch (error) {
    console.error('取得使用者失敗:', error);
  }
}
```

### POST 請求

```javascript
async function createPost(title, content) {
  try {
    const response = await fetch('/api/posts', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ title, content })
    });
    const result = await response.json();
    return result;
  } catch (error) {
    console.error('建立文章失敗:', error);
  }
}
```

### 錯誤處理

```javascript
async function fetchWithError(url) {
  const response = await fetch(url);

  if (!response.ok) {
    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
  }

  return await response.json();
}
```

## 完整範例：待辦事項應用

```javascript
// 待辦事項管理
class TodoApp {
  constructor() {
    this.todos = JSON.parse(localStorage.getItem('todos') || '[]');
    this.init();
  }

  init() {
    this.form = document.getElementById('todo-form');
    this.input = document.getElementById('todo-input');
    this.list = document.getElementById('todo-list');

    this.form.addEventListener('submit', (e) => {
      e.preventDefault();
      this.addTodo(this.input.value);
      this.input.value = '';
    });

    this.render();
  }

  addTodo(text) {
    const todo = {
      id: Date.now(),
      text,
      completed: false
    };
    this.todos.push(todo);
    this.save();
    this.render();
  }

  toggleTodo(id) {
    const todo = this.todos.find(t => t.id === id);
    if (todo) {
      todo.completed = !todo.completed;
      this.save();
      this.render();
    }
  }

  deleteTodo(id) {
    this.todos = this.todos.filter(t => t.id !== id);
    this.save();
    this.render();
  }

  save() {
    localStorage.setItem('todos', JSON.stringify(this.todos));
  }

  render() {
    this.list.innerHTML = this.todos.map(todo => `
      <li class="${todo.completed ? 'completed' : ''}">
        <input type="checkbox"
               ${todo.completed ? 'checked' : ''}
               data-id="${todo.id}">
        <span>${todo.text}</span>
        <button data-id="${todo.id}">刪除</button>
      </li>
    `).join('');

    // 事件委託
    this.list.addEventListener('click', (e) => {
      const id = parseInt(e.target.dataset.id);
      if (e.target.matches('input[type="checkbox"]')) {
        this.toggleTodo(id);
      } else if (e.target.matches('button')) {
        this.deleteTodo(id);
      }
    });
  }
}

// 初始化
document.addEventListener('DOMContentLoaded', () => {
  new TodoApp();
});
```

## localStorage 操作

```javascript
// 設定值
localStorage.setItem('key', 'value');
localStorage.setItem('user', JSON.stringify({ name: 'John', age: 30 }));

// 取得值
const value = localStorage.getItem('key');
const user = JSON.parse(localStorage.getItem('user'));

// 刪除值
localStorage.removeItem('key');

// 清除全部
localStorage.clear();

// 事件監聽（跨分頁同步）
window.addEventListener('storage', (e) => {
  console.log('Key:', e.key);
  console.log('Old Value:', e.oldValue);
  console.log('New Value:', e.newValue);
});
```

## 程式碼展示

本期的程式碼位於 `_code/` 目錄：

- `dom-demo.js` - DOM 操作基礎範例
- `event-handler.js` - 事件處理範例
- `fetch-demo.js` - Fetch API 範例

執行方式：

```bash
node dom-demo.js
node event-handler.js
node fetch-demo.js
```

---

*本期程式實作到此結束。*