# 低延遲模型推論

## 從 GPU 批次到即時推論（2019-2028）

### 前言

模型推論的延遲直接決定使用者體驗。2019 年，BERT 推論需要 100ms 以上；到了 2028 年，同樣的任務可以在 1ms 內完成。這背後是演算法、編譯器和硬體的聯合最佳化。

### 推論引擎的演進

**TensorFlow Serving（2019）**

```python
# TensorFlow Serving：批次推論
import requests
data = {"instances": [{"input": img.tolist()}]}
resp = requests.post("http://localhost:8501/v1/models/resnet:predict",
                     json=data)
# 批次處理可提高吞吐，但增加單次延遲
```

TensorFlow Serving 引入了**動態批次**（dynamic batching）——自動累積請求到最佳批次大小。

**NVIDIA Triton（2020-2025）**

Triton Inference Server 重新定義了推論基礎設施：

```
┌──────────────────────────┐
│       Triton Server       │
│  ┌─────┐ ┌─────┐ ┌─────┐│
│  │GPU  │ │GPU  │ │CPU  ││
│  │模型A │ │模型B │ │模型C ││
│  └─────┘ └─────┘ └─────┘│
│  調度器 │ 模型倉庫 │ 指標 │
└──────────────────────────┘
```

```python
# Triton Python client
import tritonclient.http as httpclient
client = httpclient.InferenceServerClient("localhost:8000")
result = client.infer("bert", inputs)
```

### 低延遲推論技術

**1. 編譯器最佳化**

```python
# TensorRT：將模型編譯為 GPU 最佳化圖
import tensorrt as trt
builder = trt.Builder(trt.Logger())
network = builder.create_network()
# TensorRT 自動融合 kernel、最佳化記憶體布局
# 推論延遲降低 2-5 倍
```

**2. 推論快取**

```python
# 語意快取（Semantic Cache）
# 相近的查詢直接返回快取結果
from redis import Redis
cache = Redis()
key = hash_embedding(query)
if cached := cache.get(key):
    return cached  # 延遲 <1ms
```

**3. 推論降級**

```python
def infer_with_fallback(input_data):
    for model in [large_model, medium_model, small_model]:
        start = time.time()
        result = model.predict(input_data)
        if time.time() - start < 10:  # 10ms 預算
            return result
    return rule_based_fallback(input_data)
```

### 延遲預算管理（2024-2028）

現代即時 AI 系統採用**延遲預算分解**：

| 組件 | 預算 | 技術 |
|------|------|------|
| 網路傳輸 | 2ms | gRPC、QUIC |
| 前處理 | 1ms | GPU 預處理 |
| 模型推論 | 3ms | TensorRT、量化 |
| 後處理 | 1ms | Rust/Native |
| 總計 | <10ms | — |

### 小結

低延遲推論的核心原則：**減少計算、減少傳輸、減少不必要的精度**。從 Triton 的動態批次到 TensorRT 的圖編譯，從語意快取到推論降級——每一個毫秒都是最佳化出來的。

---

**下一步**：[模型量化與編譯](focus4.md)

## 延伸閱讀

- [NVIDIA Triton Inference Server 指南](https://www.google.com/search?q=NVIDIA+Triton+inference+server+guide)
- [TensorRT 效能最佳化](https://www.google.com/search?q=TensorRT+performance+optimization+2026)
- [低延遲 ML 推論架構](https://www.google.com/search?q=low+latency+machine+learning+inference+architecture)
