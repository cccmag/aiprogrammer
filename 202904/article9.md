# 即時多模態互動

## 1. 即時挑戰

多模態 Agent 需從「請求-回應」進化到即時串流互動，處理語音流、影片幀、螢幕變化的即時感知。關鍵在於管線平行化與模型量化。

## 2. 串流處理管線

```python
import cv2, threading, queue, asyncio

class StreamPipeline:
    def __init__(self):
        self.fq = queue.Queue(maxsize=10)

    def capture(self):
        cap = cv2.VideoCapture(0)
        while True:
            ret, f = cap.read()
            if ret and not self.fq.full(): self.fq.put(f)

    def process(self, model):
        while True:
            f = self.fq.get()
            if f is None: break
            yield model(f)
```

## 3. 即時螢幕監控

```python
import mss, numpy as np

class ScreenMonitor:
    def __init__(self, agent, fps=2):
        self.agent = agent; self.interval = 1.0/fps; self.last = None

    async def loop(self):
        with mss.mss() as sct:
            while True:
                f = np.array(sct.grab(sct.monitors[1]))
                if self.last is None or np.mean(np.abs(f.astype(float)-self.last.astype(float))) > 10:
                    self.last = f
                    asyncio.create_task(self.agent.analyze(f))
                await asyncio.sleep(self.interval)
```

## 4. 語音中斷處理

```python
class InterruptHandler:
    def __init__(self):
        self.is_speaking = False; self.interrupted = False

    def on_user_speech(self):
        if self.is_speaking: self.interrupted = True; self.stop_tts()

    def stop_tts(self):
        print("TTS 中斷")

    def should_continue(self):
        if self.interrupted: self.interrupted = False; return False
        return True
```

## 5. 即時 Agent 整合

```python
class RealtimeAgent:
    def __init__(self):
        self.screen = ScreenMonitor(self); self.pipe = StreamPipeline()

    async def run(self):
        t = threading.Thread(target=self.pipe.capture); t.start()
        await self.screen.loop()

    async def analyze(self, frame):
        print("分析幀")
```

## 6. 結語

即時多模態互動的核心是非同步架構與事件驅動設計。WebRTC 與串流框架的成熟將使 Agent 具備接近人類的反應速度。

- https://www.google.com/search?q=WebRTC+AI+agent+streaming
- https://www.google.com/search?q=realtime+video+processing+python+agent
