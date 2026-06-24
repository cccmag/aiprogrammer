# XML-RPC 到 SOAP：RPC 協定的演進

## 前言

從 XML-RPC 到 SOAP，分散式呼叫經歷了漫長的演進。

## XML-RPC

```xml
<?xml version="1.0"?>
<methodCall>
  <methodName>examples.getProductName</methodName>
  <params>
    <param><value><int>12345</int></value></param>
  </params>
</methodCall>
```

## SOAP

```xml
<?xml version="1.0"?>
<soap:Envelope xmlns:soap="...">
  <soap:Body>
    <ns2:getProductName xmlns:ns2="...">
      <productId>12345</productId>
    </ns2:getProductName>
  </soap:Body>
</soap:Envelope>
```

## 結語

SOAP 相比 XML-RPC 提供了更豐富的標準和企業功能。

---

## 延伸閱讀

- [XML-RPC+vs+SOAP+history](https://www.google.com/search?q=XML-RPC+vs+SOAP+history)

---