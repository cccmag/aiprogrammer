# CSS 引入方式

## 三種引入方式

CSS 可以透過三種方式引入 HTML 文件：行內樣式、內部樣式表和外部樣式表。每種方式各有適用場景。

---

## 行內樣式

行內樣式直接寫在 HTML 元素的 style 屬性中：

```html
<p style="color: red; font-size: 16px; margin: 10px 0;">
  這段文字是紅色的。
</p>

<div style="background: #f5f5f5; padding: 20px; border-radius: 8px;">
  <h2 style="margin-top: 0;">行內樣式範例</h2>
</div>
```

### 優缺點

**優點**：
- 優先級最高（可覆蓋其他樣式）
- 適用於動態生成的樣式（JavaScript 操作）
- 快速測試和原型設計

**缺點**：
- 無法重用，違反 DRY 原則
- 混合了結構與表現，難以維護
- 無法使用偽類（:hover）和動畫
- 增加 HTML 檔案大小

一般不建議在生產環境中使用行內樣式。

---

## 內部樣式表

內部樣式表在 HTML 文件的 `<head>` 中使用 `<style>` 標籤：

```html
<!DOCTYPE html>
<html lang="zh-TW">
<head>
  <meta charset="UTF-8">
  <title>內部樣式表示例</title>
  <style>
    body {
      font-family: system-ui, sans-serif;
      line-height: 1.6;
      margin: 0;
      padding: 20px;
    }
    .card {
      background: white;
      border: 1px solid #ddd;
      padding: 20px;
      border-radius: 8px;
    }
    .card h2 {
      margin-top: 0;
      color: #333;
    }
    .btn {
      display: inline-block;
      padding: 8px 16px;
      background: #007bff;
      color: white;
      text-decoration: none;
      border-radius: 4px;
    }
    .btn:hover {
      background: #0056b3;
    }
  </style>
</head>
<body>
  <div class="card">
    <h2>卡片標題</h2>
    <p>卡片內容...</p>
    <a href="#" class="btn">按鈕</a>
  </div>
</body>
</html>
```

### 優缺點

**優點**：
- 可在單一頁面內重用樣式
- 支援所有 CSS 功能
- 無需額外的 HTTP 請求

**缺點**：
- 只在單一頁面有效，無法跨頁面共用
- 增加 HTML 檔案大小
- 不適合大型專案

內部樣式表適合單頁應用、登入頁面或原型設計。

---

## 外部樣式表

外部樣式表將 CSS 寫在獨立的 `.css` 檔案中，然後使用 `<link>` 引入：

```html
<!DOCTYPE html>
<html lang="zh-TW">
<head>
  <meta charset="UTF-8">
  <title>外部樣式表示例</title>
  <link rel="stylesheet" href="styles/main.css">
  <link rel="stylesheet" href="styles/components.css">
</head>
<body>
  ...
</body>
</html>
```

### 多重樣式表

可以引入多個 CSS 檔案，瀏覽器會按順序合併規則：

```html
<link rel="stylesheet" href="reset.css">     <!-- 重置樣式 -->
<link rel="stylesheet" href="layout.css">    <!-- 佈局樣式 -->
<link rel="stylesheet" href="theme.css">     <!-- 主題樣式 -->
```

### 媒體查詢引入

可以根據裝置條件選擇性載入：

```html
<link rel="stylesheet" href="print.css" media="print">
<link rel="stylesheet" href="mobile.css" media="(max-width: 768px)">
```

### 優缺點

**優點**：
- 樣式可跨頁面重用
- 分離結構與表現，維護性最佳
- 瀏覽器可快取 CSS 檔案
- 適合團隊協作

**缺點**：
- 需要額外的 HTTP 請求（可透過打包解決）
- 載入順序需要管理

外部樣式表是生產環境的標準做法。

---

## @import 指令

另一種引入外部 CSS 的方式是在 CSS 檔案中使用 @import：

```css
/* main.css */
@import url("reset.css");
@import url("variables.css");
@import url("layout.css");

body {
  font-family: sans-serif;
}
```

### 注意事項

- @import 必須在 CSS 檔案開頭
- 會增加檔案載入的序列化延遲
- 現代專案通常使用建置工具處理模組化

---

## 優先級比較

當出現衝突時，瀏覽器根據以下原則決定哪個樣式生效：

1. **行內樣式**（style 屬性）→ 最高
2. **內部樣式表**（style 標籤）
3. **外部樣式表**（link 引入）

同層級時，後定義的規則優先。!important 可以覆蓋所有樣式（應謹慎使用）。

---

## 載入效能考量

- 外部樣式表在 `<head>` 中載入可避免 FOUC（Flash of Unstyled Content）
- 使用媒體屬性避免不必要的 CSS 下載
- 較小的 CSS 檔案可以內聯在 HTML 中以減少請求數
- 現代理工具（如 Vite、webpack）會自動最佳化 CSS 載入

---

## 延伸閱讀

- [MDN: CSS 引入方式](https://www.google.com/search?q=MDN+how+to+add+CSS)
- [CSS 效能最佳化](https://www.google.com/search?q=CSS+performance+optimization)
- [Critical CSS 技術](https://www.google.com/search?q=critical+CSS+technique)

---

*本篇文章為「AI 程式人雜誌 2024 年 3 月號」精選文章之一。*
