# CSS 定位與層級

## position 屬性

CSS 的 position 屬性控制元素在文件中的定位方式。它有五個值：static、relative、absolute、fixed 和 sticky。

### static（靜態定位）

這是所有元素的預設值。元素遵循正常的文件流排列，top、right、bottom、left 和 z-index 屬性無效。

```css
.element {
  position: static; /* 預設值 */
}
```

### relative（相對定位）

元素保持正常文件流中的位置，但可以相對其原始位置進行偏移：

```css
.box {
  position: relative;
  top: 10px;
  left: 20px;
}
```

元素偏移後，原始位置仍然保留，不會影響其他元素的佈局。

### absolute（絕對定位）

元素脫離正常文件流，相對於最近的非 static 定位祖先元素進行定位。如果沒有這樣的祖先，則相對於初始包含塊（通常是 viewport）。

```css
.container {
  position: relative;
}
.child {
  position: absolute;
  top: 0;
  right: 0;
}
```

這是實現重疊、工具提示、下拉選單等效果的常用方式。

### fixed（固定定位）

元素脫離正常文件流，相對於 viewport 定位。即使頁面滾動，元素也保持固定位置：

```css
.navbar {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  z-index: 1000;
}
```

常見用途：固定導航欄、回到頂端按鈕、浮動廣告。

### sticky（黏性定位）

sticky 是 relative 和 fixed 的混合體。元素在正常文件流中滾動，直到達到指定的臨界值，然後固定在該位置：

```css
.section-header {
  position: sticky;
  top: 0;
  background: white;
  z-index: 10;
}
```

---

## 定位偏移屬性

使用 top、right、bottom、left 設定偏移量。支援的單位包括 px、em、rem、% 等：

```css
.overlay {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%); /* 精確置中 */
}
```

### 百分比基準

- **relative**：相對於元素本身的尺寸
- **absolute**：相對於定位祖先元素的對應邊界
- **fixed**：相對於 viewport 對應邊界

---

## z-index 層級

z-index 控制重疊元素的堆疊順序。數值越大，元素越靠近使用者。

```css
.modal {
  position: fixed;
  z-index: 1000; /* 高層級 */
}
.backdrop {
  position: fixed;
  z-index: 999;  /* 低於 modal */
}
```

### 堆疊上下文

z-index 只在同一個堆疊上下文（stacking context）中比較。以下情況會建立新的堆疊上下文：

- position 非 static 且 z-index 非 auto
- opacity 小於 1
- transform、filter 等屬性非 none
- isolation: isolate

```html
<div class="parent" style="z-index: 1;">
  <div class="child" style="z-index: 999;">被限制在 parent 內</div>
</div>
<div class="sibling" style="z-index: 2;">這個會蓋住 child</div>
```

---

## 常見定位模式

### 置中元素

```css
/* 水平置中 */
.h-center {
  margin: 0 auto;
}

/* 絕對置中 */
.center {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

/* Flexbox 置中 */
.flex-center {
  display: flex;
  justify-content: center;
  align-items: center;
}
```

### 全螢幕覆蓋層

```css
.overlay {
  position: fixed;
  inset: 0; /* top: 0; right: 0; bottom: 0; left: 0; */
  background: rgba(0, 0, 0, 0.5);
  z-index: 500;
}
```

### 提示框定位

```css
.tooltip {
  position: absolute;
  bottom: 100%;
  left: 50%;
  transform: translateX(-50%);
  margin-bottom: 8px;
}
```

---

## 定位與文件流對比

| 定位 | 脫離文件流 | 定位基準 | 適用場景 |
|------|-----------|---------|---------|
| static | 否 | 不適用 | 預設 |
| relative | 否 | 自身原始位置 | 微調位置 |
| absolute | 是 | 最近定位祖先 | 浮動元素 |
| fixed | 是 | viewport | 固定元素 |
| sticky | 否 | 滾動容器 | 黏性標題 |

---

## 延伸閱讀

- [MDN: CSS position](https://www.google.com/search?q=MDN+CSS+position)
- [MDN: z-index](https://www.google.com/search?q=MDN+z-index+CSS)
- [CSS Positioning 教學](https://www.google.com/search?q=CSS+positioning+tutorial)

---

*本篇文章為「AI 程式人雜誌 2024 年 3 月號」精選文章之一。*
