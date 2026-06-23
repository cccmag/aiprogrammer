# 持續評估與監控（2024-2029）

## 從一次性測試到持續監控

### 前言

模型上線後的表現往往與離線評估不同。資料漂移、對抗性攻擊、使用者行為變化——這些都需要持續監控。

### 資料漂移偵測

訓練資料與生產資料的分佈差異是模型衰退的主因：

```python
# 資料漂移監控
def detect_drift(reference_dist, production_dist, threshold=0.05):
    from scipy.stats import ks_2samp
    statistic, p_value = ks_2samp(reference_dist, production_dist)
    if p_value < threshold:
        print(f"資料漂移偵測：KS={statistic:.3f}, p={p_value:.4f}")
        return True
    return False
```

### 即時評估管線

2025 年後，評估從批處理轉向串流：

```python
# 即時評估管線
class StreamingEvaluator:
    def __init__(self, model, window_size=1000):
        self.model = model
        self.window = deque(maxlen=window_size)
    def observe(self, input, output, feedback):
        self.window.append({
            "input": input, "output": output,
            "feedback": feedback, "timestamp": now()
        })
    def metrics(self):
        recent = list(self.window)[-100:]
        return {
            "avg_feedback": np.mean([r["feedback"] for r in recent]),
            "latency_p99": latency_p99(recent),
            "drift_score": self.drift_vs_yesterday(),
        }
```

### 退化偵測與警報

當關鍵指標下降時自動觸發警報：

```python
# 退化警報系統
alert_rules = {
    "正確性": lambda m: m["accuracy"] < 0.9,
    "安全性": lambda m: m["harmful_rate"] > 0.001,
    "延遲性": lambda m: m["p99_latency"] > 2000,
    "公平性": lambda m: m["demographic_parity"] > 0.05,
}

def check_alerts(metrics):
    for name, rule in alert_rules.items():
        if rule(metrics):
            send_alert(f"{name} 指標異常：{metrics}")
            trigger_rollback()
```

### A/B 評估與金絲雀部署

新模型版本需要逐步上線並比較：

```python
# 金絲雀部署評估
def canary_deploy(new_model, old_model, traffic_ratio=0.05):
    for request in live_traffic():
        if random.random() < traffic_ratio:
            response = new_model(request)
        else:
            response = old_model(request)
    return compare_metrics(new_model, old_model)
```

### 小結

持續評估讓模型營運從「消防模式」轉變為**預測性維護**——在問題影響使用者之前就發現它。

---

**下一步**：[評估的未來](focus7.md)

## 延伸閱讀

- [ML 監控與可觀測性](https://www.google.com/search?q=ML+model+monitoring+observability+2024)
- [資料漂移偵測方法](https://www.google.com/search?q=data+drift+detection+machine+learning)
- [金絲雀部署策略](https://www.google.com/search?q=canary+deployment+LLM+evaluation)
