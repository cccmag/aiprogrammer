# JSON 取代 XML：資料交換格式的演進

## 概述

在 2007 年的 Web 開發領域，JSON (JavaScript Object Notation) 已經開始取代 XML 成為首選的資料交換格式。JSON 以其簡潔的語法和對 JavaScript 的原生支援，迅速成為 AJAX 應用和 RESTful API 的標準資料格式。

## XML 的歷史與問題

### XML 的優勢

XML（eXtensible Markup Language）在 2000 年代初期是 Web 服務和資料交換的標準：

```xml
<!-- XML 格式範例 -->
<?xml version="1.0" encoding="UTF-8"?>
<users>
    <user>
        <id>1</id>
        <name>John Doe</name>
        <email>john@example.com</email>
        <profile>
            <age>30</age>
            <city>New York</city>
        </profile>
        <interests>
            <interest>Programming</interest>
            <interest>Reading</interest>
        </interests>
    </user>
</users>
```

### XML 的問題

然而，XML 也有一些明顯的缺點：

1. **語法冗長** -- 標籤需要開始和結束
2. **解析複雜** -- DOM 解析需要較多程式碼
3. **傳輸量大** -- 重複的標籤名稱增加傳輸量
4. **人類不易閱讀** -- 複雜巢狀時難以追蹤

```javascript
// 解析 XML 的繁瑣過程
var xmlString = "<user><name>John</name></user>";
var parser = new DOMParser();
var xmlDoc = parser.parseFromString(xmlString, "text/xml");
var name = xmlDoc.getElementsByTagName("name")[0].childNodes[0].nodeValue;
```

## JSON 的崛起

### JSON 語法

JSON 以其簡潔的語法脫穎而出：

```json
// JSON 格式範例
{
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "profile": {
        "age": 30,
        "city": "New York"
    },
    "interests": ["Programming", "Reading"]
}
```

### 比較：同一筆資料

```xml
<!-- XML 版本（152 字元） -->
<user><id>1</id><name>John</name><email>john@example.com</email></user>
```

```json
// JSON 版本（68 字元）
{"id":1,"name":"John","email":"john@example.com"}
```

JSON 節省了約 55% 的傳輸量。

## JavaScript 與 JSON

### 原生解析

JSON 與 JavaScript 有天然的親和力：

```javascript
// 解析 JSON
var jsonString = '{"name": "John", "age": 30}';
var obj = JSON.parse(jsonString);
console.log(obj.name);  // "John"

// 序列化為 JSON
var data = { name: "John", age: 30 };
var jsonString = JSON.stringify(data);
console.log(jsonString);  // '{"name":"John","age":30}'
```

### eval 的早期使用

在 JSON.parse 出現之前（2007 年瀏覽器支援情況），開發者使用 eval 解析 JSON：

```javascript
// 早期 JSON 解析方式（存在安全風險）
var jsonString = '{"name": "John"}';
var obj = eval("(" + jsonString + ")");  // 需要括號避免語法問題
```

### 安全問題

eval 的安全問題：

```javascript
// 危險！程式碼注入攻擊
var malicious = '({"name": "John"}); alert("XSS!");';
var obj = eval("(" + malicious + ")");  // 執行了恶意程式碼

// 安全的做法：使用 JSON.parse
var obj = JSON.parse(malicious);  // 拋出語法錯誤
```

## JSON 在 AJAX 中的應用

### jQuery 與 JSON

```javascript
// jQuery AJAX 請求 JSON
$.ajax({
    url: "/api/user",
    dataType: "json",
    success: function(user) {
        console.log(user.name);
        $("#name").text(user.name);
        $("#email").html(user.email);
    },
    error: function(xhr, status, error) {
        console.error("請求失敗:", error);
    }
});

// 簡化版本
$.getJSON("/api/user", function(user) {
    console.log(user.name);
});

// 提交 JSON 資料
$.ajax({
    url: "/api/user",
    type: "POST",
    contentType: "application/json",
    data: JSON.stringify({ name: "John", email: "john@example.com" }),
    success: function(response) {
        console.log("成功:", response);
    }
});
```

