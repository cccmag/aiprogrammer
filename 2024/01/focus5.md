# DOM 操作與事件處理

## DOM 樹結構

### 什麼是 DOM

DOM（Document Object Model）是瀏覽器將 HTML 文件解析為的樹狀結構。每個 HTML 元素都是樹中的一個節點：

```html
<html>
  <head>
    <title>我的頁面</title>
  </head>
  <body>
    <h1 id="title">Hello</h1>
    <div class="content">
      <p>一段文字</p>
    </div>
  </body>
</html>
```

DOM 樹對應的結構：
```
document
 └── html
      ├── head
      │    └── title
      └── body
           ├── h1#title
           └── div.content
                └── p
```

## 元素選取

### 選取單一元素

```javascript
// 依 ID 選取
const title = document.getElementById('title');

// 依 CSS 選擇器選取（第一個符合）
const firstParagraph = document.querySelector('p');
const mainDiv = document.querySelector('#main > .content');

// 依 name 屬性選取
const usernameInput = document.querySelector('[name="username"]');
```

### 選取多個元素

```javascript
// 依類別選取
const items = document.getElementsByClassName('item');

// 依標籤名稱選取
const paragraphs = document.getElementsByTagName('p');

// 依 CSS 選擇器選取（所有符合）
const allLinks = document.querySelectorAll('nav a.external');
```

## 元素操作

### 內容操作

```javascript
const element = document.querySelector('#myElement');

// 文字內容
element.textContent = '新文字內容';

// HTML 內容（注意 XSS 風險）
element.innerHTML = '<strong>粗體文字</strong>';

// 取得或設定屬性
element.getAttribute('data-id'); // 取得
element.setAttribute('class', 'highlight'); // 設定
element.hasAttribute('disabled'); // 檢查
element.removeAttribute('disabled'); // 移除

// class 操作（現代方式）
element.classList.add('active');
element.classList.remove('hidden');
element.classList.toggle('visible');
element.classList.contains('active'); // true/false
```

### 樣式操作

```javascript
const box = document.querySelector('.box');

// 行內樣式
box.style.backgroundColor = 'blue';
box.style.color = 'white';
box.style.fontSize = '20px';
box.style.display = 'flex';

// 讀取計算後的樣式
const styles = getComputedStyle(box);
console.log(styles.backgroundColor);
```

### DOM 操作

```javascript
// 建立元素
const newDiv = document.createElement('div');
newDiv.textContent = '我是新元素';
newDiv.classList.add('new-item');

// 插入元素
const parent = document.querySelector('#container');

parent.appendChild(newDiv);           // 插入到尾部
parent.insertBefore(newDiv, refNode); // 插入到某元素之前
parent.prepend(newDiv);               // 插入到頭部
parent.append(newDiv);                // 插入到尾部（更現代）

// 取代和移除
parent.replaceChild(newDiv, oldDiv);
parent.removeChild(oldDiv);           // 舊方式
oldDiv.remove();                      // 新方式
```

## 事件處理

### 事件監聽

```javascript
const button = document.querySelector('#myButton');

// 基本事件監聽
button.addEventListener('click', function(event) {
  console.log('按鈕被點擊了！');
  console.log('事件物件：', event);
});

// 箭頭函數形式
button.addEventListener('click', (event) => {
  console.log('點擊位置：', event.clientX, event.clientY);
});
```

### 常見事件類型

```javascript
// 滑鼠事件
element.addEventListener('click', handler);      // 點擊
element.addEventListener('dblclick', handler);   // 雙擊
element.addEventListener('mouseenter', handler); // 滑鼠進入
element.addEventListener('mouseleave', handler); // 滑鼠離開
element.addEventListener('mousemove', handler);  // 滑鼠移動

// 鍵盤事件
document.addEventListener('keydown', (e) => {
  console.log(`按下了 ${e.key}，鍵碼 ${e.code}`);
  if (e.key === 'Enter') {
    console.log('按下了 Enter');
  }
});

// 表單事件
form.addEventListener('submit', (e) => {
  e.preventDefault(); // 阻止表單提交
  console.log('表單已提交');
});

input.addEventListener('input', (e) => {
  console.log('輸入值：', e.target.value);
});

// 文件事件
document.addEventListener('DOMContentLoaded', () => {
  console.log('DOM 準備就緒');
});

window.addEventListener('load', () => {
  console.log('所有資源載入完成');
});

// 滾動事件
window.addEventListener('scroll', () => {
  console.log('滾動位置：', window.scrollY);
});
```

### 事件物件

```javascript
element.addEventListener('click', (event) => {
  event.preventDefault();    // 阻止預設行為
  event.stopPropagation();  // 阻止事件冒泡
  event.stopImmediatePropagation(); // 阻止後續監聽器

  console.log(event.type);         // 'click'
  console.log(event.target);       // 真正觸發的元素
  console.log(event.currentTarget);// 綁定監聽器的元素
  console.log(event.clientX);      // 滑鼠 X 座標
  console.log(event.clientY);      // 滑鼠 Y 座標
});
```

## 事件委派

事件委派是利用事件冒泡機制的效能優化技巧：

```javascript
// 不優雅的方式：為每個 li 添加監聽器
const items = document.querySelectorAll('li.item');
items.forEach(item => {
  item.addEventListener('click', () => {
    console.log('點擊了項目');
  });
});

// 事件委派：在父元素上監聽
const list = document.querySelector('#itemList');

list.addEventListener('click', (event) => {
  const target = event.target;

  // 只處理 li.item 元素
  if (target.matches('li.item')) {
    console.log('點擊了項目：', target.textContent);

    // 根據 data-* 屬性執行不同操作
    const action = target.dataset.action;
    if (action === 'delete') {
      target.remove();
    } else if (action === 'edit') {
      promptEdit(target);
    }
  }
});
```

## 實用範例

### 動態表單驗證

```javascript
const form = document.querySelector('#signupForm');
const emailInput = document.querySelector('#email');
const errorMsg = document.querySelector('#error');

emailInput.addEventListener('input', () => {
  const email = emailInput.value;
  const isValid = email.includes('@') && email.includes('.');

  if (!email) {
    errorMsg.textContent = '';
  } else if (isValid) {
    errorMsg.textContent = '✓ 有效的電子郵件';
    errorMsg.style.color = 'green';
  } else {
    errorMsg.textContent = '✗ 請輸入有效的電子郵件';
    errorMsg.style.color = 'red';
  }
});
```

---

**延伸閱讀**

- [MDN DOM 操作](https://www.google.com/search?q=MDN+DOM+manipulation)
- [MDN 事件參考](https://www.google.com/search?q=MDN+event+reference)
- [JavaScript 事件委派](https://www.google.com/search?q=JavaScript+event+delegation)
