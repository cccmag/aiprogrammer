# 合成資料與模型偏見

## 1. 引言

合成資料看似是解決公平性問題的良方——理論上，我們可以生成平衡的資料集來補足弱勢群體的樣本。然而合成資料也可能反過來放大偏見。如果生成模型本身就帶有偏見，那麼合成資料只會讓偏見蔓延。本文探討這個雙面刃問題。

## 2. 偏見的來源

合成資料中的偏見可能來自三個層面：

- **原始資料偏見**：訓練生成模型的真實資料本身就不平衡
- **生成模型偏見**：模型架構與訓練過程引入的偏差
- **使用方式偏見**：不當的取樣或過濾策略

## 3. 偏見偵測工具

```python
import numpy as np
import pandas as pd

class BiasDetector:
    """偵測合成資料中的群體偏差"""
    def __init__(self, sensitive_attrs: list[str]):
        self.sensitive_attrs = sensitive_attrs

    def compute_demographic_parity(self,
                                   data: pd.DataFrame,
                                   prediction_col: str) -> dict:
        """計算人口統計平穩性"""
        results = {}
        for attr in self.sensitive_attrs:
            groups = data.groupby(attr)[prediction_col]
            pos_rates = groups.mean()
            max_diff = pos_rates.max() - pos_rates.min()
            results[f"{attr}_disparity"] = max_diff
        return results

    def compute_equalized_odds(self,
                               data: pd.DataFrame,
                               prediction_col: str,
                               label_col: str) -> dict:
        """計算均等化概率"""
        results = {}
        for attr in self.sensitive_attrs:
            for label in [0, 1]:
                subset = data[data[label_col] == label]
                groups = subset.groupby(attr)[prediction_col]
                tpr = groups.mean()
                max_diff = tpr.max() - tpr.min()
                results[f"{attr}_label_{label}_disparity"] = max_diff
        return results

```

## 4. 去偏見合成策略

去偏見取樣透過控制生成樣本的群體分佈來達到公平性目標：

```python
def reweight_loss(logits, labels, sensitive_attr, group_weights):
    ce = torch.nn.functional.cross_entropy(logits, labels, reduction="none")
    w = torch.tensor([group_weights[a.item()] for a in sensitive_attr])
    return (ce * w).mean()
```

## 5. 反事實合成

反事實合成（Counterfactual Synthesis）翻轉敏感屬性值來生成公平性訓練資料。例如將性別從男改為女，同時保持其他特徵不變，然後用因果模型預測新的標籤。

## 6. 結語

合成資料不是偏見的萬靈丹。如果不謹慎處理，它反而會成為偏見的放大器。最佳做法是：在生成前分析原始偏見來源，生成中使用去偏見取樣策略，生成後持續監控公平性指標。

## 延伸閱讀

- [Fairness in Machine Learning](https://www.google.com/search?q=fairness+machine+learning+disparate+impact)
- [Counterfactual Fairness](https://www.google.com/search?q=counterfactual+fairness+machine+learning)
