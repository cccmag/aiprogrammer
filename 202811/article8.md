# 邊緣 AI 作業系統

## 1. 為何需要專用作業系統

傳統嵌入式 RTOS 缺乏 AI 推論所需的排程與記憶體管理。專用系統正在興起。

## 2. 主流方案

| 系統 | 廠商 | 核心 | 硬體 | AI 框架 |
|------|------|------|------|---------|
| EdgeX Foundry | Linux 基金會 | Linux | x86/ARM | OpenVINO |
| Azure IoT Edge | Microsoft | Linux | x86/ARM | ONNX Runtime |
| AWS Greengrass | Amazon | Linux | x86/ARM | SageMaker Neo |
| RT-Thread AI | 睿賽德 | RTOS | ARM/RISC-V | TFLM |
| AliOS Things | 阿里巴巴 | RTOS | ARM/XTENSA | TFLM |

## 3. AI 優先排程器

模擬邊緣 AI 排程器的任務優先級設計：

```python
import heapq

class EdgeAITask:
    def __init__(self, name, period, priority):
        self.name = name
        self.period = period
        self.priority = priority
        self.next = 0

    def __lt__(self, other):
        return self.priority < other.priority

class EdgeScheduler:
    def __init__(self):
        self.tasks = []

    def add(self, task):
        heapq.heappush(self.tasks, task)

    def run(self, now):
        ready = []
        while self.tasks and self.tasks[0].next <= now:
            ready.append(heapq.heappop(self.tasks))
        ready.sort(key=lambda t: t.priority)
        for t in ready:
            print(f'[{now}ms] 執行 {t.name}')
            t.next = now + t.period
            heapq.heappush(self.tasks, t)

s = EdgeScheduler()
s.add(EdgeAITask('人臉偵測', 33, 1))
s.add(EdgeAITask('語音指令', 100, 2))
for i in range(3):
    s.run(i * 30)
```

## 4. 鏡像安全更新

使用 A/B 分割區確保更新失敗可回滾：

```python
def ab_update(current, image_path):
    backup = 'B' if current == 'A' else 'A'
    try:
        with open(f'/dev/{backup}', 'wb') as f:
            f.write(open(image_path, 'rb').read())
        print(f'下次開機使用 {backup}')
        return backup
    except:
        print('失敗，回滾')
        return current
```

## 5. 結語

邊緣 AI OS 從通用 RTOS 演化為 AI 優先的專用系統。更多資訊請參考 https://www.google.com/search?q=edge+AI+operating+system+comparison
