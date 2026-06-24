# 漂移偵測演算法實作

## 前言

模型在生產環境中的效能衰退是一個必然趨勢——資料分布會改變、使用者行為會演化、業務規則會更新。漂移偵測（Drift Detection）的任務就是及早發現這些變化，在模型效能顯著下降之前觸發警報或自動補救措施。

本文將深入四種漂移偵測演算法：PSI、KS 檢定、MMD 以及專為 LLM 設計的輸出漂移檢測，並討論如何將它們組合成實用的監控系統。

## 資料漂移與概念漂移

在深入演算法之前，需要釐清兩者的差異：

- **資料漂移（Data Drift）**：輸入特徵的分布發生變化。例如，一個在年輕族群資料上訓練的推薦系統，當使用者基數擴大到年長族群時，輸入分布就會漂移。
- **概念漂移（Concept Drift）**：輸入與輸出之間的關係發生變化。例如，「受歡迎的內容」從長篇文章變成短影片——同樣的輸入特徵，對應的標籤變了。

```python
# 兩種類型的模擬
import numpy as np

def simulate_data_drift():
    """模擬資料漂移：輸入分布變化"""
    # 訓練資料：正常分布
    train_data = np.random.normal(loc=0.5, scale=0.1, size=1000)
    # 生產資料：分布偏移
    prod_data = np.random.normal(loc=0.7, scale=0.15, size=1000)
    return train_data, prod_data

def simulate_concept_drift():
    """模擬概念漂移：輸入-輸出關係變化"""
    X = np.random.rand(1000, 5)
    # 舊概念：y = 2*x1 + 3*x2
    y_old = 2 * X[:, 0] + 3 * X[:, 1]
    # 新概念：y = -1*x1 + 3*x2 + 5*x3
    y_new = -1 * X[:, 0] + 3 * X[:, 1] + 5 * X[:, 2]
    return y_old, y_new
```

## PSI（Population Stability Index）

PSI 是金融業最早使用的漂移偵測指標，衡量兩個分布之間的差異程度。它計算每個 bin 中兩個分布的比率差異：

```python
import numpy as np

def psi_score(reference: np.ndarray, current: np.ndarray,
              bins: int = 10, epsilon: float = 1e-10) -> float:
    """計算 Population Stability Index"""
    # 根據 reference 的分布建立 bin 邊界
    bin_edges = np.linspace(0, 1, bins + 1)

    # 計算兩個分布的直方圖
    ref_hist, _ = np.histogram(reference, bins=bin_edges)
    cur_hist, _ = np.histogram(current, bins=bin_edges)

    # 轉換為比例
    ref_pct = ref_hist / len(reference) + epsilon
    cur_pct = cur_hist / len(current) + epsilon

    # 計算 PSI
    psi = np.sum((ref_pct - cur_pct) * np.log(ref_pct / cur_pct))
    return psi

# PSI 閾值
PSI_THRESHOLDS = {
    "no_drift": 0.0,
    "low_drift": 0.1,    # < 0.1: 無顯著漂移
    "medium_drift": 0.2,  # 0.1-0.2: 中度漂移，需要關注
    "high_drift": 0.3    # > 0.2: 顯著漂移，需要行動
}

class PSIDriftDetector:
    def __init__(self, reference: np.ndarray, threshold: float = 0.2,
                 window_size: int = 100):
        self.reference = reference
        self.threshold = threshold
        self.window_size = window_size
        self.history: list[float] = []

    def check(self, new_samples: np.ndarray) -> dict:
        """檢查新樣本是否有漂移"""
        current = new_samples[-self.window_size:] if len(new_samples) > self.window_size else new_samples
        psi = psi_score(self.reference, current)
        self.history.append(psi)

        drift_level = "none"
        if psi > PSI_THRESHOLDS["high_drift"]:
            drift_level = "high"
        elif psi > PSI_THRESHOLDS["medium_drift"]:
            drift_level = "medium"
        elif psi > PSI_THRESHOLDS["low_drift"]:
            drift_level = "low"

        return {
            "psi": round(psi, 4),
            "drifted": psi > self.threshold,
            "drift_level": drift_level,
            "window_size": len(current),
        }

    def get_trend(self) -> dict:
        """取得 PSI 趨勢"""
        if len(self.history) < 2:
            return {"trend": "insufficient_data"}
        recent = self.history[-10:]
        return {
            "current": self.history[-1],
            "mean": np.mean(self.history),
            "max": max(self.history),
            "trend": "increasing" if recent[-1] > recent[0] else "stable",
        }
```

