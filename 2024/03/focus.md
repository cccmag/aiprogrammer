# 本期焦點

## 前端開發實戰 — HTML、CSS、JavaScript

### 引言

網頁前端開發是現代軟體工程中最貼近使用者的一環。從 1990 年 Tim Berners-Lee 發明第一個網頁瀏覽器開始，前端技術經歷了翻天覆地的變化。今天，前端開發不再只是「切版」——它涵蓋了語意化結構、響應式設計、動畫互動、表單驗證、狀態管理，甚至包含完整的應用架構。

本期雜誌將帶領讀者從基礎到進階，系統性地學習前端開發的三大核心技術：HTML 提供文件結構與語意，CSS 負責視覺呈現與排版，JavaScript 實現互動邏輯與資料處理。

我們將從 HTML 的語意化標籤開始，深入 CSS 的選擇器與盒模型，探討 Flexbox 與 Grid 的現代排版技術，然後進入 JavaScript 的 DOM 操作與事件處理，最後以響應式設計和建置工具收尾。

---

## 大綱

* [程式：前端開發完整實作](focus_code.md)
   - 虛擬 DOM 操作
   - CSS 解析引擎
   - 表單驗證系統

1. [HTML 語意化標籤](focus1.md)
   - 什麼是語意化 HTML
   - header、nav、main、article、section、aside、footer
   - 語意化對 SEO 與無障礙的影響

2. [CSS 選擇器與盒模型](focus2.md)
   - 基本選擇器：標籤、類別、ID
   - 組合選擇器：後代、子代、兄弟
   - 盒模型：margin、border、padding、content

3. [Flexbox 與 Grid 排版](focus3.md)
   - Flexbox 單軸排版
   - Grid 雙軸網格排版
   - 實戰對比與應用場景

4. [JavaScript DOM 操作](focus4.md)
   - DOM 樹結構
   - 查詢元素：querySelector、querySelectorAll
   - 修改元素：innerText、setAttribute、classList

5. [事件處理與表單驗證](focus5.md)
   - 事件監聽：addEventListener
   - 事件物件：target、preventDefault
   - 表單驗證邏輯與實作

6. [CSS 動畫與過渡](focus6.md)
   - transition 過渡效果
   - animation 與 @keyframes
   - 動畫效能最佳化

7. [響應式網頁設計](focus7.md)
   - Media Query 基本用法
   - 行動優先設計策略
   - 常見響應式模式

8. [結論與展望](focus.md#結論與展望)

---

## 濃縮回顧

### HTML 語意化

HTML5 引入了多個語意化標籤，讓網頁結構更加清晰。header 表示頁首，nav 表示導航，main 表示主要內容，article 表示獨立文章，section 表示主題區塊，aside 表示側邊欄，footer 表示頁尾。

### CSS 盒模型

CSS 盒模型是所有排版的基礎。每個元素都是一個盒子，由外到內包含 margin（外距）、border（邊框）、padding（內距）和 content（內容）。box-sizing 屬性控制寬度計算方式。

### Flexbox 與 Grid

Flexbox 擅長一維排版，適合導航欄、卡片列表等場景。Grid 擅長二維網格，適合整體頁面佈局與複雜儀表板。

### DOM 操作

DOM（Document Object Model）是 HTML 文件的程式化表示。透過 querySelector、createElement 等方法，JavaScript 可以動態查詢、新增、修改和刪除網頁元素。

### 事件處理

addEventListener 是現代事件監聽的標準方式。事件物件提供 target、preventDefault、stopPropagation 等方法。事件委派利用事件冒泡機制，在父層處理子元素事件。

### 動畫與過渡

transition 適合簡單的狀態變化動畫，animation 搭配 @keyframes 適合複雜的連續動畫。使用 transform 和 opacity 進行動畫可以獲得最佳效能。

### 響應式設計

Media Query 根據螢幕寬度調整樣式。行動優先設計從最小螢幕開始，逐步增加樣式。常見模式包括流體網格、彈性圖片和斷點設計。

---

## 結論與展望

前端開發技術仍在快速演進。2024 年，我們看到 WebAssembly 在瀏覽器中蓬勃發展、React Server Components 改變了前端架構思維，以及 AI 輔助程式設計工具的普及。然而，HTML、CSS 和 JavaScript 這三大核心技術的重要性從未改變。

無論未來框架如何變化，紮實的前端基礎將使開發者能夠快速適應新技術。本期文章涵蓋了前端開發的核心知識體系，希望能為讀者打下堅實的基礎。

---

## 延伸閱讀

- [HTML 語意化標籤](focus1.md)
- [CSS 選擇器與盒模型](focus2.md)
- [Flexbox 與 Grid 排版](focus3.md)
- [JavaScript DOM 操作](focus4.md)
- [事件處理與表單驗證](focus5.md)
- [CSS 動畫與過渡](focus6.md)
- [響應式網頁設計](focus7.md)

---

*本期焦點到此結束。下期我們將聚焦另一個影響深遠的主題，敬請期待。*
