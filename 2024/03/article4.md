# 字型、顏色與背景

## CSS 字型系統

### font-family

font-family 定義文字的字型。建議同時指定備用字型：

```css
body {
  font-family: "Noto Sans TC", "Microsoft JhengHei", "PingFang TC",
               system-ui, -apple-system, sans-serif;
}
```

**通用字型分類**：
- `serif`：對線字體（Times New Roman）
- `sans-serif`：無對線字體（Arial, Helvetica）
- `monospace`：等寬字體（Courier New）
- `cursive`：手寫體
- `fantasy`：裝飾體

### font-size

字型大小可以使用多種單位：

```css
h1 { font-size: 2rem; }     /* 相對根元素 */
p  { font-size: 16px; }     /* 固定像素 */
small { font-size: 0.8em; } /* 相對父元素 */
.title { font-size: clamp(1.5rem, 4vw, 3rem); } /* 流體字型 */
```

### font-weight

字型粗細：

```css
.normal { font-weight: 400; }  /* 一般 */
.bold   { font-weight: 700; }  /* 粗體 */
.light  { font-weight: 300; }  /* 細體 */
```

### font-style

```css
.italic { font-style: italic; }   /* 斜體 */
.normal { font-style: normal; }
```

### 文字排版屬性

```css
p {
  line-height: 1.6;           /* 行高 */
  letter-spacing: 0.5px;      /* 字距 */
  text-align: justify;        /* 對齊 */
  text-decoration: none;      /* 裝飾 */
  text-transform: uppercase;  /* 大小寫轉換 */
  text-indent: 2em;           /* 首行縮排 */
}
```

---

## CSS 顏色

### 顏色表示法

CSS 支援多種顏色表示方式：

```css
/* 關鍵字 */
color: red;
color: transparent;

/* HEX */
color: #ff6600;
color: #f60;         /* 簡寫 */
color: #00000033;    /* 含透明度（RGBA HEX） */

/* RGB / RGBA */
color: rgb(255, 102, 0);
color: rgba(255, 102, 0, 0.5);

/* HSL / HSLA */
color: hsl(24, 100%, 50%);
color: hsla(24, 100%, 50%, 0.5);
```

HSL 更接近人類對顏色的直覺理解：
- **H**ue（色調）：0-360 度的色環
- **S**aturation（飽和度）：0-100%
- **L**ightness（亮度）：0-100%

### 顏色變數

使用 CSS 自訂屬性定義顏色：

```css
:root {
  --primary: #007bff;
  --secondary: #6c757d;
  --success: #28a745;
  --danger: #dc3545;
  --warning: #ffc107;
  --info: #17a2b8;
  --light: #f8f9fa;
  --dark: #343a40;
}

.btn-primary {
  background: var(--primary);
  color: white;
}
```

---

## CSS 背景

### background-color

```css
.element {
  background-color: #f0f0f0;
  background-color: transparent;
}
```

### background-image

```css
.element {
  background-image: url("pattern.png");
  background-image: linear-gradient(to right, #ff7e5f, #feb47b);
  background-image: radial-gradient(circle, #fff, #aaa);
}
```

### 漸層背景

```css
/* 線性漸層 */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

/* 徑向漸層 */
background: radial-gradient(circle at center, #f5af19, #f12711);

/* 多重漸層 */
background:
  linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)),
  url("hero.jpg");
```

### background-size

```css
.cover {
  background-size: cover;      /* 覆蓋整個區域 */
}
.contain {
  background-size: contain;    /* 完整顯示 */
}
.custom {
  background-size: 100% auto;  /* 自訂大小 */
}
```

### 背景組合

```css
.hero {
  background: url("bg.jpg") center/cover no-repeat fixed;
  /* 順序：image position/size repeat attachment */
}
```

---

## 外部字型載入

### Google Fonts

```html
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;700&display=swap" rel="stylesheet">
```

```css
body {
  font-family: "Noto Sans TC", sans-serif;
}
```

### @font-face

```css
@font-face {
  font-family: "MyCustomFont";
  src: url("fonts/myfont.woff2") format("woff2"),
       url("fonts/myfont.woff") format("woff");
  font-weight: normal;
  font-style: normal;
  font-display: swap; /* 改善載入體驗 */
}
```

---

## 文字與背景組合最佳實踐

- **對比度**：確保文字與背景有足夠對比，符合 WCAG AA 標準（對比度至少 4.5:1）
- **透明度**：使用 rgba 或透明度屬性時，確保底層顏色不會影響可讀性
- **漸層覆蓋**：背景圖片上方加一層半透明漸層，可提升文字可讀性

---

## 延伸閱讀

- [Google Fonts](https://www.google.com/search?q=Google+Fonts)
- [MDN: CSS 顏色](https://www.google.com/search?q=MDN+CSS+color)
- [Coolors 調色盤生成器](https://www.google.com/search?q=Coolors+color+palette+generator)
- [Color Contrast Checker](https://www.google.com/search?q=web+accessibility+color+contrast+checker)

---

*本篇文章為「AI 程式人雜誌 2024 年 3 月號」精選文章之一。*