## KS 檢定（Kolmogorov-Smirnov Test）

KS 檢定是統計學中最經典的分布比較方法，計算兩個經驗累積分布函數的最大差異：

```python
from scipy.stats import ks_2samp

def ks_drift_test(reference: np.ndarray, current: np.ndarray,
                  alpha: float = 0.05) -> dict:
    """使用 KS 檢定檢測漂移"""
    statistic, p_value = ks_2samp(reference, current)

    return {
        "ks_statistic": round(statistic, 4),
        "p_value": round(p_value, 4),
        "drifted": p_value < alpha,
        "alpha": alpha,
        "interpretation": (
            f"KS={statistic:.3f}, p={p_value:.4f} — "
            f"{'有顯著差異' if p_value < alpha else '無顯著差異'}"
        )
    }

# KS 檢定的進階應用：每個特徵獨立檢測
class FeatureWiseKSChecker:
    def __init__(self, reference_data: np.ndarray, feature_names: list[str],
                 alpha: float = 0.05):
        self.reference = reference_data
        self.feature_names = feature_names
        self.alpha = alpha

    def check_all_features(self, current_data: np.ndarray) -> dict:
        """對每個特徵獨立進行 KS 檢定"""
        results = {}
        for i, name in enumerate(self.feature_names):
            if i < self.reference.shape[1] and i < current_data.shape[1]:
                ref_feat = self.reference[:, i]
                cur_feat = current_data[:, i]
                result = ks_drift_test(ref_feat, cur_feat, self.alpha)
                results[name] = result

        # 彙總
        drifted_features = [
            name for name, r in results.items() if r["drifted"]
        ]
        return {
            "features": results,
            "drifted_count": len(drifted_features),
            "drifted_features": drifted_features,
            "total_features": len(self.feature_names),
            "drift_ratio": len(drifted_features) / max(len(self.feature_names), 1),
        }

    def report(self, current_data: np.ndarray) -> str:
        """產生人類可讀報告"""
        results = self.check_all_features(current_data)
        lines = [f"=== 特徵漂移報告 ==="]
        lines.append(f"檢測特徵數: {results['total_features']}")
        lines.append(f"漂移特徵數: {results['drifted_count']} ({results['drift_ratio']*100:.1f}%)")
        lines.append("")

        for name, r in results["features"].items():
            icon = "⚠" if r["drifted"] else "✓"
            lines.append(f"  {icon} {name}: KS={r['ks_statistic']:.3f} (p={r['p_value']:.4f})")

        if results["drifted_features"]:
            lines.append(f"\n漂移特徵: {', '.join(results['drifted_features'])}")

        return "\n".join(lines)
```

## MMD（Maximum Mean Discrepancy）

MMD 是機器學習社群更常用的漂移檢測方法，特別適合高維資料。它將資料映射到 RKHS（再生核希爾伯特空間），比較兩個分布的均值嵌入：

