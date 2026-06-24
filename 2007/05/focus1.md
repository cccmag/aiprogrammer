# SOAP 與 REST 的比較：兩種 Web 服務架構

## SOAP：企業級 XML 協定

SOAP（Simple Object Access Protocol）誕生於 1998 年，由 Microsoft、IBM 等公司推動。SOAP 的設計目標是「企業級的 Web 服務互操作性」。

### SOAP 訊息格式

```xml
<?xml version="1.0" encoding="UTF-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://example.com/stock">
  <soap:Header>
    <tns:AuthHeader>
      <tns:Username>user123</tns:Username>
      <tns:Password>secret</tns:Password>
    </tns:AuthHeader>
  </soap:Header>
  <soap:Body>
    <tns:GetStockPrice>
      <tns:symbol>GOOG</tns:symbol>
    </tns:GetStockPrice>
  </soap:Body>
</soap:Envelope>
```

### SOAP 的元件

```
SOAP 協定堆疊：
────────────────
┌─────────────────┐
│ Service Layer   │ WS-Discovery, WS-Eventing
├─────────────────┤
│ Description     │ WSDL, WSIL
├─────────────────┤
│ Messaging       │ SOAP, WS-Addressing
├─────────────────┤
│ Transport       │ HTTP, SMTP, JMS
├─────────────────┤
│ Security        │ WS-Security, SAML
└─────────────────┘
```

### WSDL：服務介面定義

```xml
<?xml version="1.0" encoding="UTF-8"?>
<definitions name="StockService"
    targetNamespace="http://example.com/stock"
    xmlns="http://schemas.xmlsoap.org/wsdl/"
    xmlns:soap="http://schemas.xmlsoap.org/wsdl/soap/"
    xmlns:tns="http://example.com/stock"
    xmlns:xsd="http://www.w3.org/2001/XMLSchema">

  <message name="GetStockPriceInput">
    <part name="symbol" type="xsd:string"/>
  </message>

  <message name="GetStockPriceOutput">
    <part name="price" type="xsd:float"/>
  </message>

  <portType name="StockPortType">
    <operation name="GetStockPrice">
      <input message="tns:GetStockPriceInput"/>
      <output message="tns:GetStockPriceOutput"/>
    </operation>
  </portType>

  <binding name="StockBinding" type="tns:StockPortType">
    <soap:binding style="document" transport="http://schemas.xmlsoap.org/soap/http"/>
    <operation>
      <soap:operation soapAction="http://example.com/GetStockPrice"/>
      <input><soap:body use="literal"/></input>
      <output><soap:body use="literal"/></output>
    </operation>
  </binding>

  <service name="StockService">
    <port name="StockPort" binding="tns:StockBinding">
      <soap:address location="http://example.com/stock"/>
    </port>
  </service>
</definitions>
```

## REST：網路原生架構

REST（Representational State Transfer）是由 Roy Fielding 在 2000 年博士論文中提出的架構風格。REST 不是一個協定，而是一組設計原則。

### REST 的核心原則

1. **客戶端-伺服器分離**
2. **Stateless（無狀態）**
3. **可緩存**
4. **統一介面**
5. **分層系統**

### REST 的 HTTP 應用

```http
GET /stocks/GOOG HTTP/1.1
Host: api.example.com
Accept: application/json

---

HTTP/1.1 200 OK
Content-Type: application/json

{
  "symbol": "GOOG",
  "price": 520.30,
  "currency": "USD",
  "timestamp": "2007-05-15T10:30:00Z"
}
```

## SOAP vs REST：功能比較

```
SOAP 與 REST 比較（2007 年）：
─────────────────────────────────────────────────────────
特性              SOAP                    REST
─────────────────────────────────────────────────────────
資料格式          XML                     JSON, XML, YAML
介面定義          WSDL                    無強制標準
傳輸層            HTTP, SMTP, JMS         通常只用 HTTP
設計風格          Remote Procedure Call   Resource-oriented
類型系統          完整（XML Schema）      無（字串為主）
安全性            WS-Security             HTTPS + OAuth
事務支援          WS-AtomicTransaction   無標準
學習曲線          高                      低
工具支援          企業工具鏈成熟          簡單（curl 即可）
效能              較低（XML 膨脹）        較高
─────────────────────────────────────────────────────────
```

## 何時選擇 SOAP

SOAP 適合的場景：

- **企業應用整合（EAI）**：需要嚴格的介面契約
- **事務處理**：需要跨服務的事務支援
- **安全需求高**：需要 WS-Security 的豐富安全特性
- **現有投資**：已有基於 SOAP 的系統

```java
// JAX-WS（Java）呼叫 SOAP 服務
@WebService
public class StockService {
    @WebMethod
    public float getStockPrice(String symbol) {
        // 實作
    }
}
```

## 何時選擇 REST

REST 適合的場景：

- **Web API**：對外開放的 API
- **簡單資料存取**：CRUD 操作
- **需要 AJAX 支援**：瀏覽器端呼叫
- **高效能需求**：JSON 比 XML 更緊湊

```python
# Python + Flask 實作 REST API
from flask import Flask, jsonify, request
app = Flask(__name__)

@app.route('/stocks/<symbol>', methods=['GET'])
def get_stock(symbol):
    price = lookup_price(symbol)
    return jsonify({'symbol': symbol, 'price': price})

@app.route('/stocks', methods=['POST'])
def create_stock():
    data = request.json
    return jsonify({'created': True}), 201
```

## 結語

SOAP 和 REST 代表了兩種不同的設計哲學：

- **SOAP** 是「企業級」的解決方案——嚴謹、完善、但複雜
- **REST** 是「網路原生」的解決方案——簡單、實用、但缺乏標準

2007 年的趨勢是：**公共 API 越來越傾向 REST，企業內部整合仍以 SOAP 為主**。

---

## 延伸閱讀

- [SOAP+Web+Services+2007](https://www.google.com/search?q=SOAP+Web+Services+2007)
- [REST+vs+SOAP+comparison](https://www.google.com/search?q=REST+vs+SOAP+comparison)
- [Roy+Fielding+REST+dissertation](https://www.google.com/search?q=Roy+Fielding+REST+dissertation+2000)

---

*本篇文章為「AI 程式人雜誌 2007 年 5 月號」本期焦點系列之一。*