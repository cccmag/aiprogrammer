# DOM 查詢與修改

## DOM 查詢方法

JavaScript 提供了多種查詢 DOM 元素的方法，選擇適當的方法可以提升程式碼效率和可讀性。

### 單一元素查詢

```javascript
// 根據 ID 查詢
const header = document.getElementById("header");

// 根據 CSS 選擇器查詢（返回第一個匹配）
const firstBtn = document.querySelector(".btn-primary");
const mainEl = document.querySelector("main");
const form = document.querySelector("#login-form");
```

### 多元素查詢

```javascript
// 根據類別名稱查詢
const cards = document.getElementsByClassName("card");

// 根據標籤名稱查詢
const paragraphs = document.getElementsByTagName("p");

// 根據 CSS 選擇器查詢（返回 NodeList）
const items = document.querySelectorAll(".menu-item");
const links = document.querySelectorAll("nav a");
```

### NodeList vs HTMLCollection

| 特性 | NodeList | HTMLCollection |
|------|----------|---------------|
| 回傳方法 | querySelectorAll | getElementsBy* |
| 是否即時更新 | 否（靜態） | 是（即時） |
| 可用 forEach | 是 | 否 |
| 可用陣列方法 | 需轉換 | 需轉換 |

NodeList 可以使用 `forEach`，但若要使用 `map`、`filter` 等方法，需先轉換為陣列：

```javascript
const items = document.querySelectorAll(".item");
const texts = Array.from(items).map(item => item.textContent);
```

---

## DOM 遍歷

### 父子節點

```javascript
const parent = element.parentElement;
const children = element.children;        // HTMLCollection
const first = element.firstElementChild;
const last = element.lastElementChild;
```

### 兄弟節點

```javascript
const prev = element.previousElementSibling;
const next = element.nextElementSibling;
```

### 最近祖先

```javascript
const card = button.closest(".card");
const form = input.closest("form");
```

closest 從當前元素向上遍歷，返回第一個匹配選擇器的祖先元素。

---

## DOM 修改

### 文字內容

```javascript
// 設定純文字（安全，自動跳脫 HTML）
element.textContent = "新的文字內容";

// 取得文字
const text = element.textContent;

// 設定 HTML（注意 XSS 風險）
element.innerHTML = "<strong>粗體</strong>";
```

### 屬性操作

```javascript
// 設定屬性
element.setAttribute("data-id", "123");
element.setAttribute("aria-label", "描述");

// 取得屬性
const id = element.getAttribute("data-id");

// 移除屬性
element.removeAttribute("disabled");

// 檢查屬性
const hasClass = element.hasAttribute("class");

// 直接屬性訪問（部分屬性）
img.src = "photo.jpg";
input.value = "預設值";
a.href = "https://example.com";
```

### 類別操作

```javascript
element.classList.add("active");
element.classList.remove("hidden");
element.classList.toggle("expanded");
element.classList.replace("old", "new");
const isActive = element.classList.contains("active");
```

### 行內樣式

```javascript
element.style.color = "#333";
element.style.fontSize = "16px";
element.style.backgroundColor = "#f5f5f5";
element.style.cssText = "color: red; font-size: 14px;";
```

---

## DOM 建立與插入

### 建立元素

```javascript
const div = document.createElement("div");
const p = document.createElement("p");
const img = document.createElement("img");
```

### 插入方法

```javascript
// 插入到末尾
parent.appendChild(child);

// 插入到參考節點前
parent.insertBefore(newChild, referenceChild);

// 相對於元素插入
element.insertAdjacentElement("beforebegin", el);  // 元素前
element.insertAdjacentElement("afterbegin", el);   // 內部開頭
element.insertAdjacentElement("beforeend", el);    // 內部末尾
element.insertAdjacentElement("afterend", el);     // 元素後

// 插入 HTML
element.insertAdjacentHTML("beforeend", "<li>新項目</li>");
```

### 複製與刪除

```javascript
// 複製節點（true 表示深層複製）
const clone = element.cloneNode(true);

// 刪除節點
element.remove();
parent.removeChild(element);
```

---

## 實戰範例

### 動態載入資料

```javascript
async function loadUsers() {
  const list = document.querySelector("#user-list");
  list.innerHTML = '<li class="loading">載入中...</li>';

  try {
    const res = await fetch("https://api.example.com/users");
    const users = await res.json();
    list.innerHTML = "";

    const fragment = document.createDocumentFragment();
    users.forEach(user => {
      const li = document.createElement("li");
      li.textContent = user.name;
      li.dataset.id = user.id;
      fragment.appendChild(li);
    });
    list.appendChild(fragment);
  } catch (err) {
    list.innerHTML = '<li class="error">載入失敗</li>';
  }
}
```

---

## 效能建議

- 使用 DocumentFragment 進行批量插入
- 避免在迴圈中頻繁操作 DOM
- 使用 classList 代替 className 的字串操作
- 需要大量修改時，先隱藏元素、修改、再顯示

---

## 延伸閱讀

- [MDN: DOM 查詢](https://www.google.com/search?q=MDN+DOM+querySelector)
- [MDN: 節點操作](https://www.google.com/search?q=MDN+DOM+node+manipulation)
- [DOM 效能建議](https://www.google.com/search?q=DOM+performance+tips)

---

*本篇文章為「AI 程式人雜誌 2024 年 3 月號」精選文章之一。*
