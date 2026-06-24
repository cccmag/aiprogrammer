# 文字與視覺效果：陰影、漸層與圓角

## CSS 視覺效果的演進

### 過去：依賴圖片

在 CSS 3 之前，實現圓角和陰影需要：

1. **多張圖片**：每個角落一張
2. **JavaScript 庫**：如 Curved Corner
3. **CSS Hacks**：複雜的技巧

```
傳統圓角做法：

┌──────────────────────────────────┐
│ ┌────────┐                      │
│ │ corner │  用戶代理需要多張圖片   │
│ │ image  │  來模擬圓角效果         │
└──┴────────┘                      │
缺點：                                   
- HTTP 請求增加
- 維護困難
- 解析度問題
```

### 現在：純 CSS 實現

CSS 3 提供了原生的視覺效果屬性：

- `border-radius`：圓角
- `box-shadow`：陰影
- `text-shadow`：文字陰影
- `linear-gradient`：線性漸層
- `radial-gradient`：徑向漸層

## 圓角（border-radius）

### 基本語法

```css
.box {
  border-radius: 10px;
}
```

### 語法擴展

```css
/* 四角相同 */
border-radius: 10px;

/* 水平/垂直 */
border-radius: 10px / 20px;

/* 左上 右上 右下 左下 */
border-radius: 5px 10px 15px 20px;

/* 左上右下 | 右上左下 */
border-radius: 10px 20px;

/* 每個角不同 */
border-radius: 5px 10px 15px 20px;
```

### 圓形與膠囊

```css
/* 圓形 */
.circle {
  width: 100px;
  height: 100px;
  border-radius: 50%;
}

/* 膠囊形狀 */
.pill {
  width: 200px;
  height: 50px;
  border-radius: 25px;
}
```

### 複雜形狀

```css
/* 蛋形 */
.egg {
  width: 80px;
  height: 100px;
  border-radius: 50% / 60%;
}

/* 半圓 */
.semi-circle {
  width: 100px;
  height: 50px;
  border-radius: 50px 50px 0 0;
}
```

## 陰影（box-shadow）

### 基本語法

```css
.box {
  box-shadow: 5px 5px 10px rgba(0, 0, 0, 0.3);
}
```

### 語法結構

```
box-shadow: X軸偏移 Y軸偏移 模糊半徑 擴散半徑 顏色;

參數說明：
- X軸偏移：正值向右，負值向左
- Y軸偏移：正値向下，負值向上
- 模糊半�س：越大越模糊
- 擴散半徑：正值擴大，負值縮小
- 顏色：可以使用 rgba 透明色
```

### 陰影類型

```css
/* 基本陰影 */
.shadow-1 {
  box-shadow: 0 2px 5px rgba(0,0,0,0.2);
}

/* 柔和陰影 */
.shadow-soft {
  box-shadow: 0 10px 30px rgba(0,0,0,0.15);
}

/* 內陰影 */
.shadow-inset {
  box-shadow: inset 0 2px 5px rgba(0,0,0,0.2);
}

/* 多重陰影 */
.shadow-multiple {
  box-shadow:
    0 2px 5px rgba(0,0,0,0.1),
    0 5px 15px rgba(0,0,0,0.1),
    0 10px 30px rgba(0,0,0,0.1);
}

/* 彩色陰影 */
.shadow-color {
  box-shadow: 0 5px 15px rgba(52, 152, 219, 0.5);
}
```

### 陰影與效能

```css
/* 效能優化 */
/* 只動畫 transform 和 opacity */
.box {
  transform: translateY(0);
  box-shadow: 0 2px 5px rgba(0,0,0,0.2);
  transition: box-shadow 0.3s ease;
}

.box:hover {
  box-shadow: 0 5px 15px rgba(0,0,0,0.3);
}

/* 更好的方式：使用 transform */
.box-transform {
  transform: translateY(0);
  transition: transform 0.3s ease;
}
.box-transform:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0,0,0,0.3);
}
```

## 文字陰影（text-shadow）

### 基本語法

```css
.text {
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
}
```

### 文字陰影效果

```css
/* 柔和陰影 */
.text-shadow-soft {
  text-shadow: 0 2px 4px rgba(0,0,0,0.3);
}

/* 強烈陰影 */
.text-shadow-strong {
  text-shadow: 3px 3px 0 rgba(0,0,0,0.5);
}

/* 光暈效果 */
.text-glow {
  text-shadow: 0 0 10px rgba(255,255,255,0.8);
}

/* 多重陰影 */
.text-3d {
  text-shadow:
    0 1px 0 #ccc,
    0 2px 0 #c9c9c9,
    0 3px 0 #bbb,
    0 4px 0 #b9b9b9,
    0 5px 0 #aaa,
    0 6px 1px rgba(0,0,0,.1);
}
```

### 文字陰影與排版

```css
/* 凹版文字效果 */
.engraved {
  color: #999;
  text-shadow: 0 1px 0 rgba(255,255,255,0.5);
  background: #333;
}

/* 凸版文字效果 */
.embossed {
  color: #eee;
  text-shadow: 0 -1px 0 rgba(0,0,0,0.5);
  background: linear-gradient(#666, #333);
}
```

## 漸層（Gradients）

### 線性漸層（linear-gradient）

```css
/* 基本語法 */
.gradient {
  background: linear-gradient(direction, color-stop1, color-stop2, ...);
}

/* 由上到下 */
.gradient-top-bottom {
  background: linear-gradient(red, blue);
}

/* 由左到右 */
.gradient-left-right {
  background: linear-gradient(to right, red, blue);
}

/* 對角線 */
.gradient-diagonal {
  background: linear-gradient(to bottom right, red, blue);
}

/* 特定角度 */
.gradient-angle {
  background: linear-gradient(45deg, red, blue);
}
```

