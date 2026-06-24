# CSS 框架的起源：從 Blueprint 到 Bootstrap（2007-2010）

## 前言

在 Bootstrap 成為前端開發標準工具之前，已有多個 CSS 框架嘗試解決同樣的問題：如何讓網頁開發更有效率？如何確保不同開發者做出的頁面風格一致？

本章節將回顧 CSS 框架的早期歷史，這些先驅者的設計理念直接影響了後來的 Bootstrap。

## Blueprint CSS：第一個通用 CSS 框架

### 背景與動機

2007 年，Olav Bjorkum 創建了 Blueprint CSS，這是第一個廣泛使用的通用 CSS 框架。當時的 Web 開發面臨几个問題：

1. **瀏覽器相容性**：不同瀏覽器對 CSS 的支援差異巨大
2. **樣式不一致**：沒有統一的基礎樣式
3. **開發效率低**：每個專案都要從頭開始寫 CSS

Blueprint 的核心目標是提供一套「開箱即用」的 CSS 基礎，讓開發者可以快速開始頁面構建。

### Blueprint 的核心功能

Blueprint 提供了三個主要檔案：

```
blueprint/
  screen.css    # 螢幕顯示樣式
  print.css     # 列印樣式
  ie.css        # Internet Explorer 修正
```

#### 栅格系統

Blueprint 採用了 24 欄的固定宽度栅格：

```css
/* Blueprint 栅格系統 */
.container { width: 950px; margin: 0 auto; }
.span-1 { width: 30px; }
.span-2 { width: 70px; }
.span-3 { width: 110px; }
/* ...以此類推 */
```

使用方法：

```html
<div class="container">
  <div class="span-16">
    <h1>主內容區</h1>
  </div>
  <div class="span-8 pull-16">
    <h2>側邊欄</h2>
  </div>
</div>
```

#### 基礎樣式

Blueprint 提供了統一的 HTML 元素預設樣式：

```css
h1 { font-size: 2em; margin-bottom: 1em; }
h2 { font-size: 1.5em; margin-bottom: 0.83em; }
p { margin-bottom: 1em; }
```

#### 表格樣式

Blueprint 的表格樣式特别实用：

```css
table.bp { width: 100%; border-collapse: collapse; }
table.bp th { background: #c99; }
table.bp td, table.bp th { padding: 4px; border: 1px solid #999; }
```

### Blueprint 的局限性

Blueprint 虽然解决了许多问题，但也存在明显局限：

1. **固定寬度**：950px 的固定容器不支援響應式設計
2. **缺乏靈活性**：過度依賴 class 名稱
3. **沒有 JavaScript 组件**：只有 CSS，沒有互動元件

## 960 Grid System：簡潔的栅格系統

### 960.gs 的設計理念

Nathan Smith 在 2008 年創建了 960 Grid System，名稱來自其預設寬度（960 像素）。與 Blueprint 的 24 欄不同，960.gs 採用了更靈活的 12 欄設計：

```
960px 總寬度
├── 12 × 60px 欄位 = 720px
└── 11 × 20px 間距 = 220px
```

### 核心檔案

```css
/* 960.gs 栅格系統 */
.grid_1 { width: 60px; }
.grid_2 { width: 140px; }
.grid_3 { width: 220px; }
.grid_4 { width: 300px; }
.grid_5 { width: 380px; }
.grid_6 { width: 460px; }
.grid_7 { width: 540px; }
.grid_8 { width: 620px; }
.grid_9 { width: 700px; }
.grid_10 { width: 780px; }
.grid_11 { width: 860px; }
.grid_12 { width: 940px; }
```

### CSS Reset

960.gs 還包含了 Eric Meyer 的 CSS Reset 2.0，這成為後來許多框架的標配。

### 與 Blueprint 的比較

| 特性 | Blueprint | 960.gs |
|------|----------|--------|
| 欄數 | 24 | 12 |
| 預設寬度 | 950px | 960px |
| 樣式丰富度 | 中等 | 基礎 |
| 社區支持 | 中等 | 較好 |

## Twitter Blueprint：Bootstrap 的前身

### Twitter 的 UI 問題

2010 年，Twitter 的前開發者 Mark Otto 和 Jacob Thornton 發現公司面臨嚴重的 UI 不一致性問題。Twitter 早期使用了大量自定義的 CSS，導致：

