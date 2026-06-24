# GPU 推論最佳化

## 計算 vs 記憶體瓶頸

深度學習推論的延遲主要受限於兩個因素：計算強度和記憶體頻寬。Arithmetic Intensity（FLOPs / Bytes loaded）決定了一個運算是否是記憶體綁定。

## CUDA 核心最佳化

```python
import torch
import triton
import triton.language as tl

@triton.jit
def fused_matmul_relu_kernel(
    a_ptr, b_ptr, c_ptr,
    M, N, K,
    stride_am, stride_ak,
    stride_bk, stride_bn,
    stride_cm, stride_cn,
    BLOCK_SIZE_M: tl.constexpr,
    BLOCK_SIZE_N: tl.constexpr,
    BLOCK_SIZE_K: tl.constexpr,
):
    pid_m = tl.program_id(0)
    pid_n = tl.program_id(1)

    offs_m = pid_m * BLOCK_SIZE_M + tl.arange(0, BLOCK_SIZE_M)
    offs_n = pid_n * BLOCK_SIZE_N + tl.arange(0, BLOCK_SIZE_N)
    offs_k = tl.arange(0, BLOCK_SIZE_K)

    a_ptrs = a_ptr + offs_m[:, None] * stride_am + offs_k[None, :] * stride_ak
    b_ptrs = b_ptr + offs_k[:, None] * stride_bk + offs_n[None, :] * stride_bn

    accumulator = tl.zeros((BLOCK_SIZE_M, BLOCK_SIZE_N), dtype=tl.float32)
    for k in range(0, K, BLOCK_SIZE_K):
        a = tl.load(a_ptrs, mask=offs_k[None, :] < K - k, other=0.0)
        b = tl.load(b_ptrs, mask=offs_k[:, None] < K - k, other=0.0)
        accumulator += tl.dot(a, b)
        a_ptrs += BLOCK_SIZE_K * stride_ak
        b_ptrs += BLOCK_SIZE_K * stride_bk

    c = tl.relu(accumulator.to(tl.float16))
    c_ptrs = c_ptr + offs_m[:, None] * stride_cm + offs_n[None, :] * stride_cn
    tl.store(c_ptrs, c)
```

## 運算元融合

每個 kernel launch 都有數十微秒的開銷。運算元融合將多個運算合併為單一 kernel：

```python
class FusedMultiHeadAttention(torch.nn.Module):
    def __init__(self, dim, num_heads):
        super().__init__()
        self.num_heads = num_heads
        self.head_dim = dim // num_heads

    def forward(self, x):
        B, T, C = x.shape
        # 單一矩陣乘法計算 QKV
        qkv = x @ self.w_qkv  # (B, T, 3*C)
        q, k, v = qkv.chunk(3, dim=-1)

        # 融合的 flash attention
        output = torch.nn.functional.scaled_dot_product_attention(
            q, k, v, is_causal=True
        )
        return output @ self.w_out
```

## Flash Attention

Flash Attention 透過 tiling 減少 HBM 存取，將注意力計算的 IO 複雜度從 O(N²) 降到 O(N)：

```python
# PyTorch 2.x 已內建 Flash Attention
# 使用 SDPA 即可自動啟用
attention = torch.nn.functional.scaled_dot_product_attention(
    query, key, value,
    attn_mask=None,
    dropout_p=0.0,
    is_causal=True,
).to(query.dtype)
```

## 批次動態排程

```python
class DynamicBatcher:
    def __init__(self, max_batch_size=32, max_wait_ms=5):
        self.queue = asyncio.Queue()
        self.max_batch = max_batch_size
        self.max_wait = max_wait_ms / 1000

    async def infer(self, request):
        future = asyncio.Future()
        await self.queue.put((request, future))
        return await future

    async def process_batch(self):
        while True:
            batch, futures = [], []
            deadline = time.time() + self.max_wait

            while len(batch) < self.max_batch:
                remaining = deadline - time.time()
                if remaining <= 0:
                    break
                try:
                    req, fut = await asyncio.wait_for(
                        self.queue.get(), remaining
                    )
                    batch.append(req)
                    futures.append(fut)
                except asyncio.TimeoutError:
                    break

            if batch:
                results = self.model(batch)
                for fut, res in zip(futures, results):
                    fut.set_result(res)
```

## TensorRT 編譯

```python
import tensorrt as trt

def build_trt_engine(onnx_path, precision='fp16'):
    logger = trt.Logger(trt.Logger.INFO)
    builder = trt.Builder(logger)
    network = builder.create_network()
    parser = trt.OnnxParser(network, logger)

    with open(onnx_path, 'rb') as f:
        parser.parse(f.read())

    config = builder.create_builder_config()
    if precision == 'fp16':
        config.set_flag(trt.BuilderFlag.FP16)

    engine = builder.build_engine(network, config)
    return engine
```

## 延伸閱讀

- [Triton 程式設計指南](https://www.google.com/search?q=Triton+programming+guide+GPU)
- [Flash Attention 原理](https://www.google.com/search?q=Flash+Attention+algorithm+explanation)
- [TensorRT 最佳化](https://www.google.com/search?q=TensorRT+inference+optimization+guide)
