# Bootstrap 元件系統：栅格、按鈕、表單

## 前言

Bootstrap 的核心價值在於其豐富的 UI 组件系統。從最基本的按鈕到複雜的導航欄，每個组件都經過精心設計，確保在各種場景下都能提供一致的使用者體驗。

本章節將深入探討 Bootstrap 的核心元件，揭示其設計思想和使用方法。

## 栅格系統（Grid System）

### Bootstrap 栅格的設計原理

Bootstrap 採用了 12 欄的栅格系統，這個數字的選擇有其深層考量：

```
12 的因數：1, 2, 3, 4, 6, 12

可實現的布局：
- 2 欄：6 + 6
- 3 欄：4 + 4 + 4
- 4 欄：3 + 3 + 3 + 3
- 6 欄：2 + 2 + 2 + 2 + 2 + 2
- 任意組合：3 + 9, 2 + 3 + 7, etc.
```

### 基本語法

```html
<div class="container">
  <div class="row">
    <div class="span3">
      <!-- 3/12 寬度 -->
    </div>
    <div class="span9">
      <!-- 9/12 寬度 -->
    </div>
  </div>
</div>
```

### 響應式栅格

```html
<div class="row">
  <!-- 行動設備：全寬 -->
  <!-- 平板：半寬 -->
  <!-- 桌面：三分之一寬 -->
  <div class="col-xs-12 col-md-6 col-lg-4">
    <h3>響應式欄位</h3>
    <p>內容...</p>
  </div>

  <div class="col-xs-12 col-md-6 col-lg-4">
    <h3>響應式欄位</h3>
    <p>內容...</p>
  </div>

  <div class="col-xs-12 col-md-12 col-lg-4">
    <h3>響應式欄位</h3>
    <p>內容...</p>
  </div>
</div>
```

### 偏移和推拉

```html
<div class="row">
  <!-- 居中偏移 -->
  <div class="col-md-6 col-md-offset-3">
    置中內容
  </div>
</div>

<div class="row">
  <!-- 欄位順序控制 -->
  <div class="col-md-9 col-md-push-3">
    主內容（在手機上優先顯示）
  </div>
  <div class="col-md-3 col-md-pull-9">
    側邊欄
  </div>
</div>
```

## 按鈕（Buttons）

### 按鈕樣式

Bootstrap 提供了多種預設按鈕樣式：

```html
<!-- 基本按鈕 -->
<button class="btn btn-default">默认</button>

<!-- 語義化按鈕 -->
<button class="btn btn-primary">主要</button>
<button class="btn btn-success">成功</button>
<button class="btn btn-info">資訊</button>
<button class="btn btn-warning">警告</button>
<button class="btn btn-danger">危險</button>

<!-- 鏈接和輸入 -->
<a class="btn btn-primary" href="#">連結按鈕</a>
<input type="button" class="btn btn-primary" value="輸入按鈕">
```

### 按鈕尺寸

```html
<button class="btn btn-primary btn-lg">大按鈕</button>
<button class="btn btn-primary">預設尺寸</button>
<button class="btn btn-primary btn-sm">小按鈕</button>
<button class="btn btn-primary btn-xs">最小按鈕</button>
```

### 狀態按鈕

```html
<!-- 禁用狀態 -->
<button class="btn btn-primary" disabled="disabled">
  禁用按鈕
</button>

<!-- 加載狀態 -->
<button class="btn btn-primary" data-loading-text="加載中...">
  提交
</button>
```

### Less 樣式定義

```less
// 按鈕基本樣式
.btn {
  display: inline-block;
  padding: 4px 12px;
  margin-bottom: 0;
  font-size: @baseFontSize;
  font-weight: normal;
  text-align: center;
  cursor: pointer;
  border: 1px solid transparent;
  border-radius: 3px;
  white-space: nowrap;
}

// 按鈕變體
.btn-primary {
  .buttonBackground(@btnPrimaryBackground, @btnPrimaryBackgroundHighlight);
}
```

## 表單（Forms）

### 基本表單

```html
<form class="form-horizontal">
  <div class="form-group">
    <label class="col-sm-2 control-label" for="inputEmail">
      電子郵件
    </label>
    <div class="col-sm-10">
      <input type="email" class="form-control" id="inputEmail"
             placeholder="Email">
    </div>
  </div>

  <div class="form-group">
    <label class="col-sm-2 control-label" for="inputPassword">
      密碼
    </label>
    <div class="col-sm-10">
      <input type="password" class="form-control" id="inputPassword"
             placeholder="Password">
    </div>
  </div>

  <div class="form-group">
    <div class="col-sm-offset-2 col-sm-10">
      <div class="checkbox">
        <label>
          <input type="checkbox"> 記住我
        </label>
      </div>
    </div>
  </div>

  <div class="form-group">
    <div class="col-sm-offset-2 col-sm-10">
      <button type="submit" class="btn btn-default">登入</button>
    </div>
  </div>
</form>
```

### 內聯表單

