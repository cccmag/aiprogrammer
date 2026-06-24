# 本期焦點

## REST API 與 Web 服務：REST、SOAP、Web Service、OAuth 先驅

### 引言

2007 年，Web 服務正在經歷一場典範轉移。從 SOAP 到 REST，從 XML 到 JSON，從封閉系統到開放平台，Web 服務的設計哲學正在發生根本性的變化。

本期，我們將回顧 Web 服務技術的發展歷程，分析 REST 和 SOAP 的優劣勢，並探討未來的發展趨勢。

---

## 大綱

* [程式：實作 REST 伺服器與客戶端](focus_code.md)
   - Python Flask 實作 REST API
   - AJAX 客戶端呼叫

1. [SOAP 與 REST 的比較](focus1.md)
   - 兩種 Web 服務架構的哲學差異
   - 企業應用 vs 網路應用

2. [RESTful API 設計原則](focus2.md)
   - 資源、URI、HTTP 動詞
   -  Stateless 設計

3. [JSON 與 XML 的抉擇](focus3.md)
   - 資料格式的比較與選擇
   - 何時用 JSON、何時用 XML

4. [Web 服務安全](focus4.md)
   - OAuth 先驅（Google AuthSub、Yahoo BBAuth）
   - API 認證策略

5. [AJAX 與 REST](focus5.md)
   - 瀏覽器端的 Web 服務呼叫
   - 跨域問題與解決方案

6. [企業級 Web 服務](focus6.md)
   - SOAP、WS-* 標準
   - 企業應用整合

---

## 濃縮回顧

### SOAP 的企業應用傳統

SOAP（Simple Object Access Protocol）在 2000 年代初期的企業應用整合中佔據主導地位。SOAP 的設計理念是「企業級」——嚴格的類型系統、豐富的擴展機制、完整的標準家族（WS-Security、WS-Addressing 等）。

SOAP 的優點：
- 嚴格的介面定義（WSDL）
- 豐富的安全擴展
- 事務支援
- 企業工具鏈成熟

### REST 的網路原生設計

REST（Representational State Transfer）則是「網路原生」的設計。REST 並非一個協定，而是一種架構風格，基於 HTTP 的設計原則。

REST 的優點：
- 簡單易懂
- 充分利用 HTTP
- 客戶端-伺服器分離
- 可緩存性

### 2007 年的趨勢

2007 年，越來越多的網路服務開始提供 REST API：

```
2007 年主流 REST API：
───────────────────────
Twitter API       RESTful（早期版本）
Flickr API        REST
del.icio.us API   REST
Amazon S3         REST
Google Data API   GData（REST-ish）
```

---

## 結論與展望

Web 服務的未來將是 REST 與 SOAP 的融合——簡單的公共 API 使用 REST，複雜的企業整合使用 SOAP+WS-*。

未來幾年，我們將看到：
1. **OAuth 標準化**：2007 年的 OAuth 1.0 草稿將在 2009 年成為標準
2. **JSON 勝出**：JSON 將成為 Web API 的主流格式
3. **GraphQL 興起**：Facebook 將在 2015 年推出 GraphQL

---

## 延伸閱讀

- [SOAP 與 REST 的比較](focus1.md)
- [RESTful API 設計原則](focus2.md)
- [JSON 與 XML 的抉擇](focus3.md)
- [Web 服務安全](focus4.md)
- [AJAX 與 REST](focus5.md)
- [企業級 Web 服務](focus6.md)

---

*本期焦點到此結束。下期我們將聚焦版本控制與協作開發。*