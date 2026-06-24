# 模型監控與漂移偵測（2018-2026）

## 資料漂移與概念漂移

在生產環境中，模型的效能衰退主要有兩種原因：

**資料漂移（Data Drift）**：輸入資料的分布發生了變化。例如一個在晴天資料上訓練的降雨預測模型，在梅雨季節的表現就會下降。資料漂移可以用統計方法檢測——比較訓練資料和生產資料的分布是否一致。

**概念漂移（Concept Drift）**：輸入和輸出之間的關係發生了變化。例如使用者對「好文章」的定義隨著時間改變——十年前大家喜歡長篇深度文，現在偏好短影音。概念漂移更難檢測，因為它需要標籤資料。

```python
# 使用 PSI 檢測資料漂移
import numpy as np
from scipy.stats import ks_2samp

def population_stability_index(reference, current, bins=10):
    """計算 Population Stability Index (PSI)"""
    ref_hist, edges = np.histogram(reference, bins=bins, range=(0, 1))
    cur_hist, _ = np.histogram(current, bins=bins, range=(0, 1))
    
    ref_pct = ref_hist / len(reference) + 1e-10
    cur_pct = cur_hist / len(current) + 1e-10
    
    psi = np.sum((ref_pct - cur_pct) * np.log(ref_pct / cur_pct))
    return psi

# PSI > 0.2 表示顯著漂移
psi = population_stability_index(train_scores, prod_scores)
print(f"PSI: {psi:.3f} {'DRIFT' if psi > 0.2 else 'OK'}")
```

## 漂移偵測演算法

除了 PSI，還有幾種常見的漂移偵測方法：

**KS 檢定（Kolmogorov-Smirnov Test）**：比較兩個樣本的累積分布函數的最大差異。KS 統計量小表示分布相似。

**MMD（Maximum Mean Discrepancy）**：將資料映射到再生核希爾伯特空間，計算兩個分布之間的最大均值差異。MMD 對高維資料特別有用。

```python
# KS 檢定與 MMD 範例
from scipy.stats import ks_2samp
import numpy as np

def detect_drift_with_ks(reference, current, alpha=0.05):
    stat, p_value = ks_2samp(reference, current)
    return {"drifted": p_value < alpha, "ks_stat": stat, "p_value": p_value}

def mmd_linear(x, y):
    """線性 MMD 計算"""
    xx = np.dot(x, x.T)
    yy = np.dot(y, y.T)
    xy = np.dot(x, y.T)
    n = x.shape[0]
    m = y.shape[0]
    mmd = xx.sum() / (n * n) + yy.sum() / (m * m) - 2 * xy.sum() / (n * m)
    return max(0, mmd)
```

## 監控指標金字塔

生產環境中的 AI 監控需要分層次：

```
         ┌──────────┐
         │  品質指標  │  ← 輸出品質、使用者滿意度
        ┌┴──────────┴┐
        │  正確性指標  │  ← 準確率、錯誤率、幻覺率
       ┌┴────────────┴┐
       │  效能指標     │  ← 延遲、吞吐量、資源使用率
      ┌┴──────────────┴┐
      │  基礎監控      │  ← 可用性、錯誤率、系統狀態
```

```python
# 全端監控實作
class AIMonitor:
    def __init__(self):
        self.metrics = {
            "latency_p50": [], "latency_p99": [],
            "throughput": [], "error_rate": [],
            "drift_score": [], "quality_score": [],
        }
    
    def record_inference(self, latency_ms, success, quality=None):
        self.metrics["latency_p50"].append(latency_ms)
        if quality is not None:
            self.metrics["quality_score"].append(quality)
    
    def get_health_report(self):
        latencies = sorted(self.metrics["latency_p50"])
        n = len(latencies)
        return {
            "p50_latency": latencies[n // 2] if n else 0,
            "p99_latency": latencies[int(n * 0.99)] if n else 0,
            "error_rate": sum(1 for e in self.metrics["error_rate"] if e) / max(len(self.metrics["error_rate"]), 1),
            "avg_quality": np.mean(self.metrics["quality_score"]) if self.metrics["quality_score"] else 0,
        }
```

## LLM 特有的監控

LLM 引入了一些傳統 MLOps 不需要關注的監控維度：

**輸出長度監控**：LLM 的輸出長度直接影響延遲和成本。異常的長輸出可能是指令注入攻擊。

**毒性與偏見檢測**：使用專用模型（如 Detoxify）對 LLM 輸出進行即時篩查。

**主題漂移**：LLM 是否偏離了預定的主題範圍，特別是在多輪對話中。

```python
# LLM 專用監控
import re

class LLMQualityMonitor:
    def check_toxicity(self, text):
        """使用正則表達式進行基本的毒性檢測"""
        toxic_patterns = [
            r"\b(hate|kill|destroy|attack)\b",
        ]
        return any(re.search(p, text.lower()) for p in toxic_patterns)
    
    def check_output_length(self, text, max_tokens=4096):
        token_count = len(text.split())
        return {
            "token_count": token_count,
            "too_long": token_count > max_tokens,
            "too_short": token_count < 10,
        }
    
    def check_topic_drift(self, text, allowed_topics):
        """檢查主題是否偏移"""
        text_lower = text.lower()
        drift_score = 1.0 - max(
            sum(1 for t in topic if t in text_lower) / len(topic)
            for topic in allowed_topics
        )
        return drift_score
```

當監控偵測到異常時，應該觸發警報並自動執行補救措施：回滾到上一個穩定的模型版本、切換提示詞、或通知值班工程師。

---

**下一步**：[提示詞管理與版本控制](focus3.md)

## 延伸閱讀

- [資料漂移偵測技術](https://www.google.com/search?q=data+drift+detection+techniques)
- [PSI 與 KS 檢定比較](https://www.google.com/search?q=PSI+vs+KS+test+drift+detection)
- [LLM 輸出監控工具](https://www.google.com/search?q=LLM+output+monitoring+tools)
- [AI 系統可靠性工程](https://www.google.com/search?q=AI+reliability+engineering)
