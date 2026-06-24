# CSS3 與動畫：Flexbox、Grid、Transitions、Keyframes

## 前言

CSS3 是 CSS 標準的第三個主要版本，引入了大量新特性，從布局系統到動畫效果徹底改變了網頁設計的可能性。

## Flexbox 彈性布局

### 為什麼需要 Flexbox？

傳統的 `float` 和 `inline-block` 布局有很多痛點：

```css
/* 傳統方法：float 布局 */
.parent::after {
  content: '';
  display: block;
  clear: both;
}
.child {
  float: left;
  width: 33.33%;
}

/* 問題：需要清除浮動、垂直置中困難 */
```

Flexbox 優雅地解決了這些問題：

```css
/* Flexbox 布局 */
.parent {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.child {
  flex: 1; /* 彈性生長 */
}
```

### Flexbox 基本概念

```
Flexbox 模型：
──────────────

         Main Axis (主軸)
              →
    ┌─────────────────────┐
    │ ┌───┐ ┌───┐ ┌───┐  │
    │ │ 1 │ │ 2 │ │ 3 │  │
    │ └───┘ └───┘ └───┘  │
    │     ↑              │
    │  Cross Axis        │
    │  (交錯軸)          │
    └─────────────────────┘

父容器屬性：
├── display: flex
├── flex-direction: row | column
├── flex-wrap: nowrap | wrap
├── justify-content: 主軸對齊
├── align-items: 交錯軸對齊
└── gap: 間距
```

### Flexbox 父容器屬性

```css
.container {
  display: flex;

  /* 主軸方向 */
  flex-direction: row;           /* 預設，水平 */
  flex-direction: column;        /* 垂直 */

  /* 換行 */
  flex-wrap: nowrap;             /* 預設，不換行 */
  flex-wrap: wrap;               /* 換行 */

  /* 主軸對齊 (horizontal) */
  justify-content: flex-start;   /* 靠左（預設）*/
  justify-content: flex-end;     /* 靠右 */
  justify-content: center;        /* 置中 */
  justify-content: space-between; /* 兩端對齊 */
  justify-content: space-around;  /* 等距分布 */

  /* 交錯軸對齊 (vertical) */
  align-items: stretch;           /* 拉伸（預設）*/
  align-items: flex-start;        /* 靠上 */
  align-items: flex-end;          /* 靠下 */
  align-items: center;           /* 垂直置中 */
  align-items: baseline;         /* 基線對齊 */

  /* 多行對齊 */
  align-content: flex-start;     /* 靠上 */
  align-content: center;          /* 置中 */
  align-content: space-between;   /* 兩端對齊 */
}
```

### Flexbox 子項目屬性

```css
.item {
  /* 彈性係數 */
  flex: 1;                       /* 全部等寬 */
  flex: 0 0 200px;               /* (grow, shrink, basis) */

  /* 個別對齊 */
  align-self: center;            /* 覆寫父容器設定 */

  /* 排列順序 */
  order: 1;                      /* 數字越小越前面 */
}
```

### 常見佈局範例

```css
/* 水平導航列 */
.nav {
  display: flex;
  list-style: none;
  gap: 20px;
}

/* 卡片網格 */
.card-container {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}
.card {
  flex: 1 1 300px;               /* 最小 300px */
}

/* 聖杯布局 */
.layout {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}
.header { flex: 0 0 60px; }
.main { flex: 1; display: flex; }
.sidebar { flex: 0 0 200px; }
.content { flex: 1; }
.footer { flex: 0 0 40px; }
```

## CSS Grid 網格布局

### Grid vs Flexbox

```
Grid vs Flexbox：
─────────────────
Flexbox:   單維度布局（行或列）
Grid:      雙維度布局（行和列）

何時用 Flexbox：
- 一維排列的元素
- 導航列、水平列表
- 需要彈性調整大小

何時用 Grid：
- 二維布局（行和列）
- 複雜的頁面布局
- 需要精確控制間距
```

### Grid 基本語法

```css
.container {
  display: grid;

  /* 定義欄位 */
  grid-template-columns: 200px 1fr 200px;
  grid-template-rows: auto 1fr auto;
  grid-template-areas:
    "header header header"
    "sidebar main content"
    "footer footer footer";

  /* 間距 */
  gap: 20px;

  /* 對齊 */
  justify-items: stretch;        /* 水準 */
  align-items: stretch;          /* 垂直 */
}

.header { grid-area: header; }
.sidebar { grid-area: sidebar; }
.main { grid-area: main; }
.footer { grid-area: footer; }
```

