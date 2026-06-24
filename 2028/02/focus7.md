# 即時 AI 監控與營運

## MLOps 的即時時代（2022-2028）

### 前言

即時 AI 系統的營運挑戰遠大於批次系統。一個批次模型出錯影響幾小時的報表；一個即時推論出錯可能直接導致錯誤的交易、誤診或車禍。

### 即時監控的三個層級

**1. 系統層級監控**

```python
# 即時推論指標收集
from prometheus_client import Histogram, Counter, Gauge

inference_latency = Histogram(
    "inference_latency_ms", "推論延遲（毫秒）",
    buckets=[1, 5, 10, 25, 50, 100, 500]
)
prediction_counter = Counter(
    "predictions_total", "推論總數",
    ["model_name", "version"]
)
data_drift_gauge = Gauge(
    "data_drift_score", "資料漂移分數",
    ["feature_name"]
)
```

**2. 資料品質監控**

即時管道中的資料漂移檢測：

```python
def detect_drift(reference_stats, streaming_window):
    """即時檢測特徵分布漂移"""
    drift_scores = {}
    for feature in streaming_window:
        ks_stat = ks_test(
            reference_stats[feature],
            streaming_window[feature]
        )
        drift_scores[feature] = ks_stat
        if ks_stat > 0.1:  # 漂移閥值
            alert(f"Feature {feature} drifting: {ks_stat}")
    return drift_scores
```

**3. 模型效能監控**

即時模型效能的關鍵指標：

| 指標 | 定義 | 警示閥值 |
|------|------|---------|
| 延遲 P99 | 99% 請求在時間內完成 | >50ms |
| 錯誤率 | 推論失敗比例 | >1% |
| 預測分布 | 輸出類別分布 | 與訓練偏離 >5% |
| 資料漂移 | 輸入特徵分布變化 | KS > 0.1 |
| 概念漂移 | 真實標籤分布變化 | 精度下降 >3% |

### 自動回饋循環（2024-2028）

即時 AI 系統的關鍵優勢：**能夠在毫秒內對問題做出反應**。

```python
# 自動補償機制
class AutoCompensator:
    def check_and_compensate(self, metrics):
        if metrics.latency_p99 > 50:
            self.switch_to_lightweight_model()
        if metrics.error_rate > 0.01:
            self.rollback_to_previous_version()
        if metrics.data_drift > 0.1:
            self.trigger_recalibration()
    
    def trigger_recalibration(self):
        # 使用自動標籤資料進行線上微調
        online_data = collect_recent_samples(window="10m")
        self.model.train(online_data, steps=100)
```

### 可觀測性架構

```
事件串流（Kafka）
    ↓
即時指標計算（Flink SQL）
    ↓
監控儀表板（Grafana）  ←→  自動警示（PagerDuty）
    ↓
自動補償（控制平面）    ─→  降級/回滾/重訓
```

### 疑難排解流程

![即時 AI 除錯流程圖](https://www.google.com/search?q=real+time+ML+troubleshooting+flow+diagram)

實際操作中的除錯腳本：

```python
def debug_latency_spike():
    """排查延遲暴增的根因"""
    # 1. 檢查是否有模型版本更新
    recent_deploys = get_recent_deployments("10m")
    
    # 2. 檢查上游資料源
    kafka_lag = get_consumer_lag("feature-pipeline")
    
    # 3. 檢查 GPU 利用率
    gpu_util = nvidia_smi_query()
    
    # 4. 檢查排隊長度
    queue_depth = get_triton_queue_depth()
    
    return analyze_correlation(
        recent_deploys, kafka_lag, gpu_util, queue_depth
    )
```

### 營運成熟度模型

| 等級 | 特徵 | 自動化程度 |
|------|------|-----------|
| L1 | 手動監控、人工處理 | 0% |
| L2 | 基本儀表板、email 警示 | 30% |
| L3 | 自動回滾、漂移檢測 | 60% |
| L4 | 自動補償、線上重訓 | 80% |
| L5 | 自主營運、自我修復 | 95%+ |

### 小結

即時 AI 系統的營運不是傳統 MLOps 的簡單延伸，而是一個全新的挑戰。當系統在毫秒級時間尺度上運作時，人類無法即時介入——**自動化不再是選項，而是必要條件**。

---

**下一步**：[程式實作：即時推論系統](focus_code.md)

## 延伸閱讀

- [ML 監控最佳實踐](https://www.google.com/search?q=real+time+ML+monitoring+best+practices)
- [資料漂移檢測工具](https://www.google.com/search?q=data+drift+detection+tools+whylogs+evidently)
- [即時 AI 營運案例](https://www.google.com/search?q=real+time+AI+operations+MLOps+case+study)
