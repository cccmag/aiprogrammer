# 模型服務框架：Triton 與 BentoML 實戰

## 前言

訓練一個好模型只是成功的一半——如何將模型穩定、高效地提供服務，是 MLOps 的最後一哩路。模型服務框架負責處理 GPU 資源管理、請求路由、自動擴展、模型版本管理等關鍵任務。本文深入兩個最受歡迎的開源服務框架：NVIDIA Triton Inference Server 和 BentoML。

## NVIDIA Triton Inference Server

Triton 是 NVIDIA 開發的高效能模型推理伺服器，支援 GPU 與 CPU 上的多模型、多框架部署。它的核心優勢包括動態批次處理、Concurrent Model Execution、Model Ensemble 與模型版本管理。

### 安裝與基本配置

```bash
# 使用 Docker 啟動 Triton
docker run --gpus all -p 8000:8000 -p 8001:8001 -p 8002:8002 \
  -v /path/to/model_repository:/models \
  nvcr.io/nvidia/tritonserver:24.12-py3 \
  tritonserver --model-repository=/models
```

Triton 的模型倉庫遵循嚴格的目錄結構：

```
model_repository/
├── sentiment_model/
│   ├── config.pbtxt          # 模型配置
│   ├── 1/                    # 版本 1
│   │   └── model.onnx
│   └── 2/                    # 版本 2
│       └── model.onnx
```

### 動態批次處理

動態批次處理是 Triton 最有價值的特性之一。它會自動將多個請求合併為一個批次執行，大幅提升 GPU 利用率：

```python
# config.pbtxt — 啟用動態批次處理
name: "sentiment_model"
platform: "onnxruntime_onnx"
max_batch_size: 64
input [
  {
    name: "input_ids"
    data_type: TYPE_INT64
    dims: [128]
  }
]
output [
  {
    name: "probabilities"
    data_type: TYPE_FP32
    dims: [2]
  }
]
dynamic_batching {
  preferred_batch_size: [4, 8, 16, 32]
  max_queue_delay_microseconds: 100
}
```

### Python Client SDK

```python
import tritonclient.http as httpclient
import numpy as np

# 建立連接
client = httpclient.InferenceServerClient(url="localhost:8000")

# 準備輸入
input_data = np.array([[101, 2056, 3003, 102]], dtype=np.int64)
input_tensor = httpclient.InferInput("input_ids", input_data.shape, "INT64")
input_tensor.set_data_from_numpy(input_data)

# 執行推論
result = client.infer(
    model_name="sentiment_model",
    model_version="2",  # 指定版本
    inputs=[input_tensor]
)

# 取得輸出
output = result.as_numpy("probabilities")
print(f"Positive: {output[0][1]:.3f}")
```

### Model Ensemble

Triton 支援將多個模型組合為一個 Ensemble Pipeline，減少客戶端與伺服器之間的多次通訊：

```python
# config.pbtxt — Ensemble 配置
name: "rag_ensemble"
platform: "ensemble"
ensemble_scheduling {
  step [
    {
      model_name: "text_encoder"
      model_version: -1
      input_map: { key: "TEXT", value: "INPUT__0" }
      output_map: { key: "EMBEDDING", value: "ENCODER__0" }
    },
    {
      model_name: "reranker"
      model_version: -1
      input_map: { key: "EMBEDDING", value: "ENCODER__0" }
      output_map: { key: "RANKED", value: "OUTPUT__0" }
    }
  ]
}
```

## BentoML：從模型到微服務

BentoML 採取不同的哲學——它將模型、預處理邏輯、後處理邏輯打包為一個「Bento」（便當），然後部署為標準化的 REST/gRPC 服務。BentoML 與 MLflow 有深度整合，可以直接載入 MLflow 註冊的模型。

### 定義服務

```python
import bentoml
import numpy as np
from bentoml.io import JSON, Image

# 載入 MLflow 註冊的模型
runner = bentoml.mlflow.get("sentiment_model:production").to_runner()

# 定義 BentoML 服務
svc = bentoml.Service("sentiment-service", runners=[runner])

@svc.api(input=JSON(), output=JSON())
async def predict(input_data: dict) -> dict:
    """情感分析 API"""
    text = input_data["text"]

    # 預處理
    tokens = preprocess(text)
    input_tensor = np.array([tokens], dtype=np.int64)

    # 推論
    output = await runner.async_run(input_tensor)
    probabilities = output.tolist()[0]

    # 後處理
    result = {
        "label": "positive" if probabilities[1] > 0.5 else "negative",
        "confidence": float(max(probabilities)),
        "probabilities": {
            "negative": float(probabilities[0]),
            "positive": float(probabilities[1])
        }
    }
    return result

def preprocess(text: str) -> list[int]:
    """簡化的預處理（實務上使用 tokenizer）"""
    # tokenize, pad, truncate
    return [101, 2056, 3003, 102]
```

### 部署選項

BentoML 提供多種部署模式：

```python
# 1. 本地部署
# bentoml serve service.py:svc --reload

# 2. 容器化部署
# bentoml containerize sentiment-service:latest \
#   -t myregistry/sentiment-service:latest

# 3. Kubernetes 部署 (使用 BentoDeployment CRD)
from bentoml.deployment import BentoDeployment

deployment = BentoDeployment(
    name="sentiment-service",
    bento="sentiment-service:latest",
    scaling={"min_replicas": 3, "max_replicas": 10},
    resources={"gpu": 1, "memory": "4Gi"}
)
deployment.apply()
```

### 非同步推論與串流

BentoML 原生支援非同步處理，適合高吞吐量場景：

```python
@svc.api(input=JSON(), output=JSON())
async def batch_predict(input_data: dict) -> dict:
    """批次預測 API"""
    texts = input_data["texts"]
    tokens = [preprocess(t) for t in texts]
    input_array = np.array(tokens, dtype=np.int64)

    # 非同步批次推論
    outputs = await runner.async_run(input_array)

    results = []
    for probs in outputs.tolist():
        results.append({
            "label": "positive" if probs[1] > 0.5 else "negative",
            "confidence": max(probs)
        })
    return {"results": results}
```

## Triton vs BentoML 比較

| 面向 | Triton Inference Server | BentoML |
|------|------------------------|---------|
| 核心優勢 | GPU 推論效能極致優化 | 模型打包與服務化 |
| 多框架支援 | TensorRT、ONNX、PyTorch、TF | MLflow、SKlearn、PyTorch |
| 批次處理 | 動態批次 + Concurrent Execution | 應用層批次 |
| 學習曲線 | 中高（需理解 GPU 配置） | 低（Pythonic API） |
| 適合場景 | 高效能模型服務、GPU 密集 | 快速原型到生產、微服務整合 |

實務上，許多組織將兩者組合使用：BentoML 負責模型打包與服務邏輯，Triton 負責 GPU 推論引擎——用 BentoML 作為前端 API，將推論請求轉發給後端的 Triton。

## 參考資源

- [NVIDIA Triton 官方文件](https://www.google.com/search?q=Triton+Inference+Server+documentation)
- [BentoML 快速入門](https://www.google.com/search?q=BentoML+quickstart+guide)
- [Triton 動態批次處理最佳化](https://www.google.com/search?q=Triton+dynamic+batching+optimization)
- [BentoML 與 MLflow 整合](https://www.google.com/search?q=BentoML+MLflow+integration)
