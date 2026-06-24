# 非同步請求與 WebSocket

## 為什麼需要非同步？

傳統的同步 HTTP 請求在等待伺服器回應時會阻塞執行緒。當需要同時發送多個請求時，這種阻塞會導致嚴重的效能浪費。非同步程式設計允許程式在等待 I/O 時執行其他任務，大幅提升吞吐量。

## Python asyncio 基礎

```python
import asyncio

async def main():
    print("開始")
    await asyncio.sleep(1)
    print("結束")

asyncio.run(main())
```

## aiohttp 非同步 HTTP 客戶端

```bash
pip install aiohttp
```

### 基本用法

```python
import aiohttp
import asyncio

async def fetch_url(session, url):
    async with session.get(url) as response:
        return await response.json()

async def main():
    async with aiohttp.ClientSession() as session:
        data = await fetch_url(session,
            "https://jsonplaceholder.typicode.com/posts/1")
        print(data)

asyncio.run(main())
```

### 並行請求

```python
import aiohttp
import asyncio
import time

async def fetch(session, url):
    async with session.get(url) as resp:
        return await resp.text()

async def main():
    urls = [
        "https://jsonplaceholder.typicode.com/posts/1",
        "https://jsonplaceholder.typicode.com/posts/2",
        "https://jsonplaceholder.typicode.com/posts/3",
        "https://jsonplaceholder.typicode.com/posts/4",
        "https://jsonplaceholder.typicode.com/posts/5",
    ]
    start = time.time()
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url) for url in urls]
        results = await asyncio.gather(*tasks)
    elapsed = time.time() - start
    print(f"請求 {len(urls)} 個 URL，耗時 {elapsed:.2f} 秒")

asyncio.run(main())
```

## 非同步 FastAPI

FastAPI 原生支援非同步端點，在處理 I/O 密集型操作時能提升效能：

```python
from fastapi import FastAPI
import aiohttp
import asyncio

app = FastAPI()

@app.get("/fetch-all")
async def fetch_all():
    urls = [
        "https://jsonplaceholder.typicode.com/posts/1",
        "https://jsonplaceholder.typicode.com/posts/2",
        "https://jsonplaceholder.typicode.com/posts/3",
    ]
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url) for url in urls]
        return await asyncio.gather(*tasks)

async def fetch(session, url):
    async with session.get(url) as resp:
        return await resp.json()
```

## WebSocket 即時通訊

WebSocket 是 HTML5 引入的協定，允許在客戶端和伺服器之間建立持久連線，實現全雙工通訊。不同於 HTTP 的請求和回應模式，WebSocket 允許伺服器主動推送資料給客戶端。

### WebSocket 客戶端

```python
import asyncio
import websockets

async def connect():
    url = "wss://echo.websocket.org"
    async with websockets.connect(url) as ws:
        await ws.send("Hello, WebSocket!")
        response = await ws.recv()
        print(f"收到：{response}")

asyncio.run(connect())
```

### FastAPI WebSocket 伺服器

```python
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse

app = FastAPI()

html = """
<!DOCTYPE html>
<html>
<head><title>WebSocket 測試</title></head>
<body>
    <input id="msg" type="text">
    <button onclick="send()">發送</button>
    <div id="log"></div>
    <script>
        const ws = new WebSocket("ws://localhost:8000/ws");
        ws.onmessage = (event) => {
            document.getElementById("log").innerHTML +=
                "<p>" + event.data + "</p>";
        };
        function send() {
            ws.send(document.getElementById("msg").value);
        }
    </script>
</body>
</html>
"""

@app.get("/")
def get():
    return HTMLResponse(html)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"收到：{data}")
```

### WebSocket 聊天室範例

```python
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()

class ConnectionManager:
    def __init__(self):
        self.connections: list[WebSocket] = []

    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.connections.append(ws)

    def disconnect(self, ws: WebSocket):
        self.connections.remove(ws)

    async def broadcast(self, message: str):
        for connection in self.connections:
            await connection.send_text(message)

manager = ConnectionManager()

@app.websocket("/chat")
async def chat(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"使用者：{data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast("一位使用者離開了聊天室")
```

## Server-Sent Events（SSE）

SSE 是比 WebSocket 更簡單的即時通訊方案，僅支援伺服器向客戶端的單向推送：

```python
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import asyncio

app = FastAPI()

@app.get("/events")
async def event_stream():
    async def generate():
        for i in range(10):
            yield f"data: 事件編號 {i}\n\n"
            await asyncio.sleep(1)
    return StreamingResponse(generate(), media_type="text/event-stream")
```

## 非同步與同步的選擇

| 場景 | 使用同步 | 使用非同步 |
|------|---------|-----------|
| 簡單 CRUD | 是 | 可選 |
| 多個並行 API 呼叫 | 否 | 是 |
| WebSocket 即時通訊 | 否 | 是 |
| 檔案上傳/下載 | 可選 | 可選 |
| CPU 密集任務 | 是（多執行緒） | 否 |

---

## 延伸閱讀

- [aiohttp 官方文件](https://www.google.com/search?q=aiohttp+python+library)
- [WebSocket 協定 RFC 6455](https://www.google.com/search?q=WebSocket+RFC+6455)
- [FastAPI WebSocket 指南](https://www.google.com/search?q=FastAPI+WebSocket)