### Grid 簡寫與函式

```css
.container {
  /* fr 單位：分數空間 */
  grid-template-columns: 1fr 2fr 1fr;

  /* repeat() 函式 */
  grid-template-columns: repeat(3, 1fr);

  /* auto-fill / auto-fit：響應式欄位 */
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));

  /* 命名區域 */
  grid-template-areas:
    "header header"
    "sidebar main"
    "footer footer";
}
```

## Transitions 過渡效果

### 基本語法

```css
.box {
  background: blue;
  transition: property duration timing-function delay;
}

/* 常用寫法 */
.box {
  transition: all 0.3s ease;           /* 全部屬性 */
  transition: background 0.3s ease;    /* 特定屬性 */
  transition: transform 0.5s ease-in-out;
  transition: opacity 0.2s linear;
}

.box:hover {
  background: red;
  transform: scale(1.1);
}
```

### Timing Functions

```css
.linear {
  transition-timing-function: linear;       /* 線性（等速）*/
}

.ease {
  transition-timing-function: ease;         /* 慢-快-慢 */
}

.ease-in {
  transition-timing-function: ease-in;      /* 漸快 */
}

.ease-out {
  transition-timing-function: ease-out;     /* 漸慢 */
}

.ease-in-out {
  transition-timing-function: ease-in-out;  /* 慢-快-慢 */
}

.custom {
  transition-timing-function: cubic-bezier(0.68, -0.55, 0.265, 1.55);
  /* 自訂貝茲曲線 */
}
```

### 常用過渡屬性

```css
.transition-demo {
  transition-property: all;
  transition-duration: 0.3s;

  /* 可過渡的屬性： */
  /* - 色彩：background, color, border-color */
  /* - 尺寸：width, height, margin, padding */
  /* - 位置：transform, left, top */
  /* - 陰影：box-shadow */
  /* - 透明度：opacity */
}
```

## Keyframes 動畫

### @keyframes 語法

```css
@keyframes slideIn {
  from {
    transform: translateX(-100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

@keyframes fadeInOut {
  0% { opacity: 0; }
  50% { opacity: 1; }
  100% { opacity: 0; }
}

@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.1); }
}
```

### 應用動畫

```css
.animated-element {
  animation: slideIn 0.5s ease forwards;
  animation-delay: 0.2s;                   /* 延遲 */
  animation-iteration-count: 1;             /* 播放次數 */
  animation-iteration-count: infinite;      /* 無限循環 */
  animation-direction: normal;              /* 正向播放 */
  animation-direction: reverse;            /* 反向播放 */
  animation-direction: alternate;          /* 交替播放 */
  animation-fill-mode: forwards;           /* 停在最終狀態 */
  animation-fill-mode: both;               /* 應用開始/結束狀態 */
}

/* 組合動畫 */
.combo {
  animation:
    slideIn 0.5s ease forwards,
    fadeIn 0.3s ease 0.3s forwards;
}
```

### 實用動畫範例

```css
/* 載入動畫 */
.loader {
  width: 50px;
  height: 50px;
  border: 5px solid #f3f3f3;
  border-top: 5px solid #3498db;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* 彈跳效果 */
.bounce {
  animation: bounce 0.6s ease infinite;
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-20px); }
}

/* 打字機效果 */
.typewriter {
  overflow: hidden;
  white-space: nowrap;
  animation:
    typing 2s steps(20) forwards,
    blink 0.5s step-end infinite;
}

@keyframes typing {
  from { width: 0; }
  to { width: 100%; }
}

@keyframes blink {
  50% { border-color: transparent; }
}
```

## 結語

CSS3 的布局系統（Flexbox 和 Grid）和動畫系統（Transitions 和 Keyframes）徹底改變了網頁開發的可能性。Flexbox 解決了一維布局的問題、Grid 解決了二維布局的問題，而動畫系統讓網頁從靜態走向動態。

---

## 延伸閱讀

- [Flexbox 完全指南](https://www.google.com/search?q=CSS3+Flexbox+complete+guide)
- [CSS Grid 教程](https://www.google.com/search?q=CSS+Grid+layout+tutorial)
- [CSS 動畫入門](https://www.google.com/search?q=CSS3+animations+keyframes+tutorial)

---

*本篇文章為「AI 程式人雜誌 2015 年 1 月號」歷史回顧系列之一。*