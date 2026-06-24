# 本期焦點

## CSS 3 與現代樣式設計：從規格到實踐

### 引言

2009 年是網頁設計的轉捩點。在這一年，CSS 3 從一個遙遠的規格願景，變成了開發者可以實際使用的工具。瀏覽器廠商的積極實作，讓設計師和開發者終於可以使用純 CSS 實現過去需要圖片或 JavaScript 才能完成的效果。

本期歷史回顧將帶領讀者探索 CSS 3 的誕生歷程，以及它如何改變了網頁設計的實踐。

---

## 大綱

* [程式：實作 CSS3 彈性盒模型](focus_code.md)
   - Flexbox 佈局引擎實作
   - 彈性容器與彈性項目的屬性
   - 響應式佈局實例

1. [CSS3 的誕生與模組化架構](focus1.md)
   - CSS 的歷史與 CSS 3 的設計理念
   - 模組化規格的優點
   - 主要瀏覽器的支援狀況

2. [彈性盒模型（Flexbox）](focus2.md)
   - Flexbox 的起源與設計目標
   - 彈性容器與彈性項目
   - 對齊與間距控制

3. [CSS3 動畫與轉場效果](focus3.md)
   - transition 屬性
   - @keyframes 動畫
   - 硬體加速與效能優化

4. [媒體查詢與響應式設計](focus4.md)
   - @media 查詢語法
   - 行動優先設計原則
   - 彈性圖片與 fluid grid

5. [文字與視覺效果](focus5.md)
   - text-shadow 與文字陰影
   - 漸層（linear-gradient, radial-gradient）
   - 圓角（border-radius）
   - 陰影（box-shadow）

6. [CSS3 選擇器與偽類](focus6.md)
   - 屬性選擇器
   - 結構性偽類
   - 偽元素 ::before 與 ::after

7. [瀏覽器相容性與未來展望](focus7.md)
   - 前綴字（-webkit-, -moz-）
   - Polyfill 與 Modernizr
   - CSS 4 的未來方向

---

## 濃縮回顧

### CSS 的起源

1994 年，Håkon Wium Lie 提出了 CSS（Cascading Style Sheets）的想法，當時他是 CERN 的研究人員。CSS 的設計目標是讓網頁開發者可以將內容（HTML）和表現（樣式）分離。1996 年 CSS 1 正式成為 W3C 推薦標準。

### CSS 2 的困境

CSS 2 於 1998 年發布，包含了定位、媒體類型等進階功能。然而 CSS 2 的規格過於龐大，瀏覽器實作進度緩慢且不一致。開發者往往需要使用 CSS Hacks 或條件註釋來處理瀏覽器相容性問題。

### CSS 3 的模組化改革

CSS 3 採取了完全不同的策略：將龐大的規格拆分成多個獨立的模組。每個模組可以單獨發展，瀏覽器可以選擇性地實作支援的模組。這種模組化設計讓 CSS 3 的推進速度大大加快。

### 2009 年的瀏覽器大戰

2009 年是瀏覽器廠商積極實作 CSS 3 的一年。Firefox、Safari、Chrome、Opera 都在爭先恐後地實作新特性。這種良性競爭加速了 CSS 3 的普及。

---

## 結論與展望

CSS 3 不僅是一組新屬性，它代表了一種新的網頁設計思維：漸進增強（Progressive Enhancement）、響應式設計（Responsive Design）、以及內容與表現的徹底分離。

展望未來，我們可以看到幾個趨勢：

1. **Flexbox 成為主流佈局工具**：2009 年 Flexbox 規格逐漸穩定
2. **CSS Grid 蓄勢待發**：二維佈局系統即將來臨
3. **原生動畫取代 Flash**：CSS Animation 與 Web Animations API
4. **變數（CSS Custom Properties）**：更強大的樣式重用機制
5. **瀏覽器前綴的結束**：隨著規格成熟，前綴將逐漸消失

對於前端開發者而言，掌握 CSS 3 不僅是學習新屬性，更是理解現代網頁設計原理的關鍵。

---

## 延伸閱讀

- [CSS3 的誕生與模組化架構](focus1.md)
- [彈性盒模型（Flexbox）](focus2.md)
- [CSS3 動畫與轉場效果](focus3.md)
- [媒體查詢與響應式設計](focus4.md)
- [文字與視覺效果](focus5.md)
- [CSS3 選擇器與偽類](focus6.md)
- [瀏覽器相容性與未來展望](focus7.md)

---

*本期焦點到此結束。下期我們將聚焦另一個影響深遠的主題，敬請期待。*