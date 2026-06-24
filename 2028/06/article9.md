# 持續批次與動態批次

## 批次的兩種模式

深度學習推論中的批次（batching）可大幅提升吞吐量。但 LLM 推理的批次處理比傳統 CV 模型複雜得多——因為每個請求的輸出長度**不可預測**。

## 靜態批次（Static Batching）

傳統靜態批次等待收集 $N$ 個請求後才執行一次前向傳播。問題在於：

```python
import time
import random

def static_batch(requests, batch_size=4):
    outputs = []
    for i in range(0, len(requests), batch_size):
        batch = requests[i:i + batch_size]
        max_len = max(len(r) for r in batch)
        padded = [r + [0] * (max_len - len(r)) for r in batch]
        out = model_infer(padded)  # All padded to same length
        outputs.extend(out)
    return outputs
```

短序列浪費大量 padding 計算。

## 持續批次（Continuous Batching / In-flight Batching）

vLLM 引入的持續批次：**每個 token 完成後立即退出，空位立刻填入新請求**：

```python
class ContinuousBatchScheduler:
    def __init__(self, max_slots=8):
        self.slots = [None] * max_slots
        self.running = 0

    def add_request(self, prompt):
        for i, slot in enumerate(self.slots):
            if slot is None:
                self.slots[i] = {"prompt": prompt, "pos": 0, "tokens": []}
                self.running += 1
                return i
        return -1  # queue full

    def step(self):
        """Generate one token per active request, evict completed"""
        active = [(i, s) for i, s in enumerate(self.slots) if s is not None]
        if not active:
            return

        # Batch decode: shape (active_count, 1, d_model)
        batch_outputs = self.model_forward([s["prompt"][s["pos"]]
                                            for _, s in active])

        for (i, slot), token_id in zip(active, batch_outputs):
            slot["tokens"].append(token_id)
            slot["pos"] += 1

            if self.is_eos(token_id) or slot["pos"] >= 2048:
                self.slots[i] = None  # evict, slot freed
                self.running -= 1
```

## 動態批次（Dynamic Batching）

動態批次在**請求到達時**決定批次大小，而非固定：

```python
class DynamicBatcher:
    def __init__(self, max_batch=8, max_delay=0.05):
        self.queue = []
        self.max_batch = max_batch
        self.max_delay = max_delay

    async def schedule(self, request):
        self.queue.append(request)
        if len(self.queue) >= self.max_batch:
            return await self.flush()
        await asyncio.sleep(self.max_delay / len(self.queue))
        return await self.flush()

    async def flush(self):
        if not self.queue:
            return
        batch = self.queue[:self.max_batch]
        self.queue = self.queue[self.max_batch:]
        return await self.infer_batch(batch)

    async def infer_batch(self, batch):
        await asyncio.sleep(0.1 * len(batch))
        return [f"out_{i}" for i in range(len(batch))]
```

## 效能分析

| 策略 | 吞吐量 | 延遲 | 適用場景 |
|------|-------|------|---------|
| 靜態批次 | 低 | 高 | 批次大小固定 |
| 動態批次 | 中 | 中 | 傳統 CV/ASR |
| 持續批次 | 高 | 低 | LLM 推理 |

## 延伸閱讀

- [vLLM 持續批次](https://www.google.com/search?q=vLLM+continuous+batching)
- [動態批次最佳化](https://www.google.com/search?q=dynamic+batching+deep+learning)
- [NVIDIA Triton 批次策略](https://www.google.com/search?q=NVIDIA+Triton+Inference+Server+batching)

持續批次是 LLM 推理吞吐量的關鍵突破。它讓 GPU 在每個 decode step 都保持滿載，消除靜態批次中因序列長度差異造成的 padding 浪費，生產環境建議優先採用。
