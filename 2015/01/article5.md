# Bootstrap 4 開發中：全新元素布局系統

## 前言

Bootstrap 4 正在開發中，引入了從 Less 到 Sass 的重大轉變，以及全新的 Flexbox 布局系統。

## 從 Less 轉向 Sass

```bash
# Bootstrap 3（Less）
lessc bootstrap.less bootstrap.css

# Bootstrap 4（Sass）
sass --style=compressed scss/bootstrap.scss bootstrap.css
```

## Flexbox 支援

```html
<!-- Flexbox 工具類別 -->
<div class="d-flex justify-content-between">
  <div>左側</div>
  <div>右側</div>
</div>

<!-- 響應式顯示 -->
<div class="d-flex flex-column flex-md-row">
  ...
</div>
```

## 新元件

```html
<!-- 卡片元件 -->
<div class="card">
  <div class="card-header">標題</div>
  <div class="card-body">
    <h5 class="card-title">標題</h5>
    <p class="card-text">內容</p>
  </div>
  <div class="card-footer">備註</div>
</div>
```

## 結語

Bootstrap 4 的開發代表了前端框架向現代 CSS 技術的靠攏，Flexbox 和 Sass 的支援讓 Bootstrap 更加強大。

---

## 延伸閱讀

- [Bootstrap 4 開發公告](https://www.google.com/search?q=Bootstrap+4+alpha+released+2015)

---

*本篇文章為「AI 程式人雜誌 2015 年 1 月號」文章之一。*