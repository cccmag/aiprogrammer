# 響應式網頁設計

## 什麼是響應式設計

響應式網頁設計（Responsive Web Design, RWD）是一種讓網頁在不同裝置——從手機到平板到桌上型電腦——都能提供最佳瀏覽體驗的設計方法。它透過彈性網格、彈性圖片和 Media Query 來適應各種螢幕尺寸。

### 核心原則

1. **流體網格**：使用相對單位而不是固定像素
2. **彈性圖片**：圖片自動縮放適應容器
3. **Media Query**：根據裝置特徵應用不同樣式

---

## Viewport 設定

響應式設計的第一步是設定 viewport meta 標籤：

```html
<meta name="viewport" content="width=device-width, initial-scale=1.0">
```

這個標籤告訴瀏覽器使用裝置的實際寬度作為 viewport 寬度，並設定初始縮放比例為 1。

---

## Media Query

Media Query 是響應式設計的核心工具，允許根據裝置特性應用不同的 CSS 樣式。

### 基本語法

```css
/* 當螢幕寬度小於等於 768px 時 */
@media (max-width: 768px) {
  .sidebar {
    display: none;
  }
}

/* 當螢幕寬度大於等於 1024px 時 */
@media (min-width: 1024px) {
  .container {
    max-width: 960px;
    margin: 0 auto;
  }
}
```

### 常用斷點

斷點是 Media Query 中使用的寬度值，常見的斷點設定：

```css
/* 手機：小於 576px */
@media (max-width: 575px) { }

/* 平板：576px - 991px */
@media (min-width: 576px) and (max-width: 991px) { }

/* 桌面：大於等於 992px */
@media (min-width: 992px) { }

/* 大螢幕：大於等於 1200px */
@media (min-width: 1200px) { }
```

---

## 行動優先設計

行動優先（Mobile First）是一種從最小螢幕開始設計，然後逐步為更大的螢幕增加樣式的方法。

```css
/* 基礎樣式（手機優先） */
.container {
  padding: 16px;
}
.grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 16px;
}

/* 平板 */
@media (min-width: 768px) {
  .grid {
    grid-template-columns: 1fr 1fr;
  }
}

/* 桌面 */
@media (min-width: 1024px) {
  .grid {
    grid-template-columns: 1fr 1fr 1fr;
  }
  .container {
    max-width: 960px;
    margin: 0 auto;
  }
}
```

---

## 響應式排版

### 流體字型

使用 clamp() 實現流體字型：

```css
h1 {
  font-size: clamp(1.5rem, 4vw, 3rem);
}
p {
  font-size: clamp(1rem, 2.5vw, 1.2rem);
}
```

### 相對單位

使用 rem 和 em 代替固定像素：

```css
html {
  font-size: 16px;
}
@media (max-width: 768px) {
  html {
    font-size: 14px;
  }
}
```

---

## 響應式圖片

```css
img {
  max-width: 100%;
  height: auto;
}
```

使用 picture 元素在不同螢幕下載不同圖片：

```html
<picture>
  <source media="(min-width: 1024px)" srcset="large.jpg">
  <source media="(min-width: 768px)" srcset="medium.jpg">
  <img src="small.jpg" alt="描述">
</picture>
```

---

## 常見響應式模式

### 漢堡選單

行動版使用漢堡圖示切換導航：

```css
.nav-links {
  display: flex;
}
.hamburger {
  display: none;
}

@media (max-width: 768px) {
  .nav-links {
    display: none; /* 隱藏導航 */
    flex-direction: column;
  }
  .nav-links.open {
    display: flex; /* 點擊後顯示 */
  }
  .hamburger {
    display: block; /* 顯示漢堡按鈕 */
  }
}
```

### 卡片網格

```css
.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 24px;
}
```

auto-fit 和 minmax 的組合會自動根據容器寬度調整欄數，無需 Media Query。

### 內容重排

側邊欄在行動版移至內容下方：

```css
.layout {
  display: grid;
  grid-template-columns: 1fr 300px;
  grid-template-areas: "main aside";
  gap: 24px;
}

@media (max-width: 768px) {
  .layout {
    grid-template-columns: 1fr;
    grid-template-areas:
      "main"
      "aside";
  }
}
```

---

## 測試響應式設計

- 瀏覽器開發者工具的裝置模擬模式
- 實際裝置測試
- 線上工具：Responsinator、BrowserStack
- 使用相對單位而非固定寬度

---

## 延伸閱讀

- [MDN: 響應式設計](https://www.google.com/search?q=MDN+responsive+design)
- [Google Web Fundamentals](https://www.google.com/search?q=Google+responsive+web+design+fundamentals)
- [CSS Media Query 指南](https://www.google.com/search?q=CSS+media+query+guide)

---

*本篇文章為「AI 程式人雜誌 2024 年 3 月號」前端開發系列之一。*