- 不同頁面視覺風格不統一
- 開發者重複造輪子
- 維護成本極高

### 內部框架的開發

他們決定開發一個統一的 CSS 框架，内部代號為「Twitter Blueprint」。這個框架：

1. 借鑒了 Blueprint 和 960.gs 的栅格思想
2. 加入了自己開發的 UI 组件
3. 大量使用 Less 動態樣式表
4. 提供了 JavaScript 插件系統

### 與現有框架的差異

Twitter Blueprint 相比之前的框架有幾個關鍵創新：

```less
// Twitter Blueprint 採用 Less
@baseFontSize: 13px;
@blue: #049CDB;

// Mixin 用於快速創建按鈕
.button(@color: @blue) {
  background: @color;
  color: white;
  padding: 4px 12px;
  border-radius: 3px;
}

.btn-primary {
  .button(#0460A3);
}
```

### Bootstrap 的雛型功能

2010 年的 Twitter Blueprint 已經包含了許多後來 Bootstrap 的核心功能：

- **栅格系統**：12 欄響應式布局
- **基本樣式**：表格、表單、按鈕
- **導航元件**：頂欄、標籤、 pills
- **JavaScript 插件**：模式對話框、下拉選單

## CSS 框架的設計模式

### 框架的核心要素

從 Blueprint 到 Twitter Blueprint，我們可以看到 CSS 框架的設計模式：

```
CSS Framework
├── Reset/Base     # 統一瀏覽器預設樣式
├── Grid System     # 栅格布局
├── Typography      # 字體排版
├── Forms           # 表單元素
├── Tables          # 表格元素
├── Buttons         # 按鈕樣式
└── Utilities       # 工具類別
```

### 命名約定

早期的框架主要采用語義化命名：

```css
/* Blueprint 命名 */
.span-3 { width: 220px; }
.append-1 { padding-right: 40px; }
.prepend-1 { padding-left: 40px; }

/* 960.gs 命名 */
.grid_3 { width: 220px; }
.push_1 { margin-left: 80px; }
.pull_1 { margin-right: 80px; }
```

### 栅格系統的設計原則

栅格系統是所有 CSS 框架的核心：

```
┌──────────────────────────────────────────────────────────┐
│                      Container (950px)                   │
├─────────────┬─────────────┬─────────────┬───────────────┤
│   Column    │  Column     │  Column     │   Column      │
│    60px     │   60px      │   60px      │    60px       │
│             │             │             │               │
│─────────────│─────────────│─────────────│───────────────│
│      20px Gutter       │      20px Gutter               │
└─────────────┴─────────────┴─────────────┴───────────────┘
```

## 框架的演進方向

### 從固定到響應式

2010 年以前，大多数框架采用固定寬度設計。但隨著行動設備的普及，響應式設計成為剛需。

### 從純 CSS 到 CSS + JavaScript

Blueprint 和 960.gs 僅提供 CSS。但 Twitter Blueprint 開始集成 jQuery 插件，這極大增強了框架的互動能力。

### 從手寫到預處理

Less 的引入讓 CSS 開發更加靈活。變數、Mixin、嵌套規則等特性大幅提升了樣式表的可維護性。

## 結語

從 2007 年的 Blueprint 到 2010 年的 Twitter Blueprint，CSS 框架經歷了從無到有、從基礎到豐富的演進過程。

這些早期框架確立的設計模式——栅格系統、統一的基本樣式、元件化設計——被 Bootstrap 完整繼承並發揚光大。

下一篇文章我們將深入探討響應式設計的原理，這是 Bootstrap 区别於早期框架的關鍵特點。

---

## 延伸閱讀

- [Blueprint CSS 官方網站](https://www.google.com/search?q=Blueprint+CSS+framework)
- [960 Grid System](https://www.google.com/search?q=960+Grid+System)
- [Twitter Bootstrap history](https://www.google.com/search?q=Twitter+Bootstrap+history)
- [響應式 Web 設計](https://www.google.com/search?q=responsive+web+design+Ethan+Marcotte)

---

*本篇文章為「AI 程式人雜誌 2010 年 7 月號」歷史回顧系列之一。*