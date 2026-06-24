# HTML5 的新特性：語意標籤、表單強化、Web Storage

## 前言

HTML5 不只是一個版本的更新，而是一次革命。2014 年 10 月，W3C 正式發布 HTML5 推薦標準，為 Web 開發開啟了新紀元。

## 語意標籤的革命

### 為什麼需要語意標籤？

傳統網頁大量使用 `<div>` 堆疊，導致：

```html
<!-- 這樣的結構沒有任何語意意義 -->
<div class="header">
  <div class="nav">...</div>
</div>
<div class="content">
  <div class="article">...</div>
  <div class="sidebar">...</div>
</div>
```

語意標籤讓結構「自帶意義」：

```html
<header>  <!-- 頁面或區塊的標題區 -->
  <nav>   <!-- 導航連結區 -->
</header>
<main>   <!-- 主內容區 -->
  <article>  <!-- 獨立的文章內容 -->
  <aside>    <!-- 側邊欄，相關內容 -->
</main>
<footer>  <!-- 頁腳資訊 -->
```

### 語意標籤的瀏覽器支援（2015 年）

```
語意標籤支援情況（2015 年）：
─────────────────────────────
IE 9+:      部分支援（需要 shim）
IE 10+:     完整支援
Chrome:     完整支援
Firefox:    完整支援
Safari:     完整支援
Mobile:     完整支援
```

### 使用範例

```html
<!DOCTYPE html>
<html lang="zh-TW">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>我的部落格</title>
</head>
<body>
  <header>
    <h1>我的部落格</h1>
    <nav>
      <ul>
        <li><a href="/">首頁</a></li>
        <li><a href="/about">關於</a></li>
        <li><a href="/contact">聯絡</a></li>
      </ul>
    </nav>
  </header>

  <main>
    <article>
      <header>
        <h2>HTML5 語意標籤詳解</h2>
        <time datetime="2015-01-15">2015年1月15日</time>
      </header>
      <p>本文介紹 HTML5 的語意標籤...</p>
      <section>
        <h3>header 標籤</h3>
        <p>header 可以包含整個頁面的標題...</p>
      </section>
      <footer>
        <p>作者：陳小明</p>
      </footer>
    </article>
  </main>

  <footer>
    <p>&copy; 2015 我的部落格</p>
  </footer>
</body>
</html>
```

## 表單強化與驗證

### 新的輸入類型

HTML5 為 `<input>` 標籤引入了許多新的 type 屬性：

```html
<!-- 傳統表單 -->
<input type="text" name="email">

<!-- HTML5 新類型 -->
<input type="email"    name="email"    placeholder="example@mail.com">
<input type="url"      name="website"  placeholder="https://...">
<input type="tel"       name="phone"    placeholder="09xx-xxx-xxx">
<input type="number"    name="age"      min="0" max="150">
<input type="range"     name="volume"   min="0" max="100">
<input type="date"      name="birthday">
<input type="color"     name="favcolor">
<input type="search"    name="query"    results="5">
<input type="datetime-local" name="meeting">
<input type="month"     name="birthmonth">
<input type="week"      name="vacation-week">
```

### 原生驗證屬性

```html
<input type="text" required>
<input type="email" required pattern="[a-z]+@[a-z]+\.[a-z]+">
<input type="url"   required>
<input type="number" min="0" max="100" step="0.01">

<!-- 自訂錯誤訊息 -->
<input type="text"
       required
       pattern="[A-Za-z]{3,}"
       title="請輸入至少3個字母">
```

### 表單驗證 API

```javascript
// 檢查表單是否有效
document.querySelector('form').checkValidity();

// 驗證特定欄位
const email = document.querySelector('input[type="email"]');
if (!email.validity.valid) {
  console.log('驗證失敗:', email.validationMessage);
}

// 自訂驗證訊息
email.setCustomValidity('請輸入有效的電子郵件地址');

// 驗證狀態
console.log(email.validity.valueMissing);    // 必填但空白
console.log(email.validity.typeMismatch);     // 類型不符
console.log(email.validity.patternMismatch); // 格式不符
console.log(email.validity.tooLong);          // 太長
console.log(email.validity.rangeUnderflow);  // 低於最小值
```

