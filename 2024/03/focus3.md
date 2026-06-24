# Flexbox 與 Grid 排版

## Flexbox 排版

Flexbox（彈性盒子）是 CSS3 引入的一維排版模型，擅長在單一方向上排列元素。

### 基本用法

設定容器為 flex 容器：

```css
.container {
  display: flex;
}
```

所有直接子元素自動成為 flex 項目，沿主軸排列。

### 主軸方向

flex-direction 控制主軸方向：

```css
flex-direction: row;            /* 水平（預設） */
flex-direction: row-reverse;    /* 水平反向 */
flex-direction: column;         /* 垂直 */
flex-direction: column-reverse; /* 垂直反向 */
```

### 對齊方式

主軸對齊（justify-content）：

```css
justify-content: flex-start;   /* 靠左（預設） */
justify-content: center;       /* 居中 */
justify-content: space-between;/* 兩端對齊 */
justify-content: space-around; /* 均勻分布 */
justify-content: space-evenly; /* 等距分布 */
```

交錯軸對齊（align-items）：

```css
align-items: stretch;    /* 拉伸（預設） */
align-items: flex-start; /* 靠上 */
align-items: center;     /* 居中 */
align-items: flex-end;   /* 靠下 */
```

### 換行與間距

```css
flex-wrap: nowrap;   /* 不換行（預設） */
flex-wrap: wrap;     /* 換行 */
gap: 16px;           /* 項目間距 */
```

### 項目屬性

子元素的彈性屬性：

```css
.item {
  flex-grow: 1;   /* 伸展比例 */
  flex-shrink: 1; /* 收縮比例 */
  flex-basis: 0;  /* 基礎大小 */
  align-self: center; /* 個別對齊 */
}
```

簡寫 `flex: 1` 等於 `flex: 1 1 0`。

### 實戰範例：導航欄

```css
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
}
.nav-links {
  display: flex;
  gap: 24px;
  list-style: none;
}
```

---

## Grid 排版

Grid（網格）是 CSS 的二維排版系統，可以同時控制行和列。

### 基本用法

```css
.grid {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr; /* 三欄等寬 */
  grid-template-rows: auto;
  gap: 16px;
}
```

### 定義欄位

grid-template-columns 支援多種單位：

```css
/* 固定寬度 */
grid-template-columns: 200px 300px 200px;

/* fr 單位：剩餘空間比例 */
grid-template-columns: 1fr 2fr 1fr;

/* 自動填充 */
grid-template-columns: repeat(3, 1fr);

/* 混合 */
grid-template-columns: 200px 1fr 200px;

/* 自適應 */
grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
```

### 定義行

```css
grid-template-rows: 100px auto 100px;
grid-template-rows: repeat(3, minmax(100px, auto));
```

### 區域命名

使用 grid-template-areas 定義命名區域：

```css
.layout {
  display: grid;
  grid-template-columns: 200px 1fr;
  grid-template-rows: auto 1fr auto;
  grid-template-areas:
    "header  header"
    "sidebar main"
    "footer  footer";
  height: 100vh;
}
.header  { grid-area: header; }
.sidebar { grid-area: sidebar; }
.main    { grid-area: main; }
.footer  { grid-area: footer; }
```

### 項目定位

```css
.item {
  grid-column: 1 / 3;    /* 從第1列到第3列 */
  grid-row: 1 / span 2;  /* 從第1行跨越2行 */
}
```

---

## Flexbox vs Grid 對比

| 特性 | Flexbox | Grid |
|------|---------|------|
| 維度 | 一維（行或列） | 二維（行與列） |
| 適用場景 | 導航欄、卡片列表、工具欄 | 頁面佈局、儀表板、圖庫 |
| 內容驅動 | 大小由內容決定 | 大小可固定或由容器決定 |
| 瀏覽器支援 | 全部現代瀏覽器 | 全部現代瀏覽器 |

### 選擇原則

- **一維排列**：單行或單列 → Flexbox
- **二維排列**：需要同時控制行與列 → Grid
- **內容對齊**：需要自動對齊且不確定項目數量 → Flexbox
- **整體佈局**：定義頁面骨架 → Grid
- **內部細節**：卡片、按鈕組 → Flexbox

---

## 延伸閱讀

- [MDN: Flexbox 指南](https://www.google.com/search?q=MDN+Flexbox+guide)
- [MDN: Grid 指南](https://www.google.com/search?q=MDN+CSS+Grid+guide)
- [Flexbox Froggy 練習](https://www.google.com/search?q=Flexbox+Froggy+game)
- [Grid Garden 練習](https://www.google.com/search?q=CSS+Grid+Garden)

---

*本篇文章為「AI 程式人雜誌 2024 年 3 月號」前端開發系列之一。*
