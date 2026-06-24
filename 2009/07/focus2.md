# 彈性盒模型（Flexbox）：一維佈局的新標準

## Flexbox 的起源

### 為什麼需要 Flexbox？

在 Flexbox 出現之前，網頁佈局主要依靠以下幾種技術：

```
傳統佈局方式：
┌─────────────────────────────────────┐
│ 1. Float                            │
│    - 文字環繞圖片                    │
│    - 清除浮動的問題                  │
│    - 響應式困難                      │
├─────────────────────────────────────┤
│ 2. Position                         │
│    - 絕對定位                        │
│    - 脫離文件流                      │
│    - 難以響應式                      │
├─────────────────────────────────────┤
│ 3. Display: table                   │
│    - 可用於整頁佈局                  │
│    - 語義不符                        │
│    - 難以響應式                      │
└─────────────────────────────────────┘
```

這些傳統方法的問題：
- 垂直居中困難
- 等高欄位不易實現
- 響應式佈局複雜
- 元素順序難以控制

### Flexbox 的誕生

2009 年，CSS 3 推出了 Flexbox 模組，這是專為一維佈局設計的強大工具。Flexbox 的設計目標是：

1. **簡化常見佈局任務**：水平居中、垂直居中、等高欄位
2. **提供彈性佈局能力**：項目可以根據可用空間自動調整大小
3. **支援方向控制**：可以改變項目的排列方向

## Flexbox 基礎概念

### 彈性容器與彈性項目

```css
/* 彈性容器 */
.container {
  display: flex;
}

/* 彈性項目 */
.item {
  /* 項目會自動排列成一行 */
}
```

```
Flexbox 術語圖：

┌─────────────────────────────────────────┐
│            彈性容器 (flex container)    │
│  ┌───────────────────────────────────┐  │
│  │ 主軸 (main axis)                   │  │
│  │ ←──────────────────────────────→  │  │
│  │ ┌────┐  ┌────┐  ┌────┐  ┌────┐    │  │
│  │ │item│  │item│  │item│  │item│    │  │
│  │ │ 1  │  │ 2  │  │ 3  │  │ 4  │    │  │
│  │ └────┘  └────┘  └────┘  └────┘    │  │
│  │ ←──────────────────────────────→  │  │
│  │            主軸 (main axis)        │  │
│  └───────────────────────────────────┘  │
│                                         │
│  ┌───────────────────────────────────┐  │
│  │ 交錯軸 (cross axis)               │  │
│  │ ↑                                 │  │
│  │ ↑  ┌────┐                         │  │
│  │ ↑  │item│                         │  │
│  │ ↑  │ 1  │                         │  │
│  │ ↑  └────┘                         │  │
│  │ ↓                                 │  │
│  └───────────────────────────────────┘  │
└─────────────────────────────────────────┘
```

### Flexbox 屬性一覽

#### 彈性容器屬性

| 屬性 | 描述 | 範例值 |
|------|------|--------|
| display | 啟用 flex | flex, inline-flex |
| flex-direction | 主軸方向 | row, row-reverse, column, column-reverse |
| flex-wrap | 換行方式 | nowrap, wrap, wrap-reverse |
| justify-content | 主軸對齊 | flex-start, flex-end, center, space-between, space-around |
| align-items | 交錯軸對齊 | flex-start, flex-end, center, stretch, baseline |
| align-content | 多行對齊 | flex-start, flex-end, center, stretch, space-between, space-around |

#### 彈性項目屬性

| 屬性 | 描述 | 範例值 |
|------|------|--------|
| flex-grow | 放大比例 | 0, 1, 2 |
| flex-shrink | 縮小比例 | 0, 1, 2 |
| flex-basis | 初始大小 | auto, 100px, 50% |
| flex | 簡寫屬性 | 1, 0 0 100px |
| align-self | 單項目對齊 | auto, flex-start, flex-end, center |
| order | 排列順序 | 0, 1, -1 |