```python
def mmd_linear(X: np.ndarray, Y: np.ndarray) -> float:
    """線性 MMD 計算"""
    n = X.shape[0]
    m = Y.shape[0]

    XX = X @ X.T
    YY = Y @ Y.T
    XY = X @ Y.T

    mmd = (XX.sum() - np.trace(XX)) / (n * (n - 1))
    mmd += (YY.sum() - np.trace(YY)) / (m * (m - 1))
    mmd -= 2 * XY.sum() / (n * m)

    return max(0, mmd)

def mmd_rbf(X: np.ndarray, Y: np.ndarray, sigma: float = 1.0) -> float:
    """RBF 核 MMD 計算"""
    def rbf_kernel(a, b, sigma):
        dists = np.sum(a**2, axis=1, keepdims=True) + \
                np.sum(b**2, axis=1) - 2 * (a @ b.T)
        return np.exp(-dists / (2 * sigma**2))

    n = X.shape[0]
    m = Y.shape[0]

    K_XX = rbf_kernel(X, X, sigma)
    K_YY = rbf_kernel(Y, Y, sigma)
    K_XY = rbf_kernel(X, Y, sigma)

    # 去掉對角線項
    np.fill_diagonal(K_XX, 0)
    np.fill_diagonal(K_YY, 0)

    mmd = K_XX.sum() / (n * (n - 1))
    mmd += K_YY.sum() / (m * (m - 1))
    mmd -= 2 * K_XY.sum() / (n * m)

    return max(0, mmd)

class MMDDriftDetector:
    def __init__(self, reference: np.ndarray, kernel: str = "rbf",
                 threshold: float = 0.05):
        self.reference = reference
        self.kernel = kernel
        self.threshold = threshold

    def check(self, current: np.ndarray) -> dict:
        if self.kernel == "linear":
            mmd = mmd_linear(self.reference, current)
        else:
            # 使用中位數距離作為 sigma
            median_dist = np.median(
                np.abs(self.reference[:, None] - self.reference[None, :])
            )
            sigma = max(median_dist, 0.1)
            mmd = mmd_rbf(self.reference, current, sigma)

        return {
            "mmd": round(mmd, 6),
            "drifted": mmd > self.threshold,
            "kernel": self.kernel,
            "threshold": self.threshold,
        }
```

## LLM 專用的輸出漂移檢測

LLM 的輸出漂移檢測需要從語義層面分析。單純的統計分布檢測無法捕捉語義變化：

```python
class LLMOutputDriftDetector:
    def __init__(self, reference_outputs: list[str]):
        self.reference = reference_outputs

    def check_output_drift(self, current_outputs: list[str]) -> dict:
        """檢測 LLM 輸出是否有語義漂移"""
        # 1. 長度分布漂移
        ref_lengths = np.array([len(o.split()) for o in self.reference])
        cur_lengths = np.array([len(o.split()) for o in current_outputs])
        length_psi = psi_score(ref_lengths / max(ref_lengths.max(), 1),
                                cur_lengths / max(cur_lengths.max(), 1))

        # 2. 詞彙多樣性漂移
        ref_diversity = self._vocabulary_diversity(self.reference)
        cur_diversity = self._vocabulary_diversity(current_outputs)

        # 3. 情感漂移（簡化版）
        ref_sentiment = self._average_sentiment(self.reference)
        cur_sentiment = self._average_sentiment(current_outputs)

        # 4. 主題分佈漂移（使用關鍵詞作為代理）
        ref_topics = self._extract_topic_distribution(self.reference)
        cur_topics = self._extract_topic_distribution(current_outputs)
        topic_sim = self._cosine_similarity(ref_topics, cur_topics)

        drifts = []
        if length_psi > 0.2:
            drifts.append("output_length")
        if abs(ref_diversity - cur_diversity) > 0.1:
            drifts.append("vocabulary_diversity")
        if abs(ref_sentiment - cur_sentiment) > 0.3:
            drifts.append("sentiment")
        if topic_sim < 0.7:
            drifts.append("topic_distribution")

        return {
            "drifted": len(drifts) > 0,
            "drift_dimensions": drifts,
            "metrics": {
                "length_psi": round(length_psi, 3),
                "diversity_change": round(cur_diversity - ref_diversity, 3),
                "sentiment_shift": round(cur_sentiment - ref_sentiment, 3),
                "topic_similarity": round(topic_sim, 3),
            },
        }

    def _vocabulary_diversity(self, texts: list[str]) -> float:
        all_words = " ".join(texts).split()
        return len(set(all_words)) / max(len(all_words), 1)

    def _average_sentiment(self, texts: list[str]) -> float:
        """簡化情感分析（-1 到 1）"""
        positive = {"好", "優秀", "讚", "喜歡", "推薦", "實用"}
        negative = {"差", "爛", "糟", "無用", "浪費", "困擾"}
        total = 0
        for text in texts:
            words = set(text.lower().split())
            pos = len(words & positive)
            neg = len(words & negative)
            total += (pos - neg) / max(pos + neg, 1) if pos + neg > 0 else 0
        return total / max(len(texts), 1)

    def _extract_topic_distribution(self, texts: list[str]) -> list[float]:
        """提取主題分布（簡化版：使用預定義主題詞表）"""
        topics = {
            "技術": {"程式碼", "API", "函式", "框架", "部署"},
            "產品": {"功能", "價格", "方案", "版本", "更新"},
            "問題": {"錯誤", "異常", "失敗", "困擾", "議題"},
        }
        vec = []
        for topic, keywords in topics.items():
            count = sum(
                1 for kw in keywords
                if any(kw in t for t in texts)
            )
            vec.append(count)
        return vec / np.linalg.norm(vec) if np.linalg.norm(vec) > 0 else vec

    def _cosine_similarity(self, a: list[float], b: list[float]) -> float:
        a = np.array(a)
        b = np.array(b)
        return float(a @ b / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-10))
```

