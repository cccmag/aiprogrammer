# 媒體查詢與響應式設計：從桌面到行動裝置

## 響應式設計的興起

### 2009：行動網頁的元年

2009 年是智慧手機普及的關鍵年份。iPhone 已經上市兩年，Android 系統開始快速成長。然而，大多数網站仍然是針對桌面瀏覽器設計的，在手機上的體驗很差。

```
2009 年裝置解析度分布：

桌面：
┌────────────────────────────────────────────┐
│ 1024x768    ████████████████████  30%      │
│ 1280x800    ██████████████████    25%      │
│ 1440x900    ██████████████        20%      │
│ 其他        ████████████           25%      │
└────────────────────────────────────────────┘

行動：
┌────────────────────────────────────────────┐
│ 320x480     ██████████████████████████ 60% │
│ 480x320     ████████████████        30%   │
│ 其他        ████████                  10%  │
└────────────────────────────────────────────┘
```

問題在於：設計一個針對 1024px 寬度優化的網站，在 320px 的手機螢幕上幾乎無法使用。

### Ethan Marcotte 與響應式設計

2009 年，網頁設計師 Ethan Marcotte 在 A List Apart 發表了「Responsive Web Design」文章，首次提出了「響應式設計」的概念。

響應式設計的核心思想：**一個網站，適配所有裝置**。

## 媒體查詢（Media Queries）

### 基本語法

```css
/* 全部螢幕 */
body {
  font-size: 16px;
}

/* 螢幕宽度小於 768px */
@media screen and (max-width: 768px) {
  body {
    font-size: 14px;
  }
}

/* 螢幕宽度小於 480px */
@media screen and (max-width: 480px) {
  body {
    font-size: 12px;
  }
}
```

### 媒體類型

| 類型 | 說明 |
|------|------|
| all | 所有裝置 |
| screen | 螢幕 |
| print | 印表機 |
| tv | 電視 |
| handheld | 掌上型裝置 |

### 媒體特性

```css
/* 最小宽度 */
@media screen and (min-width: 768px) { }

/* 最大宽度 */
@media screen and (max-width: 768px) { }

/* 設備宽度 */
@media screen and (device-width: 320px) { }

/* 橫向模式 */
@media screen and (orientation: landscape) { }

/* 縱向模式 */
@media screen and (orientation: portrait) { }

/* 像素密度 */
@media screen and (-webkit-min-device-pixel-ratio: 2) { }
```

### AND 與 OR

```css
/* AND 條件 */
@media screen and (min-width: 768px) and (max-width: 1024px) {
  .container {
    width: 750px;
  }
}

/* OR 條件（逗號分隔）*/
@media screen and (min-width: 768px),
print and (color) {
  .container {
    width: 750px;
  }
}

/* NOT 條件 */
@media not screen {
  .hide-on-print {
    display: none;
  }
}
```

## 響應式設計實踐

### 行動優先（Mobile First）

```css
/* 預設：手機樣式 */
.container {
  padding: 10px;
}

/* 平板及以上 */
@media screen and (min-width: 768px) {
  .container {
    padding: 20px;
  }
}

/* 桌面及以上 */
@media screen and (min-width: 1024px) {
  .container {
    padding: 30px;
    max-width: 1200px;
  }
}
```

### 響應式佈局

```css
/* 桌面：三欄 */
.container {
  display: flex;
}

.column {
  flex: 1;
}

/* 平板：兩欄 */
@media screen and (max-width: 768px) {
  .container {
    flex-wrap: wrap;
  }
  .sidebar {
    flex: 0 0 100%;
  }
  .main {
    flex: 0 0 100%;
  }
}

/* 手機：單欄 */
@media screen and (max-width: 480px) {
  .column {
    flex: 0 0 100%;
  }
}
```

### 響應式圖片

```css
/* 方法1：max-width */
img {
  max-width: 100%;
  height: auto;
}

/* 方法2：picture 元素（較新）*/
.picture-source {
  display: none;
}

@media screen and (min-width: 768px) {
  .desktop-image {
    display: block;
  }
  .mobile-image {
    display: none;
  }
}
```

