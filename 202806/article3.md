# TensorRT 與模型編譯

## 從解釋執行到編譯執行

深度學習框架（PyTorch、TensorFlow）預設採用**解釋執行**：定義計算圖後，每次推理逐個 kernel 啟動。這帶來大量 kernel launch overhead。TensorRT 將模型**編譯**為優化後的執行計畫（plan file），大幅減少啟動開銷。

## TensorRT 最佳化管道

```python
import tensorrt as trt

def build_trt_engine(onnx_path: str, precision: str = "fp16"):
    """Convert ONNX model to TensorRT engine"""
    logger = trt.Logger(trt.Logger.INFO)
    builder = trt.Builder(logger)
    network = builder.create_network(1 << int(trt.NetworkDefinitionCreationFlag.EXPLICIT_BATCH))
    parser = trt.OnnxParser(network, logger)

    with open(onnx_path, "rb") as f:
        parser.parse(f.read())

    config = builder.create_builder_config()
    config.set_memory_pool_limit(trt.MemoryPoolType.WORKSPACE, 1 << 30)  # 1 GB

    if precision == "fp16":
        config.set_flag(trt.BuilderFlag.FP16)

    # INT8 量化需校準資料
    if precision == "int8":
        config.set_flag(trt.BuilderFlag.INT8)

    plan = builder.build_serialized_network(network, config)
    with open("model.plan", "wb") as f:
        f.write(plan)

    return plan
```

## Kernel Auto-Tuning

TensorRT 對每個運算層執行**數百種 kernel 變體**的自動搜索：

```python
import time

def simulate_autotune(M: int, N: int, K: int):
    """Simulate TensorRT's kernel autotuning"""
    configs = [
        {"tile_m": 64, "tile_n": 64},
        {"tile_m": 128, "tile_n": 128},
        {"tile_m": 64, "tile_n": 128},
        {"tile_m": 128, "tile_n": 64},
    ]
    best_time = float("inf")
    best_config = None
    for cfg in configs:
        # Simulated timing
        t = (M * N * K) / (cfg["tile_m"] * cfg["tile_n"]) * 0.001
        if t < best_time:
            best_time = t
            best_config = cfg
    return best_config, best_time
```

## 圖層融合（Layer Fusion）

TensorRT 將相鄰的 kernel 合併為單一 kernel：

```
原始: Conv → Bias → ReLU → Conv → Bias → ReLU
融合: ConvBiasReLU → ConvBiasReLU  (2 kernels 而非 6)
```

## 實務建議

| 最佳化 | 延遲降低 | 適用場景 |
|--------|---------|---------|
| FP16 推論 | 40-50% | 通用生產 |
| INT8 量化 | 60-70% | 延遲敏感 |
| 動態形狀 | 彈性 | 可變批次 |

## 延伸閱讀

- [TensorRT 開發者指南](https://www.google.com/search?q=TensorRT+developer+guide)
- [TensorRT ONNX 匯入](https://www.google.com/search?q=TensorRT+ONNX+import)
- [模型編譯 vs 解釋執行](https://www.google.com/search?q=model+compilation+vs+interpreted+execution)

TensorRT 透過圖融合、kernel autotuning、和精度校準，將模型推理加速 2-5 倍，是 NVIDIA GPU 上生產部署的標配工具。
