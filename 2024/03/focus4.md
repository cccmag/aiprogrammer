# JavaScript DOM 操作

## DOM 簡介

DOM（Document Object Model）是 HTML 文件的物件表示。瀏覽器將 HTML 解析為一棵樹狀結構，每個節點代表文件中的一個元素、文字或屬性。JavaScript 可以透過 DOM API 讀取和修改這棵樹，實現動態網頁效果。

### DOM 樹結構

```
document
 └── html
      ├── head
      │    ├── title
      │    └── link
      └── body
           ├── header
           ├── main
           │    └── article
           └── footer
```

每個節點都是一個物件，具有屬性、方法和事件。

---

## 查詢元素

### getElementById

根據 id 查找單一元素：

```javascript
const header = document.getElementById("header");
```

### getElementsByClassName / getElementsByTagName

返回 HTMLCollection（即時更新）：

```javascript
const cards = document.getElementsByClassName("card");
const paragraphs = document.getElementsByTagName("p");
```

### querySelector / querySelectorAll

使用 CSS 選擇器查詢（推薦方式）：

```javascript
const firstBtn = document.querySelector(".btn");
const allBtns = document.querySelectorAll(".btn");
const sidebar = document.querySelector("#sidebar");
const articleP = document.querySelectorAll("article p");
```

querySelector 返回第一個匹配元素，querySelectorAll 返回 NodeList。

---

## 修改元素

### 文字內容

```javascript
// 設定純文字（安全）
element.innerText = "新的文字";

// 設定 HTML（注意 XSS 風險）
element.innerHTML = "<strong>粗體文字</strong>";
```

### 屬性操作

```javascript
// 讀取屬性
const src = img.getAttribute("src");
const cls = element.getAttribute("class");

// 設定屬性
element.setAttribute("data-id", "123");
element.setAttribute("disabled", "");

// 移除屬性
element.removeAttribute("disabled");

// 直接訪問（部分屬性）
img.src = "image.jpg";
input.value = "預設值";
```

### class 操作

使用 classList API：

```javascript
element.classList.add("active");
element.classList.remove("hidden");
element.classList.toggle("expanded");
element.classList.contains("active"); // true/false
```

---

## 新增與刪除元素

### 建立元素

```javascript
const div = document.createElement("div");
div.textContent = "新元素";
div.classList.add("box");
```

### 插入元素

```javascript
container.appendChild(div);         // 加到末尾
container.insertBefore(div, ref);   // 插入到參考前
container.insertAdjacentElement("beforeend", div);
```

### 刪除元素

```javascript
element.remove();              // 直接刪除
parent.removeChild(element);   // 從父元素刪除
```

---

## 遍歷 DOM

### 父子關係

```javascript
const parent = element.parentElement;
const children = element.children;        // HTMLCollection
const first = element.firstElementChild;
const last = element.lastElementChild;
```

### 兄弟關係

```javascript
const prev = element.previousElementSibling;
const next = element.nextElementSibling;
```

---

## 實戰範例

### 動態列表

```javascript
const list = document.querySelector("#todo-list");
const input = document.querySelector("#todo-input");
const addBtn = document.querySelector("#add-btn");

addBtn.addEventListener("click", () => {
  const text = input.value.trim();
  if (!text) return;

  const li = document.createElement("li");
  li.textContent = text;
  li.addEventListener("click", () => li.remove());

  list.appendChild(li);
  input.value = "";
});
```

### 批次更新

使用 DocumentFragment 提升效能：

```javascript
const fragment = document.createDocumentFragment();
for (let i = 0; i < 100; i++) {
  const li = document.createElement("li");
  li.textContent = `項目 ${i + 1}`;
  fragment.appendChild(li);
}
list.appendChild(fragment);
```

---

## 效能注意事項

- 盡量避免頻繁操作 DOM，應使用 DocumentFragment 或離線元素
- 使用 classList 代替直接操作 className
- 批量修改時先隱藏元素，修改後再顯示
- 使用事件委派代替大量事件監聽器

---

## 延伸閱讀

- [MDN: DOM 文件](https://www.google.com/search?q=MDN+Document+Object+Model)
- [JavaScript DOM 教學](https://www.google.com/search?q=JavaScript+DOM+tutorial)
- [DOM 效能最佳化](https://www.google.com/search?q=DOM+performance+optimization)

---

*本篇文章為「AI 程式人雜誌 2024 年 3 月號」前端開發系列之一。*
