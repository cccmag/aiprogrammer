# Chrome 與網頁標準

## 網頁標準的重要性

### 為何需要標準？

```python
web_standards_importance = {
    "跨瀏覽器": "同一份程式碼在各瀏覽器都能運作",
    "長期維護": "標準化的程式碼更易維護",
    "可近性": "殘疾人士也能使用",
    "未來相容": "遵循標準的網站能持久"
}
```

### 主要標準組織

```python
standards_bodies = {
    "W3C": "World Wide Web Consortium，主要標準制定者",
    "WHATWG": "Web Hypertext Application Technology Working Group",
    "ECMA International": "負責 ECMAScript (JavaScript)",
    "IETF": "負責 HTTP 等網路協定"
}
```

## HTML 5 支援

### Chrome 的 HTML 5 策略

```python
chrome_html5_strategy = {
    "優先實作": "優先實作被廣泛支援的功能",
    "新標籤": "支援 section, article, nav, aside 等",
    "表單增強": "新的 input 類型和驗證 API",
    "離線支援": "Application Cache, Web Storage"
}
```

### HTML 5 新元素

```html
<!-- 結構化標籤 -->
<header>頁首</header>
<nav>導航選單</nav>
<main>主要內容</main>
<article>文章內容</article>
<section>章節</section>
<aside>側邊欄</aside>
<footer>頁尾</footer>

<!-- 媒體標籤 -->
<video src="video.mp4" controls></video>
<audio src="music.mp3" controls></audio>

<!-- 互動標籤 -->
<detail>
    <summary>點擊展開</summary>
    這是隱藏的內容
</detail>
```

### 表單增強

```html
<!-- 新的 input 類型 -->
<input type="email" placeholder="請輸入 email">
<input type="url" placeholder="請輸入網址">
<input type="date" value="2025-01-15">
<input type="range" min="0" max="100">
<input type="color" value="#ff0000">

<!-- 驗證屬性 -->
<input type="text" required pattern="[A-Za-z]{3}">
<input type="email" multiple>

<!-- 資料清單 -->
<input list="browsers">
<datalist id="browsers">
    <option value="Chrome">
    <option value="Firefox">
    <option value="Safari">
</datalist>
```

## CSS 支援

### CSS 3 模組

```python
css3_modules = {
    "Selectors": "更豐富的選擇器",
    "Box Model": "彈性盒子和網格佈局",
    "Colors": "HSLA、RGBA、opacity",
    "Backgrounds": "多背景、圓角背景圖",
    "Text Effects": "文字陰影、換行處理",
    "Transforms": "2D/3D 變換",
    "Animations": "動畫和過渡效果",
    "Transitions": "平滑過渡"
}
```

### 彈性盒子和網格

```css
/* Flexbox 範例 */
.container {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

/* Grid 範例 */
.grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
}
```

### 動畫

```css
/* 過渡效果 */
.button {
    transition: background-color 0.3s ease, transform 0.2s;
}

.button:hover {
    background-color: #ff6600;
    transform: scale(1.05);
}

/* 動畫 */
@keyframes slideIn {
    from {
        transform: translateX(-100%);
    }
    to {
        transform: translateX(0);
    }
}

.animated {
    animation: slideIn 0.5s ease-out;
}
```

## JavaScript 標準

### ECMAScript 版本

```python
ecmascript_versions = {
    "ES3 (1999)": "JavaScript 1.5，基礎功能",
    "ES4 (2008 放棄)": "原本要大改，最後失敗",
    "ES5 (2009)": "Strict mode、JSON、更多陣列方法",
    "ES6/ES2015 (2015)": "類、箭頭函式、Promise、模組",
    "ES2016+": "每年小版本更新"
}
```

### V8 的 ES 支援

```javascript
// Chrome 對新語法的支援（2008 年仍是 ES5 時代）

// 2008 年 Chrome 支援
var obj = {
    name: "test",
    value: 42
};

// 陣列方法
[1, 2, 3].forEach(function(x) {
    console.log(x);
});

var squared = [1, 2, 3].map(function(x) {
    return x * x;
});

// JSON 支援
var json = JSON.parse('{"name": "test"}');
var str = JSON.stringify({name: "test"});
```

## DOM 標準

### DOM 支援

