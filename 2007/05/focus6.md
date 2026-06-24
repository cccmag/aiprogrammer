# 企業級 Web 服務：SOAP、WS-* 標準與企業應用

## SOAP 的企業應用場景

2007 年，SOAP 仍在企業應用整合（EAI）中佔據主導地位。SOAP 的豐富標準家族提供了企業所需的可靠性、安全性和事務支援。

### SOAP 的優點

```
SOAP 企業應用優勢：
─────────────────────
1. 嚴格的介面定義（WSDL）
2. 完整的安全擴展（WS-Security）
3. 事務支援（WS-AtomicTransaction）
4. 可靠的訊息傳遞（WS-ReliableMessaging）
5. 企業工具鏈成熟
```

### SOAP 訊息範例

```xml
<?xml version="1.0" encoding="UTF-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd">
  <soap:Header>
    <wsse:Security>
      <wsse:UsernameToken>
        <wsse:Username>serviceaccount</wsse:Username>
        <wsse:Password Type="...#PasswordDigest">
          hash_of_password
        </wsse:Password>
        <wsse:Nonce>random_nonce</wsse:Nonce>
        <wsu:Created>2007-05-15T10:00:00Z</wsu:Created>
      </wsse:UsernameToken>
    </wsse:Security>
  </soap:Header>
  <soap:Body>
    <SubmitOrder xmlns="http://example.com/orders">
      <orderId>ORD-12345</orderId>
      <customerId>CUST-67890</customerId>
      <items>
        <item productId="P001" quantity="5"/>
        <item productId="P002" quantity="3"/>
      </items>
    </SubmitOrder>
  </soap:Body>
</soap:Envelope>
```

## WS-* 標準家族

### WS-Security

WS-Security 提供了企業級的安全機制：

```xml
<!-- WS-Security SOAP 頭 -->
<wsse:Security soap:mustUnderstand="true">
    <!-- Username Token -->
    <wsse:UsernameToken>
        <wsse:Username>user</wsse:Username>
        <wsse:Password Type="...#Digest">...</wsse:Password>
    </wsse:UsernameToken>

    <!-- Binary Security Token（如 X.509 憑證）-->
    <wsse:BinarySecurityToken
        ValueType="...#X509v3"
        EncodingType="...#Base64Binary">
        MIIB...
    </wsse:BinarySecurityToken>

    <!-- 數位簽章 -->
    <ds:Signature xmlns:ds="http://www.w3.org/2000/09/xmldsig#">
        <ds:SignedInfo>
            <ds:CanonicalizationMethod Algorithm="..."/>
            <ds:SignatureMethod Algorithm="...#rsa-sha1"/>
            <ds:Reference URI="#body">
                <ds:DigestMethod Algorithm="...#sha1"/>
                <ds:DigestValue>...</ds:DigestValue>
            </ds:Reference>
        </ds:SignedInfo>
        <ds:SignatureValue>...</ds:SignatureValue>
    </ds:Signature>
</wsse:Security>
```

### WS-AtomicTransaction

分散式事務支援：

```xml
<!-- SOAP 操作中的事務上下文 -->
<soap:Header>
    <wscoor:CoordinationContext>
        <wscoor:Identifier>urn:uuid:transaction-123</wscoor:Identifier>
        <wscoor:Expires>2007-05-15T11:00:00Z</wscoor:Expires>
        <wscoor:CoordinationType>
            http://schemas.xmlsoap.org/ws/2004/10/wsat
        </wscoor:CoordinationType>
        <wsat:ParticipantPortType/>
    </wscoor:CoordinationContext>
</soap:Header>
```

### WS-ReliableMessaging

可靠訊息傳遞：

```xml
<!-- SOAP WS-ReliableMessaging -->
<srm:CreateSequence xmlns:srm="http://schemas.xmlsoap.org/ws/2005/02/rm">
    <wsrm:AcknowledgementInterval>
        <wsu:Expires>PT5S</wsu:Expires>
    </wsrm:AcknowledgementInterval>
    <wsrm:Expires>PT1H</wsrm:Expires>
    <wsrm:DeliveryAssurance>
        <wsrm:Assurance xmlns:wsrm="...">ExactlyOnce</wsrm:Assurance>
    </wsrm:DeliveryAssurance>
</srm:CreateSequence>
```

