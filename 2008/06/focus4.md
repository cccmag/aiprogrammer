# Ajax 與非同步請求

## $.ajax 基本用法

### 設定選項

```javascript
$.ajax({
    url: '/api/data',
    type: 'GET',
    dataType: 'json',
    data: { page: 1, limit: 10 },
    success: function(data) {
        console.log(data);
    },
    error: function(xhr, status, error) {
        console.error(error);
    },
    complete: function(xhr, status) {
        console.log('Request complete');
    },
    timeout: 5000
});
```

## 快捷方法

### GET 請求

```javascript
$.get('/api/data', { id: 1 }, function(data) {
    console.log(data);
}, 'json');
```

### POST 請求

```javascript
$.post('/api/submit', { name: 'John', email: 'john@example.com' },
    function(response) {
        console.log(response);
    }, 'json');
```

### 取得 JSON

```javascript
$.getJSON('/api/users', function(users) {
    $.each(users, function(index, user) {
        console.log(user.name);
    });
});
```

### 載入 HTML

```javascript
$('#content').load('/partials/header.html');
```

## 全域設定

```javascript
// 設定預設值
$.ajaxSetup({
    url: '/api',
    type: 'POST',
    dataType: 'json',
    timeout: 10000
});

// 現在所有 $.ajax 呼叫都會使用這些預設值
$.ajax({
    data: { key: 'value' }  // url, type 等使用預設值
});
```

## 事件鉤子

```javascript
//全域事件
$(document).ajaxStart(function() {
    $('#loading').show();
});

$(document).ajaxStop(function() {
    $('#loading').hide();
});

$(document).ajaxError(function(event, xhr, options, error) {
    console.error('Ajax error:', error);
});

$(document).ajaxSuccess(function(event, xhr, options) {
    console.log('Ajax success');
});
```

## 處理 JSON

### JSON.stringify

```javascript
var data = { name: 'John', age: 30 };
var json = JSON.stringify(data);
```

### JSON.parse

```javascript
var json = '{"name":"John","age":30}';
var data = JSON.parse(json);
```

### jQuery 的自動處理

```javascript
// 當 dataType: 'json' 時
// jQuery 會自動解析回應為 JavaScript 物件
$.ajax({
    url: '/api/user',
    dataType: 'json',
    success: function(user) {
        // user 已是 JavaScript 物件
        console.log(user.name);
    }
});
```

## 跨域請求

### JSONP

```javascript
$.ajax({
    url: 'http://example.com/api',
    dataType: 'jsonp',
    jsonp: 'callback',
    success: function(data) {
        console.log(data);
    }
});

// 快捷方法
$.getJSON('http://example.com/api?callback=?', function(data) {
    console.log(data);
});
```

### CORS（需要伺服器支援）

```javascript
$.ajax({
    url: 'http://other-domain.com/api',
    dataType: 'json',
    headers: {
        'Authorization': 'Bearer token'
    },
    xhrFields: {
        withCredentials: true
    }
});
```

## 佇列請求

### Sequential Ajax

```javascript
$.ajax({
    url: '/api/step1',
    success: function(data1) {
        $.ajax({
            url: '/api/step2',
            data: { fromStep1: data1 },
            success: function(data2) {
                $.ajax({
                    url: '/api/step3',
                    data: { fromStep2: data2 },
                    success: function(final) {
                        console.log(final);
                    }
                });
            }
        });
    }
});
```

### 使用 Deferred

```javascript
$.when($.get('/api/step1'), $.get('/api/step2'))
    .then(function(result1, result2) {
        console.log(result1[0]);
        console.log(result2[0]);
    });
```

## 結論

jQuery 的 Ajax 功能完善，支援從簡單的 GET 請求到複雜的跨域和錯誤處理。善用 Deferred 可以優雅地處理非同步流程。

---

**延伸閱讀**

- [事件處理與委派](focus3.md)
- [jQuery+Ajax+tutorial](https://www.google.com/search?q=jQuery+Ajax+tutorial)