# AJAX 技術實作

## 前言

AJAX（Asynchronous JavaScript and XML）是 Web 2.0 時代的核心技術。本篇文章將詳細解析 AJAX 的原理，並提供 Python/JavaScript 混合實作範例。

---

## XMLHttpRequest 詳解

### 原始 AJAX 請求

```javascript
// 原始 XMLHttpRequest 用法
var xhr = new XMLHttpRequest();
xhr.open('GET', '/api/data', true);

xhr.onreadystatechange = function() {
    if (xhr.readyState === 4) {
        if (xhr.status === 200) {
            console.log(xhr.responseText);
        } else {
            console.error('Error:', xhr.status);
        }
    }
};

xhr.send();
```

### POST 請求

```javascript
// POST 請求範例
var xhr = new XMLHttpRequest();
xhr.open('POST', '/api/submit', true);
xhr.setRequestHeader('Content-Type', 'application/json');

xhr.onreadystatechange = function() {
    if (xhr.readyState === 4 && xhr.status === 200) {
        var response = JSON.parse(xhr.responseText);
        console.log(response);
    }
};

var data = JSON.stringify({ name: 'John', age: 30 });
xhr.send(data);
```

---

## jQuery AJAX 方法

```javascript
// jQuery AJAX 語法
$.ajax({
    url: '/api/data',
    type: 'GET',
    dataType: 'json',
    timeout: 5000,
    success: function(data, textStatus, xhr) {
        console.log('Success:', data);
    },
    error: function(xhr, textStatus, errorThrown) {
        console.error('Error:', textStatus);
    }
});

// 簡化版本
$.get('/api/data', function(data) {
    $('#result').html(data);
});

$.post('/api/submit', { name: 'John' }, function(response) {
    console.log(response);
});
```

---

## 原始碼

完整的 AJAX 模擬範例：[_code/ajax.py](_code/ajax.py)

```python
#!/usr/bin/env python3
"""AJAX Pattern Simulation - 非同步請求模擬"""

import json
import time
from typing import Callable, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

class RequestState(Enum):
    UNSENT = 0
    OPENED = 1
    HEADERS_RECEIVED = 2
    LOADING = 3
    DONE = 4

class AJAXRequest:
    def __init__(self):
        self.state = RequestState.UNSENT
        self.status = 0
        self.response_text = ""
        self.onreadystatechange: Optional[Callable] = None
        self._headers: Dict[str, str] = {}

    def open(self, method: str, url: str, async: bool = True):
        self.state = RequestState.OPENED
        self.method = method
        self.url = url
        self._trigger_callback()

    def setRequestHeader(self, name: str, value: str):
        self._headers[name] = value

    def send(self, data: Optional[str] = None):
        self._headers_received()
        self._loading(data)

    def _headers_received(self):
        self.state = RequestState.HEADERS_RECEIVED
        self.status = 200
        self._trigger_callback()

    def _loading(self, data: Optional[str]):
        self.state = RequestState.LOADING
        self._trigger_callback()
        time.sleep(0.01)
        self.response_text = self._mock_response()
        self.state = RequestState.DONE
        self._trigger_callback()

    def _mock_response(self) -> str:
        mock_data = {
            "user": {"id": 1, "name": "John", "email": "john@example.com"},
            "timestamp": datetime.now().isoformat(),
            "data": [1, 2, 3, 4, 5]
        }
        return json.dumps(mock_data)

    def _trigger_callback(self):
        if self.onreadystatechange:
            self.onreadystatechange()

class AJAXSimulator:
    @staticmethod
    def get(url: str, callback: Callable) -> AJAXRequest:
        req = AJAXRequest()
        def on_state_change():
            if req.state == RequestState.DONE:
                callback(req.response_text)
        req.onreadystatechange = on_state_change
        req.open('GET', url)
        req.send()
        return req

    @staticmethod
    def post(url: str, data: Dict, callback: Callable) -> AJAXRequest:
        req = AJAXRequest()
        def on_state_change():
            if req.state == RequestState.DONE:
                callback(req.response_text)
        req.onreadystatechange = on_state_change
        req.open('POST', url)
        req.setRequestHeader('Content-Type', 'application/json')
        req.send(json.dumps(data))
        return req

def demo():
    print("=== AJAX 模式模擬 ===")
    print()

    print("1. GET 請求")
    print("發送請求到 /api/users...")
    AJAXSimulator.get('/api/users', lambda response: print(f"回應: {response[:50]}..."))
    print()

    print("2. POST 請求")
    print("發送資料到 /api/submit...")
    AJAXSimulator.post('/api/submit', {'name': 'John', 'age': 30},
                      lambda response: print(f"回應: {response}"))
    print()

    print("=== 模擬完成 ===")

if __name__ == "__main__": demo()
```

---

## 執行結果

```
=== AJAX 模式模擬 ===

1. GET 請求
發送請求到 /api/users...
回應: {"user": {"id": 1, "name": "John", "email":...

2. POST 請求
發送資料到 /api/submit...
回應: {"user": {"id": 1, "name": "John", "email":...

=== 模擬完成 ===
```

---

## JSON vs XML

### 比較

```javascript
// XML 格式
<users>
    <user>
        <name>John</name>
        <age>30</age>
    </user>
    <user>
        <name>Mary</name>
        <age>25</age>
    </user>
</users>

// JSON 格式
{
    "users": [
        {"name": "John", "age": 30},
        {"name": "Mary", "age": 25}
    ]
}
```

### 優勢

```
JSON 優勢：
- 更緊湊
- JavaScript 原生支援
- 解析更快
- 對人類更易讀
```

---

## 結論

AJAX 技術徹底改變了 Web 應用的互動方式。從最初的 XMLHttpRequest 到現代的 fetch API，AJAX 的核心概念——非同步資料交換——仍然是現代 Web 開發的基石。

---

## 延伸閱讀

- [XMLHttpRequest 規範](https://www.google.com/search?q=XMLHttpRequest+specification)
- [jQuery AJAX 文檔](https://www.google.com/search?q=jQuery+ajax+documentation)
- [AJAX 最佳化](https://www.google.com/search?q=AJAX+best+practices)

---

*本篇文章為「AI 程式人雜誌 2007 年 2 月號」本期焦點系列補充文章。*