# 網路通訊基礎：HTTP 與 REST

## HTTP 協定的誕生與演進

1989 年，英國科學家 Tim Berners-Lee 在歐洲核子研究組織（CERN）提出了全球資訊網（World Wide Web）的概念。作為 Web 的通訊協定，HTTP（HyperText Transfer Protocol）從此誕生。

### HTTP/0.9 到 HTTP/1.0

最早的 HTTP/0.9 極為簡單：客戶端發起連線，傳送一行請求（如 `GET /index.html`），伺服器回應 HTML 內容後關閉連線。1996 年發布的 HTTP/1.0（RFC 1945）引入了請求頭、回應頭和狀態碼，使協定變得更加豐富：

```
GET /api/users HTTP/1.0
User-Agent: Python/3.12
Accept: application/json
```

### HTTP/1.1 的重大改進

HTTP/1.1（RFC 2616，1997）引入了持久連線（Keep-Alive），允許在同一個 TCP 連線上傳送多個請求。管線化（Pipelining）技術讓客戶端可以連續發送多個請求而無需等待回應。

### HTTP/2 與 HTTP/3

HTTP/2（2015）基於 Google 的 SPDY 協定，引入了多路復用（Multiplexing）、伺服器推送（Server Push）和二進位分幀（Binary Framing）。HTTP/3（2022）則完全改用了 UDP 基礎的 QUIC 協定，大幅降低了連線建立延遲。

## HTTP 請求與回應

一個典型的 HTTP 請求包含以下結構：

```
POST /api/users HTTP/1.1
Host: api.example.com
Content-Type: application/json
Authorization: Bearer <token>

{"name": "Alice", "email": "alice@example.com"}
```

回應結構：

```
HTTP/1.1 201 Created
Content-Type: application/json

{"id": 123, "name": "Alice", "email": "alice@example.com"}
```

### 重要 HTTP 方法

| 方法 | 用途 | 是否冪等 |
|------|------|---------|
| GET | 取得資源 | 是 |
| POST | 建立資源 | 否 |
| PUT | 更新（覆蓋）資源 | 是 |
| PATCH | 部分更新資源 | 否 |
| DELETE | 刪除資源 | 是 |

### 常見狀態碼

- **200 OK**：請求成功
- **201 Created**：資源建立成功
- **204 No Content**：成功但無回應內容
- **400 Bad Request**：請求格式錯誤
- **401 Unauthorized**：未認證
- **403 Forbidden**：無權限
- **404 Not Found**：資源不存在
- **429 Too Many Requests**：請求過於頻繁
- **500 Internal Server Error**：伺服器錯誤

## REST 架構風格

REST（Representational State Transfer）由 Roy Fielding 在 2000 年的博士論文中提出。REST 不是協定，而是一種架構風格。

### REST 六大原則

1. **客戶端-伺服器分離**：關注點分離，客戶端和伺服器可以獨立演進
2. **無狀態**：伺服器不儲存客戶端狀態，每個請求都包含所有必要資訊
3. **可快取**：回應應明確標示是否可快取
4. **統一介面**：資源識別、資源操作、自我描述訊息、超媒體
5. **分層系統**：代理、閘道器等中介可以透明地插入
6. **隨需程式碼**（可選）：伺服器可以擴展客戶端功能

### RESTful 資源設計

```
GET    /users          # 取得使用者列表
GET    /users/{id}     # 取得特定使用者
POST   /users          # 建立使用者
PUT    /users/{id}     # 更新使用者
DELETE /users/{id}     # 刪除使用者
GET    /users/{id}/orders  # 使用者的訂單
```

### REST 與 RPC 的差異

REST 以資源為中心（名詞），RPC 以動作為中心（動詞）：

```
RESTful:  POST /orders  {"product": "book", "qty": 2}
RPC:      POST /createOrder  {"product": "book", "qty": 2}
```

RESTful 設計的核心在於 URL 描述資源而非動作，HTTP 方法描述操作。

## URL 結構

一個完整的 URL 包含以下部分：

```
https://api.example.com:443/v1/users?page=1&limit=10#section
\___/   \______________/\__/\____/\________________/\______/
方案        主機        埠號  路徑      查詢參數        片段
```

## HTTP 的無狀態性與 Session

HTTP 本質上是無狀態協定——伺服器在處理完請求後不保留任何客戶端資訊。為了實現狀態管理，開發者通常使用 Cookie 和 Session 機制。然而在 REST API 設計中，無狀態是核心原則，每個請求都應包含所有需要的認證資訊。

---

## 延伸閱讀

- [HTTP/1.1 RFC 2616](https://www.google.com/search?q=HTTP+1.1+RFC+2616)
- [REST 架構風格論文 (Fielding 2000)](https://www.google.com/search?q=REST+architectural+style+Fielding)
- [MDN HTTP 指南](https://www.google.com/search?q=MDN+HTTP+guide)
