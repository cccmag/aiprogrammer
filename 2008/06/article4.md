# 前端效能優化的實踐

## 最小化

```bash
# JavaScript
uglifyjs app.js -o app.min.js

# CSS
csso style.css -o style.min.css
```

## 合併

```html
<!-- 合併多個 CSS -->
<link rel="stylesheet" href="combined.min.css">

<!-- 合併多個 JS -->
<script src="combined.min.js"></script>
```

## 快取

```html
<!-- 添加版本號 -->
<script src="app.js?v=1.0.1"></script>
```

## 結論

效能優化提升使用者體驗。

---

**延伸閱讀**

- [前端效能優化](https://www.google.com/search?q=frontend+performance+optimization)