# 推論服務與水平擴展（2022-2028）

## 從單機到分散式

當一個 LLM 模型需要服務數千個使用者時，單機部署顯然不夠。推論服務架構需要解決：負載均衡、自動擴展、容錯、以及成本控制。

## 推論服務架構

```
              ┌─────────────┐
              │   Load      │
使用者 ──────►│   Balancer  ├─────► Router
              └─────────────┘
                      │
        ┌─────────────┼─────────────┐
        ▼             ▼             ▼
   ┌─────────┐   ┌─────────┐   ┌─────────┐
   │ vLLM    │   │ vLLM    │   │ vLLM    │
   │ Node 1  │   │ Node 2  │   │ Node N  │
   └─────────┘   └─────────┘   └─────────┘
        │             │             │
        └─────────────┼─────────────┘
                      ▼
              ┌─────────────┐
              │  Tensor     │
              │  Parallel   │
              └─────────────┘
```

## 服務調度策略

### Request-Level 負載均衡

```python
class LoadBalancer:
    def __init__(self, backends):
        self.backends = backends
        self.queues = [0] * len(backends)
    
    def select_backend(self, model_id, seq_len):
        # 選擇等候佇列最短的後端
        min_queue = min(self.queues)
        idx = self.queues.index(min_queue)
        
        # 估算處理時間
        estimated_time = seq_len / self.backends[idx].throughput
        self.queues[idx] += estimated_time
        
        return idx
    
    def complete_request(self, idx, actual_time):
        self.queues[idx] -= actual_time
```

### 模型並行推論

當單個 GPU 記憶體不足以載入模型時，需要跨 GPU 分散：

```
張量並行（Tensor Parallel）:
    Layer 1          Layer 2
    ┌──┬──┬──┐      ┌──┬──┬──┐
GPU0│W1│W2│W3│      │W1│W2│W3│
    └──┴──┴──┘      └──┴──┴──┘

管線並行（Pipeline Parallel）:
GPU0: Layer 1-8  ──► GPU1: Layer 9-16
```

## 連續批次處理

傳統批次處理等待所有請求完成後才處理下一批，導致 GPU 利用率低下：

```
傳統批次:
[Req1 ████████][Req2 ████████][空白 ░░░░░░░░]
               ↑ 等待最慢的請求

連續批次:
[Req1 ██][Req2 ████][Req1 ██][Req3 ██][Req1 ██]
        ↑ Req1 完成後立即插入 Req3
```

## 推論服務的關鍵指標

| 指標 | 定義 | 理想值 |
|------|------|--------|
| TTFT | 首個 token 生成時間 | < 500ms |
| TPOT | 每個 token 生成時間 | < 50ms |
| Throughput | 每秒處理請求數 | 越高越好 |
| GPU 利用率 | GPU 使用率 | > 80% |

## 2024-2028 的服務化趨勢

推論即服務（Inference as a Service）已成為主流。AWS SageMaker、Together AI、Anyscale 等平台提供託管推論。開源方案如 vLLM + Ray 讓團隊可以在自己的基礎設施上搭建媲美雲端服務的推論系統。

## 延伸閱讀

- [vLLM: Easy, Fast, Cheap LLM Serving](https://www.google.com/search?q=vLLM+LLM+serving+continuous+batching)
- [Ray: Distributed Inference Framework](https://www.google.com/search?q=Ray+distributed+inference+LLM)
- [MLOps Inference Serving Patterns](https://www.google.com/search?q=MLOps+LLM+inference+serving+architecture)

---

*本篇文章為「AI 程式人雜誌 2026 年 6 月號」焦點系列之六。*
