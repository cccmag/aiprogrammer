# CSS3 選擇器與偽類：更強大的 DOM 選取

## CSS 選擇器的歷史

### CSS 1 與 CSS 2.1 選擇器

在 CSS 3 之前，常用的選擇器相對簡單：

| 選擇器 | 範例 | 說明 |
|--------|------|------|
| 標籤選擇器 | p | 所有 \<p\> 元素 |
| 類別選擇器 | .intro | class="intro" |
| ID 選擇器 | #header | id="header" |
| 後代選擇器 | div p | div 內的所有 \<p\> |
| 子選擇器 | div > p | div 的直接 \<p\> 子元素 |
| 屬性選擇器 | a[href] | 有 href 屬性的 \<a\> |

### CSS 3 的選擇器擴展

CSS 3 大幅擴展了選擇器的能力，引入了：
- 進階屬性選擇器
- 結構性偽類
- 偽元素
- UI 狀態偽類

## 屬性選擇器

### 基本屬性選擇器

```css
/* 有屬性 */
a[target] { }

/* 屬性等於值 */
a[href="https://example.com"] { }

/* 屬性包含值（空白分隔）*/
[class~="button"] { }

/* 屬性以值開頭（連字符分隔）*/
[lang|="zh"] { }

/* 屬性開頭匹配 */
[href^="https"] { }

/* 屬性結尾匹配 */
[href$=".pdf"] { }

/* 屬性包含子字串 */
[href*="example"] { }
```

### 實用範例

```css
/* 外部連結 */
a[href^="http"]::after {
  content: " (外部連結)";
}

/* PDF 下載連結 */
a[href$=".pdf"]::before {
  content: "📄 ";
}

/* 電子郵件連結 */
a[href^="mailto"]::before {
  content: "✉ ";
}

/* 電話連結 */
a[href^="tel"]::before {
  content: "📞 ";
}

/* 圖片連結 */
a[href*=".jpg"],
a[href*=".png"],
a[href*=".gif"] {
  /* 圖片預覽樣式 */
}
```

## 結構性偽類

### :nth-child 選擇器

```css
/* 第 N 個子元素 */
li:nth-child(3) { }              /* 第三個 */
li:nth-child(odd) { }            /* 奇數 */
li:nth-child(even) { }           /* 偶數 */
li:nth-child(3n) { }             /* 每 3 個 */
li:nth-child(3n+1) { }           /* 3 的倍數加 1 */
li:nth-child(-n+5) { }          /* 前 5 個 */

/* 範例：斑馬紋表格 */
tr:nth-child(odd) {
  background: #f2f2f2;
}
```

### :nth-child 參數解析

```
公式：:nth-child(an+b)

a = 循環大小
n = 從 0 開始的計數
b = 偏移量

常見用法：
- :nth-child(2)      = 第2個
- :nth-child(3n)     = 3, 6, 9, 12, ...
- :nth-child(3n+1)   = 1, 4, 7, 10, ...
- :nth-child(-n+3)   = 1, 2, 3
- :nth-child(n+4)    = 4, 5, 6, ...
- :nth-child(2n)     = 偶數 = even
- :nth-child(2n+1)   = 奇數 = odd
```

### 其他結構性偽類

```css
/* 第一個/最後一個子元素 */
li:first-child { }   /* 父元素的第一個子元素 */
li:last-child { }    /* 父元素的最後一個子元素 */

/* 唯一子元素 */
li:only-child { }     /* 父元素只有一個子元素時 */

/* 首個/末個同類型元素 */
p:first-of-type { }   /* 每個容器中第一個 \<p\> */
p:last-of-type { }    /* 每個容器中最後一個 \<p\> */

/* 唯一同類型元素 */
p:only-of-type { }    /* 同類型中唯一的元素 */

/* 空元素 */
div:empty { }         /* 完全空白的元素 */
```

### :not() 否定偽類

```css
/* 選取不是某類的元素 */
input:not([type="submit"]) { }

/* 選取除了第一個之外的元素 */
li:not(:first-child) { }

/* 選取不包含連結的元素 */
div:not(.external) a { }
```

### :first-child vs :first-of-type

```html
<div>
  <span>Span 1</span>
  <p>Paragraph</p>
  <p>Paragraph</p>
</div>
```

```css
/* :first-child：父元素的第一個孩子 */
p:first-child { }  /* 選不到任何元素，因為第一個孩子是 span */

/* :first-of-type：父元素中同類型的第一個 */
p:first-of-type { }  /* 選取第一個 \<p\> */
```

## 偽元素

###  ::before 與 ::after

```css
/* 插入內容在元素之前 */
h1::before {
  content: "★ ";
  color: gold;
}

/* 插入內容在元素之後 */
h1::after {
  content: " ★";
  color: gold;
}
```

