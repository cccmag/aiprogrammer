# GPU vs NPU vs TPU 比較

## 三種架構的設計哲學

AI 推論硬體可分成三大陣營。理解它們的設計取捨，才能為工作負載選擇正確的加速器。

## GPU — 通用並行計算

GPU 擁有數以千計的 CUDA 核心，專為矩陣乘法設計。NVIDIA H100 配備 Transformer Engine，支援 FP8：

```python
def gpu_matmul_simulate(M, N, K, sm_count=132):
    """Simulate GPU GEMM with SMs"""
    flops = 2 * M * N * K
    peak_tflops = 2000  # H100 FP16 TFLOPS
    ideal_time = flops / (peak_tflops * 1e12)

    # Memory-bound for small matrices
    mem_read = M * K + K * N
    mem_write = M * N
    mem_bytes = (mem_read + mem_write) * 2  # FP16
    bw = 3.35e12  # H100 HBM bandwidth (3350 GB/s)
    mem_time = mem_bytes / bw

    return max(ideal_time, mem_time)
```

## NPU — 神經網路專用處理器

NPU 採用**資料流架構**（dataflow architecture），運算單元直接相連：

```python
class NPUSimulator:
    """Simulated NPU systolic array"""
    def __init__(self, array_size=128):
        self.array = [[0] * array_size for _ in range(array_size)]

    def systolic_matmul(self, A, B):
        n = len(A)  # Assume square
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for k in range(n):
                for j in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
```

特性：極低功耗（~15W vs GPU ~300W）、固定管線（無法用於訓練）、適合邊緣部署。

## TPU — Google 的矩陣單元

TPU 的核心是 **MXU（Matrix Multiply Unit）**，一個巨大的脈動陣列：

```python
class MXUSimulator:
    """Simulate TPU's Matrix Multiply Unit"""
    def __init__(self, size=128):
        self.size = size

    def matmul(self, A, B):
        """Systolic matrix multiply in one cycle (simplified)"""
        result = [[0] * self.size for _ in range(self.size)]
        for i in range(self.size):
            for k in range(self.size):
                val = A[i][k]
                for j in range(self.size):
                    result[i][j] += val * B[k][j]
        return result
```

TPU v5p 單一 pod 可達 9000+ TFLOPS BF16。

## 橫向比較

| 維度 | GPU (H100) | NPU (Ascend 910B) | TPU v5p |
|------|-----------|-----------------|---------|
| 峰值 TFLOPS | 2000 FP16 | 400 FP16 | 9000+ BF16 |
| 記憶體 | 80 GB HBM3 | 64 GB HBM2e | 95 GB HBM2e |
| 功耗 | 700W | 310W | ~500W |
| 靈活性 | 高 | 中 | 低 |
| 生態成熟度 | 極高 | 中 | 高 |

## 選擇指南

- **GPU**：通用首選，支援 PyTorch/TensorRT/ vLLM，生態最完整
- **NPU**：邊緣或中國市場，低功耗場景
- **TPU**：Google Cloud 超大規模訓練與推論，稀有但高效

## 延伸閱讀

- [NVIDIA H100 白皮書](https://www.google.com/search?q=NVIDIA+H100+Transformer+Engine)
- [Google TPU v5p](https://www.google.com/search?q=Google+TPU+v5p)
- [NPU 架構比較](https://www.google.com/search?q=NPU+AI+architecture+comparison)

選擇硬體沒有絕對答案。GPU 是通用平台，NPU 是高效節能方案，TPU 則是 Google 生態中的超級加速器。理解三者的設計哲學，就能根據成本、延遲、功耗的權衡做出最佳決策。
