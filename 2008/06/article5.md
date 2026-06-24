# 瀏覽器相容性處理

## 常見問題

### IE 特有

```javascript
// 事件處理
element.attachEvent('onclick', handler);

//  XMLHttpRequest
var xhr = new ActiveXObject('Microsoft.XMLHTTP');
```

### CSS Hack

```css
/* IE 6 */
* html .box { }

/* IE 7 */
*+html .box { }

/* IE 8 */
@media \0screen {
    .box { }
}
```

## 結論

使用 jQuery 等框架可以簡化相容性處理。

---

**延伸閱讀**

- [Browser+compatibility](https://www.google.com/search?q=browser+compatibility+javascript)