### 原生 JavaScript

```javascript
// 建立 XMLHttpRequest
var xhr = new XMLHttpRequest();
xhr.open("GET", "/api/data.json", true);

xhr.onreadystatechange = function() {
    if (xhr.readyState === 4 && xhr.status === 200) {
        var data = JSON.parse(xhr.responseText);
        processData(data);
    }
};

xhr.send();

// POST 請求
xhr.open("POST", "/api/create", true);
xhr.setRequestHeader("Content-Type", "application/json");
xhr.send(JSON.stringify({ name: "John", age: 30 }));
```

## JSON 資料類型

### 支援的類型

```javascript
// 物件
{ "name": "John" }

// 陣列
[1, 2, 3, 4, 5]

// 字串
{ "message": "Hello, World!" }

// 數字
{ "price": 29.99, "count": 100 }

// 布林值
{ "active": true, "deleted": false }

// null
{ "middleName": null }

// 巢狀結構
{
    "user": {
        "name": "John",
        "address": {
            "city": "New York",
            "zip": "10001"
        }
    },
    "orders": [
        { "id": 1, "total": 99.99 },
        { "id": 2, "total": 149.99 }
    ]
}
```

### 無效的 JSON

```javascript
// 這些都不是有效的 JSON
{ name: "John" }           // 鍵必須是字串
{ 'name': 'John' }         // 必須使用雙引號
{ name: "John", }           // 結尾不能有逗號
{ name: "John" }            // 這是 JavaScript 物件，不是 JSON
```

## JSON 的標準化

### RFC 4627

2006 年，JSON 被正式標準化為 RFC 4627，定義了 JSON 的 MIME type 為 `application/json`。

### JSON Schema

JSON Schema 用於描述和驗證 JSON 結構：

```json
{
    "$schema": "http://json-schema.org/draft-04/schema#",
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
            "minLength": 1,
            "maxLength": 100
        },
        "email": {
            "type": "string",
            "format": "email"
        },
        "age": {
            "type": "integer",
            "minimum": 0,
            "maximum": 150
        }
    },
    "required": ["name", "email"]
}
```

## 伺服器端的 JSON

### Python

```python
import json

# 序列化
data = {"name": "John", "age": 30}
json_string = json.dumps(data)

# 反序列化
data = json.loads(json_string)

# 檔案操作
with open("data.json", "w") as f:
    json.dump(data, f, indent=2)
```

### PHP

```php
<?php
// 序列化
$data = array("name" => "John", "age" => 30);
$json = json_encode($data);

// 反序列化
$data = json_decode($json, true);

// 讀取 JSON 檔案
$json_string = file_get_contents("data.json");
$data = json_decode($json_string, true);
?>
```

### Ruby

```ruby
require "json"

# 序列化
data = { name: "John", age: 30 }
json_string = data.to_json

# 反序列化
data = JSON.parse(json_string)
```

## JSON vs XML 比較

| 方面 | JSON | XML |
|------|------|-----|
| 語法簡潔性 | 簡潔 | 冗長 |
| 資料類型 | 原生支援 | 需要 schema |
| 解析速度 | 快 | 慢 |
| 可讀性 | 高 | 中 |
| 查詢能力 | 有限 | XPath/XQuery |
| 傳輸效率 | 高 | 低 |
| 工具支援 | 完善 | 成熟 |

## 結語

2007 年是 JSON 取代 XML 成为 Web 資料交換主流格式的轉捩點。JSON 以其簡潔、高效和對 JavaScript 的原生支援，成為 AJAX 應用和 RESTful API 的首選格式。這種趨勢一直延續到今天，JSON 已經成為 Web 開發中最重要的資料格式之一。

---

*延伸閱讀：*
- [JSON 官方網站](https://developers.google.com/search/?q=json+official)
- [JSON vs XML 比較](https://developers.google.com/search/?q=json+vs+xml)