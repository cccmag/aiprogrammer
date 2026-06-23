# WebSocket 即時通訊

## 從 HTTP 到 WebSocket

HTTP 的請求-回應模型對即時 AI 系統不夠友善。伺服器推播、即時語音辨識、串流回應——這些場景需要雙向即時連線。WebSocket 在單一 TCP 連線上提供全雙工通訊。

## 串流 LLM 回應

```python
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from vllm import AsyncLLMEngine, SamplingParams

app = FastAPI()
engine = AsyncLLMEngine.from_engine_args(engine_args)

@app.websocket("/chat/stream")
async def chat_stream(websocket: WebSocket):
    await websocket.accept()

    try:
        while True:
            prompt = await websocket.receive_text()
            sampling = SamplingParams(max_tokens=1024)

            # 串流產出每個 token
            async for output in engine.generate(
                prompt, sampling
            ):
                token = output.outputs[0].text
                await websocket.send_json({
                    'token': token,
                    'finished': output.finished,
                })
    except WebSocketDisconnect:
        print("Client disconnected")
```

## 即時語音串流

```python
import asyncio
import pyaudio
import websockets
import json

async def stream_audio(model_url):
    p = pyaudio.PyAudio()
    stream = p.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=16000,
        input=True,
        frames_per_buffer=1024,
    )

    async with websockets.connect(model_url) as ws:
        try:
            while True:
                data = stream.read(1024)
                await ws.send(data)

                result = await ws.recv()
                transcription = json.loads(result)
                print(transcription['text'], end='', flush=True)
        except websockets.ConnectionClosed:
            print("\n連線中斷")
```

## 後端 WebSocket 管理

```python
class ConnectionManager:
    def __init__(self):
        self.active: dict[str, WebSocket] = {}

    async def connect(self, client_id: str, ws: WebSocket):
        await ws.accept()
        self.active[client_id] = ws

    def disconnect(self, client_id: str):
        self.active.pop(client_id, None)

    async def broadcast(self, message: dict):
        dead = []
        for cid, ws in self.active.items():
            try:
                await ws.send_json(message)
            except WebSocketDisconnect:
                dead.append(cid)
        for cid in dead:
            self.disconnect(cid)

manager = ConnectionManager()

@app.websocket("/ws/{client_id}")
async def ws_endpoint(ws: WebSocket, client_id: str):
    await manager.connect(client_id, ws)
    try:
        while True:
            data = await ws.receive_json()
            result = await process_realtime(data)
            await ws.send_json(result)
    except WebSocketDisconnect:
        manager.disconnect(client_id)
```

## 連線池與負載均衡

WebSocket 長連線比短連線消耗更多資源。需要連線池管理和優雅關閉：

```python
class WebSocketPool:
    def __init__(self, max_connections=1000):
        self.pool = asyncio.Queue(max_connections)
        self.active_count = 0

    async def acquire(self):
        self.active_count += 1
        return await self.pool.get()

    async def release(self, ws):
        self.active_count -= 1
        await self.pool.put(ws)

    async def health_check(self):
        while True:
            await asyncio.sleep(30)
            dead = []
            for ws in self.pool._queue:
                try:
                    await ws.ping()
                except Exception:
                    dead.append(ws)
            for ws in dead:
                self.pool._queue.remove(ws)
```

## 延遲最佳化

WebSocket 的延遲最佳化重點：
- **二進位框架**：使用 protobuf 或 msgpack 取代 JSON
- **Nagle 演算法關閉**：TCP_NODELAY 減少封包延遲
- **壓縮**：串流較大 payload 時啟用 permessage-deflate

## 延伸閱讀

- [WebSocket 通訊協定 RFC 6455](https://www.google.com/search?q=WebSocket+RFC+6455)
- [FastAPI WebSocket 指南](https://www.google.com/search?q=FastAPI+WebSocket+tutorial)
- [即時語音辨識架構](https://www.google.com/search?q=real+time+speech+recognition+WebSocket)
