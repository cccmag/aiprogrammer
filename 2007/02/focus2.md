# AJAX 技術的成熟

## 前言

AJAX（Asynchronous JavaScript and XML）並非新技術，但到了 2007 年，這項技術終於完全成熟，成為 Web 2.0 應用的核心。

## XMLHttpRequest 的歷史

### 1999 年的發明

Microsoft 在 1999 年的 Outlook Web Access 團隊發明了 XMLHttpRequest（最初稱為 IXMLHTTPRequest）：

```javascript
// 原始發明
var xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
xmlhttp.open("GET", "/data.xml", true);
xmlhttp.onreadystatechange = function() {
    if (xmlhttp.readyState == 4) {
        alert(xmlhttp.responseText);
    }
};
xmlhttp.send();
```

### 主流瀏覽器支援

2007 年，所有主流瀏覽器都支援 XMLHttpRequest：

```python
# 2007 年瀏覽器 AJAX 支援
BROWSER_AJAX_SUPPORT = {
    "IE": "ActiveX 控制（後來內建 XMLHttpRequest）",
    "Firefox": "原生 XMLHttpRequest",
    "Safari": "原生 XMLHttpRequest",
    "Opera": "原生 XMLHttpRequest"
}
```

## 非同步模式的優勢

### 對比傳統同步模式

```javascript
// 同步模式（傳統表單提交）
// 頁面會刷新，使用者等待

// 非同步模式（AJAX）
// 頁面不刷新，后臺請求
$.get('/api/data', function(response) {
    $('#content').html(response);
});
```

### 使用場景

```python
# AJAX 適合的場景
AJAX_USE_CASES = {
    "表單驗證": "即時檢查用戶名是否可用",
    "自動完成": "搜尋時即時顯示建議",
    "無刷新分頁": "載入更多內容",
    "即時更新": "股票報價、聊天訊息",
    "檔案上傳": "進度條顯示"
}
```

## 前端框架的繁榮

### 2007 年的主要框架

```
┌────────────────────────────────────────────────────────┐
│            2007 年 JavaScript 框架                      │
├────────────────────────────────────────────────────────┤
│                                                        │
│  完整框架：                                            │
│  - Dojo Toolkit —— 完整工具箱                         │
│  - Ext JS —— 企業級 UI                               │
│  - YUI —— Yahoo 的框架                               │
│                                                        │
│  函式庫：                                              │
│  - jQuery —— DOM 操作                               │
│  - Prototype —— 類別擴展                             │
│  - MooTools —— 模組化                               │
│                                                        │
│  特殊用途：                                            │
│  - Scriptaculous —— 視覺效果                         │
│  - Raphael —— SVG 圖表                               │
│                                                        │
└────────────────────────────────────────────────────────┘
```

### jQuery 的 AJAX 封裝

```javascript
// jQuery 封裝的 AJAX 方法
$.ajax({
    url: '/api/endpoint',
    type: 'POST',
    data: JSON.stringify({ name: 'John' }),
    contentType: 'application/json',
    dataType: 'json',
    success: function(data) {
        console.log(data);
    }
});
```

## JSON 的崛起

### JSON vs XML

2007 年，JSON 開始取代 XML 成為 AJAX 資料交換的首選格式：

```javascript
// JSON 優點
JSON_ADVANTAGES = {
    "緊湊": "比 XML 更短",
    "原生支援": "JavaScript 直接解析",
    "易讀": "對人類更友好",
    "快速": "解析速度更快"
};
```

## 結論

AJAX 技術的成熟是 Web 2.0 革命的技術基礎。它讓 Web 應用可以像桌面應用一樣即時、互動，為使用者帶來全新的體驗。

---

## 延伸閱讀

- [XMLHttpRequest 歷史](https://www.google.com/search?q=XMLHttpRequest+history)
- [AJAX 框架比較](https://www.google.com/search?q=AJAX+framework+comparison+2007)

---

*本篇文章為「AI 程式人雜誌 2007 年 2 月號」本期焦點系列文章。*