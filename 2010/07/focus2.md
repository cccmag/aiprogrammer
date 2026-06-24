# 響應式設計原理：媒體查詢與彈性佈局

## 前言

2010 年，Ethan Marcotte 在 A List Apart 發表了「Responsive Web Design」一文，首次系統性地提出了響應式設計的概念。這篇文章徹底改變了 Web 開發的思路，標誌著「一個網站適配所有設備」時代的開始。

## 媒體查詢（Media Queries）

### CSS2 的媒體類型

CSS2 已經支援媒體類型，但使用有限：

```css
/* 僅螢幕設備 */
@media screen {
  body { font-size: 16px; }
}

/* 僅列印設備 */
@media print {
  body { font-size: 12pt; }
}
```

### CSS3 的媒體查詢

CSS3 大幅扩展了媒體查詢的能力：

```css
/* 基本語法 */
@media media_type and (feature: value) {
  /* 樣式規則 */
}

/* 螢幕宽度小於 768px */
@media screen and (max-width: 768px) {
  .container { width: 100%; }
  .sidebar { display: none; }
}

/* 平板設備 */
@media screen and (min-width: 768px) and (max-width: 1024px) {
  .container { width: 750px; }
}

/* 桌面設備 */
@media screen and (min-width: 1024px) {
  .container { width: 960px; }
}
```

### 常見的媒體查詢特性

```css
/* 螢幕尺寸 */
@media (max-width: 480px) { /* 手機 */ }
@media (min-width: 481px) and (max-width: 768px) { /* 平板 */ }
@media (min-width: 769px) { /* 桌面 */ }

/* 螢幕解析度 */
@media (-webkit-min-device-pixel-ratio: 2) {
  /* Retina 顯示器 */
}

/* 螢幕方向 */
@media (orientation: landscape) { /* 橫向 */ }
@media (orientation: portrait) { /* 豎向 */ }
```

### 行動優先 vs 桌面優先

#### 桌面優先（Desktop First）

```css
/* 預設桌面樣式 */
.container { width: 960px; }
.sidebar { width: 300px; }

/* 平板以下調整 */
@media (max-width: 1024px) {
  .container { width: 750px; }
  .sidebar { width: 200px; }
}

/* 手機調整 */
@media (max-width: 768px) {
  .container { width: 100%; }
  .sidebar { width: 100%; }
}
```

#### 行動優先（Mobile First）

```css
/* 預設手機樣式 */
.container { width: 100%; }
.sidebar { display: none; }

/* 平板以上展開側邊欄 */
@media (min-width: 768px) {
  .container { width: 750px; }
  .sidebar {
    display: block;
    width: 200px;
  }
}

/* 桌面完整布局 */
@media (min-width: 1024px) {
  .container { width: 960px; }
  .sidebar { width: 300px; }
}
```

## 彈性佈局（Fluid Grid）

### 固定寬度 vs 彈性寬度

```css
/* 固定寬度（不響應） */
.container { width: 960px; }

/* 彈性寬度（響應式） */
.container { width: 96%; max-width: 960px; }

/* 使用 calc() 計算 */
.column { width: calc(33.333% - 20px); }
```

### 彈性圖片

```css
/* 方法一：max-width */
img {
  max-width: 100%;
  height: auto;
}

/* 方法二：picture 標籤 */
<picture>
  <source media="(min-width: 1024px)" srcset="large.jpg">
  <source media="(min-width: 768px)" srcset="medium.jpg">
  <img src="small.jpg" alt="響應式圖片">
</picture>
```

### 彈性字體

```css
/* 使用 rem 單位 */
html { font-size: 16px; }
body { font-size: 1rem; }
h1 { font-size: 2rem; }

/* 使用 vw 單位實現縮放字體 */
h1 {
  font-size: 5vw;
  /* 限制最小和最大字體大小 */
  font-size: clamp(1.5rem, 5vw, 3rem);
}
```

## 栅格系統的響應式實作

### 基礎栅格

```css
/* 定義栅格變數 */
:root {
  --columns: 12;
  --gutter: 20px;
  --margin: 10px;
}

/* 栅格容器 */
.grid {
  display: flex;
  flex-wrap: wrap;
  margin: 0 calc(-1 * var(--margin));
}

/* 欄位 */
.col {
  flex: 1;
  padding: 0 var(--margin);
  box-sizing: border-box;
}

/* 響應式欄位 */
.col-1 { flex: 0 0 calc(100% / 12); }
.col-2 { flex: 0 0 calc(100% / 6); }
.col-3 { flex: 0 0 calc(100% / 4); }
.col-4 { flex: 0 0 calc(100% / 3); }
.col-6 { flex: 0 0 50%; }
.col-12 { flex: 0 0 100%; }

@media (max-width: 768px) {
  .col { flex: 0 0 100%; }
}
```

