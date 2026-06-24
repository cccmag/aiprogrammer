# JSON 與 XML 的抉擇：資料格式的選擇

## XML 的優勢

XML（eXtensible Markup Language）在 2000 年代初期是 Web 服務的標準格式。XML 的優點包括：

### 結構化與自我描述

```xml
<?xml version="1.0" encoding="UTF-8"?>
<order id="12345">
    <customer>
        <name>John Doe</name>
        <email>john@example.com</email>
        <address>
            <street>123 Main St</street>
            <city>Taipei</city>
            <zip>100</zip>
        </address>
    </customer>
    <items>
        <item product-id="P001">
            <name>Widget A</name>
            <quantity>3</quantity>
            <price currency="TWD">299</price>
        </item>
        <item product-id="P002">
            <name>Widget B</name>
            <quantity>1</quantity>
            <price currency="TWD">599</price>
        </item>
    </items>
    <total currency="TWD">1496</total>
</order>
```

### 豐富的生態系統

```python
# Python XML 處理
import xml.etree.ElementTree as ET

tree = ET.parse('order.xml')
root = tree.getroot()

for item in root.findall('.//item'):
    name = item.find('name').text
    qty = item.find('quantity').text
    print(f'{name}: {qty}')
```

## JSON 的崛起

2007 年，JSON 正在快速取代 XML 成為 Web API 的首選格式。

### JSON 的簡潔性

```json
{
  "id": 12345,
  "customer": {
    "name": "John Doe",
    "email": "john@example.com",
    "address": {
      "street": "123 Main St",
      "city": "Taipei",
      "zip": "100"
    }
  },
  "items": [
    {"productId": "P001", "name": "Widget A", "quantity": 3, "price": 299},
    {"productId": "P002", "name": "Widget B", "quantity": 1, "price": 599}
  ],
  "total": 1496
}
```

### JavaScript 原生支援

```javascript
// JavaScript 原生 JSON 支援（2007 年的瀏覽器）
var data = JSON.parse(xhr.responseText);

// 存取資料
console.log(data.customer.name);
console.log(data.items[0].name);

// 序列化
var jsonString = JSON.stringify(data);
```

## 比較分析

```
JSON 與 XML 比較：
────────────────────────────────────────────────────────
特性              JSON                    XML
────────────────────────────────────────────────────────
資料大小          較小                    較大（標籤冗長）
解析速度          快（原生 JS）            慢（需 DOM 解析）
人類可讀性        高（簡潔）              中（標籤干擾）
類型支援          有限（字串、數值、布林）豐富（XML Schema）
巢狀結構          支援                    支援
屬性 vs 元素      需抉擇                  可並存
查詢能力          有限                    XPath/XQuery
附加說明          無（需文件）            自我描述
生態系統          Web API 為主            企業應用廣泛
────────────────────────────────────────────────────────
```

## 何時選擇 JSON

適合使用 JSON 的場景：

### 1. JavaScript 優先的應用

```javascript
// AJAX 回應（瀏覽器端）
fetch('/api/users')
    .then(response => response.json())
    .then(users => {
        // 直接使用
        users.forEach(u => console.log(u.name));
    });
```

### 2. 行動應用

```json
// 行動 API 回應（頻寬敏感）
{
  "users": [
    {"id": 1, "name": "John"},
    {"id": 2, "name": "Mary"}
  ]
}
```

### 3. 簡單的 CRUD API

```http
# 簡單的資源 API
GET /api/products/123
Accept: application/json

# 回應
{
  "id": 123,
  "name": "Widget",
  "price": 29.99
}
```

## 何時選擇 XML

適合使用 XML 的場景：

### 1. 文件類資料

```xml
<!-- 文件、書籍、複雜結構 -->
<book>
    <metadata>
        <title>XML 入門</title>
        <author>John Smith</author>
        <chapters>
            <chapter num="1">基礎概念</chapter>
            <chapter num="2">DTD 與 Schema</chapter>
        </chapters>
    </metadata>
</book>
```

### 2. 需要驗證的結構

```xml
<!-- XML Schema 驗證 -->
<order xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xsi:noNamespaceSchemaLocation="order.xsd">
    <id>123</id>
    <total>1496</total>
</order>
```

### 3. 企業整合

SOAP Web 服務仍需要 XML：

```xml
<!-- SOAP 訊息必須是 XML -->
<soap:Envelope>
    <soap:Body>
        <GetOrderRequest xmlns="http://example.com">
            <orderId>123</orderId>
        </GetOrderRequest>
    </soap:Body>
</soap:Envelope>
```

## 實務建議

### 2007 年的選擇

```python
# 根據應用場景選擇

def api_response(data, format='json'):
    if format == 'json':
        return jsonify(data)
    elif format == 'xml':
        return xml_response(data)
```

### 內容協商

```http
# 客戶端指定偏好
Accept: application/json, application/xml;q=0.5

# 伺服器根據 Accept 頭回應
GET /api/users HTTP/1.1
Accept: application/json

---

HTTP/1.1 200 OK
Content-Type: application/json

[{"id": 1, "name": "John"}]
```

## 結語

2007 年的趨勢是：**新的 Web API 越來越傾向使用 JSON，但 XML 在企業應用和文件處理中仍有一席之地**。

選擇建議：
- **對外公開的 Web API**：優先選擇 JSON
- **企業整合、SOAP 服務**：使用 XML
- **文件類資料**：XML 更適合
- **簡單的 CRUD API**：JSON 更高效

---

## 延伸閱讀

- [JSON+vs+XML+2007](https://www.google.com/search?q=JSON+vs+XML+2007)
- [when+to+use+JSON+vs+XML](https://www.google.com/search?q=when+to+use+JSON+vs+XML)
- [REST+API+JSON+best+practices](https://www.google.com/search?q=REST+API+JSON+best+practices)

---

*本篇文章為「AI 程式人雜誌 2007 年 5 月號」本期焦點系列之一。*