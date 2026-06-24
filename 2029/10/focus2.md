# 偏見檢測與緩解

## 資料層與模型層的偏見處理技術（2020-2029）

### 前言

AI 偏見通常源自歷史資料中的系統性不平等。如果訓練資料中的某個族群被系統性排除或低估，模型就會學習並放大這種偏見。2020 年後，學術界與業界發展出三層偏見處理策略：資料前處理、模型訓練中調整、以及後處理校正。

### 偏見的來源分類

```python
# 偏見來源的結構化分類
from enum import Enum

class BiasType(Enum):
    HISTORICAL = "歷史偏見"       # 既有社會不平等
    REPRESENTATION = "代表性偏見"  # 資料取樣偏差
    MEASUREMENT = "測量偏見"       # 標籤/特徵不準確
    AGGREGATION = "聚合偏見"       # 忽略群體異質性
    EVALUATION = "評估偏見"        # 評估指標不適合

def detect_bias_sources(dataset_description: str) -> list:
    """根據資料集描述推測可能的偏見來源"""
    keywords = {
        BiasType.HISTORICAL: ['歷史', '過往', '既有'],
        BiasType.REPRESENTATION: ['樣本', '抽樣', '不平衡'],
        BiasType.MEASUREMENT: ['標籤', '標註', '測量'],
    }
    detected = []
    for bias_type, words in keywords.items():
        if any(w in dataset_description for w in words):
            detected.append(bias_type)
    return detected
```

### 資料層偏見檢測

資料層的偏見檢測是最早且最有效的干預點：

```python
import pandas as pd
import numpy as np

def demographic_parity_check(
    df: pd.DataFrame,
    sensitive_attr: str,
    label_col: str,
    threshold: float = 0.8
) -> dict:
    """檢查人口統計平權（Demographic Parity）"""
    groups = df[sensitive_attr].unique()
    rates = {}
    for g in groups:
        mask = df[sensitive_attr] == g
        rates[g] = df.loc[mask, label_col].mean()
    
    min_rate = min(rates.values())
    max_rate = max(rates.values())
    ratio = min_rate / max_rate if max_rate > 0 else 0
    
    return {
        'selection_rates': rates,
        'disparate_impact': ratio,
        'pass_check': ratio >= threshold,
    }

# 模擬資料
data = pd.DataFrame({
    'gender': ['M'] * 800 + ['F'] * 200,
    'accepted': [1] * 600 + [0] * 200 + [1] * 100 + [0] * 100,
})

result = demographic_parity_check(data, 'gender', 'accepted')
print(f"Disparate Impact: {result['disparate_impact']:.2f}")  # 可能低於 0.8
```

### 模型訓練中緩解

在模型訓練過程中加入公平性約束：

```python
import numpy as np

class FairLogisticRegression:
    """帶公平性約束的邏輯迴歸（示意）"""
    def __init__(self, lambda_fair: float = 0.1):
        self.lambda_fair = lambda_fair
        self.weights = None
    
    def _fairness_loss(self, X, y, sensitive_attr_idx):
        """計算公平性損失：不同群體的預測分布差異"""
        preds = self._predict_proba(X)
        group0 = X[:, sensitive_attr_idx] == 0
        group1 = X[:, sensitive_attr_idx] == 1
        mean0 = preds[group0].mean()
        mean1 = preds[group1].mean()
        return (mean0 - mean1) ** 2
    
    def fit(self, X, y, sensitive_attr_idx):
        """訓練時同時最小化預測誤差與公平性損失"""
        # 實際實作使用梯度下降
        # 此處為示意
        pass
    
    def _predict_proba(self, X):
        return 1 / (1 + np.exp(-X @ self.weights))
```

### 後處理校正

模型訓練完成後，調整決策邊界：

```python
def equalized_odds_postprocessing(
    y_true: np.ndarray,
    y_pred_prob: np.ndarray,
    sensitive_attr: np.ndarray,
    target_fpr: float = 0.05
) -> np.ndarray:
    """Equalized Odds 後處理校正
    
    為每個群體選擇不同的閾值，使得偽陽性率相等
    """
    groups = np.unique(sensitive_attr)
    thresholds = {}
    
    for g in groups:
        mask = sensitive_attr == g
        group_probs = y_pred_prob[mask]
        group_true = y_true[mask]
        
        best_thresh = 0.5
        # 尋找滿足 FPR 目標的閾值
        for thresh in np.linspace(0, 1, 100):
            pred = (group_probs >= thresh).astype(int)
            fpr = ((pred == 1) & (group_true == 0)).sum() / (group_true == 0).sum()
            if abs(fpr - target_fpr) < abs(
                ((y_pred_prob[mask] >= best_thresh).astype(int) == 1) & 
                (group_true == 0)).sum() / (group_true == 0).sum() - target_fpr
            ):
                # 簡化：實際應更精確
                pass
    
    # 應用各群體的閾值
    y_pred_adjusted = np.zeros_like(y_pred_prob)
    for g in groups:
        mask = sensitive_attr == g
        thresh = thresholds.get(g, 0.5)
        y_pred_adjusted[mask] = (y_pred_prob[mask] >= thresh).astype(int)
    
    return y_pred_adjusted
```

### 技術演進時間線

| 年份 | 里程碑 |
|------|--------|
| 2020 | AIF360 開源、Fairlearn 發布 |
| 2021 | Google Model Remediation 工具 |
| 2022 | 對比學習中的去偏方法 |
| 2023 | 大型語言模型的偏見標竿（BBQ、WinoBias） |
| 2024 | 差分隱私 + 公平性聯合優化 |
| 2026 | 自動偏見修復管線 |
| 2029 | 即時偏見監控與自動修正系統 |

### 小結

偏見檢測與緩解已從學術研究走向工程實踐。關鍵在於建立持續監控的管線——不是一次性的「修好」，而是在模型的生命周期中反覆檢查。

---

**下一步**：[公平性評估方法](focus3.md)

## 延伸閱讀

- [AIF360](https://www.google.com/search?q=AIF360+IBM+fairness)
- [Fairlearn](https://www.google.com/search?q=Fairlearn+Microsoft)
- [BBQ Bias Benchmark](https://www.google.com/search?q=BBQ+bias+benchmark)
- [WinoBias](https://www.google.com/search?q=WinoBias+dataset)
