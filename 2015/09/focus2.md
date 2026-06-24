# HTTP 協議進化

HTTP（HyperText Transfer Protocol）是 Web 的基礎。從 HTTP/1.0 到 HTTP/1.1，再到 HTTP/2，協議持續演化以提升效能和安全性。

---

## HTTP/1.1

1999 年發布，至今仍是主流。

### 持續連線

```http
GET /index.html HTTP/1.1
Host: example.com
Connection: keep-alive
```

### 虛擬主機

```http
Host: www.example.com
```

### 快取控制

```http
Cache-Control: max-age=3600
ETag: "abc123"
Last-Modified: Wed, 21 Oct 2015 07:28:00 GMT
```

### 請求方法

| 方法 | 說明 | 安全 | 冪等 |
|------|------|------|------|
| GET | 取得資源 | 是 | 是 |
| POST | 提交資料 | 否 | 否 |
| PUT | 上傳資源 | 否 | 是 |
| DELETE | 刪除資源 | 否 | 是 |
| HEAD | 取得標頭 | 是 | 是 |
| OPTIONS | 選項 | 是 | 是 |

### 狀態碼

| 範圍 | 說明 |
|------|------|
| 1xx | 資訊 |
| 2xx | 成功 |
| 3xx | 重新導向 |
| 4xx | 用戶端錯誤 |
| 5xx | 伺服器錯誤 |

---

## HTTP/2

2015 年 5 月正式標準化（RFC 7540）。

### 主要改進

#### 1. 多工傳輸

HTTP/1.1 的問題：
```
請求1 ────────────────────>
          <───────────────── 回應1
請求2 ────────────────────>
          <───────────────── 回應2
```

HTTP/2 的優勢：
```
交錯的請求和回應：
請求1 ──> 請求2 ──> 請求3 ──>
<── 回應1 <── 回應2 <── 回應3
```

#### 2. 標頭壓縮 (HPACK)

```bash
# 請求1
:method: GET
:path: /index.html
:scheme: https
:authority: example.com
user-agent: curl/7.43.0

# 請求2（使用索引）
:path: /about.html  # 只有 path 改變
```

#### 3. 伺服器推送

```http
HTTP/2 200
content-type: text/html

# 伺服器自動推送以下資源
PUSH_PROMISE Stream 2: style.css
PUSH_PROMISE Stream 3: script.js
```

#### 4. 流量控制

```
HEADERS + DATA 框架，包含視窗更新
```

---

## HTTP/1.1 優化技巧

### 域名分割

```
www1.example.com  ──┐
www2.example.com  ──┼──> 突破瀏覽器連線限制
www3.example.com  ──┘
```

### 合併檔案

```
多個 CSS/JS 合併為一個，減少請求數
```

### 圖片優化

```
雪碧圖（Sprite）
內嵌 Base64
漸進式載入
```

### 快取

```http
Cache-Control: public, max-age=31536000
```

---

## 從 HTTP 到 HTTPS

### 為什麼要 HTTPS？

1. **加密傳輸**：防止竊聽
2. **完整性**：防止篡改
3. **身份驗證**：防止偽造
4. **SEO**：Google 偏好 HTTPS

### TLS 握手

```
用戶端                      伺服器
  │                          │
  │────── ClientHello ──────>│
  │                          │
  │<───── ServerHello ───────│
  │<───── Certificate ───────│
  │<───── ServerHelloDone ───│
  │                          │
  │────── ClientKeyExchange ─>│
  │────── ChangeCipherSpec ─>│
  │────── Finished ─────────>│
  │                          │
  │<───── ChangeCipherSpec ───│
  │<───── Finished ───────────│
  │                          │
  │     加密的 HTTP 資料      │
```

[搜尋 HTTP/2 vs HTTP/1.1 performance](https://www.google.com/search?q=HTTP+2+vs+HTTP+1.1+performance)

---

## 瀏覽器支援

```javascript
// 檢查 HTTP/2 支援
if ('protocol' in navigator) {
    navigator.protocol.then(protocol => {
        console.log('支援 HTTP/2:', protocol === 'h2');
    });
}
```

---

## 小結

HTTP 協議的進化反映了 Web 效能最佳化的持續追求，了解這些變化能幫助你構建更好的 Web 應用。

---

*作者：AI 程式人團隊*