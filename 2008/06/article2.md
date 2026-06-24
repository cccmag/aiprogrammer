# Ajax 技術的深度解析

## XMLHttpRequest

```javascript
var xhr = new XMLHttpRequest();
xhr.open('GET', '/api/data', true);
xhr.onreadystatechange = function() {
    if (xhr.readyState === 4 && xhr.status === 200) {
        var data = JSON.parse(xhr.responseText);
        console.log(data);
    }
};
xhr.send();
```

## jQuery Ajax

```javascript
$.ajax({
    url: '/api/data',
    type: 'GET',
    dataType: 'json',
    success: function(data) {
        console.log(data);
    }
});
```

## 跨域請求

### JSONP

```javascript
$.getJSON('http://example.com/api?callback=?', function(data) {
    console.log(data);
});
```

## 結論

Ajax 是現代 Web 應用的基礎技術。

---

**延伸閱讀**

- [Ajax 與非同步請求](focus4.md)