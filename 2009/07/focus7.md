# 瀏覽器相容性與未來展望：前端工程的挑戰與機會

## 2009 年的瀏覽器大戰

### 市場概況

```
2009 年 7 月瀏覽器市場佔有率：

Internet Explorer  ████████████████████████  65%
Firefox            ████████████             22%
Chrome             ███                       3%
Safari             ██                        4%
Opera              █                         2%
其他               █                         4%
```

### 主要瀏覽器版本

| 瀏覽器 | 版本 | 發布日期 | CSS 3 支援 |
|--------|------|----------|------------|
| IE | 8.0 | 2009年3月 | 有限 |
| Firefox | 3.5 | 2009年6月 | 部分 |
| Chrome | 3.0 | 2009年10月 | 部分 |
| Safari | 4.0 | 2009年6月 | 部分 |
| Opera | 10 | 2009年8月 | 部分 |

## 前綴字（PREFIX）的問題

### 前綴字的由來

前綴字是瀏覽器廠商在 CSS 3 規格未穩定前，實驗性地提供新功能的方式：

```css
/* 標準化前 */
-webkit-border-radius: 10px;   /* Chrome, Safari */
-moz-border-radius: 10px;       /* Firefox */
-o-border-radius: 10px;         /* Opera */
-ms-border-radius: 10px;        /* IE */
border-radius: 10px;            /* 標準 */
```

### 2009 年的典型寫法

```css
.button {
  /* 圓角 */
  -webkit-border-radius: 5px;
  -moz-border-radius: 5px;
  border-radius: 5px;

  /* 漸層 */
  -webkit-linear-gradient(top, #4a90e2, #357abd);
  -moz-linear-gradient(top, #4a90e2, #357abd);
  -o-linear-gradient(top, #4a90e2, #357abd);
  linear-gradient(to bottom, #4a90e2, #357abd);

  /* 陰影 */
  -webkit-box-shadow: 0 2px 5px rgba(0,0,0,0.2);
  -moz-box-shadow: 0 2px 5px rgba(0,0,0,0.2);
  box-shadow: 0 2px 5px rgba(0,0,0,0.2);
}
```

### 前綴字的缺點

```
前綴字問題：

1. 程式碼膨脹
   - 每個屬性需要重複 4-5 次

2. 順序敏感
   - 標準屬性應放在最後

3. 版本追蹤困難
   - 何時可以移除前綴？

4. 新屬性需要前綴
   - 開發者需要知道哪些需要

5. 不同廠商支援不同
   - -webkit- 只能在 WebKit 瀏覽器
```

## Polyfill 與 Modernizr

### Modernizr

Modernizr 是一個 JavaScript 庫，用於檢測瀏覽器對 CSS 3 和 HTML 5 特性的支援：

```html
<script src="modernizr.min.js"></script>
```

```css
/* 使用 Modernizr 檢測結果 */
.flexbox .container {
  display: flex;
}

.no-flexbox .container {
  display: table;
}

.cssgradients .header {
  background: linear-gradient(red, blue);
}

.no-cssgradients .header {
  /* 降級：使用圖片 */
  filter: progid:DXImageTransform.Microsoft.gradient(startColorstr='#ff0000', endColorstr='#0000ff');
}
```

### 其他 Polyfill

| 庫 | 功能 | 2009年 |
|----|------|--------|
| html5shiv | HTML 5 新元素 | 是 |
| respond.js | 媒體查詢（IE 8） | 是 |
| CSS PIE | CSS 3 效果（IE 6-8） | 是 |
| selectivizr | CSS 3 選擇器（IE 6-8） | 是 |

### 條件註釋

```html
<!--[if IE 8]>
  <link href="ie8.css" rel="stylesheet">
<![endif]-->

<!--[if lt IE 9]>
  <script src="html5shiv.js"></script>
  <script src="respond.min.js"></script>
<![endif]-->
```

## 漸進增強策略

### 範例：響應式導航

```css
/* 基本：行動裝置（不需要 JS/CSS 3）*/
.nav-list {
  display: block;
}

.nav-item {
  display: block;
  padding: 10px;
}

/* 增強：支援 Flexbox 的瀏覽器 */
@supports (display: flex) {
  .nav-list {
    display: flex;
  }
}

/* 增強：支援媒體查詢的瀏覽器 */
@media screen and (min-width: 768px) {
  .nav-item {
    display: inline-block;
  }
}
```

### 設計模式

```
漸進增強檢查清單：

□ 基本功能是否正常？（無 CSS）
□ 基本樣式是否正常？（CSS 1/2.1）
□ 增強樣式是否正常？（CSS 3）
□ JavaScript 是否必要？
□ 降級方案是否合理？

測試策略：
□ Chrome（WebKit）
□ Firefox（Gecko）
□ Safari（WebKit）
□ Opera（Presto）
□ IE 6/7/8
□ iPhone Safari
□ Android Browser
```

## CSS 3 的未來

### 即將到來的功能

#### CSS Grid Layout

2009 年 CSS Grid 還在早期討論中，但即將成為現實：

```css
.grid-container {
  display: -ms-grid;    /* IE 10 */
  display: grid;
  grid-template-columns: 1fr 2fr 1fr;
  grid-template-rows: auto;
  gap: 20px;
}
```

#### CSS Variables

自訂屬性（CSS Variables）當時仍在提案階段：

```css
:root {
  --primary-color: #3498db;
  --font-size-base: 16px;
}

.button {
  background: var(--primary-color);
  font-size: var(--font-size-base);
}
```

#### 區域設定與書寫模式

```css
/* 從右到左的文字方向 */
[dir="rtl"] .menu {
  direction: rtl;
}

/* 垂直寫作模式 */
.vertical-text {
  writing-mode: vertical-rl;
}
```

### CSS 4 的發展方向

```
CSS 4 規劃中的功能：

1. 父選擇器（:has）
   - header:has(.menu) { }

2. 條件規則（@when/@else）
   - @when media(screen) { }

3. 巢狀規則
   - parent {
     - child { }
   - }

4. 滾動 Snap
   - scroll-snap-type: x mandatory;

5. 容器查詢
   - @container (min-width: 400px) { }
```

## 開發者工具的演进

### 2009 年的工具

| 工具 | 說明 |
|------|------|
| Firebug | Firefox 擴展，JavaScript 調試 |
| Chrome DevTools | 內建，2009 年還很簡陋 |
| Web Inspector | Safari 開發工具 |
| IE Developer Toolbar | IE 8 內建 |

### DevTools 的 CSS 支援

2009 年的 DevTools 對 CSS 3 的支援有限：
- 不顯示前綴字的廠商標誌
- 不支援即時編輯 CSS 3 屬性
- 不提供效能分析

## 結語

2009 年是 CSS 3 開始被廣泛採用的元年。雖然瀏覽器支援仍然不一致，前綴字問題困擾著開發者，但 CSS 3 的未來已經明確。

對於前端開發者來說，這是一個充滿挑戰與機會的時代。掌握 CSS 3、響應式設計、漸進增強等概念，將成為現代網頁開發的基本技能。

---

## 延伸閱讀

- [CSS 3 規格現狀](https://www.google.com/search?q=CSS3+specification+status+2009)
- [Vendor Prefix 討論](https://www.google.com/search?q=vendor+prefix+debate+2009)
- [Modernizr 文件](https://www.google.com/search?q=Modernizr+documentation)
- [CSS 3 前端相容性指南](https://www.google.com/search?q=CSS3+compatibility+guide)

---

*本篇文章為「AI 程式人雜誌 2009 年 7 月號」焦點系列之一。*