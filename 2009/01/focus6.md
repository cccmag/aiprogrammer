# 即時通訊應用：WebSocket 與 Socket.IO

## 前言

傳統的 HTTP 請求-回應模式不適合需要即時雙向通訊的應用。WebSocket 協定的出現，改變了這一點。雖然在 2009 年 WebSocket 還是新技術，但 Node.js 已經為其提供了良好的支援。

## HTTP 的局限性

```
HTTP 請求-回應模型：
───────────────────
Client ──── 請求 ────▶ Server
        ◀─── 回應 ────
（客戶端必須先發起請求）

問題：
───────────────────
1. 即時性：伺服器無法主動推送資料
2. 效率：每次請求都要發送完整的 HTTP 表頭
3. 連線：每個請求都建立新的 TCP 連線
```

## WebSocket 協定

WebSocket 是一種在單個 TCP 連線上提供全雙工通訊的協定。

```
WebSocket 連線建立過程：
─────────────────────────
1. HTTP 握手請求
   GET /chat HTTP/1.1
   Host: example.com
   Upgrade: websocket
   Connection: Upgrade

2. 伺服器回應
   HTTP/1.1 101 Switching Protocols
   Upgrade: websocket
   Connection: Upgrade

3. 連線升級完成，開始雙向通訊
   Client ◀──── 雙向 ────▶ Server
```

## Node.js 中的 WebSocket

### 基本 WebSocket 伺服器

```javascript
const http = require('http');
const crypto = require('crypto');

const server = http.createServer((req, res) => {
  res.writeHead(200);
  res.end('WebSocket 伺服器');
});

server.on('upgrade', (req, socket, head) => {
  // 解析 WebSocket 握手
  const key = req.headers['sec-websocket-key'];

  // 生成 accept 金鑰
  const acceptKey = crypto
    .createHash('sha1')
    .update(key + '258EAFA5-E914-47DA-95CA-C5AB0DC85B11')
    .digest('base64');

  const headers = [
    'HTTP/1.1 101 Switching Protocols',
    'Upgrade: websocket',
    'Connection: Upgrade',
    'Sec-WebSocket-Accept: ' + acceptKey,
    ''
  ].join('\r\n') + '\r\n';

  socket.write(headers);
  socket.write('\r\n');

  // WebSocket 連線已建立
  socket.on('data', (buffer) => {
    // 處理客戶端訊息
    const message = parseFrame(buffer);
    console.log('收到：', message);

    // 傳送回應
    const response = createFrame('收到訊息：' + message);
    socket.write(response);
  });
});

function parseFrame(buffer) {
  // 簡化的框架解析
  const secondByte = buffer[1];
  let length = secondByte & 0x7F;
  let offset = 2;

  if (length === 126) {
    length = buffer.readUInt16BE(2);
    offset = 4;
  } else if (length === 127) {
    length = buffer.readUInt32BE(2);
    offset = 6;
  }

  const data = buffer.slice(offset, offset + length);
  return data.toString();
}

function createFrame(message) {
  const buffer = Buffer.alloc(message.length + 2);
  buffer[0] = 0x81; // FIN + text frame
  buffer[1] = message.length;
  buffer.write(message, 2);
  return buffer;
}

server.listen(3000);
```

## Socket.IO 簡介

Socket.IO 是一個抽象了 WebSocket 複雜性的函式庫（在 2009 年還不存在，它是 2010 年發布的）。但了解其概念很重要。

```
Socket.IO 的設計理念：
──────────────────────
1. 自動降級：如果 WebSocket 不可用，回退到其他機制
2. 心跳檢測：保持連線活躍
3. 房間和命名空間：組織式的訊息傳遞
4. 自動重新連線：網路中斷後自動重連
```

## 即時應用的常見用例

### 1. 聊天室

```javascript
// 聊天室伺服器概念（2009 年的實現方式）
const clients = new Set();

const server = http.createServer((req, res) => {
  if (req.url === '/') {
    res.writeHead(200, { 'Content-Type': 'text/html' });
    res.end(`
      <html>
      <body>
        <input id="msg" placeholder="輸入訊息">
        <button onclick="send()">傳送</button>
        <div id="chat"></div>
        <script>
          const ws = new WebSocket('ws://localhost:3000');
          ws.onmessage = (e) => {
            document.getElementById('chat').innerHTML += '<p>' + e.data + '</p>';
          };
          function send() {
            ws.send(document.getElementById('msg').value);
          }
        </script>
      </body>
      </html>
    `);
  }
});

server.on('upgrade', (req, socket) => {
  clients.add(socket);
  // 處理 WebSocket 訊息...
});
```

### 2. 即時通知

```javascript
// 通知系統
function notifyClients(message) {
  clients.forEach(client => {
    const frame = createFrame(JSON.stringify({
      type: 'notification',
      message: message,
      timestamp: Date.now()
    }));
    client.write(frame);
  });
}
```

### 3. 協作編輯

```javascript
// 簡化的協作編輯概念
function broadcastUpdate(docId, update) {
  clients.forEach(client => {
    if (client.docId === docId) {
      const frame = createFrame(JSON.stringify({
        type: 'update',
        docId: docId,
        update: update
      }));
      client.write(frame);
    }
  });
}
```

## WebSocket 與 HTTP 的比較

```
特性比較：
───────────────────────────────
                HTTP        WebSocket
連線建立：       每次新建     一次握手
方向：           客戶端發起    雙向
伺服器推送：      不支援       支援
效能：           較低（表頭大） 高（較小表頭）
相容性：         所有瀏覽器    需要瀏覽器支援
復用連線：       每請求新建    持續連線
```

## 即時技術的演進

```
即時通訊技術時間線：
──────────────────────
1990s：Polling（輪詢）- 客戶端不斷請求
2000s：Long Polling（長輪詢）- 伺服器等待
2009：  WebSocket 標準化
2010：  Socket.IO 發布
2011：  Server-Sent Events（SSE）
現在：  WebRTC 用於點對點通訊
```

## 結語

WebSocket 為 Web 應用帶來了真正的即時雙向通訊能力。雖然在 2009 年 WebSocket 還是新技術，瀏覽器支援也很有限，但它的設計理念預示了未來 Web 應用的發展方向。

Node.js 的事件驅動模型非常適合處理 WebSocket 連線，使得建立即時應用變得相對簡單。

---

## 延伸閱讀

- [WebSocket 協定 RFC 6455](https://www.google.com/search?q=WebSocket+protocol+RFC+6455)
- [WebSocket vs HTTP comparison](https://www.google.com/search?q=WebSocket+vs+HTTP+comparison)
- [即時 Web 應用程式設計](https://www.google.com/search?q=real-time+web+applications)

---

*本篇文章為「AI 程式人雜誌 2009 年 1 月號」歷史回顧系列之一。*