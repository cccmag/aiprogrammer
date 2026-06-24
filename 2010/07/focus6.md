# 框架比較與選型：Bootstrap、Foundation、Semantic UI

## 前言

經過數年的發展，前端 CSS 框架生態已經相當成熟。2010 年代初期，最流行的三個框架是 Bootstrap、Foundation 和 Semantic UI。每個框架都有其獨特的設計哲學和適用場景。

本章節將深入比較這三個框架，幫助讀者根據專案需求做出正確的選擇。

## Bootstrap

### 概述

Bootstrap 由 Twitter 開發和維護，2011 年開源後迅速成為最受歡迎的前端框架。

**優點：**
- 最大的社區支援和生態系統
- 豐富的元件庫和詳細文檔
- 广泛的第三方主題和模板
- 對響應式設計的原生支援

**缺點：**
- 預設樣式辨識度過高
- 高度客製化需要覆蓋大量樣式
- 生成的 HTML 較為複雜
- 行動優先設計較晚引入

### 核心特色

```html
<!-- Bootstrap 標準布局 -->
<div class="container">
  <div class="row">
    <div class="col-md-8">
      <h1>主內容</h1>
    </div>
    <div class="col-md-4">
      <h2>側邊欄</h2>
    </div>
  </div>
</div>

<!-- Bootstrap 按鈕 -->
<button class="btn btn-primary btn-lg">主要按鈕</button>
<button class="btn btn-secondary btn-sm">次要按鈕</button>

<!-- Bootstrap 導航欄 -->
<nav class="navbar navbar-default">
  <div class="container-fluid">
    <div class="navbar-header">
      <a class="navbar-brand" href="#">品牌</a>
    </div>
    <ul class="nav navbar-nav">
      <li class="active"><a href="#">首頁</a></li>
      <li><a href="#">關於</a></li>
    </ul>
  </div>
</nav>
```

### 響應式設計

```html
<!-- 響應式欄位 -->
<div class="row">
  <div class="col-xs-12 col-sm-6 col-md-4 col-lg-3">
    卡片內容
  </div>
</div>
```

### 定制化方式

```less
// Bootstrap 3 的 Less 變數覆蓋
@brand-primary: #0460A3;
@brand-success: #5cb85c;
@brand-danger: #d9534f;
@border-radius-base: 2px;
@font-family-base: "Helvetica Neue", Helvetica, Arial, sans-serif;

// 編譯自定義版本
lessc bootstrap.less custom-bootstrap.css
```

## Foundation

### 概述

Foundation 由 ZURB 設計工作室開發，2011 年發布，是另一個廣泛使用的前端框架。

**優點：**
- 真正的「行動優先」設計
- 更加靈活的栅格系統
- 專業的商業支援
- 豐富的 Email 模板

**缺點：**
- 學習曲線較陡
- 社區規模較 Bootstrap 小
- 文檔相對較少

### 核心特色

```html
<!-- Foundation 栅格系統 -->
<div class="row">
  <div class="medium-8 large-8 columns">
    主內容
  </div>
  <div class="medium-4 large-4 columns">
    側邊欄
  </div>
</div>

<!-- Foundation 按鈕 -->
<button class="button primary">主要按鈕</button>
<button class="button secondary">次要按鈕</button>
<button class="button success">成功</button>
<button class="button alert">警告</button>

<!-- Foundation 頂欄 -->
<nav class="top-bar" data-topbar role="navigation">
  <ul class="title-area">
    <li class="name">
      <h1><a href="#">品牌</a></h1>
    </li>
  </ul>

  <section class="top-bar-section">
    <ul class="right">
      <li><a href="#">首頁</a></li>
      <li><a href="#">關於</a></li>
    </ul>
  </section>
</nav>
```

### 行動優先

```html
<!-- Foundation 的 Mobile First 設計 -->
<div class="column">
  <!-- 預設是單欄（手機） -->
  <!-- medium- 是平板 -->
  <!-- large- 是桌面 -->
  <div class="medium-6 large-4">
    響應式內容
  </div>
</div>
```

### 定制化

```scss
// Foundation 的 Sass 定制
$primary-color: #0460A3;
$secondary-color: #777;
$alert-color: #f04124;
$success-color: #43ac6a;

@import "foundation/scss/foundation";
```

## Semantic UI

### 概述

Semantic UI 由 Jack Lukic 開發，2013 年發布，其核心理念是「語義化」。

**優點：**
- 最語義化的 class 命名
- 豐富的主題和變體
- 自然的語言語法
- 良好的可讀性

**缺點：**
- 檔案體積較大
- 學習曲線較陡
- 社區規模較小

### 核心特色