## 常用佈局範例

### 垂直居中

```css
.parent {
  display: flex;
  justify-content: center;  /* 水平居中 */
  align-items: center;      /* 垂直居中 */
}
```

### Sticky Footer（頁腳固定）

```css
body {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

main {
  flex: 1;  /* 佔據剩餘空間 */
}
```

### 導航列

```css
.nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.nav-links {
  display: flex;
  gap: 20px;
}
```

### 三欄佈局

```css
.container {
  display: flex;
}

.sidebar-left,
.sidebar-right {
  flex: 0 0 200px;  /* 不放大，不縮小，固定 200px */
}

.main {
  flex: 1;  /* 佔據剩餘空間 */
}
```

## Flexbox 與響應式設計

### 從 row 到 column

```css
.container {
  display: flex;
  flex-direction: row;
}

@media (max-width: 768px) {
  .container {
    flex-direction: column;
  }
}
```

### 彈性項目換行

```css
.gallery {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.gallery-item {
  flex: 1 1 calc(33.33% - 10px);
  min-width: 200px;
}
```

## Flexbox 的瀏覽器支援（2009年）

2009 年，Flexbox 仍處於實驗階段：

```css
/* 2009 年的前綴字 */
.container {
  display: -webkit-flex;    /* Chrome, Safari */
  display: -moz-flex;       /* Firefox */
  display: -ms-flex;        /* IE */
  display: -o-flex;         /* Opera */
  display: flex;            /* 標準 */
}
```

| 瀏覽器 | 版本 | 支援狀況 |
|--------|------|----------|
| Firefox | 3.5+ | -moz-flexbox |
| Safari | 3.1+ | -webkit-box |
| Chrome | 1.0+ | -webkit-box |
| Opera | 10.5+ | 有限支援 |
| IE | 10+ | flexbox (2012) |

### Modernizr 檢測

```javascript
if (Modernizr.flexbox) {
  // 使用 Flexbox
} else {
  // 使用 float 或 table 作為降級方案
}
```

## Flexbox 的優勢

```
Flexbox vs 傳統佈局：

┌────────────────┬────────────────────────┬────────────────────────┐
│ 特性           │ 傳統方式                │ Flexbox                │
├────────────────┼────────────────────────┼────────────────────────┤
│ 垂直居中        │ 困難，需要技巧          │ justify-content        │
├────────────────┼────────────────────────┼────────────────────────┤
│ 等高欄位        │ display: table-cell     │ align-items: stretch    │
├────────────────┼────────────────────────┼────────────────────────┤
│ 順序控制        │ HTML 順序固定           │ order 屬性             │
├────────────────┼────────────────────────┼────────────────────────┤
│ 空間分配        │ 複雜的百分比計算        │ flex 屬性              │
├────────────────┼────────────────────────┼────────────────────────┤
│ 響應式          │ Media Query + Float     │ Media Query + Flex     │
└────────────────┴────────────────────────┴────────────────────────┘
```

## 結語

Flexbox 是 CSS 3 最實用的功能之一。雖然 2009 年的瀏覽器支援還不完整，但開發者已經開始在實際專案中使用它。Flexbox 解決了無數過去需要 JavaScript 或 hack 才能實現的佈局問題。

下一篇文章將介紹 CSS 3 的另一個重要功能：動畫與轉場效果。

---

## 延伸閱讀

- [Flexbox 規格（W3C）](https://www.google.com/search?q=Flexbox+W3C+specification)
- [CSS Tricks Flexbox 指南](https://www.google.com/search?q=Flexbox+完整指南+2009)
- [Google Chrome Flexbox 實作](https://www.google.com/search?q=Chrome+flexbox+implementation+2009)
- [A Complete Guide to Flexbox 中文](https://www.google.com/search?q=Flexbox+教學+屬性)

---

*本篇文章為「AI 程式人雜誌 2009 年 7 月號」焦點系列之一。*