## Java 中的 SOAP 服務

### JAX-WS

```java
// Java JAX-WS 服務
@WebService
@SOAPBinding(style = Style.DOCUMENT)
public class OrderService {

    @WebMethod
    @WebResult(name = "orderConfirmation")
    public OrderConfirmation submitOrder(
        @WebParam(name = "orderId") String orderId,
        @WebParam(name = "customerId") String customerId,
        @WebParam(name = "items") List<OrderItem> items
    ) {
        // 處理訂單
        OrderConfirmation confirmation = processOrder(orderId, customerId, items);
        return confirmation;
    }

    @WebMethod
    @WebFault
    public void handleOrderError() throws OrderException {
        throw new OrderException("Order processing failed");
    }
}
```

### 用戶端

```java
// JAX-WS 客戶端
public class OrderClient {
    public static void main(String[] args) {
        OrderService service = new OrderService();
        OrderPort port = service.getOrderPort();

        OrderConfirmation result = port.submitOrder(
            "ORD-123",
            "CUST-456",
            Arrays.asList(
                new OrderItem("P001", 5),
                new OrderItem("P002", 3)
            )
        );

        System.out.println("Order confirmed: " + result.getConfirmationId());
    }
}
```

## .NET 中的 SOAP 服務

### ASP.NET Web Services

```csharp
// C# ASP.NET Web Service
[WebService(Namespace = "http://example.com/orders")]
public class OrderService : WebService {

    [WebMethod]
    public OrderConfirmation SubmitOrder(string orderId, string customerId, OrderItem[] items) {
        // 處理訂單
        OrderConfirmation confirmation = ProcessOrder(orderId, customerId, items);
        return confirmation;
    }

    [WebMethod]
    public Order[] GetOrders(string customerId) {
        return OrderRepository.GetByCustomer(customerId);
    }
}
```

## SOAP 與 REST 的融合

2007 年，越來越多企業開始探索「SOAP 和 REST 的融合」：

### REST 和 SOAP 的比較

```
企業應用 SOAP vs REST：
─────────────────────────────────────────────────────────
場景              SOAP                    REST
─────────────────────────────────────────────────────────
內部整合          ✓ 成熟工具鏈           △ 需要額外工作
外部 API          △ 複雜                  ✓ 簡單易用
安全需求高        ✓ WS-* 完整支援         △ 依賴 HTTPS
事務支援          ✓ 標準化               △ 無標準
效能需求          △ XML 解析開銷         ✓ JSON 更高效
─────────────────────────────────────────────────────────
```

### 實用策略：雙模式服務

```java
// 同一個服務提供 SOAP 和 REST 介面
@WebService
public class ProductService {

    // REST 介面
    @GET
    @Path("/products/{id}")
    @Produces(MediaType.APPLICATION_JSON)
    public Product getProduct(@PathParam("id") String id) {
        return productRepository.find(id);
    }

    // SOAP 介面
    @WebMethod
    public ProductInfo getProductInfo(String productId) {
        Product p = productRepository.find(productId);
        return new ProductInfo(p);
    }
}
```

## 結語

SOAP 和 REST 代表了 Web 服務的兩種哲學：

- **SOAP** 是「萬能的」——提供完整的功能，但代價是複雜性
- **REST** 是「簡單的」——只做最基本的功能，但足夠大多數場景

2007 年的最佳實踐是：
- 對外 API 使用 REST（簡單、易用）
- 企業內部整合可以使用 SOAP（可靠性、安全性）
- 複雜場景可以考慮兩者結合

---

## 延伸閱讀

- [SOAP+WS-+standards+enterprise+2007](https://www.google.com/search?q=SOAP+WS-standards+enterprise+2007)
- [JAX-WS+web+services+Java](https://www.google.com/search?q=JAX-WS+web+services+Java)
- [WS-Security+SOAP+authentication](https://www.google.com/search?q=WS-Security+SOAP+authentication)

---

*本篇文章為「AI 程式人雜誌 2007 年 5 月號」本期焦點系列之一。*