```python
dom_standards = {
    "DOM Core": "文件物件模型核心",
    "DOM Views": "檢視和樣式",
    "DOM Events": "事件處理",
    "DOM Traversal": "節點遍歷",
    "DOM Range": "範圍選擇"
}
```

### DOM 遍歷

```javascript
// 查詢元素
document.getElementById("id");
document.querySelector(".class");
document.querySelectorAll("div > p");

// 遍歷
var parent = element.parentNode;
var children = element.childNodes;
var next = element.nextSibling;
```

## 網頁 API

### 重要的 Web API

```python
web_apis = {
    "Canvas 2D": "2D 繪圖 API",
    "WebGL": "3D 圖形（基於 OpenGL ES）",
    "Web Storage": "localStorage 和 sessionStorage",
    "Web Workers": "背景執行緒",
    "Geolocation": "位置資訊",
    "Drag and Drop": "拖放 API",
    "History API": "瀏覽歷史操作",
    "Notifications": "桌面通知"
}
```

### Canvas 範例

```javascript
var canvas = document.getElementById("myCanvas");
var ctx = canvas.getContext("2d");

// 繪製矩形
ctx.fillStyle = "#ff0000";
ctx.fillRect(10, 10, 100, 100);

// 繪製文字
ctx.font = "24px Arial";
ctx.fillText("Hello", 20, 50);

// 繪製路徑
ctx.beginPath();
ctx.moveTo(0, 0);
ctx.lineTo(100, 100);
ctx.stroke();
```

## WebGL

### 3D 圖形

```python
webgl_info = {
    "基礎": "基於 OpenGL ES 2.0",
    "用途": "遊戲、資料視覺化、3D 體驗",
    "複雜度": "需要較多程式碼",
    "替代": "Three.js 等函式庫簡化開發"
}
```

## SVG 支援

### 向量圖形

```python
svg_support = {
    "格式": "Scalable Vector Graphics",
    "優點": "任意縮放不失真",
    "互動": "可與 JavaScript 和 CSS 互動",
    "動畫": "可使用 SMIL 或 JavaScript 動畫"
}
```

```html
<svg width="200" height="200">
    <circle cx="100" cy="100" r="80" fill="#3498db"/>
    <rect x="50" y="50" width="100" height="100" fill="#e74c3c"/>
</svg>
```

## 媒體 API

### 影音支援

```python
media_apis = {
    "HTML5 Video": "<video> 標籤和 JavaScript API",
    "HTML5 Audio": "<audio> 標籤和 JavaScript API",
    "MediaStream": "從攝影機和麥克風獲取串流",
    "WebRTC": "點對點通訊"
}
```

### Video API

```javascript
var video = document.querySelector("video");

video.play();
video.pause();
video.currentTime = 10;  // 跳到 10 秒
video.volume = 0.5;     // 音量 50%

// 事件
video.addEventListener("ended", function() {
    console.log("播放完畢");
});
```

## 標準測試

### Acid 測試

```python
acid_tests = {
    "Acid1": "1999 年，測試基本 CSS/HTML",
    "Acid2": "2001 年，更嚴格的 CSS 和 PNG 測試",
    "Acid3": "2008 年，DOM、DOM Events、HTML5、CSS 等"
}
```

### Can I Use

```python
compatibility_check = {
    "網站": "caniuse.com",
    "用途": "查詢各瀏覽器對 HTML5/CSS3/JS API 的支援",
    "更新": "持續更新最新的支援資訊"
}
```

## 標準化過程

### W3C 流程

```python
w3c_process = {
    "1. Editor's Draft": "編輯者草案，最初始的規範",
    "2. Working Draft": "工作草案，W3C 內部審查",
    "3. Candidate Recommendation": "候選建議書，公開測試",
    "4. Proposed Recommendation": "提議建議書，最終審查",
    "5. Recommendation": "正式 W3C 建議書，標準完成"
}
```

### 先行實作

```python
implementation_first = {
    "好處": "在標準定案前就能使用新功能",
    "風險": "規範可能改變導致相容性問題",
    "建議": "產品功能可用，謹慎用於核心功能"
}
```

---

**延伸閱讀**

- [Chrome+HTML5+support](https://www.google.com/search?q=Chrome+HTML5+support)
- [Web+standards+compatibility](https://www.google.com/search?q=Web+standards+compatibility)
- [CSS3+browser+support](https://www.google.com/search?q=CSS3+browser+support)