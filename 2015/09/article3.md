# WebSocket 即時通訊

## 前言

WebSocket 提供了瀏覽器和伺服器之間的全雙工通訊，適合需要即時更新的應用。

---

## WebSocket 與 HTTP

### HTTP 的限制

- 客戶端主動請求
- 單向通訊
- 常輪詢造成資源浪費

### WebSocket 優勢

- 真正的雙向通訊
- 只需一次連線
- 低延遲

```
HTTP:
用戶端 ────────> 請求 ──────────> 伺服器
用戶端 <─────── 回應 <────────── 伺服器

WebSocket:
用戶端 ←────── 雙向通道 ────────→ 伺服器
```

---

## 基本 API

### 建立連線

```javascript
const ws = new WebSocket('ws://example.com/ws');

// 或安全的 WebSocket
const ws = new WebSocket('wss://example.com/ws');
```

### 事件處理

```javascript
ws.onopen = () => {
    console.log('連線已建立');
    ws.send('Hello server!');
};

ws.onmessage = (event) => {
    console.log('收到:', event.data);
};

ws.onerror = (error) => {
    console.error('錯誤:', error);
};

ws.onclose = () => {
    console.log('連線已關閉');
};
```

### 傳送訊息

```javascript
ws.send('Hello server!');
ws.send(JSON.stringify({ type: 'ping' }));
```

### 關閉連線

```javascript
ws.close();
ws.close(1000, '正常關閉');
```

---

## 伺服器端實作

### Python (asyncio)

```python
import asyncio
import websockets

async def echo(websocket, path):
    async for message in websocket:
        print(f"收到: {message}")
        await websocket.send(f"回應: {message}")

start_server = websockets.serve(echo, 'localhost', 8765)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
```

### Node.js

```javascript
const WebSocket = require('ws');
const wss = new WebSocket.Server({ port: 8765 });

wss.on('connection', (ws) => {
    console.log('客戶端連線');
    
    ws.on('message', (message) => {
        console.log('收到:', message);
        ws.send(`回應: ${message}`);
    });
    
    ws.on('close', () => {
        console.log('客戶端斷線');
    });
});
```

---

## 心跳機制

保持連線活躍：

```javascript
// 用戶端
setInterval(() => {
    if (ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({ type: 'ping' }));
    }
}, 30000);

// 伺服器回應
ws.on('message', (message) => {
    const data = JSON.parse(message);
    if (data.type === 'ping') {
        ws.send(JSON.stringify({ type: 'pong' }));
    }
});
```

---

## 重連機制

```javascript
class ReconnectingWebSocket {
    constructor(url, options = {}) {
        this.url = url;
        this.reconnectInterval = options.reconnectInterval || 1000;
        this.maxReconnectAttempts = options.maxReconnectAttempts || 10;
        this.attempts = 0;
        this.connect();
    }
    
    connect() {
        this.ws = new WebSocket(this.url);
        
        this.ws.onopen = () => {
            console.log('連線建立');
            this.attempts = 0;
        };
        
        this.ws.onclose = () => {
            this.reconnect();
        };
        
        this.ws.onmessage = (event) => {
            this.onmessage(event);
        };
    }
    
    reconnect() {
        if (this.attempts < this.maxReconnectAttempts) {
            this.attempts++;
            console.log(`嘗試重新連線 (${this.attempts})`);
            setTimeout(() => this.connect(), this.reconnectInterval);
        }
    }
    
    send(data) {
        if (this.ws.readyState === WebSocket.OPEN) {
            this.ws.send(data);
        }
    }
}
```

---

## 應用場景

### 即時聊天

```javascript
// 發送訊息
function sendMessage(text) {
    ws.send(JSON.stringify({
        type: 'message',
        text: text,
        timestamp: Date.now()
    }));
}

// 接收訊息
ws.onmessage = (event) => {
    const msg = JSON.parse(event.data);
    if (msg.type === 'message') {
        addMessageToUI(msg);
    }
};
```

### 線上協作

```javascript
// 發送操作
ws.send(JSON.stringify({
    type: 'operation',
    action: 'cursor_move',
    position: { x: 100, y: 200 }
}));
```

### 即時通知

```javascript
// 訂閱通知
ws.send(JSON.stringify({
    type: 'subscribe',
    channels: ['user_123', 'global']
}));

// 接收通知
ws.onmessage = (event) => {
    const notification = JSON.parse(event.data);
    showNotification(notification);
};
```

---

## 安全考量

### 驗證

```javascript
// 連線時傳送權杖
const ws = new WebSocket('wss://example.com/ws?token=xxx');

// 伺服器驗證
server.on('connection', (ws, req) => {
    const url = new URL(req.url, 'ws://example.com');
    const token = url.searchParams.get('token');
    
    if (!validateToken(token)) {
        ws.close(1008, 'Invalid token');
        return;
    }
});
```

### WSS

```bash
# 必須使用加密連線
wss://example.com/ws
```

[搜尋 WebSocket security best practices](https://www.google.com/search?q=WebSocket+security+best+practices)

---

## 小結

WebSocket 是實現即時功能的最佳選擇，但需要注意連線管理和錯誤處理。

---

*作者：AI 程式人團隊*

*延伸閱讀：*
- [WebSocket 規格](https://www.google.com/search?q=WebSocket+specification)
- [WebSocket API 文档](https://www.google.com/search?q=WebSocket+API+documentation)