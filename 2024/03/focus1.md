# HTML 語意化標籤

## 什麼是語意化 HTML

語意化 HTML 指的是使用具有明確意義的標籤來標記網頁內容，而非僅使用 div 和 span 進行排版。從 HTML5 開始，W3C 引入了多個語意化標籤，幫助開發者構建更具結構性和可訪問性的網頁。

語意化 HTML 的優勢包括：
- **SEO 優化**：搜尋引擎能更準確理解頁面結構
- **無障礙性**：螢幕閱讀器等輔助技術可以正確導航
- **可維護性**：程式碼更容易理解和修改
- **標準化**：符合網頁標準的最佳實踐

---

## HTML5 語意化標籤

### header（頁首）

header 定義頁面或區塊的標頭，通常包含 logo、導航連結、搜尋框等元素。

```html
<header>
  <h1>我的網站</h1>
  <nav>
    <a href="/">首頁</a>
    <a href="/about">關於</a>
  </nav>
</header>
```

### nav（導航）

nav 用於主要導航區塊。一個頁面可以有多個 nav，但應該只用於主要的導航連結。

```html
<nav aria-label="主導航">
  <ul>
    <li><a href="/">首頁</a></li>
    <li><a href="/blog">部落格</a></li>
    <li><a href="/contact">聯絡我們</a></li>
  </ul>
</nav>
```

### main（主要內容）

main 代表頁面的主要內容，每個頁面只能有一個 main 元素，不應包含側邊欄、導航等重複性內容。

```html
<main>
  <article>
    <h2>文章標題</h2>
    <p>文章內容...</p>
  </article>
</main>
```

### article（獨立文章）

article 代表獨立的內容單元，如部落格文章、新聞報導、評論等。它應該能獨立於頁面其他部分被理解。

```html
<article>
  <header>
    <h2>前端開發入門</h2>
    <time datetime="2024-03-15">2024年3月15日</time>
  </header>
  <p>這是文章的內容...</p>
  <footer>
    <p>作者：OpenCode</p>
  </footer>
</article>
```

### section（主題區塊）

section 表示文件中的主題區塊，通常包含一個標題。不要將 section 用作 div 的替代品——只有當內容有明確的主題時才使用。

```html
<section>
  <h2>我們的服務</h2>
  <p>我們提供以下服務...</p>
</section>
```

### aside（側邊欄）

aside 表示與周圍內容間接相關的內容，如側邊欄、廣告、相關連結等。

```html
<aside>
  <h3>相關文章</h3>
  <ul>
    <li><a href="#">CSS 基礎教學</a></li>
    <li><a href="#">JavaScript 入門</a></li>
  </ul>
</aside>
```

### footer（頁尾）

footer 定義頁面或區塊的頁尾，通常包含版權資訊、聯絡方式、隱私權政策連結等。

```html
<footer>
  <p>&copy; 2024 AI 程式人雜誌</p>
  <nav>
    <a href="/privacy">隱私權政策</a>
  </nav>
</footer>
```

---

## 語意化 vs 非語意化

| 語意化 | 非語意化 |
|--------|---------|
| `<header>` | `<div id="header">` |
| `<nav>` | `<div class="nav">` |
| `<main>` | `<div id="main">` |
| `<article>` | `<div class="post">` |
| `<footer>` | `<div id="footer">` |

使用非語意化標籤的 div 排版仍然可以運作，但搜尋引擎和輔助技術無法理解內容的結構意義。語意化 HTML 是專業前端開發的基礎要求。

---

## 進階語意化技巧

### 嵌套語意

語意化標籤可以互相嵌套。例如，article 內部可以包含 header 和 footer：

```html
<article>
  <header>...</header>
  <section>...</section>
  <footer>...</footer>
</article>
```

### ARIA 角色輔助

當無法使用合適的語意標籤時，可以搭配 ARIA 角色：

```html
<div role="navigation">...</div>
<div role="banner">...</div>
```

但優先使用原生語意標籤是更好的選擇。

---

## 延伸閱讀

- [MDN: HTML 語意化元素](https://www.google.com/search?q=MDN+HTML+semantic+elements)
- [W3C HTML5 規範](https://www.google.com/search?q=W3C+HTML5+semantic+markup)
- [Web Content Accessibility Guidelines](https://www.google.com/search?q=WCAG+accessibility+HTML)

---

*本篇文章為「AI 程式人雜誌 2024 年 3 月號」前端開發系列之一。*