```html
<!-- Semantic UI 的語義化命名 -->
<div class="ui three column grid">
  <div class="column">
    <div class="ui segment">
      <h2 class="ui header">卡片標題</h2>
      <p>卡片內容</p>
      <div class="ui blue button">按鈕</div>
    </div>
  </div>
</div>

<!-- Semantic UI 按鈕 -->
<button class="ui primary button">主要</button>
<button class="ui secondary button">次要</button>
<button class="ui positive button">成功</button>
<button class="ui negative button">危險</button>

<!-- Semantic UI 選單 -->
<div class="ui menu">
  <div class="header item">品牌</div>
  <a class="active item">首頁</a>
  <a class="item">關於</a>
  <div class="right menu">
    <a class="item">設定</a>
  </div>
</div>
```

### 主題系統

```javascript
// Semantic UI 的主題配置
{
  "default": {
    "primaryColor": "#0460A3",
    "borderRadius": "0.2857rem"
  },
  "github": {
    "primaryColor": "#333333"
  }
}
```

## 詳細比較

### 栅格系統比較

| 特性 | Bootstrap | Foundation | Semantic UI |
|------|-----------|------------|-------------|
| 欄數 | 12 | 12 | 16 |
| 最大寬度 | 1170px（lg）| 1200px | 1520px |
| 響應式斷點 | xs/sm/md/lg | small/medium/large | mobile/tablet/computer |
| 語法 | `.col-md-*` | `.medium-*` | `.wide-*` |

### 按鈕系統比較

```html
<!-- Bootstrap -->
<button class="btn btn-primary">主要</button>

<!-- Foundation -->
<button class="button primary">主要</button>

<!-- Semantic UI -->
<button class="ui primary button">主要</button>
```

### 組件豐富度

| 組件 | Bootstrap | Foundation | Semantic UI |
|------|-----------|------------|-------------|
| 基本組件 | 完整 | 完整 | 完整 |
| JavaScript 組件 | 完整 | 完整 | 完整 |
| Email 模板 | 無 | 強大 | 無 |
| 視覺化元件 | 無 | 無 | 豐富 |

### 檔案大小

| 版本 | 原始大小 | 壓縮後 |
|------|---------|--------|
| Bootstrap 3 | ~130KB | ~40KB |
| Foundation 5 | ~200KB | ~50KB |
| Semantic UI 2 | ~300KB | ~80KB |

## 選擇指南

### 選擇 Bootstrap 當：

1. **快速開發**：需要快速構建原型或 MVP
2. **學習資源**：希望有大量的教程和範例
3. **社區支援**：需要廣泛的第三方擴展
4. **企業應用**：需要穩定性和長期支援

### 選擇 Foundation 當：

1. **專業設計**：需要高度客製化的設計
2. **Email 開發**：需要 Email 模板
3. **SEM 應用**：需要針對搜尋引擎的行銷頁面
4. **企業支援**：願意為商業支援付費

### 選擇 Semantic UI 當：

1. **語義化優先**：希望 HTML 盡可能語義化
2. **主題多樣性**：需要多種視覺主題
3. **長期維護**：願意投資學習曲線
4. **現代體驗**：需要更新穎的 UI 體驗

## 框架混合使用

### 可能的組合

```html
<!-- 使用 Bootstrap 栅格 + Semantic UI 組件 -->
<div class="container">
  <div class="row">
    <div class="col-md-8">
      <div class="ui cards">
        <!-- Semantic UI 卡片 -->
      </div>
    </div>
    <div class="col-md-4">
      <!-- Bootstrap 面板 -->
      <div class="panel panel-default">
        <div class="panel-heading">標題</div>
        <div class="panel-body">內容</div>
      </div>
    </div>
  </div>
</div>
```

### 不推薦的做法

- 同時使用多個框架的核心样式
- 混用不同框架的栅格系統
- 依賴多個框架的 JavaScript 插件

## 結語

選擇前端框架是一個需要綜合考慮多個因素的決策：

1. **專案需求**：是原型還是生產環境？
2. **團隊能力**：熟悉程度和學習意願？
3. **時間限制**：有多少時間可以投入學習？
4. **長期規劃**：專案的生命週期是多久？

無論選擇哪個框架，重要的是理解其設計理念和限制，才能充分發揮其價值。

下一篇文章我們將探討行動優先設計策略，這是現代 Web 開發的核心原則。

---

## 延伸閱讀

- [Bootstrap 官方網站](https://www.google.com/search?q=Bootstrap+official+website)
- [Foundation 官方網站](https://www.google.com/search?q=Foundation+CSS+framework)
- [Semantic UI 官方網站](https://www.google.com/search?q=Semantic+UI+framework)
- [CSS Framework Comparison](https://www.google.com/search?q=CSS+framework+comparison+2010)

---

*本篇文章為「AI 程式人雜誌 2010 年 7 月號」歷史回顧系列之一。*