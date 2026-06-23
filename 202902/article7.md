# 合成資料品質指標

## 1. 引言

合成資料的品質直接決定了它的實用價值。然而「品質」是一個多維度的概念——一組機器學習模型能用的合成資料，可能對統計分析完全無用。本文介紹系統性的合成資料品質評估指標與 Python 實作。

## 2. 品質評估的三個維度

合成資料品質可從三個面向檢視：

- **保真度（Fidelity）**：合成資料與真實資料的相似程度
- **多樣性（Diversity）**：合成資料的變異程度
- **隱私性（Privacy）**：合成資料是否洩漏原始資訊

## 3. 保真度指標

```python
import numpy as np
from scipy.stats import wasserstein_distance, ks_2samp

def fidelity_metrics(real: np.ndarray, synthetic: np.ndarray) -> dict:
    wass = [wasserstein_distance(real[:, i], synthetic[:, i])
            for i in range(real.shape[1])]
    ks = [ks_2samp(real[:, i], synthetic[:, i])[0]
          for i in range(real.shape[1])]
    corr_diff = np.mean(np.abs(np.corrcoef(real.T) - np.corrcoef(synthetic.T)))
    return {"wasserstein": np.mean(wass), "ks": np.mean(ks),
            "correlation": 1 - corr_diff}
```

## 4. 多樣性指標

```python
from sklearn.neighbors import NearestNeighbors

def diversity_metrics(real: np.ndarray, synthetic: np.ndarray) -> dict:
    nn_r = NearestNeighbors(n_neighbors=1).fit(real)
    d_s2r, _ = nn_r.kneighbors(synthetic)
    nn_s = NearestNeighbors(n_neighbors=1).fit(synthetic)
    d_r2s, _ = nn_s.kneighbors(real)
    return {"coverage": float(np.mean(d_s2r < np.percentile(d_s2r, 5))),
            "novelty": float(np.mean(d_r2s > np.percentile(d_r2s, 95)))}
```

## 5. 隱私風險指標

```python
def privacy_metrics(real: np.ndarray, synthetic: np.ndarray) -> dict:
    nn_r = NearestNeighbors(n_neighbors=2).fit(real)
    nn_s = NearestNeighbors(n_neighbors=1).fit(synthetic)
    d_r2s, _ = nn_s.kneighbors(real)
    _, indices = nn_r.kneighbors(real)
    d_r2r = nn_r.kneighbors(real)[0][:, 1]
    ndr = np.mean(d_r2s.flatten() / (d_r2r + 1e-8))
    return {"ndr": float(ndr), "membership_inference": float(np.mean(d_r2s < d_r2r))}
```

## 6. 綜合評分

```python
def overall_score(m: dict) -> float:
    w = {"wasserstein": -0.3, "ks": -0.2, "correlation": 0.2,
         "coverage": 0.1, "novelty": 0.1, "ndr": 0.1}
    score = sum(w[k] * min(m.get(k, 0), 1) if w[k] > 0
                else w[k] * m.get(k, 0) for k in w)
    return max(0.0, min(1.0, score))
```

## 7. 結語

合成資料品質評估需要在保真度、多樣性與隱私性之間取得平衡。沒有任何單一指標能完整描述品質，建議建立自動化儀表板同時追蹤多項指標。

## 延伸閱讀

- [Synthetic Data Quality Framework](https://www.google.com/search?q=synthetic+data+quality+metrics+framework)
- [Membership Inference Attacks](https://www.google.com/search?q=membership+inference+attack+machine+learning)
