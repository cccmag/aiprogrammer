# 事件委派

## 什麼是事件委派

事件委派（Event Delegation）是一種利用事件冒泡機制來處理事件的設計模式。與其為每個子元素分別綁定事件監聽器，不如在共同的父元素上綁定一個監聽器，透過 event.target 判斷實際觸發事件的元素。

這種模式可以大幅減少事件監聽器的數量，提升效能，並自動處理動態新增的元素。

---

## 事件冒泡回顧

當一個事件在某個元素上觸發時，它會沿著 DOM 樹向上傳播：

```
document
 └── <div id="list">          ← 委派監聽器在這裡
      ├── <li>項目一</li>     ← 點擊這裡
      ├── <li>項目二</li>     ← 或這裡
      └── <li>項目三</li>     ← 或這裡
```

所有 li 的點擊事件最終都會冒泡到父元素 div#list。

---

## 基本用法

### 傳統方式 vs 事件委派

傳統方式：為每個 li 綁定監聽器

```javascript
// 不推薦：N 個元素需要 N 個監聽器
document.querySelectorAll("li").forEach(li => {
  li.addEventListener("click", () => {
    li.classList.toggle("selected");
  });
});
```

事件委派：只在父元素綁定一個監聽器

```javascript
// 推薦：只需要一個監聽器
document.querySelector("#list").addEventListener("click", (e) => {
  const li = e.target.closest("li");
  if (li) {
    li.classList.toggle("selected");
  }
});
```

---

## 實際應用場景

### 動態列表

當列表中的項目會動態新增或刪除時，事件委派特別有用：

```javascript
const list = document.querySelector("#todo-list");
const input = document.querySelector("#todo-input");
const form = document.querySelector("#todo-form");

// 事件委派：處理動態新增的項目
list.addEventListener("click", (e) => {
  const item = e.target.closest(".todo-item");
  if (!item) return;

  // 刪除按鈕
  if (e.target.closest(".delete-btn")) {
    item.remove();
  }
  // 完成切換
  else if (e.target.closest(".checkbox")) {
    item.classList.toggle("completed");
  }
  // 編輯
  else if (e.target.closest(".edit-btn")) {
    const text = item.querySelector(".todo-text");
    const newText = prompt("編輯待辦事項", text.textContent);
    if (newText) text.textContent = newText;
  }
});

// 新增項目（不需再綁定事件）
form.addEventListener("submit", (e) => {
  e.preventDefault();
  const text = input.value.trim();
  if (!text) return;

  const item = document.createElement("div");
  item.className = "todo-item";
  item.innerHTML = `
    <span class="todo-text">${text}</span>
    <button class="delete-btn">刪除</button>
  `;
  list.appendChild(item);
  input.value = "";
});
```

### 表格操作

```javascript
document.querySelector("#data-table").addEventListener("click", (e) => {
  const btn = e.target.closest("button");
  if (!btn) return;

  const row = btn.closest("tr");
  const action = btn.dataset.action;

  switch (action) {
    case "edit":
      editRow(row);
      break;
    case "delete":
      row.remove();
      break;
    case "duplicate":
      cloneRow(row);
      break;
  }
});
```

### 下拉選單

```javascript
document.querySelector("#dropdown").addEventListener("click", (e) => {
  const option = e.target.closest(".dropdown-item");
  if (!option) return;

  const value = option.dataset.value;
  const text = option.textContent;
  const trigger = document.querySelector("#dropdown-trigger");

  trigger.textContent = text;
  trigger.dataset.value = value;
  document.querySelector("#dropdown-menu").classList.remove("open");
});
```

---

## 判斷目標元素

在事件委派中，正確判斷目標元素是關鍵：

```javascript
parent.addEventListener("click", (e) => {
  // 方法一：使用 matches
  if (e.target.matches(".item")) {
    handleItem(e.target);
  }

  // 方法二：使用 closest（推薦，可處理嵌套結構）
  const item = e.target.closest(".item");
  if (item) {
    handleItem(item);
  }

  // 方法三：檢查特定元素
  if (e.target.tagName === "BUTTON") {
    handleButton(e.target);
  }
});
```

---

## 優點與限制

### 優點

1. **減少監聽器數量**：從 N 個減少到 1 個，節省記憶體
2. **自動處理動態元素**：新加入的元素自動獲得事件處理
3. **簡化程式碼**：事件處理邏輯集中在一處
4. **減少初始化時間**：不需要遍歷所有元素綁定監聽器

### 限制

1. **不適用於不冒泡的事件**：如 focus、blur、scroll、load
2. **可能需要較多的條件判斷**：需要過濾出實際要處理的元素
3. **不適合極深層的 DOM 結構**：事件冒泡經過太多層可能影響效能

---

## 不冒泡事件的替代方案

對於不冒泡的事件，可以使用 capture 階段監聽或直接綁定：

```javascript
// focus 不冒泡，直接在父元素捕獲階段監聽
form.addEventListener("focus", (e) => {
  const input = e.target.closest("input, textarea, select");
  if (input) input.classList.add("focused");
}, true); // capture 階段

// 或直接綁定在目標元素上
inputs.forEach(input => {
  input.addEventListener("focus", () => {...});
});
```

---

## 延伸閱讀

- [MDN: 事件冒泡與委派](https://www.google.com/search?q=MDN+event+bubbling+delegation)
- [JavaScript Event Delegation](https://www.google.com/search?q=JavaScript+event+delegation+pattern)
- [事件效能最佳化](https://www.google.com/search?q=JavaScript+event+performance)

---

*本篇文章為「AI 程式人雜誌 2024 年 3 月號」精選文章之一。*
