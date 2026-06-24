# 即時通訊：Socket.IO、WebSocket、即時更新

## 前言

即時通訊是現代 Web 應用的重要功能。Socket.IO 提供了簡單的 API 來實現雙向即時通訊。

## WebSocket 基礎

### 與 HTTP 的比較

```
HTTP:                       WebSocket:
────────                    ─────────
用戶端發起請求              雙向主動推送
每請求都需要握手            一次握手，持續連線
有額外開銷                 低延遲
無狀態                     有狀態
```

### 原生 WebSocket

```javascript
// 客戶端
const ws = new WebSocket('ws://localhost:3000/ws');

ws.onopen = () => {
  console.log('連線打開');
  ws.send('Hello Server');
};

ws.onmessage = (event) => {
  console.log('收到:', event.data);
};

ws.onerror = (error) => {
  console.error('錯誤:', error);
};

ws.onclose = () => {
  console.log('連線關閉');
};
```

## Socket.IO

### 安裝

```bash
npm install socket.io
```

### 伺服器端

```javascript
const express = require('express');
const http = require('http');
const { Server } = require('socket.io');

const app = express();
const server = http.createServer(app);
const io = new Server(server);

io.on('connection', (socket) => {
  console.log('用戶連線:', socket.id);

  // 發送訊息
  socket.emit('welcome', { message: '歡迎連線' });

  // 廣播（發送給其他人）
  socket.broadcast.emit('userJoined', { id: socket.id });

  // 處理訊息
  socket.on('chatMessage', (data) => {
    console.log('收到訊息:', data);

    // 發送給所有人
    io.emit('newMessage', {
      from: socket.id,
      message: data.message,
      timestamp: Date.now()
    });
  });

  // 斷開連線
  socket.on('disconnect', () => {
    console.log('用戶斷線:', socket.id);
    io.emit('userLeft', { id: socket.id });
  });
});

server.listen(3000, () => {
  console.log('Socket.IO 伺服器執行於 :3000');
});
```

### 客戶端

```html
<script src="/socket.io/socket.io.js"></script>
<script>
  const socket = io();

  socket.on('connect', () => {
    console.log('已連線到伺服器');
  });

  socket.on('welcome', (data) => {
    console.log('收到歡迎訊息:', data);
  });

  socket.on('newMessage', (data) => {
    console.log('新訊息:', data);
    addMessageToUI(data);
  });

  socket.on('userJoined', (data) => {
    console.log('用戶加入:', data.id);
  });

  socket.on('userLeft', (data) => {
    console.log('用戶離開:', data.id);
  });

  function sendMessage(message) {
    socket.emit('chatMessage', { message });
  }
</script>
```

## 房間與命名空間

### 房間（Rooms）

```javascript
io.on('connection', (socket) => {
  // 加入房間
  socket.join('room1');

  // 離開房間
  socket.leave('room1');

  // 發送到房間
  io.to('room1').emit('message', { msg: 'Hello Room1' });
  io.to('room1').emit('message', { msg: 'Hello Room1' });

  // 除了發送者外的房間成員
  socket.to('room1').emit('message', { msg: 'Hello' });

  // 多個房間
  socket.to(['room1', 'room2']).emit('message', { msg: 'Hello' });
});
```

### 命名空間（Namespaces）

```javascript
// 伺服器
const adminNamespace = io.of('/admin');

adminNamespace.on('connection', (socket) => {
  console.log('admin 命名空間連線');
  socket.on('adminMessage', (data) => {
    adminNamespace.emit('notification', data);
  });
});

// 客戶端
const adminSocket = io('/admin');
```

## 進階功能

### 訊息確認（Acknowledgement）

```javascript
// 客戶端
socket.emit('addUser', { name: '王小明' }, (response) => {
  console.log('伺服器回應:', response);
});

// 伺服器
socket.on('addUser', (data, callback) => {
  const result = { success: true, id: socket.id };
  callback(result);
});
```

### 中間件

```javascript
io.use((socket, next) => {
  const token = socket.handshake.auth.token;

  if (isValidToken(token)) {
    next();
  } else {
    next(new Error('Unauthorized'));
  }
});
```

### 離線訊息

```javascript
io.on('connection', (socket) => {
  const userId = socket.handshake.query.userId;

  // 取得離線期間的訊息
  const offlineMessages = messageStore.getUndelivered(userId);
  offlineMessages.forEach((msg) => {
    socket.emit('message', msg);
  });

  // 標記已送達
  messageStore.markDelivered(userId);
});
```

## 實用範例：聊天室

```javascript
const rooms = {
  general: [],
  tech: [],
  random: []
};

io.on('connection', (socket) => {
  socket.on('joinRoom', ({ room }) => {
    socket.join(room);
    io.to(room).emit('systemMessage', {
      message: `用戶 ${socket.id} 加入了 ${room}`
    });
  });

  socket.on('chatMessage', ({ room, message }) => {
    const chatMessage = {
      id: Date.now(),
      from: socket.id,
      message,
      timestamp: new Date().toISOString()
    };

    rooms[room].push(chatMessage);
    io.to(room).emit('message', chatMessage);
  });

  socket.on('typing', ({ room }) => {
    socket.to(room).emit('userTyping', { userId: socket.id });
  });

  socket.on('stopTyping', ({ room }) => {
    socket.to(room).emit('userStoppedTyping', { userId: socket.id });
  });
});
```

## 結論

Socket.IO 讓即時通訊變得簡單。其自動降級、房間支援、訊息確認等特性，使其成為 Node.js 即時應用的首選方案。

---

## 延伸閱讀

- [Socket.IO 官方文檔](https://www.google.com/search?q=Socket.IO+documentation+tutorial)
- [WebSocket+Node.js](https://www.google.com/search?q=WebSocket+Node.js+real-time)

---

*本篇文章為「AI 程式人雜誌 2015 年 2 月號」歷史回顧系列之一。*