```html
<form class="form-inline">
  <div class="form-group">
    <label class="sr-only" for="email">Email</label>
    <input type="email" class="form-control" id="email"
           placeholder="Enter email">
  </div>
  <div class="form-group">
    <label class="sr-only" for="password">Password</label>
    <input type="password" class="form-control" id="password"
           placeholder="Password">
  </div>
  <button type="submit" class="btn btn-default">登入</button>
</form>
```

### 表單驗證狀態

```html
<div class="form-group has-success has-feedback">
  <label class="control-label" for="inputSuccess">
    輸入成功
  </label>
  <input type="text" class="form-control" id="inputSuccess">
  <span class="glyphicon glyphicon-ok form-control-feedback"></span>
</div>

<div class="form-group has-warning has-feedback">
  <label class="control-label" for="inputWarning">
    輸入警告
  </label>
  <input type="text" class="form-control" id="inputWarning">
  <span class="glyphicon glyphicon-warning-sign form-control-feedback"></span>
</div>

<div class="form-group has-error has-feedback">
  <label class="control-label" for="inputError">
    輸入錯誤
  </label>
  <input type="text" class="form-control" id="inputError">
  <span class="glyphicon glyphicon-remove form-control-feedback"></span>
</div>
```

## 導航元件

### 導航欄（Navbar）

```html
<nav class="navbar navbar-default">
  <div class="container-fluid">
    <div class="navbar-header">
      <button type="button" class="navbar-toggle collapsed"
              data-toggle="collapse" data-target="#navbar">
        <span class="sr-only">切換導航</span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
      </button>
      <a class="navbar-brand" href="#">
        <img alt="Brand" src="logo.png">
      </a>
    </div>

    <div class="collapse navbar-collapse" id="navbar">
      <ul class="nav navbar-nav">
        <li class="active"><a href="#">首頁</a></li>
        <li><a href="#">關於</a></li>
        <li class="dropdown">
          <a href="#" class="dropdown-toggle"
             data-toggle="dropdown">
            產品 <span class="caret"></span>
          </a>
          <ul class="dropdown-menu">
            <li><a href="#">產品 1</a></li>
            <li><a href="#">產品 2</a></li>
            <li class="divider"></li>
            <li><a href="#">所有產品</a></li>
          </ul>
        </li>
      </ul>
      <form class="navbar-form navbar-left">
        <div class="form-group">
          <input type="text" class="form-control"
                 placeholder="搜尋">
        </div>
        <button type="submit" class="btn btn-default">
          搜尋
        </button>
      </form>
    </div>
  </div>
</nav>
```

### 標籤導航（Tabs）

```html
<ul class="nav nav-tabs">
  <li class="active">
    <a href="#home" data-toggle="tab">首頁</a>
  </li>
  <li>
    <a href="#profile" data-toggle="tab">個人資料</a>
  </li>
  <li class="dropdown">
    <a href="#" class="dropdown-toggle"
       data-toggle="dropdown">
      下拉選單 <span class="caret"></span>
    </a>
    <ul class="dropdown-menu">
      <li><a href="#dropdown1" data-toggle="tab">選項 1</a></li>
      <li><a href="#dropdown2" data-toggle="tab">選項 2</a></li>
    </ul>
  </li>
</ul>
```

## 辅助類別

### 文字顏色

```html
<p class="text-muted">柔和文字</p>
<p class="text-primary">主要文字</p>
<p class="text-success">成功文字</p>
<p class="text-info">資訊文字</p>
<p class="text-warning">警告文字</p>
<p class="text-danger">危險文字</p>
```

### 背景顏色

```html
<p class="bg-primary">主要背景</p>
<p class="bg-success">成功背景</p>
<p class="bg-info">資訊背景</p>
<p class="bg-warning">警告背景</p>
<p class="bg-danger">危險背景</p>
```

### 顯示/隱藏

```html
<p class="visible-xs-block">僅在手機顯示</p>
<p class="visible-sm-block">僅在平板顯示</p>
<p class="visible-md-block">僅在桌面顯示</p>
<p class="visible-lg-block">僅在大桌面顯示</p>

<p class="hidden-xs">在手機隱藏</p>
<p class="hidden-sm">在平板隱藏</p>
```

## 結語

Bootstrap 的元件系統體現了幾個重要的設計原則：

1. **一致性**：所有元件使用相同的命名約定和樣式模式
2. **可組合性**：元件可以自由組合，創建複雜的 UI
3. **響應式**：內建對各種設備尺寸的支援
4. **可客製化**：通過 Less 變數可以輕鬆調整整體視覺風格

這些設計原則讓 Bootstrap 成為現代 Web 開發的基礎工具，影響了後續幾乎所有 UI 框架的設計。

下一篇文章我們將探討 Bootstrap 的 JavaScript 插件架構，了解這些 UI 元件如何與 jQuery 互動。

---

## 延伸閱讀

- [Bootstrap Components](https://www.google.com/search?q=Bootstrap+components+documentation)
- [Bootstrap Grid System](https://www.google.com/search?q=Bootstrap+grid+system+tutorial)
- [Form Controls](https://www.google.com/search?q=Bootstrap+forms+documentation)

---

*本篇文章為「AI 程式人雜誌 2010 年 7 月號」歷史回顧系列之一。*