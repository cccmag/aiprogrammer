# 邊緣 NPU 比較

## 1. 邊緣推論硬體概觀

邊緣 AI 的關鍵在於專用硬體加速器——NPU（神經網路處理單元）。本文比較市面上主流的邊緣 NPU 方案。

## 2. 主要方案比較

| 方案 | 廠商 | 算力 (TOPS) | 功耗 | 支援框架 |
|------|------|-------------|------|----------|
| Coral Edge TPU | Google | 4 TOPS | 2W | TFLite |
| Intel Movidius | Intel | 1 TOPS | 1.5W | OpenVINO |
| Jetson Orin Nano | NVIDIA | 40 TOPS | 10W | TensorRT |
| RK3588 NPU | Rockchip | 6 TOPS | 3W | RKNN |
| Kendryte K210 | Canaan | 0.8 TOPS | 0.3W | Keras |

## 3. 效能測試腳本

以下 Python 腳本可在不同 NPU 上測試推論效能：

```python
import time
import numpy as np

def benchmark_npu(backend_name, model_size, infer_fn, warmup=10, runs=100):
    """通用 NPU 效能測試"""
    input_data = np.random.randn(1, model_size).astype(np.float32)

    # 暖機
    for _ in range(warmup):
        infer_fn(input_data)

    # 計時
    start = time.perf_counter()
    for _ in range(runs):
        infer_fn(input_data)
    elapsed = time.perf_counter() - start

    avg_latency = elapsed / runs * 1000  # 毫秒
    throughput = runs / elapsed

    print(f'{backend_name}:')
    print(f'  平均延遲: {avg_latency:.2f} ms')
    print(f'  吞吐量: {throughput:.0f} 次/秒')
    return avg_latency, throughput

# 模擬不同後端的推論函數
def cpu_inference(x):
    time.sleep(0.01)  # 模擬 10ms 計算
    return x.mean()

def npu_inference(x):
    time.sleep(0.002)  # 模擬 2ms 計算（NPU 加速）
    return x.mean()

benchmark_npu('CPU 基準線', 1024, cpu_inference)
benchmark_npu('NPU 模擬', 1024, npu_inference)
```

## 4. 選擇建議

低功耗 IoT 選 K210 或 Edge TPU；邊緣伺服器選 Jetson；國產方案選 RK3588。

## 5. 結語

NPU 的選擇取決於功耗預算與模型大小。更多資訊請參考 https://www.google.com/search?q=Edge+NPU+comparison+2026
