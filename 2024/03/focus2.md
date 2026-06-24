# CSS 選擇器與盒模型

## CSS 選擇器

CSS 選擇器決定樣式規則應用到哪些元素。理解選擇器是掌握 CSS 的第一步。

### 基本選擇器

**標籤選擇器**匹配所有指定類型的元素：

```css
p { color: #333; }
h1 { font-size: 2em; }
```

**類別選擇器**匹配具有指定 class 的元素：

```css
.highlight { background: yellow; }
.card { border: 1px solid #ddd; }
```

**ID 選擇器**匹配具有指定 id 的唯一元素：

```css
#header { background: #f8f9fa; }
#submit-btn { padding: 10px 20px; }
```

### 組合選擇器

**後代選擇器（空格）**：匹配在父元素內部的所有子孫元素

```css
article p { line-height: 1.6; }
```

**子代選擇器（>）**：只匹配直接子元素

```css
ul > li { list-style: none; }
```

**相鄰兄弟選擇器（+）**：匹配緊接在另一個元素後的元素

```css
h2 + p { font-weight: bold; }
```

**一般兄弟選擇器（~）**：匹配所有後續兄弟元素

```css
h2 ~ p { color: #666; }
```

### 偽類選擇器

偽類選擇器基於元素的狀態或位置進行匹配：

```css
a:hover { color: #007bff; }
a:focus { outline: 2px solid blue; }
li:first-child { font-weight: bold; }
li:last-child { border-bottom: none; }
li:nth-child(odd) { background: #f5f5f5; }
```

### 偽元素選擇器

偽元素選擇器的目標是元素的特定部分：

```css
p::first-line { font-size: 1.2em; }
p::before { content: "> "; }
p::after { content: " <"; }
```

---

## CSS 盒模型

CSS 盒模型是所有排版的基礎。每個 HTML 元素都是一個矩形盒子。

### 盒模型的組成

```
┌─────────────────────────────────┐
│           margin (外距)          │
│  ┌───────────────────────────┐  │
│  │      border (邊框)        │  │
│  │  ┌─────────────────────┐  │  │
│  │  │   padding (內距)    │  │  │
│  │  │  ┌───────────────┐  │  │  │
│  │  │  │   content     │  │  │  │
│  │  │  │   (內容)      │  │  │  │
│  │  │  └───────────────┘  │  │  │
│  │  └─────────────────────┘  │  │
│  └───────────────────────────┘  │
└─────────────────────────────────┘
```

### box-sizing 屬性

box-sizing 控制寬度計算方式：

```css
/* 預設值：width 只包含 content */
box-sizing: content-box;

/* width 包含 content + padding + border */
box-sizing: border-box;
```

建議全域設定 border-box：

```css
*, *::before, *::after {
  box-sizing: border-box;
}
```

### margin 外距

margin 控制元素外部空間，可以用於置中和控制元素間距：

```css
/* 四個方向分別設定 */
margin-top: 10px;
margin-right: 20px;
margin-bottom: 10px;
margin-left: 20px;

/* 簡寫：上 右 下 左 */
margin: 10px 20px 10px 20px;

/* 簡寫：上下 左右 */
margin: 10px 20px;

/* 水平置中 */
margin: 0 auto;
```

### padding 內距

padding 控制內容與邊框之間的內部空間：

```css
padding: 20px;         /* 四個方向相同 */
padding: 10px 20px;    /* 上下 左右 */
padding: 10px 20px 15px 25px; /* 上右下左 */
```

### border 邊框

border 為元素添加邊框：

```css
border: 1px solid #ccc;
/* 等於 */
border-width: 1px;
border-style: solid;
border-color: #ccc;
```

---

## 選擇器優先級

當多個選擇器衝突時，優先級決定哪個規則生效：

1. **!important**（最高）
2. **行內樣式**（style 屬性）
3. **ID 選擇器**
4. **類別、偽類、屬性選擇器**
5. **標籤、偽元素選擇器**
6. **萬用選擇器（*）**

計算方式：將選擇器表示為 (a, b, c) 三元組：
- a：ID 選擇器數量
- b：類別/屬性/偽類選擇器數量
- c：標籤/偽元素選擇器數量

---

## 延伸閱讀

- [MDN: CSS 選擇器](https://www.google.com/search?q=MDN+CSS+selectors)
- [CSS 盒模型詳解](https://www.google.com/search?q=CSS+box+model+explained)
- [CSS Specificity Calculator](https://www.google.com/search?q=CSS+specificity+calculator)

---

*本篇文章為「AI 程式人雜誌 2024 年 3 月號」前端開發系列之一。*
