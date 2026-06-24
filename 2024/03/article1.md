# HTML 文件結構

## HTML 文件的基本骨架

每個 HTML 文件都遵循一個固定的結構。從 HTML5 開始，文件結構變得更加簡潔和標準化。

### DOCTYPE 宣告

DOCTYPE 宣告告訴瀏覽器使用哪種 HTML 規範來解析文件：

```html
<!DOCTYPE html>
```

對於 HTML5，這是最簡潔的寫法。它觸發瀏覽器的標準模式（Standards Mode），確保頁面按照 W3C 規範渲染。

### html 根元素

`<html>` 是文件的根元素，包裹所有內容：

```html
<html lang="zh-TW">
```

lang 屬性設定頁面語言，對搜尋引擎和螢幕閱讀器很重要。

### head 元素

`<head>` 包含頁面的元資訊，不會在瀏覽器中直接顯示：

```html
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>我的網頁</title>
  <meta name="description" content="這是一個範例頁面">
  <link rel="stylesheet" href="style.css">
</head>
```

### body 元素

`<body>` 包含頁面可見內容：

```html
<body>
  <header>頁首</header>
  <main>主要內容</main>
  <footer>頁尾</footer>
  <script src="app.js"></script>
</body>
```

---

## 完整的 HTML5 範本

將上述元素組合起來，就是一個完整的 HTML5 文件：

```html
<!DOCTYPE html>
<html lang="zh-TW">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>前端開發實戰</title>
  <meta name="description" content="學習前端開發的三大核心技術">
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <header>
    <h1>前端開發實戰</h1>
    <nav>
      <a href="#html">HTML</a>
      <a href="#css">CSS</a>
      <a href="#js">JavaScript</a>
    </nav>
  </header>

  <main>
    <article id="html">
      <h2>HTML 基礎</h2>
      <p>HTML 是網頁的結構語言...</p>
    </article>
  </main>

  <footer>
    <p>&copy; 2024 AI 程式人雜誌</p>
  </footer>

  <script src="app.js"></script>
</body>
</html>
```

---

## head 中的重要元素

### meta 字元編碼

```html
<meta charset="UTF-8">
```

這行設定文件使用 UTF-8 編碼，支援所有語言字元。

### meta viewport

```html
<meta name="viewport" content="width=device-width, initial-scale=1.0">
```

這對響應式設計至關重要，確保行動裝置正確縮放頁面。

### title 標題

```html
<title>頁面標題 - 網站名稱</title>
```

title 顯示在瀏覽器標籤頁，也是搜尋結果中的主要標題。

### 外部資源連結

```html
<!-- CSS 樣式表 -->
<link rel="stylesheet" href="styles.css">

<!-- Favicon -->
<link rel="icon" type="image/png" href="favicon.png">
```

---

## body 中的結構

### 腳本放置位置

script 標籤的位置影響頁面載入效能：

```html
<!-- 在 head 中（會阻塞渲染） -->
<head>
  <script src="render-blocking.js"></script>
</head>

<!-- 在 body 末尾（推薦） -->
<body>
  <!-- 內容 -->
  <script src="app.js"></script>
</body>

<!-- 使用 defer 在 head 中 -->
<head>
  <script src="deferred.js" defer></script>
</head>
```

defer 屬性讓腳本在 HTML 解析完後執行，不阻塞渲染。

---

## HTML 的歷史演進

HTML 從 1993 年由 Tim Berners-Lee 提出的第一個版本開始，歷經了多次重大更新：

- **HTML 2.0 (1995)**：第一個標準化版本
- **HTML 4.01 (1999)**：加入表格、表單等豐富功能
- **XHTML 1.0 (2000)**：使用 XML 語法
- **HTML5 (2014)**：加入語意標籤、多媒體支援、Canvas 等

HTML5 是當前的主流標準，持續透過 Living Standard 模式更新。

---

## 驗證 HTML 文件

使用 W3C 驗證服務（[Validator](https://www.google.com/search?q=W3C+HTML+validator)）檢查 HTML 是否符合規範。驗證可以幫助發現語法錯誤和可訪問性問題。

---

## 延伸閱讀

- [MDN: HTML 文件結構](https://www.google.com/search?q=MDN+HTML+document+structure)
- [W3C HTML5 規範](https://www.google.com/search?q=W3C+HTML5+specification)
- [HTML Living Standard](https://www.google.com/search?q=HTML+Living+Standard)

---

*本篇文章為「AI 程式人雜誌 2024 年 3 月號」精選文章之一。*
