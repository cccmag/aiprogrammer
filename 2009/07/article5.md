# CSS 3 在主流瀏覽器的採用状況

## 前言

2009 年是 CSS 3 開始被廣泛採用的元年。主流瀏覽器廠商開始積極實作 CSS 3 模組，但支援程度不一，前綴字仍然是必要的小惱。

## 各瀏覽器的 CSS 3 支援（2009年）

### Firefox 3.5

Firefox 3.5 於 2009 年 6 月發布，帶來了多項 CSS 3 支援：

```css
/* text-shadow */
.title {
  text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
}

/* opacity */
.overlay {
  opacity: 0.5;
}

/* rgba 顏色 */
.highlight {
  background: rgba(52, 152, 219, 0.3);
}

/* word-wrap */
.long-word {
  word-wrap: break-word;
}

/* @font-face 改善 */
@font-face {
  font-family: 'MyFont';
  src: url('font.woff') format('woff');
}
```

### Safari 4.0

Safari 4.0 於 2009 年 6 月發布，增強了 CSS 3 支援：

```css
/* transform */
.rotated {
  -webkit-transform: rotate(45deg);
}

/* transition */
.button {
  -webkit-transition: all 0.3s ease;
}

/* animation */
@keyframes slideIn {
  from { transform: translateX(-100%); }
  to { transform: translateX(0); }
}

.animated {
  -webkit-animation: slideIn 0.5s ease;
}

/* @font-face (Web Fonts) */
@import url(http://fonts.googleapis.com/css?family=Droid+Sans);
```

### Chrome 3.0

Chrome 在 2009 年繼續擴展 CSS 3 支援：

```css
/* border-radius */
.card {
  -webkit-border-radius: 8px;
}

/* box-shadow */
.modal {
  -webkit-box-shadow: 0 4px 8px rgba(0,0,0,0.3);
}

/* gradient */
.gradient-bg {
  background: -webkit-gradient(linear, left top, left bottom,
    from(#3498db), to(#2980b9));
}
```

### Opera 10

Opera 10 於 2009 年 8 月發布，領先支援部分 CSS 3 功能：

```css
/* 率先支援的屬性 */
.border-radius {
  border-radius: 10px;
}

.text-shadow {
  text-shadow: 1px 1px 2px #333;
}

.box-shadow {
  box-shadow: 0 2px 5px rgba(0,0,0,0.3);
}
```

### Internet Explorer 8

IE 8 在 2009 年 3 月發布，但 CSS 3 支援非常有限：

```css
/* IE 8 支援的 CSS 3 */
[data-*] { }              /* 屬性選擇器 */
:first-child { }          /* :first-child */
col { }                   /* 表格欄位選擇器 */
q { quotes: "«" "»"; }    /* 雙引號 */
```

## 主要 CSS 3 模組的支援狀況

### Selectors Module

| 選擇器 | Firefox | Safari | Chrome | Opera | IE |
|--------|---------|--------|--------|-------|----|
| [attr^=val] | 1.0+ | 1.0+ | 1.0+ | 9.0+ | 7.0+ |
| [attr$=val] | 1.0+ | 1.0+ | 1.0+ | 9.0+ | 7.0+ |
| :nth-child() | 3.5+ | 3.1+ | 1.0+ | 9.5+ | - |
| :first-of-type | 3.5+ | 3.1+ | 1.0+ | 9.5+ | - |
| :not() | 3.5+ | 3.1+ | 1.0+ | 9.5+ | - |

### Visual Effects Module

| 屬性 | Firefox | Safari | Chrome | Opera | IE |
|------|---------|--------|--------|-------|----|
| border-radius | - | 3.0+ | 1.0+ | 10.5+ | 9.0+ |
| box-shadow | 3.5+ | 3.0+ | 1.0+ | 10.5+ | - |
| text-shadow | 3.5+ | 3.1+ | 1.0+ | 9.0+ | - |
| opacity | 1.0+ | 1.0+ | 1.0+ | 9.0+ | 9.0+ |

### Color Module

| 屬性 | Firefox | Safari | Chrome | Opera | IE |
|------|---------|--------|--------|-------|----|
| rgba() | 3.0+ | 3.1+ | 1.0+ | 9.0+ | 9.0+ |
| hsl() | 3.0+ | 3.1+ | 1.0+ | 9.0+ | 9.0+ |
| hsla() | 3.0+ | 3.1+ | 1.0+ | 9.5+ | - |

