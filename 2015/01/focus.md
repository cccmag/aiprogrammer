# 本期焦點

## Web 程式設計基礎：從 HTML5 到響應式設計

### 引言

網頁開發經歷了從靜態 HTML 到互動式 Web 應用的巨大轉變。2015 年是 Web 技術的關鍵時刻——HTML5 規範即將完成、CSS3 獲得廣泛支援、JavaScript ES6 蓄勢待發。

本期歷史回顧將帶領讀者從 HTML5 的語意標籤出發，經過 CSS3 的華麗視覺效果，最後到達響應式設計的行動優先世界。

---

## 大綱

* [程式：JavaScript 與 DOM 操作實務](focus_code.md)
   - DOM 查詢與操作
   - 事件處理機制
   -  AJAX 與 Fetch API

1. [HTML5 的新特性](focus1.md)
   - 語意標籤的革命
   - 表單強化與驗證
   - Web Storage 客戶端儲存

2. [CSS3 與動畫](focus2.md)
   - Flexbox 彈性布局
   - CSS Grid 網格布局
   - Transitions 與 Keyframes

3. [JavaScript ES6 新語法](focus3.md)
   - Arrow Function 與 `this`
   - Promise 與非同步編程
   - Class 與模組系統

4. [響應式網頁設計](focus4.md)
   - Media Query 媒體查詢
   - Mobile First 設計策略
   - Bootstrap 框架應用

5. [瀏覽器 APIs](focus5.md)
   - Fetch API 網路請求
   - WebSocket 即時通訊
   - Service Worker 離線應用

6. [前端工具鏈](focus6.md)
   - npm 套件管理
   - Browserify / Webpack 打包
   - Gulp / Grunt 任務自動化

7. [未來展望](focus7.md)
   - Web Components 組件化
   - ECMAScript 2016+ 的未來
   - Progressive Web Apps

---

## 濃縮回顧

### HTML5 的語意革命

HTML5 引入了一系列語意標籤，讓網頁結構更加清晰：

```html
<!-- 傳統 div 堆疊 -->
<div class="header">...</div>
<div class="nav">...</div>
<div class="main">
  <div class="article">...</div>
  <div class="sidebar">...</div>
</div>
<div class="footer">...</div>

<!-- HTML5 語意標籤 -->
<header>...</header>
<nav>...</nav>
<main>
  <article>...</article>
  <aside>...</aside>
</main>
<footer>...</footer>
```

### CSS3 的布局進化

從 `float` 時代到 Flexbox 和 Grid，CSS3 徹底改變了網頁布局：

```
布局演進：
───────────
2000s: Table layouts（表格布局）
2006: Float + Clearfix（浮動布局）
2012: Flexbox（彈性布局）
2017: CSS Grid（網格布局）
```

### JavaScript 的現代化

ES6（2015）為 JavaScript 帶來了類別、模組、Promise 等現代特性，結束了「JavaScript 是業餘愛好者語言」的偏見。

### 響應式設計的興起

隨著智慧手機普及，響應式設計成為剛性需求：

```
響應式設計策略：
─────────────────
Desktop First → 傳統先設計桌面版
Mobile First  → 現代先設計行動版
               → 更專注核心內容
               → 漸進增強體驗
```

---

## 結論與展望

Web 技術在 2015 年達到了一個重要轉折點。HTML5 提供了語意和結構基礎、CSS3 帶來了豐富的視覺效果、JavaScript ES6 賦予了開發者更強大的工具。

未來的方向是清晰的：
1. **組件化**：Web Components 將成為標準
2. **效能優化**：漸進式 Web 應用（PWA）提供接近原生的體驗
3. **跨平台**：一次開發，多平台部署
4. **開發者體驗**：更好的工具鏈、更快的建置速度

---

## 延伸閱讀

- [HTML5 的新特性](focus1.md)
- [CSS3 與動畫](focus2.md)
- [JavaScript ES6 新語法](focus3.md)
- [響應式網頁設計](focus4.md)
- [瀏覽器 APIs](focus5.md)
- [前端工具鏈](focus6.md)
- [未來展望](focus7.md)

---

*本期焦點到此結束。下期我們將聚焦 Node.js 與伺服端 JavaScript 的開發世界。*