### ::first-line 與 ::first-letter

```css
/* 第一行文字 */
p::first-line {
  font-weight: bold;
  text-transform: uppercase;
}

/* 第一個字母 */
p::first-letter {
  font-size: 3em;
  float: left;
  line-height: 1;
  margin-right: 0.1em;
}
```

### ::selection

```css
/* 使用者選取的文字 */
::selection {
  background: yellow;
  color: black;
}

/* Firefox */
::-moz-selection {
  background: yellow;
  color: black;
}
```

## UI 狀態偽類

### 表單相關偽類

```css
/* 聚焦狀態 */
input:focus {
  border-color: blue;
  box-shadow: 0 0 5px rgba(0,0,255,0.3);
}

/* 啟用/禁用 */
input:enabled { }
input:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* 唯讀 */
input:read-only { }
input:read-write { }

/* 勾選的核取方塊 */
input:checked + label {
  font-weight: bold;
}

/* 不確定狀態（progress bar）*/
progress:indeterminate { }
```

### 連結相關偽類

```css
/* 未訪問 */
a:link { }

/* 已訪問 */
a:visited { }

/* 懸停 */
a:hover { }

/* 聚焦 */
a:focus { }

/* 點擊 */
a:active { }

/* 順序很重要 */
a:link { }
a:visited { }
a:hover { }
a:focus { }
a:active { }
```

### 語義偽類

```css
/* 根元素 */
:root {
  /* 整個文檔的最高層級 */
}

/* 空白文字節點 */
p:empty {
  display: none;
}
```

## 綜合範例

### 層次選單

```css
/* 選單結構 */
nav > ul > li { }           /* 第一層 */
nav > ul > li > a { }       /* 第一層連結 */
nav li ul li { }            /* 第二層以下 */

/* 斑馬紋 */
.menu > li:nth-child(odd) {
  background: #f5f5f5;
}
.menu > li:nth-child(even) {
  background: #ffffff;
}
```

### 表格樣式

```css
/* 斑馬紋表格 */
table tr:nth-child(odd) {
  background: #f9f9f9;
}

/* 最後一行不加邊框 */
table tr:last-child {
  border-bottom: none;
}

/* 滑鼠懸停效果 */
table tr:hover {
  background: #f0f0f0;
}

/* 聚焦的儲存格 */
table td:focus {
  background: #fffde7;
  outline: 2px solid blue;
}
```

### 表單驗證樣式

```css
/* 必填欄位標記 */
input:required::after {
  content: " *";
  color: red;
}

/* 有效/無效輸入 */
input:valid {
  border-color: green;
}

input:invalid {
  border-color: red;
}

/* 輸入框內圖示 */
.input-icon {
  position: relative;
}

.input-icon::after {
  content: "";
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
}

.input-icon:invalid::after {
  background: url("warning.svg");
}

.input-icon:valid::after {
  background: url("check.svg");
}
```

## 瀏覽器支援（2009年）

### 選擇器支援矩陣

| 選擇器 | Firefox | Safari | Chrome | Opera |
|--------|---------|--------|--------|-------|
| [attr^=val] | 1.0+ | 1.0+ | 1.0+ | 9.0+ |
| [attr$=val] | 1.0+ | 1.0+ | 1.0+ | 9.0+ |
| [attr*=val] | 1.0+ | 1.0+ | 1.0+ | 9.0+ |
| :nth-child | 3.5+ | 3.1+ | 1.0+ | 9.5+ |
| :first-of-type | 3.5+ | 3.1+ | 1.0+ | 9.5+ |
| :not() | 3.5+ | 3.1+ | 1.0+ | 9.5+ |
| ::selection | 1.0+ | 1.0+ | 1.0+ | 9.5+ |

### Polyfill

```javascript
// IE 7/8 不支援 CSS 3 選擇器
// 可以使用 Selectivizr 或 ie9.js
```

## 結語

CSS 3 的選擇器大幅增強了 DOM 選取的能力，讓我們可以用更精確、更表達式的方式選取元素。從簡單的屬性選擇到複雜的結構性偽類，這些工具減少了對 JavaScript 和額外 class 的依賴。

下一篇文章將討論瀏覽器相容性問題與 CSS 的未來展望。

---

## 延伸閱讀

- [CSS3 Selectors 規格](https://www.google.com/search?q=CSS3+selectors+specification+W3C)
- [CSS 選擇器參考](https://www.google.com/search?q=CSS+selectors+complete+guide)
- [jQuery 選擇器與 CSS 選擇器](https://www.google.com/search?q=jQuery+selectors+CSS+selectors)
- [CSS 選擇器效能](https://www.google.com/search?q=CSS+selector+performance)

---

*本篇文章為「AI 程式人雜誌 2009 年 7 月號」焦點系列之一。*