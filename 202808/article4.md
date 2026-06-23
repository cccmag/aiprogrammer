# OpenTelemetry for AI 系統

## 前言

OpenTelemetry（OTel）已成為雲原生觀測的業界標準，提供統一的 API 收集追蹤、指標與日誌。對 AI 系統而言，OTel 可將推論、前處理、特徵工程等步驟納入統一觀測架構，打破 ML 與基礎設施之間的觀測孤島。

---

## 一、OTel 核心概念

- **Traces**：記錄請求從進入系統到回應的完整路徑
- **Spans**：Trace 中的單一操作單元（如特徵提取、模型推論）
- **Metrics**：聚合後的數值指標（如平均延遲、QPS）
- **Logs**：結構化的事件記錄

---

## 二、為 AI 推論加入 Tracing

```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

trace.set_tracer_provider(TracerProvider())
span_processor = BatchSpanProcessor(OTLPSpanExporter(endpoint="http://otel-collector:4317"))
trace.get_tracer_provider().add_span_processor(span_processor)
tracer = trace.get_tracer(__name__)

def predict(input_data):
    with tracer.start_as_current_span("pipeline") as span:
        span.set_attribute("input.shape", str(input_data.shape))
        features = engineer_features(input_data)
        result = model.predict(features)
        span.set_attribute("prediction.score", float(result.max()))
    return result
```

---

## 三、自訂 Metrics

```python
from opentelemetry import metrics

meter = metrics.get_meter("ai-monitor")
latency_hist = meter.create_histogram(name="prediction.latency", unit="ms")
drift_gauge = meter.create_gauge(name="feature.drift.psi")

def record(start_time, drift_values):
    latency = (time.time() - start_time) * 1000
    latency_hist.record(latency, {"model": "fraud-detector"})
    for i, s in enumerate(drift_values):
        drift_gauge.set(s, {"feature": f"f_{i}"})
```

---

## 四、OTel Collector 組態

```yaml
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
processors:
  batch:
    timeout: 1s
exporters:
  prometheus:
    endpoint: 0.0.0.0:8889
  jaeger:
    endpoint: jaeger:14250
service:
  pipelines:
    traces: [otlp, batch, jaeger]
    metrics: [otlp, batch, prometheus]
```

---

## 五、與 MLflow 整合

OTel 可與 MLflow Tracing 並存。MLflow 專注實驗層級追蹤，OTel 補足基礎設施層級觀測。建議將 MLflow 的 trace_id 注入到 OTel Span 中作為自訂屬性。

---

## 結語

OTel 為 AI 系統提供與基礎設施無縫整合的觀測框架。透過 Traces、Metrics 與 Logs 的統一收集，團隊可在同一個 Grafana 儀表板上看見應用層與 ML 層的健康狀態。

---

## 參考資料

- https://www.google.com/search?q=OpenTelemetry+AI+ML+observability
- https://www.google.com/search?q=OpenTelemetry+tracing+inference+pipeline
- https://www.google.com/search?q=OTel+collector+ML+monitoring
