# vLLM 與即時 LLM 推論

## 低延遲推論的挑戰

大型語言模型的推論延遲主要來自兩個瓶頸：注意力機制的計算複雜度（O(n²)）和 GPU 記憶體頻寬限制。vLLM 透過 PagedAttention 和連續批次處理，將 LLM 推論的吞吐量提升 2-4 倍。

## vLLM 的基本用法

```python
from vllm import LLM, SamplingParams

# 載入模型（自動 KV cache 管理）
llm = LLM(
    model="meta-llama/Llama-3-8B-Instruct",
    tensor_parallel_size=1,
    gpu_memory_utilization=0.9,
    max_model_len=4096,
)

# 連續批次推論
prompts = [
    "解釋即時 AI 系統的設計原則",
    "什麼是 KV cache 量化？",
    "比較 PagedAttention 與傳統注意力",
]

sampling_params = SamplingParams(
    temperature=0.7, top_p=0.9, max_tokens=512
)

outputs = llm.generate(prompts, sampling_params)
for output in outputs:
    print(output.outputs[0].text)
```

## PagedAttention 原理

傳統 KV cache 使用連續記憶體，導致嚴重的記憶體碎片化。PagedAttention 將 KV cache 分割成固定大小的「頁面」（16 tokens/page），類似作業系統的分頁機制：

```python
# 示意：PagedAttention 的記憶體管理
class PagedKVBlock:
    def __init__(self, block_size=16, num_heads=32):
        self.block_size = block_size
        self.num_heads = num_heads
        self.k_cache = torch.empty(
            block_size, num_heads, head_dim
        )
        self.v_cache = torch.empty(
            block_size, num_heads, head_dim
        )

    def append(self, key, value):
        # 非連續但高效的寫入
        slot = self.current_slot
        self.k_cache[slot] = key
        self.v_cache[slot] = value
        self.current_slot += 1
```

## 連續批次處理

傳統批次處理等待所有請求完成才返回。vLLM 的連續批次能在每次迭代動態增減請求：

```python
async def continuous_batching(llm, request_queue):
    running_requests = []
    while True:
        # 加入新請求
        while req := request_queue.get_nowait():
            running_requests.append(req)

        if not running_requests:
            await asyncio.sleep(0.001)
            continue

        # 執行一次前向傳播
        llm.step()

        # 移除已完成的請求
        running_requests = [
            r for r in running_requests
            if not r.is_finished
        ]
```

## 部署為 API 服務

```bash
# 啟動 OpenAI 相容 API
python -m vllm.entrypoints.openai.api_server \
    --model meta-llama/Llama-3-8B-Instruct \
    --port 8000 \
    --max-num-batched-tokens 8192
```

## 延伸閱讀

- [vLLM 官方文件](https://www.google.com/search?q=vLLM+PagedAttention+documentation)
- [PagedAttention 論文介紹](https://www.google.com/search?q=PagedAttention+efficient+memory+LLM)
- [連續批次處理說明](https://www.google.com/search?q=continuous+batching+LLM+inference)
