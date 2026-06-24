# CSS3 的誕生與模組化架構：從 CSS 2.1 到 CSS 3

## CSS 的歷史背景

### CSS 1：一切都從頭開始

1994 年，Håkon Wium Lie 在 CERN 工作時提出了 CSS 的想法。他是 HTML 的共同發明者 Tim Berners-Lee 的同事。Lie 認為 HTML 不應該承擔表現層的功能，應該有一個獨立的樣式語言。

```
1994 年：Lie 提出 CSS 概念
     ↓
1996 年：CSS 1 成為 W3C 推薦標準
     ↓
1998 年：CSS 2 發布
     ↓
2009 年：CSS 3 開始被瀏覽器廣泛支援
```

### CSS 2 的問題

CSS 2 於 1998 年發布，包含了许多先進的功能：
- 絕對定位與相對定位
- 媒體類型（@media）
- 下拉選單
- 滑鼠樣式

然而 CSS 2 有一個根本問題：**規格太過龐大且前後依賴**。瀏覽器廠商難以完整實作，開發者則被瀏覽器不一致的行為困擾。

```css
/* CSS 2 的典型 Hack */
#menu {
  width: 100px; /* IE 6 */
  width: 120px; /* 其他瀏覽器 \*/
  /width: 140px; /* IE 7 */
}
```

## CSS 3 的模組化設計

### 為什麼要模組化？

CSS 3 採用了一種革命性的設計：**模組化**。每個 CSS 3 功能被拆分成獨立的模組，每個模組有自己的版本號和發展進度。

```
CSS 3 模組化結構：
┌─────────────────────────────────────────────┐
│ CSS 3 (集合名稱)                             │
├─────────────────────────────────────────────┤
│ ┌─────────────────┐ ┌─────────────────────┐ │
│ │ Selectors Level 3│ │ Color Module       │ │
│ │ Version 3       │ │ Version 3          │ │
│ └─────────────────┘ └─────────────────────┘ │
│ ┌─────────────────┐ ┌─────────────────────┐ │
│ │ Media Queries    │ │ Namespaces Module  │ │
│ │ Version 3       │ │ Version 3          │ │
│ └─────────────────┘ └─────────────────────┘ │
│ ┌─────────────────┐ ┌─────────────────────┐ │
│ │ Flexbox         │ │ Background & Border │ │
│ │ Version 3       │ │ Version 3          │ │
│ └─────────────────┘ └─────────────────────┘ │
│ ...                                       ... │
└─────────────────────────────────────────────┘
```

### 主要 CSS 3 模組

| 模組名稱 | 描述 | 瀏覽器支援（2009年） |
|---------|------|---------------------|
| Selectors | 更強大的選擇器 | 全支援 |
| Color | rgba, hsl, hsla | 全支援 |
| Text | text-shadow, word-wrap | 部分支援 |
| Background | 多重背景, background-size | 部分支援 |
| Border | border-radius, box-shadow | 部分支援 |
| Flexbox | 彈性盒模型 | 實驗性 |
| Animation | @keyframes | 實驗性 |
| Media Queries | 響應式設計 | 全支援 |

## 瀏覽器支援狀況（2009年）

### 主流瀏覽器的 CSS 3 支援

```
2009 年瀏覽器 CSS 3 支援矩陣：

                    Firefox   Safari   Chrome   Opera    IE
border-radius       3.0+      3.1+     1.0+     10.0+    9.0+
box-shadow          3.5+      3.1+     1.0+     10.5+    9.0+
text-shadow         3.5+      3.1+     1.0+     9.0+     -
rgba                3.0+      3.1+     1.0+     9.0+     9.0+
gradients           -         4.0+     1.0+     10.5+    -
transform           3.5+      3.1+     1.0+     10.5+    9.0+
transition          -         3.1+     1.0+     10.5+    -
Flexbox             3.5+      3.1+     -        10.5+    -
```

### 前綴字（PREFIX）的使用

2009 年，瀏覽器廠商使用前綴字來實驗性地支援 CSS 3 特性：

```css
/* 2009 年的前綴字寫法 */
.element {
  /* Firefox */
  -moz-border-radius: 10px;
  /* Safari, Chrome */
  -webkit-border-radius: 10px;
  /* Opera */
  -o-border-radius: 10px;
  /* IE */
  -ms-border-radius: 10px;
  /* 標準寫法 */
  border-radius: 10px;
}
```

## CSS 3 的核心改進

### 1. 模組化帶來的彈性

不同於 CSS 2 的一次性發布，CSS 3 的各個模組可以獨立演進。瀏覽器可以選擇性地實作特定模組，開發者可以根據需求使用支援的功能。

```css
/* 檢查瀏覽器支援的語法 */
@supports (display: flex) {
  .container {
    display: flex;
  }
}
```

### 2. 新選擇器語法

CSS 3 引入了更多強大的選擇器：

```css
/* 屬性選擇器 */
input[type="email"] {
  border-color: blue;
}

/* 偽類 */
li:nth-child(odd) {
  background: #f0f0f0;
}

/* 否定偽類 */
input:not([type="submit"]) {
  border: 1px solid #ccc;
}
```

### 3. 新的顏色模型

CSS 3 新增了多種顏色表示方式：

```css
/* RGBA：帶透明度的 RGB */
.modal-backdrop {
  background: rgba(0, 0, 0, 0.5);
}

/* HSL：色相、飽和度、亮度 */
.button-primary {
  background: hsl(200, 100%, 50%);
}

/* HSLA：帶透明度的 HSL */
.highlight {
  background: hsla(200, 100%, 50%, 0.3);
}
```

### 4. 多重背景

CSS 3 允許元素有多個背景圖片：

```css
.hero {
  background:
    url('foreground.png') center center no-repeat,
    url('middle.png') left top repeat,
    url('background.png') center cover;
}
```

### 5. 圓角與陰影

```css
.card {
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}
```

## CSS 3 對網頁設計的影響

### 漸進增強的實現

CSS 3 讓「漸進增強」成為真正的實踐：

```css
/* 基礎樣式（所有瀏覽器） */
.column {
  float: left;
  width: 33.33%;
}

/* 增強樣式（支援 CSS 3 的瀏覽器） */
@supports (display: flex) {
  .container {
    display: flex;
  }
  .column {
    float: none;
    flex: 1;
  }
}
```

### 響應式設計的興起

CSS 3 的媒體查詢（Media Queries）讓響應式設計成為可能：

```css
@media screen and (max-width: 768px) {
  .container {
    flex-direction: column;
  }
}
```

## 結語

CSS 3 的模組化設計解決了 CSS 2 的諸多問題。2009 年，我們親眼見證了瀏覽器廠商積極實作 CSS 3 新特性的熱潮。雖然那時前綴字仍然必要、相容性仍有挑戰，但 CSS 3 的未來已經明確。

下一篇文章將介紹 CSS 3 中最重要的佈局工具之一：彈性盒模型（Flexbox）。

---

## 延伸閱讀

- [CSS 3 規格與標準](https://www.google.com/search?q=CSS+3+W3C+specification+2009)
- [瀏覽器前綴字的歷史](https://www.google.com/search?q=CSS+vendor+prefix+history)
- [Håkon Wium Lie 與 CSS 的發明](https://www.google.com/search?q=Håkon+Wium+Lie+CSS+history)
- [CSS 3 模組化設計的優點](https://www.google.com/search?q=CSS+3+modular+specification)

---

*本篇文章為「AI 程式人雜誌 2009 年 7 月號」焦點系列之一。*