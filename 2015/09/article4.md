# 網路程式設計面試題

## 前言

網路知識是軟體工程師面試的重要組成部分，本 文收集常見問題並提供解答。

---

## TCP 相關問題

### Q1: TCP 三向交握的過程？

```
客戶端                      伺服器
  │                          │
  │────── SYN=1, Seq=x ─────>│  客戶端發送 SYN
  │                          │
  │<───── SYN=1, ACK=x+1 ───│  伺服器回應 SYN-ACK
  │      Seq=y                │
  │                          │
  │────── ACK=y+1 ─────────>│  客戶端發送 ACK
  │                          │
  │       連線建立            │
```

### Q2: 為什麼需要三次？

- 第一次：客戶端證明自己能發送
- 第二次：伺服器證明自己能接收和發送
- 第三次：客戶端確認伺服器能接收

### Q3: TCP 四向揮手過程？

```
客戶端                      伺服器
  │                          │
  │────── FIN ─────────────>│  客戶端發送 FIN
  │<───── ACK ──────────────│  伺服器確認
  │                          │
  │<───── FIN ──────────────│  伺服器發送 FIN
  │────── ACK ─────────────>│  客戶端確認
  │                          │
  │       連線關閉            │
```

### Q4: TCP 與 UDP 的區別？

| 特性 | TCP | UDP |
|------|-----|-----|
| 連線 | 面向連線 | 無連線 |
| 可靠性 | 可靠 | 不可靠 |
| 順序 | 有序 | 無序 |
| 速度 | 較慢 | 較快 |
| 開銷 | 較大 | 較小 |

---

## HTTP 相關問題

### Q5: GET 與 POST 的區別？

| 方面 | GET | POST |
|------|-----|------|
| 參數位置 | URL query string | Request body |
| 參數長度 | 受 URL 限制（~2KB）| 無限制 |
| 快取 | 可快取 | 通常不行 |
| 安全性 | 較不安全（URL 可見）| 較安全 |
| 語義 | 取得資源 | 提交資料 |

### Q6: HTTP 狀態碼分類？

```
1xx: 資訊
2xx: 成功（200 OK, 201 Created, 204 No Content）
3xx: 重新導向（301, 302, 304）
4xx: 用戶端錯誤（400, 401, 403, 404）
5xx: 伺服器錯誤（500, 502, 503）
```

### Q7: HTTP/1.1 與 HTTP/2 的區別？

| 特性 | HTTP/1.1 | HTTP/2 |
|------|----------|--------|
| 多工 | 不支援 | 支援 |
| 標頭壓縮 | 無 | HPACK |
| 伺服器推送 | 不支援 | 支援 |
| 連線 | 多個 TCP | 單一 TCP |
| 二進制 | 文字 | 二進制框架 |

---

## Socket 相關問題

### Q8: 什麼是 Socket？

Socket 是作業系統提供的網路通訊端點抽象，用於程序之間的 TCP/UDP 通訊。

### Q9: 如何處理多個客戶端連線？

常用方法：

1. **多程序/執行緒**：每個客戶端一個程序或執行緒
2. **Select/Poll**：單一執行緒監控多個連線
3. **Epoll/Kqueue**：高效的事件通知
4. **非同步 I/O**：使用 async/await

### Q10: 什麼是 EPOLL？優勢？

```c
// 使用 epoll
int epfd = epoll_create1(0);
struct epoll_event event = { .events = EPOLLIN, .data.fd = sockfd };
epoll_ctl(epfd, EPOLL_CTL_ADD, sockfd, &event);

struct epoll_event events[10];
int nfds = epoll_wait(epfd, events, 10, -1);
```

優勢：
- O(1) 而不是 O(n) 的效能
- 不需要每次輪詢所有 fd
- 支援邊緣觸發

---

## DNS 相關問題

### Q11: DNS 查詢過程？

```
1. 檢查瀏覽器快取
2. 檢查作業系統快取
3. 查詢遞迴 DNS 伺服器（通常為 ISP）
4. 查詢根伺服器
5. 查詢 TLD 伺服器（.com, .org）
6. 查詢授權伺服器
7. 返回結果並快取
```

### Q12: DNS 記錄類型？

| 類型 | 用途 |
|------|------|
| A | IPv4 地址 |
| AAAA | IPv6 地址 |
| CNAME | 別名 |
| MX | 郵件交換 |
| NS | 名稱伺服器 |
| TXT | 文字記錄 |
| PTR | 反向查詢 |

---

## 網路安全相關問題

### Q13: HTTPS 工作原理？

```
1. 用戶端發送 ClientHello（支援的 TLS 版本、加密套件）
2. 伺服器回應 ServerHello（選擇的加密套件、憑證）
3. 用戶端驗證憑證
4. 客戶端發送 ClientKeyExchange（預備主密鑰）
5. 雙方計算會話密鑰
6. 加密的 HTTP 資料傳輸
```

### Q14: 什麼是 CORS？

跨來源資源共享（Cross-Origin Resource Sharing）。

```http
# 預檢請求
OPTIONS /api/data HTTP/1.1
Origin: https://example.com
Access-Control-Request-Method: GET

# 回應
HTTP/1.1 200 OK
Access-Control-Allow-Origin: https://example.com
Access-Control-Allow-Methods: GET, POST
```

[搜尋 network interview questions answers](https://www.google.com/search?q=network+interview+questions+answers)

---

## 小結

這些問題涵蓋了網路程式設計的核心知識，準備這些問題能幫助你在面試中表現更好。

---

*作者：AI 程式人團隊*