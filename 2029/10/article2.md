# 公平性指標計算：量化 AI 模型的社會影響

## 前言

公平性不是非黑即白的問題。不同的公平性定義可能彼此衝突，選擇合適的指標需要深入理解業務場景和法律要求。本文介紹最常用的公平性指標及其 Python 實現。

## 統計均差異（Statistical Parity Difference）

要求各群體的被接受率相等。

```python
import numpy as np

def statistical_parity(y_pred, sensitive):
    groups = np.unique(sensitive)
    rates = {}
    for g in groups:
        mask = sensitive == g
        rates[g] = y_pred[mask].mean()
    return rates[groups[0]] - rates[groups[1]]

y_pred = np.array([1, 0, 1, 1, 0, 1, 0, 0])
sensitive = np.array(['A', 'A', 'A', 'B', 'B', 'B', 'B', 'B'])
print(f"統計均差異: {statistical_parity(y_pred, sensitive):.4f}")
```

## 均等機會差異（Equal Opportunity Difference）

關注真正率的群體差異。

```python
def equal_opportunity(y_true, y_pred, sensitive):
    groups = np.unique(sensitive)
    tpr = {}
    for g in groups:
        mask = (sensitive == g) & (y_true == 1)
        if mask.sum() > 0:
            tpr[g] = y_pred[mask].mean()
        else:
            tpr[g] = 0
    return abs(tpr[groups[0]] - tpr[groups[1]])

y_true = np.array([1, 0, 1, 1, 0, 1, 0, 1])
print(f"均等機會差異: {equal_opportunity(y_true, y_pred, sensitive):.4f}")
```

## 不利影響比（Disparate Impact）

衡量群體間的選擇率比值，低於 0.8 通常被視為有不利影響。

```python
def disparate_impact(y_pred, sensitive):
    groups = np.unique(sensitive)
    rates = {}
    for g in groups:
        mask = sensitive == g
        rates[g] = y_pred[mask].mean()
    ratio = rates[groups[1]] / rates[groups[0]]
    return min(ratio, 1/ratio)

print(f"不利影響比: {disparate_impact(y_pred, sensitive):.4f}")
```

## 結語

沒有一個通用指標能涵蓋所有公平性面向。實務上應同時監控多個指標，並根據應用場景選擇最合適的定義組合。

---

**延伸閱讀**

- [公平性定義分類](https://www.google.com/search?q=fairness+definitions+machine+learning+classification)
- [Disparate Impact 法律標準](https://www.google.com/search?q=disparate+impact+legal+standard+80+percent+rule)
- [Equal Opportunity 論文](https://www.google.com/search?q=equal+opportunity+fairness+Hardt+2016)