## Web Storage 客戶端儲存

### localStorage vs sessionStorage

```javascript
// localStorage - 永久儲存
localStorage.setItem('username', 'John');
localStorage.setItem('theme', 'dark');
const username = localStorage.getItem('username');
localStorage.removeItem('username');
localStorage.clear(); // 清除所有

// sessionStorage - 會話期間儲存
sessionStorage.setItem('tempData', 'some value');
const temp = sessionStorage.getItem('tempData');
// 瀏覽器關閉後自動清除

// 支援 JSON 序列化
const user = { name: 'John', age: 30 };
localStorage.setItem('user', JSON.stringify(user));
const savedUser = JSON.parse(localStorage.getItem('user'));
```

### localStorage 的限制與注意事項

```
localStorage 規格：
──────────────────
容量限制：約 5-10 MB（瀏覽器依賴）
資料類型：僅支援字串
跨域隔離：同源策略
安全考量：勿儲存敏感資訊
生命週期：永久（除非手動清除）

2015 年支援情況：
──────────────────
IE 8+:     完整支援
所有現代瀏覽器：完整支援
行動瀏覽器：完整支援
```

### 實用範例：主題切換

```javascript
// 儲存使用者偏好
function setTheme(theme) {
  document.body.className = theme;
  localStorage.setItem('theme', theme);
}

function loadTheme() {
  const saved = localStorage.getItem('theme');
  if (saved) {
    document.body.className = saved;
  }
}

// 初始化
loadTheme();

// 事件監聽
document.getElementById('theme-toggle').addEventListener('click', () => {
  const current = document.body.className;
  setTheme(current === 'dark' ? 'light' : 'dark');
});
```

## 其他重要的 HTML5 API

### Drag and Drop API

```javascript
const draggable = document.querySelector('.item');
const dropzone = document.querySelector('.dropzone');

draggable.addEventListener('dragstart', (e) => {
  e.dataTransfer.setData('text/plain', e.target.id);
  e.dataTransfer.effectAllowed = 'move';
});

dropzone.addEventListener('dragover', (e) => {
  e.preventDefault(); // 必要！允許 drop
  e.dataTransfer.dropEffect = 'move';
});

dropzone.addEventListener('drop', (e) => {
  e.preventDefault();
  const id = e.dataTransfer.getData('text/plain');
  const element = document.getElementById(id);
  dropzone.appendChild(element);
});
```

### 地理位置 API

```javascript
if ('geolocation' in navigator) {
  navigator.geolocation.getCurrentPosition(
    (position) => {
      const { latitude, longitude } = position.coords;
      console.log(`位置：${latitude}, ${longitude}`);
    },
    (error) => {
      console.error('取得位置失敗:', error.message);
    },
    {
      enableHighAccuracy: true,
      timeout: 5000,
      maximumAge: 0
    }
  );
}
```

### 檔案 API

```javascript
const fileInput = document.querySelector('input[type="file"]');

fileInput.addEventListener('change', (e) => {
  const file = e.target.files[0];
  const reader = new FileReader();

  reader.onload = (event) => {
    const content = event.target.result;
    console.log('檔案內容:', content);
  };

  reader.readAsText(file);
});
```

## 結語

HTML5 不僅是標籤的更新，更代表了 Web 開發的現代化。語意標籤讓結構更清晰、表單驗證讓開發更簡便、Web Storage 讓客戶端儲存更強大。

---

## 延伸閱讀

- [MDN HTML5 指南](https://www.google.com/search?q=MDN+HTML5+semantic+elements)
- [HTML5 表單驗證](https://www.google.com/search?q=HTML5+form+validation+api)
- [Web Storage API](https://www.google.com/search?q=Web+Storage+API+localStorage+sessionStorage)

---

*本篇文章為「AI 程式人雜誌 2015 年 1 月號」歷史回顧系列之一。*