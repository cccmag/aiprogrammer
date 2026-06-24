# 前端框架演進

## 靜態網頁時代

1990 年代，網頁是靜態的 HTML 文件。每個頁面在伺服器上是一個獨立的 HTML 檔案，使用者點擊連結就會載入一個全新的頁面。這個時代的「前端開發」實際上就是 HTML 排版。

1995 年，Brendan Eich 在 Netscape 創造了 JavaScript，最初只是用來做一些簡單的視覺特效，如滑鼠懸停變色、跑馬燈等。然而這個「簡單的腳本語言」最終將成為前端世界的基石。

## jQuery 與 DOM 操作

2006 年，John Resig 發布了 jQuery，這是一個革命性的 JavaScript 函式庫。jQuery 解決了三個核心問題：

- **瀏覽器相容性**：統一了 IE、Firefox、Chrome 的 DOM API 差異
- **DOM 選擇器**：使用 CSS 選擇器語法來選取元素
- **鏈式調用**：允許多個 DOM 操作串聯起來

```javascript
// jQuery 寫法
$('#app').addClass('active').find('.item').each(function() {
  $(this).text('Hello')
})
```

但 jQuery 的問題在於，當應用程式規模變大時，DOM 操作散落在各處，維護變得極其困難。

## MVC 與 MVVM 的興起

2010 年，前端開始借鑒後端的 MVC 模式。Backbone.js 引入了 Model、View、Collection 的概念，為前端帶來了結構化開發的思維。

同年，AngularJS（Angular 1.x）由 Google 發布，引入了雙向資料綁定的概念：

```javascript
// AngularJS 雙向綁定
<input ng-model="name">
<p>Hello, {{name}}!</p>
```

這種模式讓 Model 和 View 之間自動同步，開發者不再需要手動操作 DOM。但雙向綁定在大型應用中會導致效能問題，且 AngularJS 的學習曲線較為陡峭。

## React 的誕生

2013 年，Facebook 開源了 React，這是一個全新的前端 UI 函式庫。React 的核心理念徹底改變了前端開發的思考方式：

- **宣告式 UI**：描述 UI 的樣子，而非如何操作 DOM
- **元件化**：將 UI 拆分為獨立、可復用的組件
- **Virtual DOM**：透過虛擬 DOM 減少真實 DOM 操作
- **單向資料流**：資料從父元件流向子元件

```jsx
function Greeting({ name }) {
  return <h1>Hello, {name}!</h1>
}
```

React 的宣告式方法意味著開發者只需關心神狀態與 UI 的對應關係，React 負責處理 DOM 的更新細節。

## 現代多元生態

2014 年，Vue.js 由尤雨溪發布，結合了 AngularJS 的模板語法和 React 的虛擬 DOM。Vue 以其平緩的學習曲線和漸進式設計獲得了大量開發者的喜愛。

2016 年，Angular 2 重新設計為基於 TypeScript 和元件的現代框架，與 AngularJS 完全斷裂。

2019 年，Svelte 帶來了一個全新思路：編譯時期框架，將元件編譯為原生 JavaScript，無需 Virtual DOM。

2020 年代，Solid.js 進一步推進了反應性系統的設計，以更細粒度的更新機制挑戰 Virtual DOM 的效率。

## 框架選擇的思考

選擇前端框架需要考慮以下因素：

1. **專案規模**：小型專案可考慮 Vue 或 Svelte，大型企業專案可能更適合 React 或 Angular
2. **團隊經驗**：既有團隊的技術棧和學習曲線
3. **生態系統**：套件、工具、社群支援的程度
4. **效能需求**：反應速度、打包大小、渲染效能

## 結語

從靜態 HTML 到現代前端框架，我們見證了 Web 開發從原始走向成熟的歷程。React 在 2013 年的誕生標誌著宣告式 UI 時代的來臨，而這個理念至今仍在影響著新興框架的設計。

---

## 延伸閱讀

- [前端框架演進史](https://www.google.com/search?q=history+of+frontend+framework)
- [React 歷史與設計哲學](https://www.google.com/search?q=React+history+design+philosophy)
- [jQuery 到 React 的轉變](https://www.google.com/search?q=from+jQuery+to+React+migration)

---

*本篇文章為「AI 程式人雜誌 2024 年 4 月號」焦點系列之一。*
