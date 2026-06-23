# SHAP 深入解析：從 Shapley Value 到模型可解釋性

## 前言

SHAP（SHapley Additive exPlanations）已成為 2026 年最廣泛使用的模型可解釋性框架。它源自合作賽局理論的 Shapley Value，將每個特徵視為「玩家」，預測結果視為「收益」，公平分配功勞。

## Shapley Value 的直覺

想像三個特徵共同預測了房價：臥室數、地點、坪數。Shapley Value 的核心思想是：計算每個特徵在所有可能特徵組合中的邊際貢獻平均值。

```python
import itertools
import numpy as np

def shapley_value(features: list, model, x: dict) -> dict:
    """Compute exact Shapley values for a prediction."""
    n = len(features)
    values = {f: 0.0 for f in features}

    for f in features:
        marginal_sum = 0.0
        count = 0
        other_features = [g for g in features if g != f]
        for size in range(n):
            for subset in itertools.combinations(other_features, size):
                set_with = set(subset) | {f}
                set_without = set(subset)
                x_with = {k: x[k] for k in set_with}
                x_without = {k: x[k] for k in set_without}
                pred_with = model(x_with)
                pred_without = model(x_without)
                marginal_sum += pred_with - pred_without
                count += 1
        values[f] = marginal_sum / count
    return values


def dummy_model(x: dict) -> float:
    base = 100
    weights = {"bedrooms": 30, "location": 50, "sqft": 0.05}
    return base + sum(weights.get(k, 0) * v for k, v in x.items())


x = {"bedrooms": 3, "location": 8, "sqft": 1500}
sv = shapley_value(list(x.keys()), dummy_model, x)
for f, v in sv.items():
    print(f"SHAP[{f}] = {v:.2f}")
```

## SHAP 的數學性質

SHAP 滿足三個關鍵公理，使其成為唯一的 additive feature attribution 方法：

- **局部準確性（Local Accuracy）**：特徵貢獻值加總等於預測值減去基準值。
- **缺失性（Missingness）**：缺失特徵的貢獻值為零。
- **一致性（Consistency）**：若某特徵對模型的重要性不減，其 SHAP 值不會下降。

## KernelSHAP 實作

當特徵數量過多時，精確計算不可行，KernelSHAP 透過加權線性回歸逼近：

```python
import random
import numpy as np
from sklearn.linear_model import Ridge


def kernelshap_explain(model, x: dict, background: list[dict],
                       n_samples: int = 1000) -> dict:
    features = list(x.keys())
    m = len(features)
    X_simplified = []
    y_preds = []

    for _ in range(n_samples):
        z = [random.randint(0, 1) for _ in range(m)]
        x_hybrid = {}
        for j, f in enumerate(features):
            if z[j] == 1:
                x_hybrid[f] = x[f]
            else:
                x_hybrid[f] = random.choice(background)[f]
        X_simplified.append(z)
        y_preds.append(model(x_hybrid))

    X_arr = np.array(X_simplified)
    y_arr = np.array(y_preds)
    # Kernel weights: SHAP kernel
    kernel_weights = []
    for z in X_arr:
        r = sum(z)
        if r == 0 or r == m:
            kernel_weights.append(1e6)
        else:
            kernel_weights.append((m - 1) / (r * (m - r)))
    W = np.diag(kernel_weights)

    reg = Ridge(alpha=1.0, fit_intercept=True)
    reg.fit(X_arr, y_arr, sample_weight=kernel_weights)

    result = {}
    for j, f in enumerate(features):
        result[f] = reg.coef_[j]
    result["base"] = reg.intercept_
    return result


background = [{"bedrooms": 2, "location": 5, "sqft": 1000},
              {"bedrooms": 4, "location": 9, "sqft": 2000}]
explanation = kernelshap_explain(dummy_model, x, background)
for f, v in explanation.items():
    print(f"{f}: {v:.2f}")
```

## SHAP 在 2026 年的實踐趨勢

- **TreeSHAP**：對 XGBoost/LightGBM 的專用加速，O(TLDM) 複雜度。
- **DeepSHAP**：神經網路的 DeepLIFT 近似，利用反向傳播計算。
- **SHAP 儀表板**：`shap` 套件內建視覺化，支援瀑布圖、力圖、依賴圖。

## 結語

SHAP 之所以成為 XAI 的標竿，在於它將博弈論的嚴謹性與機器學習的實用性完美結合。理解 Shapley Value 的計算本質，才能在實際應用中正確解讀 SHAP 圖表，避免誤用。

---

**延伸閱讀**
- [SHAP 官方文件](https://www.google.com/search?q=SHAP+SHapley+Additive+exPlanations+Python)
- [Shapley Value 博弈論原理解說](https://www.google.com/search?q=Shapley+value+game+theory+explanation)
- [TreeSHAP 論文](https://www.google.com/search?q=TreeSHAP+explainable+AI+paper)
