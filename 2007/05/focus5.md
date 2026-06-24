# AJAX 與 REST：瀏覽器端的 Web 服務呼叫

## AJAX 的興起

AJAX（Asynchronous JavaScript and XML）技術在 2005 年後迅速普及，徹底改變了 Web 應用的互動模式。

### AJAX 的核心概念

```javascript
// XMLHttpRequest 基礎用法
function fetchUser(userId) {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/api/users/' + userId, true);

    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                var user = JSON.parse(xhr.responseText);
                displayUser(user);
            } else {
                showError('載入失敗');
            }
        }
    };

    xhr.send(null);
}
```

## REST API 呼叫

### GET 請求

```javascript
// GET - 讀取資源
function getUsers() {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/api/users', true);

    xhr.setRequestHeader('Accept', 'application/json');

    xhr.onload = function() {
        if (xhr.status === 200) {
            var users = JSON.parse(xhr.responseText);
            renderUserList(users);
        }
    };

    xhr.send();
}
```

### POST 請求

```javascript
// POST - 建立資源
function createUser(userData) {
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/api/users', true);

    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.setRequestHeader('Accept', 'application/json');

    xhr.onload = function() {
        if (xhr.status === 201) {
            var newUser = JSON.parse(xhr.responseText);
            addUserToList(newUser);
        }
    };

    xhr.send(JSON.stringify(userData));
}
```

### PUT 請求

```javascript
// PUT - 更新資源
function updateUser(userId, userData) {
    var xhr = new XMLHttpRequest();
    xhr.open('PUT', '/api/users/' + userId, true);

    xhr.setRequestHeader('Content-Type', 'application/json');

    xhr.onload = function() {
        if (xhr.status === 200) {
            var updated = JSON.parse(xhr.responseText);
            refreshUser(updated);
        }
    };

    xhr.send(JSON.stringify(userData));
}
```

### DELETE 請求

```javascript
// DELETE - 刪除資源
function deleteUser(userId) {
    var xhr = new XMLHttpRequest();
    xhr.open('DELETE', '/api/users/' + userId, true);

    xhr.onload = function() {
        if (xhr.status === 204) {
            removeUserFromList(userId);
        }
    };

    xhr.send();
}
```

## 包裝函數

### AJAX 輔助函數

```javascript
// AJAX 包裝函數
var API = {
    get: function(url) {
        return this.request('GET', url);
    },

    post: function(url, data) {
        return this.request('POST', url, data);
    },

    put: function(url, data) {
        return this.request('PUT', url, data);
    },

    delete: function(url) {
        return this.request('DELETE', url);
    },

    request: function(method, url, data) {
        return new Promise(function(resolve, reject) {
            var xhr = new XMLHttpRequest();
            xhr.open(method, url, true);

            xhr.setRequestHeader('Content-Type', 'application/json');
            xhr.setRequestHeader('Accept', 'application/json');

            xhr.onload = function() {
                if (xhr.status >= 200 && xhr.status < 300) {
                    try {
                        resolve(JSON.parse(xhr.responseText));
                    } catch (e) {
                        resolve(xhr.responseText);
                    }
                } else {
                    reject(new Error(xhr.status + ': ' + xhr.statusText));
                }
            };

            xhr.onerror = function() {
                reject(new Error('Network error'));
            };

            if (data) {
                xhr.send(JSON.stringify(data));
            } else {
                xhr.send();
            }
        });
    }
};

// 使用方式
API.get('/api/users/123')
    .then(function(user) {
        console.log(user);
    })
    .catch(function(error) {
        console.error(error);
    });
```

## 跨域問題與解決方案

### 同源策略

瀏覽器的同源策略（Same-Origin Policy）限制 JavaScript 只能訪問同源的資源：

```javascript
// 這些請求會被阻止
// 假設當前頁面是 http://example.com

// 不同域
// http://other.com/api  → 阻止

// 不同子域
// http://api.example.com/api  → 阻止

// 不同端口
// http://example.com:8080/api  → 阻止

// 不同協定
// https://example.com/api  → 阻止
```

### 解決方案 1：JSONP

```javascript
// JSONP 客戶端
function jsonp(url, callback) {
    var callbackName = 'jsonp_' + Date.now();
    window[callbackName] = function(data) {
        delete window[callbackName];
        document.body.removeChild(script);
        callback(data);
    };

    var script = document.createElement('script');
    script.src = url + '?callback=' + callbackName;
    document.body.appendChild(script);
}

// 使用
jsonp('/api/users?format=jsonp', function(data) {
    console.log(data);
});
```

```python
# 伺服器端支援 JSONP
@app.route('/api/users')
def get_users():
    callback = request.args.get('callback', '')
    users = get_all_users()

    if callback:
        # JSONP 回應
        return Response(
            f'{callback}({json.dumps(users)})',
            mimetype='application/javascript'
        )
    else:
        return jsonify(users)
```

### 解決方案 2：CORS

```python
# Flask + CORS 支援
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = 'http://example.com'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'

    if request.method == 'OPTIONS':
        response.headers['Access-Control-Max-Age'] = '3600'

    return response
```

```javascript
// CORS 請求
var xhr = new XMLHttpRequest();
xhr.open('GET', 'http://api.example.com/data', true);

xhr.withCredentials = true;  // 攜帶 cookies

xhr.send();
```

## 錯誤處理

```javascript
// 統一的錯誤處理
function apiRequest(method, url, data) {
    return new Promise(function(resolve, reject) {
        var xhr = new XMLHttpRequest();
        xhr.open(method, url, true);

        xhr.setRequestHeader('Content-Type', 'application/json');

        xhr.onload = function() {
            if (xhr.status >= 200 && xhr.status < 300) {
                try {
                    resolve(JSON.parse(xhr.responseText));
                } catch (e) {
                    resolve(xhr.responseText);
                }
            } else if (xhr.status === 401) {
                reject({ code: 401, message: 'Unauthorized' });
            } else if (xhr.status === 404) {
                reject({ code: 404, message: 'Not found' });
            } else if (xhr.status >= 500) {
                reject({ code: 500, message: 'Server error' });
            } else {
                reject({ code: xhr.status, message: 'Unknown error' });
            }
        };

        xhr.onerror = function() {
            reject({ code: 'NETWORK', message: 'Network error' });
        };

        if (data) {
            xhr.send(JSON.stringify(data));
        } else {
            xhr.send();
        }
    });
}
```

## 結語

AJAX 與 REST 的結合，催生了「單頁應用」（SPA）的興起。瀏覽器端的 JavaScript 可以直接與伺服器端的 REST API 互動，無需頁面刷新。

2007 年的 AJAX 生態：
- **jQuery.ajax()**：最流行的 AJAX 包裝
- **Prototype**：另一個流行的框架
- **Dojo**：企業級解決方案

這些框架都提供了簡化 AJAX 呼叫的 API，讓開發者可以更專注於業務邏輯。

---

## 延伸閱讀

- [AJAX+REST+API+2007](https://www.google.com/search?q=AJAX+REST+API+2007)
- [XMLHttpRequest+CORS](https://www.google.com/search?q=XMLHttpRequest+CORS)
- [JSONP+cross+domain+AJAX](https://www.google.com/search?q=JSONP+cross+domain+AJAX)

---

*本篇文章為「AI 程式人雜誌 2007 年 5 月號」本期焦點系列之一。*