### Backgrounds Module

| 屬性 | Firefox | Safari | Chrome | Opera | IE |
|------|---------|--------|--------|-------|----|
| multiple backgrounds | 3.5+ | 3.1+ | 1.0+ | 10.5+ | - |
| background-size | - | 3.1+ | 1.0+ | 9.5+ | - |

### Text Module

| 屬性 | Firefox | Safari | Chrome | Opera | IE |
|------|---------|--------|--------|-------|----|
| word-wrap | 3.5+ | 3.1+ | 1.0+ | 10.0+ | 5.5+ |
| text-overflow | - | 3.1+ | 1.0+ | 9.0+ | 6.0+ |

## 前綴字的實踐

### 2009 年的標準寫法

```css
/* 圓角：幾乎所有瀏覽器都需要前綴 */
.round-box {
  -webkit-border-radius: 8px;
  -moz-border-radius: 8px;
  border-radius: 8px;
}

/* 陰影：部分瀏覽器需要前綴 */
.shadow-box {
  -webkit-box-shadow: 0 4px 8px rgba(0,0,0,0.2);
  -moz-box-shadow: 0 4px 8px rgba(0,0,0,0.2);
  box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}

/* 漸層：每個瀏覽器語法都不同 */
.gradient-box {
  background: -webkit-gradient(linear, left top, left bottom,
    from(#3498db), to(#2980b9));
  background: -moz-linear-gradient(top, #3498db, #2980b9);
  background: -o-linear-gradient(top, #3498db, #2980b9);
  background: linear-gradient(to bottom, #3498db, #2980b9);
}
```

### 前綴字順序

```css
/* 順序很重要：標準屬性應放在最後 */
.element {
  /* 前綴版本先寫 */
  -webkit-border-radius: 5px;
  -moz-border-radius: 5px;
  /* 標準版本最後 */
  border-radius: 5px;
}
```

## 漸進增強的策略

### 範例：響應式卡片

```css
/* 基本樣式（所有瀏覽器） */
.card {
  padding: 20px;
  border: 1px solid #ddd;
}

/* CSS 3 增強（支援的瀏覽器） */
.card {
  -webkit-border-radius: 8px;
  -moz-border-radius: 8px;
  border-radius: 8px;

  -webkit-box-shadow: 0 2px 5px rgba(0,0,0,0.1);
  -moz-box-shadow: 0 2px 5px rgba(0,0,0,0.1);
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}
```

### Modernizr 檢測

```html
<script src="modernizr.min.js"></script>
<script>
if (Modernizr.borderradius) {
  // 支援 border-radius
  document.documentElement.classList.add('borderradius');
} else {
  // 使用圖片或插件
  document.documentElement.classList.add('no-borderradius');
}
</script>
```

```css
.no-borderradius .card {
  /* 使用背景圖片模擬圓角 */
  background: url('card-corners.png') no-repeat;
}
```

## CSS 3 採用的挑戰

### 2009 年的主要挑戰

```markdown
CSS 3 採用挑戰：

1. 前綴字過多
   - 每個屬性需要 4-5 行
   - 維護困難

2. 規格不穩定
   - 語法可能改變
   - 瀏覽器支援不一致

3. IE 支援不足
   - IE 8 不支援大部分 CSS 3
   - 需要降級方案

4. 缺少工具
   - 沒有好的 CSS 3 編輯器支援
   - 除錯困難
```

## 結語

2009 年是 CSS 3 開始被廣泛採用的開始。雖然前綴字和瀏覽器不一致帶來了小惱，但 CSS 3 帶來的強大功能讓開發者願意擁抱這些挑戰。

## 延伸閱讀

- [CSS 3 規格現狀](https://www.google.com/search?q=CSS3+specification+status+2009)
- [Can I Use 網站](https://www.google.com/search?q=caniuse+CSS3+2009)
- [CSS 3 前綴字參考](https://www.google.com/search?q=CSS3+vendor+prefix+reference)
- [CSS 3 瀏覽器支援矩陣](https://www.google.com/search?q=CSS3+browser+compatibility+matrix+2009)

---

*本篇文章為「AI 程式人雜誌 2009 年 7 月號」文章系列之一。*