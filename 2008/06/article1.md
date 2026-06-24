# JavaScript 框架的比較與選擇

## jQuery vs Prototype vs MooTools

### jQuery

```javascript
$('#id').addClass('active');
$('div').each(function() { });
$.ajax({ url: '/api' });
```

### Prototype

```javascript
$('id').addClassName('active');
$$('div').each(function(el) { });
new Ajax.Request('/api');
```

### MooTools

```javascript
$('id').addClass('active');
$$('div').each(function(el) { });
new Request({ url: '/api' }).send();
```

## 選擇建議

| 框架 | 適用場景 |
|------|----------|
| jQuery | DOM 操作為主 |
| Prototype | 類別擴展 |
| MooTools | 元程式設計 |

## 結論

選擇框架時要考慮專案需求和團隊熟悉度。

---

**延伸閱讀**

- [jQuery 的設計哲學](focus1.md)