### 多色漸層

```css
/* 三色漸層 */
.gradient-multi {
  background: linear-gradient(red, yellow, blue);
}

/* 多色均等分佈 */
.gradient-bands {
  background: linear-gradient(
    red 0%,
    red 25%,
    yellow 25%,
    yellow 50%,
    blue 50%,
    blue 75%,
    green 75%
  );
}

/* 彩虹漸層 */
.gradient-rainbow {
  background: linear-gradient(
    to right,
    red, orange, yellow, green, blue, indigo, violet
  );
}
```

### 徑向漸層（radial-gradient）

```css
/* 基本語法 */
.gradient-radial {
  background: radial-gradient(shape, color-stop1, color-stop2, ...);
}

/* 圓形漸層 */
.radial-circle {
  background: radial-gradient(circle, red, yellow, blue);
}

/* 橢圓形漸層 */
.radial-ellipse {
  background: radial-gradient(ellipse, red, yellow, blue);
}

/* 指定位置 */
.radial-position {
  background: radial-gradient(at top left, red, yellow, blue);
}

/* 指定半徑 */
.radial-size {
  background: radial-gradient(closest-side, red, blue);
  /* closest-side: 渐层边界到中心最近的距离 */
  /* farthest-corner: 渐层边界到中心最远的距离 */
}
```

### 重複漸層

```css
/* 條紋圖案 */
.pattern-stripes {
  background: repeating-linear-gradient(
    45deg,
    red,
    red 10px,
    white 10px,
    white 20px
  );
}

/* 格紋圖案 */
.pattern-checker {
  background:
    repeating-linear-gradient(
      0deg,
      transparent,
      transparent 10px,
      rgba(0,0,0,0.1) 10px,
      rgba(0,0,0,0.1) 20px
    ),
    repeating-linear-gradient(
      90deg,
      transparent,
      transparent 10px,
      rgba(0,0,0,0.1) 10px,
      rgba(0,0,0,0.1) 20px
    );
}
```

## 漸層與效能

### 效能考量

漸層在 CSS 3 中是計算生成而非圖片，效能較好，但仍有一些注意事項：

1. **避免過度複雜的漸層**
2. **使用 rgba 而非完整透明度**
3. **考慮 GPU 加速**

### 漸層替代方案

```css
/* 對於簡單的兩色漸層，可以考虑： */
/* 1. 使用固定顏色 + 圖片 */
/* 2. 使用 box-shadow 疊加 */
/* 3. 考慮效能差異 */

.gradient-vs-solid {
  /* 渐层 */
  background: linear-gradient(#1e3c72, #2a5298);

  /* 固色 + 边框（降级方案）*/
  background: #2a5298;
  border-top: 3px solid #1e3c72;
}
```

## 綜合範例

### 按鈕效果

```css
.button {
  background: linear-gradient(180deg, #4a90e2, #357abd);
  border-radius: 5px;
  box-shadow: 0 3px 0 #2a5298, 0 5px 10px rgba(0,0,0,0.2);
  color: white;
  text-shadow: 0 -1px 0 rgba(0,0,0,0.2);
}

.button:hover {
  background: linear-gradient(180deg, #5a9fe2, #457abd);
}

.button:active {
  background: linear-gradient(180deg, #357abd, #4a90e2);
  box-shadow: 0 1px 0 #2a5298;
  transform: translateY(2px);
}
```

### 卡片效果

```css
.card {
  background: linear-gradient(145deg, #ffffff, #f0f0f0);
  border-radius: 10px;
  box-shadow:
    0 10px 30px rgba(0,0,0,0.1),
    0 1px 3px rgba(0,0,0,0.08);
}

.card-title {
  text-shadow: 0 1px 0 rgba(255,255,255,0.8);
}
```

## 瀏覽器支援（2009年）

```css
/* 前綴字 */
.element {
  /* Firefox */
  -moz-border-radius: 10px;
  -moz-box-shadow: 0 2px 5px rgba(0,0,0,0.2);
  -moz-linear-gradient(red, blue);

  /* Safari, Chrome */
  -webkit-border-radius: 10px;
  -webkit-box-shadow: 0 2px 5px rgba(0,0,0,0.2);
  -webkit-gradient(linear, red, blue);  /* 舊語法 */

  /* Opera */
  -o-border-radius: 10px;

  /* 標準 */
  border-radius: 10px;
  box-shadow: 0 2px 5px rgba(0,0,0,0.2);
  linear-gradient: linear-gradient(red, blue);  /* 標準 */
}
```

## 結語

CSS 3 的視覺效果屬性徹底改變了網頁設計。過去需要圖片才能實現的圓角、陰影和漸層，現在用純 CSS 就可以做到。這不僅加快了網站載入速度，也讓樣式調整更加靈活。

下一篇文章將介紹 CSS 3 的選擇器與偽類，這些強大的 DOM 選取工具。

---

## 延伸閱讀

- [border-radius 規格](https://www.google.com/search?q=border-radius+CSS3+specification)
- [box-shadow 屬性](https://www.google.com/search?q=box-shadow+CSS3+property)
- [CSS 漸層語法](https://www.google.com/search?q=CSS+gradient+syntax+2009)
- [CSS 視覺效果效能優化](https://www.google.com/search?q=CSS+visual+effects+performance)

---

*本篇文章為「AI 程式人雜誌 2009 年 7 月號」焦點系列之一。*