## 整合的漂移監控系統

```python
class DriftMonitoringSystem:
    def __init__(self, config: dict):
        self.detectors = {}
        self.alerts = []
        self.config = config

    def add_detector(self, name: str, reference_data: np.ndarray,
                     method: str = "psi", threshold: float = 0.2):
        """加入漂移檢測器"""
        if method == "psi":
            self.detectors[name] = PSIDriftDetector(reference_data, threshold)
        elif method == "ks":
            self.detectors[name] = FeatureWiseKSChecker(reference_data, ...)
        elif method == "mmd":
            self.detectors[name] = MMDDriftDetector(reference_data, threshold=threshold)

    def check_all(self, current_data: dict) -> dict:
        """執行所有檢測"""
        results = {}
        for name, detector in self.detectors.items():
            if name in current_data:
                results[name] = detector.check(current_data[name])
                if results[name].get("drifted"):
                    self.alerts.append({
                        "detector": name,
                        "timestamp": np.datetime64('now'),
                        "details": results[name]
                    })
        return results

    def get_alert_summary(self) -> list[dict]:
        """取得最近警報摘要"""
        return self.alerts[-10:] if self.alerts else []
```

## 實戰建議

1. **多方法組合**：PSI 適合單變量、KS 適合統計顯著性、MMD 適合高維資料
2. **設定合理的閾值**：不要過度敏感，建議根據歷史資料設定動態閾值
3. **定期更新基準**：隨著時間推移，緩慢漂移是正常的，需要定期更新參考分布
4. **結合業務指標**：統計上的漂移不一定代表業務影響，需要與實際效能指標關聯
5. **自動補救**：偵測到漂移後自動觸發模型重新訓練、提示詞回滾或流量切換

## 參考資源

- [Drift Detection Algorithms Comparison](https://www.google.com/search?q=data+drift+detection+algorithms+PSI+KS+MMD)
- [Population Stability Index Guide](https://www.google.com/search?q=population+stability+index+guide)
- [MMD for ML Monitoring](https://www.google.com/search?q=maximum+mean+discrepancy+drift+detection+ML)
- [LLM Output Drift Detection](https://www.google.com/search?q=LLM+output+drift+detection+monitoring)
