# 推論日誌與分散式追蹤

## 從請求到回應的每一毫秒（2022-2028）

### 前言

AI 推論請求經過預處理、特徵工程、模型推論、後處理等多個階段。任何一個階段的異常都可能導致最終結果錯誤或延遲過高。分散式追蹤讓你可以看到每個階段的確切耗時和狀態。

### 結構化推論日誌

日誌是除錯的第一線工具。一個好的推論日誌應包含：

```python
{
    "request_id": "req_abc123",
    "model": "gpt-5-turbo-0415",
    "input_tokens": 2048,
    "output_tokens": 512,
    "latency_ms": 3420,
    "preprocess_ms": 45,
    "inference_ms": 3250,
    "postprocess_ms": 125,
    "feature_hash": "a1b2c3d4",
    "prediction": {"class": "positive", "confidence": 0.97},
    "error": null
}
```

結構化日誌的關鍵欄位：請求 ID、模型版本、延遲分解、輸入大小、特徵指紋、預測結果、錯誤資訊。

### Span 模型

分散式追蹤的核心概念是 Span（跨度），Span 形成 Trace（追蹤）：

```
Trace: POST /predict
├── Span: preprocess (45ms)
│   ├── Span: tokenize (10ms)
│   └── Span: feature_extract (30ms)
├── Span: inference (3250ms)
│   ├── Span: attention (2800ms)
│   └── Span: logits (450ms)
└── Span: postprocess (125ms)
```

### 實作追蹤系統

以下是基於 `_code/observability.py` 中 `Tracer` 類別的示範：

```python
tracer = Tracer()
tracer.start_span("request", method="POST", path="/predict")
tracer.start_span("preprocess")
# ... 預處理邏輯 ...
tracer.end_span()
tracer.start_span("inference", model="llama-4b")
time.sleep(0.002)
tracer.end_span()
tracer.end_span()

for t in tracer.get_trace():
    print(f"{t['name']}: {t['duration_ms']}ms")
```

輸出結果類似：
```
request: 3.25ms (2 children)
preprocess: 1.01ms (0 children)
inference: 2.01ms (0 children)
```

### 延遲分析的關鍵維度

1. **模型大小**：更大的模型 → 更長的推理時間
2. **序列長度**：輸入輸出總長度影響注意力機制的計算量
3. **硬體**：GPU 類型、是否需要跨節點推理
4. **批次處理**：動態批次策略、批次大小
5. **快取命中**：KV Cache 命中率

### 常見瓶頸模式

| 模式 | 特徵 | 解決方案 |
|------|------|---------|
| 預處理慢 | 特徵提取耗時 | 預計算、快取 |
| 推理震盪 | 延遲忽高忽低 | 防止冷啟動、預載模型 |
| 尾延遲 | 少數請求極慢 | 非同步推理、超時熔斷 |
| 記憶體增長 | 推理後 VRAM 未釋放 | 模型重載、記憶體監控 |

### 與 OpenTelemetry 整合

2024 年後，OpenTelemetry 成為 AI 推論追蹤的標準。MLOps 平台透過 OTel SDK 自動注入推論請求的上下文，無需手動埋點。

### 小結

分散式追蹤讓 AI 系統的可觀測性從「知不知道有問題」提升到「知道問題在哪裡」。再搭配結構化日誌，團隊可以在數分鐘內定位到延遲異常的根因。

---

**下一步**：[警報策略與自動回復](focus5.md)

## 延伸閱讀

- [OpenTelemetry Traces](https://www.google.com/search?q=OpenTelemetry+tracing+AI+inference)
- [Distributed Tracing ML](https://www.google.com/search?q=distributed+tracing+machine+learning+systems)
- [OTel AI Semantic Conventions](https://www.google.com/search?q=OpenTelemetry+AI+semantic+conventions)
