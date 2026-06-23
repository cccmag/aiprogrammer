# 偏見檢測與緩解

## AIF360、Fairlearn、對抗性去偏（2020-2029）

### 前言

2020 年，IBM 的 AIF360 與微軟的 Fairlearn 相繼開源，標誌著偏見檢測工具化的開始。偏見可能來自訓練資料、標註過程或模型演算法本身——如果不及時檢測，AI 系統就會在現實世界中放大既有不平等。

### 偏見的來源

```python
# 模擬三種偏見來源
import numpy as np

class BiasAuditor:
    def __init__(self, sensitive_attr: str):
        self.sensitive_attr = sensitive_attr

    def data_bias_check(self, data: np.ndarray, labels: np.ndarray, group_col: int):
        """檢查資料集中的代表性偏見"""
        groups = np.unique(data[:, group_col])
        ratios = {}
        for g in groups:
            mask = data[:, group_col] == g
            ratios[f"group_{g}"] = mask.sum() / len(data)
        return ratios

    def label_bias_check(self, labels: np.ndarray, groups: np.ndarray):
        """檢查標籤分配是否偏頗"""
        results = {}
        for g in np.unique(groups):
            mask = groups == g
            pos_rate = labels[mask].mean()
            results[f"group_{g}_positive_rate"] = float(pos_rate)
        return results
```

### 對抗性去偏（Adversarial Debiasing）

對抗性去偏的核心想法：讓主模型專注於預測任務，同時讓對抗網路無法從主模型的特徵中推斷出敏感屬性。

```python
# 簡化的對抗性去偏框架
import torch
import torch.nn as nn

class AdversarialDebiaser:
    def __init__(self, input_dim: int, hidden_dim: int = 64):
        self.predictor = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, 1),
            nn.Sigmoid(),
        )
        self.adversary = nn.Sequential(
            nn.Linear(hidden_dim, 32),
            nn.ReLU(),
            nn.Linear(32, 1),
            nn.Sigmoid(),
        )

    def train_step(self, x, y, sensitive, lambda_adv=0.5):
        pred = self.predictor(x)
        hidden = self.predictor[:-2](x)  # 取倒數第二層作為特徵
        adv_pred = self.adversary(hidden.detach())

        pred_loss = nn.BCELoss()(pred, y)
        adv_loss = nn.BCELoss()(adv_pred, sensitive)
        total_loss = pred_loss - lambda_adv * adv_loss

        return total_loss
```

對抗訓練的目標是最小化 `pred_loss - λ × adv_loss`——當對抗網路無法猜出敏感屬性時，表示主模型的特徵已去除偏見。

### 偏見檢測工具比較

| 工具 | 發布 | 語言 | 核心功能 |
|------|------|------|---------|
| AIF 360 | 2020 | Python | 70+ 公平性指標 + 10+ 緩解演算法 |
| Fairlearn | 2020 | Python | 群體公平性 + 個體公平性 |
| What-If Tool | 2019 | 網頁 | 互動式偏見視覺化 |
| SHAP | 2017 | Python | 特徵貢獻分析 |

### 2025 年的進展

2025 年，大型語言模型的偏見檢測成為熱點。研究發現 LLM 在醫療問答中對特定族群的建議存在系統性差異，催生了「即時偏見監控」的需求——在模型推論的同時檢測輸出偏差。

---

**下一步**：[公平性評估方法](focus3.md)

## 延伸閱讀

- [IBM AIF 360](https://www.google.com/search?q=AIF360+IBM+fairness)
- [Microsoft Fairlearn](https://www.google.com/search?q=Fairlearn+Microsoft)
- [Adversarial Debiasing](https://www.google.com/search?q=adversarial+debiasing+fairness)
