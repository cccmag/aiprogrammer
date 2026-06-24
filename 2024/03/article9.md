# CSS 預處理器：Sass

## 什麼是 CSS 預處理器

CSS 預處理器是一種擴充 CSS 功能的工具，讓開發者可以使用變數、嵌套、函式、混入等程式設計特性來撰寫樣式，再編譯為標準 CSS。Sass（Syntactically Awesome Style Sheets）是最受歡迎的 CSS 預處理器之一。

### 為什麼需要 Sass

原生 CSS 缺乏一些程式設計的基本能力：
- 無法使用變數（直到 CSS 自訂屬性出現）
- 沒有嵌套語法（直到 CSS 原生嵌套在 2023 年納入規範）
- 無法定義可重用的程式碼區塊
- 缺少數學運算和函式

Sass 填補了這些空白，讓 CSS 的維護性和重用性大幅提升。

---

## 安裝與使用

### 安裝 Sass

透過 npm 安裝：

```bash
npm install -g sass
```

### 編譯 Sass

```bash
# 單次編譯
sass input.scss output.css

# 監聽模式
sass --watch input.scss output.css

# 監聽整個目錄
sass --watch styles/:public/styles/
```

---

## Sass 核心功能

### 變數

使用 $ 前綴定義變數：

```scss
// 顏色變數
$primary: #007bff;
$secondary: #6c757d;
$success: #28a745;
$danger: #dc3545;

// 尺寸變數
$spacing-unit: 8px;
$border-radius: 4px;
$font-size-base: 16px;

// 字型變數
$font-family-sans: "Noto Sans TC", sans-serif;

// 使用變數
.btn-primary {
  background: $primary;
  color: white;
  padding: $spacing-unit ($spacing-unit * 2);
  border-radius: $border-radius;
  font-family: $font-family-sans;
}
```

### 嵌套

Sass 允許 CSS 選擇器嵌套，反映 HTML 結構：

```scss
.card {
  background: white;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 16px;

  .card-header {
    border-bottom: 1px solid #eee;
    padding-bottom: 12px;
    margin-bottom: 12px;

    h2 {
      margin: 0;
      font-size: 1.25rem;
    }
  }

  .card-body {
    p {
      line-height: 1.6;
      color: #333;
    }
  }

  &:hover {
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  }
}
```

編譯為 CSS：

```css
.card {
  background: white;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 16px;
}
.card .card-header {
  border-bottom: 1px solid #eee;
  padding-bottom: 12px;
  margin-bottom: 12px;
}
.card .card-header h2 {
  margin: 0;
  font-size: 1.25rem;
}
/* ... 其餘部分 */
```

### Mixin（混入）

Mixin 是可重用的樣式區塊：

```scss
// 定義 mixin
@mixin flex-center {
  display: flex;
  justify-content: center;
  align-items: center;
}

@mixin responsive-font($min-size, $max-size) {
  font-size: clamp(#{$min-size}, #{$min-size} + 2vw, #{$max-size});
}

@mixin button-variant($bg, $color: white) {
  background: $bg;
  color: $color;
  border: 1px solid darken($bg, 10%);

  &:hover {
    background: darken($bg, 10%);
  }

  &:active {
    background: darken($bg, 15%);
  }
}

// 使用 mixin
.modal {
  @include flex-center;
  position: fixed;
  inset: 0;
}

.hero-title {
  @include responsive-font(1.5rem, 3rem);
}

.btn-success {
  @include button-variant(#28a745);
}
.btn-danger {
  @include button-variant(#dc3545);
}
```

### 繼承

使用 @extend 共享樣式：

```scss
%button-base {
  display: inline-block;
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: background 0.2s;
}

.btn-primary {
  @extend %button-base;
  background: $primary;
  color: white;
}

.btn-secondary {
  @extend %button-base;
  background: $secondary;
  color: white;
}
```

### 函式與運算

```scss
.container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 ($spacing-unit * 2);
}

.column {
  $columns: 12;
  @for $i from 1 through $columns {
    &.col-#{$i} {
      width: percentage($i / $columns);
    }
  }
}
```

---

## 模組化

### 拆分檔案

將 Sass 拆分為多個檔案，使用 @use 載入：

```scss
// _variables.scss
$primary: #007bff;
$font-stack: "Helvetica", sans-serif;

// _mixins.scss
@use "variables";
@mixin button-style {
  background: variables.$primary;
}

// main.scss
@use "variables";
@use "mixins";
@use "components/card";
@use "layout/grid";
```

底線前綴的檔案（如 _variables.scss）是部分檔案，不會被獨立編譯為 CSS 檔案。

### @use vs @import

Sass 已棄用 @import，推薦使用 @use：

| 特性 | @import | @use |
|------|---------|------|
| 命名空間 | 全域 | 基於檔案 |
| 重複載入 | 可能造成衝突 | 自動避免 |
| 私有成員 | 無 | 支援（前綴 - 或 _） |

---

## 延伸閱讀

- [Sass 官方文件](https://www.google.com/search?q=Sass+official+documentation)
- [Sass 指南](https://www.google.com/search?q=Sass+guide+CSS+preprocessor)
- [Sass vs Less vs Stylus](https://www.google.com/search?q=Sass+vs+Less+vs+Stylus)

---

*本篇文章為「AI 程式人雜誌 2024 年 3 月號」精選文章之一。*