### 使用 CSS Grid

```css
/* 現代 CSS Grid 實現 */
.grid-container {
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: 20px;
}

/* 響應式調整 */
@media (max-width: 768px) {
  .grid-container {
    grid-template-columns: repeat(4, 1fr);
  }
}

@media (max-width: 480px) {
  .grid-container {
    grid-template-columns: repeat(2, 1fr);
  }
}
```

## 響應式設計的最佳實踐

### 1. 不要隱藏重要內容

```css
/* 錯誤做法：手機直接隱藏側邊欄 */
@media (max-width: 768px) {
  .sidebar { display: none; } /* 資訊丟失！ */
}

/* 正確做法：重新排列或提供替代方案 */
@media (max-width: 768px) {
  .sidebar {
    position: relative;
    width: 100%;
    margin-top: 2rem;
  }
}
```

### 2. 觸控友好的點擊區域

```css
/* 最小點擊區域 44x44px（Apple HIG） */
button, a, input[type="checkbox"] {
  min-height: 44px;
  min-width: 44px;
  padding: 12px;
}
```

### 3. 效能考量

```css
/* 延遲載入大型圖片 */
@media (max-width: 768px) {
  .hero-image {
    background-image: url(small.jpg);
  }
}

@media (min-width: 769px) {
  .hero-image {
    background-image: url(large.jpg);
  }
}
```

## Bootstrap 的響應式實作

### Bootstrap 的斷點系統

```css
/* Bootstrap 4 的斷點 */
:root {
  --breakpoint-sm: 576px;
  --breakpoint-md: 768px;
  --breakpoint-lg: 992px;
  --breakpoint-xl: 1200px;
}

/* Bootstrap 的容器寬度 */
.container { max-width: 100%; }
@media (min-width: 576px) { .container { max-width: 540px; } }
@media (min-width: 768px) { .container { max-width: 720px; } }
@media (min-width: 992px) { .container { max-width: 960px; } }
@media (min-width: 1200px) { .container { max-width: 1140px; } }
```

### Bootstrap 的栅格系統

```html
<div class="container">
  <div class="row">
    <!-- 手機上 12 欄（全寬） -->
    <!-- 平板上 6 欄（半寬） -->
    <!-- 桌面上 4 欄（三分之一） -->
    <div class="col-12 col-md-6 col-lg-4">
      <h3>響應式欄位</h3>
    </div>
  </div>
</div>
```

## 響應式設計的未來

### Container Queries

即將到來的 Container Queries 將讓響應式設計更加強大：

```css
/* 根據父容器寬度而非視口寬度調整 */
.card-container {
  container-type: inline-size;
}

@container (min-width: 400px) {
  .card {
    display: flex;
  }
}
```

### 原生 CSS 巢狀

隨著 CSS 巢狀的原生支援，響應式樣式將更加簡潔：

```css
/* 未來的巢狀媒體查詢 */
.card {
  font-size: 14px;

  @media (min-width: 768px) {
    font-size: 16px;
    display: flex;
  }
}
```

## 結語

響應式設計不僅是一套技術，更是一種「以使用者為中心」的設計理念。它要求我們在設計之初就考慮各種設備的使用場景，而不是事後補救。

從媒體查詢到彈性佈局，從固定栅格到 CSS Grid，這些工具讓我們能夠構建真正「流回應式」的 Web 體驗。

下一篇文章我們將深入探討 Bootstrap 的元件系統，看看它如何將這些響應式原理應用於實際的 UI 组件中。

---

## 延伸閱讀

- [Ethan Marcotte - Responsive Web Design](https://www.google.com/search?q=responsive+web+design+Ethan+Marcotte)
- [CSS Media Queries](https://www.google.com/search?q=CSS+media+queries+specification)
- [MDN - Using media queries](https://www.google.com/search?q=MDN+media+queries)
- [CSS Grid Layout](https://www.google.com/search?q=CSS+grid+layout+guide)

---

*本篇文章為「AI 程式人雜誌 2010 年 7 月號」歷史回顧系列之一。*