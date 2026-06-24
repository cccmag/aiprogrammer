# AI 可靠度工程

## 前言

AI 可靠度工程（AIRE）是將 SRE 方法論應用於 AI 系統的實踐。不同於傳統軟體，AI 的失效模式更多樣——模型衰退、資料漂移、對抗樣本等。

---

## 一、SLA/SLO/SLI

### 定義

- **SLI**：量化的服務品質指標
- **SLO**：SLI 的目標值
- **SLA**：對外承諾的服務水準

### AI 專屬 SLI

```python
class AIMetrics:
    def __init__(self):
        self.sli_definitions = {
            "prediction_accuracy": {"target": 0.85, "measurement": "rolling_7d"},
            "p99_latency": {"target": 1.0, "measurement": "rolling_1h"},
            "drift_coverage": {"target": 0.95, "measurement": "instant"},
        }

    def check_slo(self, current_values):
        return {
            name: {
                "value": current_values[name],
                "target": defn["target"],
                "met": current_values[name] >= defn["target"]
            }
            for name, defn in self.sli_definitions.items()
        }
```

---

## 二、錯誤預算

```python
class ErrorBudget:
    def __init__(self, slo_target):
        self.total_budget = 1 - slo_target

    def consume(self, current_sli):
        consumed = 1 - current_sli
        remaining = max(self.total_budget - consumed, 0)
        return {"consumed": consumed, "remaining": remaining, "exhausted": remaining <= 0}
```

---

## 三、FMEA

| 失效模式 | 影響 | 可偵測性 | 優先級 |
|---------|------|---------|-------|
| 資料漂移 | 準確率下降 20%+ | 高（PSI） | P0 |
| GPU OOM | 推論中斷 | 高（指標） | P0 |
| 特徵管線延遲 | 預測失效 | 中 | P1 |

---

## 四、可靠性測試

```python
class AIChaosExperiment:
    def inject_feature_noise(self, noise_level=0.1): pass
    def inject_latency(self, delay_ms=1000): pass
    def simulate_traffic_spike(self, multiplier=10): pass

class CanaryEvaluator:
    def evaluate(self, baseline, canary):
        for metric in baseline:
            ratio = canary[metric] / baseline[metric]
            if ratio < 0.95:
                return False
        return True
```

---

## 五、事故回應流程

偵測 → 分類 (P0/P1/P2) → 緩解 → RCA → 改善 → Postmortem

---

## 六、成熟度模型

| 等級 | 特徵 |
|------|------|
| L0 初始 | 無監控，使用者回報才知道 |
| L1 反應 | 有儀表板但無警報 |
| L2 主動 | SLO 定義 + 自動警報 |
| L3 預測 | 能在漂移發生前預測 |
| L4 自動修復 | 系統能自我修復 |

---

## 結語

從定義 SLI/SLO 開始，逐步建立監控、警報與自動回復機制，讓 AI 系統達到生產等級的可靠性。

---

## 參考資料

- https://www.google.com/search?q=AI+reliability+engineering+SRE
- https://www.google.com/search?q=error+budget+ML+model+monitoring
- https://www.google.com/search?q=chaos+engineering+AI+systems