### 字體響應式

```css
html {
  font-size: 16px;
}

@media screen and (max-width: 768px) {
  html {
    font-size: 14px;
  }
}

@media screen and (max-width: 480px) {
  html {
    font-size: 12px;
  }
}

h1 {
  font-size: 2rem;  /* 桌面：32px，手機：24px */
}

p {
  font-size: 1rem;  /* 桌面：16px，手機：12-14px */
}
```

## 響應式設計模式

### 流動佈局（Fluid Grid）

```css
/* 使用百分比而非固定像素 */
.column-1 { width: 25%; }
.column-2 { width: 50%; }
.column-3 { width: 75%; }
.column-4 { width: 100%; }
```

### 欄位系統

```css
/* 12欄系統 */
.col-1 { width: 8.33%; }
.col-2 { width: 16.66%; }
.col-3 { width: 25%; }
.col-4 { width: 33.33%; }
.col-6 { width: 50%; }
.col-12 { width: 100%; }

[class*="col-"] {
  float: left;
  padding: 0 10px;
  box-sizing: border-box;
}
```

### 隱藏與顯示

```css
/* 桌面顯示，手機隱藏 */
.desktop-only {
  display: block;
}
.mobile-only {
  display: none;
}

@media screen and (max-width: 768px) {
  .desktop-only {
    display: none;
  }
  .mobile-only {
    display: block;
  }
}
```

## 斷點（Breakpoints）的選擇

### 常見斷點

```css
/* 超小手機 */
@media screen and (max-width: 320px) { }

/* 標準手機 */
@media screen and (max-width: 480px) { }

/* 平板（豎向）*/
@media screen and (min-width: 481px) and (max-width: 768px) { }

/* 平板（橫向）/ 小桌面 */
@media screen and (min-width: 769px) and (max-width: 1024px) { }

/* 標準桌面 */
@media screen and (min-width: 1025px) and (max-width: 1200px) { }

/* 大桌面 */
@media screen and (min-width: 1201px) { }
```

### 內容驅動斷點

```css
/* 根據內容選擇斷點，而非特定裝置 */

.container {
  width: 100%;
}

/* 當一行放不下3個卡片時 */
@media screen and (min-width: 769px) {
  .card {
    width: 33.33%;
  }
}
```

## 響應式設計的挑戰

### 2009 年的限制

1. **瀏覽器支援**
   - IE 8 不支援媒體查詢
   - 需要 Respond.js polyfill

2. **圖片效能**
   - 手機下載桌面尺寸圖片很慢
   - 響應式圖片標準尚未完成

3. **觸控 vs 滑鼠**
   - hover 效果無意義
   - 需要更大的點擊區域

### 降級方案

```html
<!--[if lt IE 9]>
<script src="respond.min.js"></script>
<![endif]-->
```

```html
<!-- 降級：不支援媒體查詢的瀏覽器顯示固定寬度 -->
<!--[if (lt IE 9)&(!IEMobile)]>
<style>
  .container { width: 960px; }
</style>
<![endif]-->
```

## 結語

媒體查詢是 CSS 3 最具影響力的功能之一。2009 年，響應式設計剛剛興起，大多數網站還沒有適配行動裝置。這個趨勢後來席捲了整個網頁設計行業，改變了我們思考網站設計的方式。

下一篇文章將介紹 CSS 3 的視覺效果：陰影、漸層和圓角。

---

## 延伸閱讀

- [Ethan Marcotte 響應式設計文章](https://www.google.com/search?q=Responsive+Web+Design+Ethan+Marcotte)
- [Media Queries 規格](https://www.google.com/search?q=CSS+media+queries+specification)
- [2009 年行動瀏覽器統計](https://www.google.com/search?q=mobile+browser+market+share+2009)
- [響應式設計最佳化](https://www.google.com/search?q=responsive+web+design+best+practices+2009)

---

*本篇文章為「AI 程式人雜誌 2009 年 7 月號」焦點系列之一。*