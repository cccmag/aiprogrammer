# 反事實解釋方法：如果世界不是這樣

## 前言

「如果我多念一年書，薪水會多多少？」「如果我的信用分數再高 30 分，貸款會通過嗎？」這些問題的核心就是反事實推理（Counterfactual Reasoning）——在給定事實觀測的條件下，回答「如果…會怎樣」的問題。

反事實解釋是 XAI 中最接近人類思考模式的方法。它不是描述模型內部的權重，而是在數據空間中尋找最小的變更，使模型改變其預測。

## 反事實解釋的數學定義

給定模型 f 和輸入 x₀，我們想找到一個反事實 x'，滿足：

x' = argmin d(x', x₀)  使得 f(x') = y' ≠ f(x₀)

其中 d 是距離函數（通常為加權 L1 或 L2），y' 是目標類別。換句話說：找到最接近的輸入點，使模型給出不同的預測。

## Python 實作：基於梯度最佳化的反事實搜尋

```python
import numpy as np
from typing import Callable, Optional


def counterfactual_search(
    model: Callable,
    x0: np.ndarray,
    target_pred: float,
    feature_names: list[str],
    feature_ranges: Optional[dict[str, tuple]] = None,
    lr: float = 0.01,
    n_steps: int = 1000,
    lambda_l1: float = 0.01,
) -> tuple[np.ndarray, dict]:
    """Find counterfactual via gradient-free optimization."""
    x_current = x0.copy()
    best_x = x_current.copy()
    best_dist = float("inf")
    history = []

    for step in range(n_steps):
        # Random perturbation
        delta = np.random.randn(len(x0)) * lr
        candidate = x_current + delta

        # Clamp to feature ranges
        if feature_ranges:
            for i, name in enumerate(feature_names):
                if name in feature_ranges:
                    lo, hi = feature_ranges[name]
                    candidate[i] = np.clip(candidate[i], lo, hi)

        pred = model(candidate)
        dist = np.sum((candidate - x0) ** 2)
        obj = (pred - target_pred) ** 2 + lambda_l1 * dist

        if obj < best_dist:
            best_dist = obj
            best_x = candidate.copy()

        x_current = (x_current + candidate) / 2

    cf_dict = {feature_names[i]: best_x[i] for i in range(len(feature_names))}
    return best_x, cf_dict


def loan_model(x: np.ndarray) -> float:
    income, credit, debt, late = x
    score = (0.3 * income / 100000 + 0.2 * credit / 800
             - 0.1 * debt - 0.05 * late)
    return float(np.clip(score, 0, 1))


names = ["income", "credit_score", "debt_ratio", "late_payments"]
x_factual = np.array([85000, 720, 0.35, 1])
ranges = {"income": (20000, 200000), "credit_score": (300, 850),
          "debt_ratio": (0, 1), "late_payments": (0, 10)}

print("Factual input:", dict(zip(names, x_factual)))
print(f"Factual prediction: {loan_model(x_factual):.3f}")

x_cf, cf_dict = counterfactual_search(
    loan_model, x_factual, target_pred=0.8,
    feature_names=names, feature_ranges=ranges
)
print("\nCounterfactual (target: 0.8):")
for f, v in cf_dict.items():
    change = v - dict(zip(names, x_factual))[f]
    print(f"  {f}: {v:.0f} ({change:+.0f})")
print(f"Counterfactual prediction: {loan_model(x_cf):.3f}")
```

## 最小變更原則與可行動性

實務中，「最小變更」不等於「最有用」。一個優秀的反事實解釋應滿足：

1. **可行性**：建議的變更必須是個人能採取的行動（例如「增加學歷」可行，「改變年齡」不可行）。
2. **稀疏性**：最好只改變少數特徵，否則解釋失去實用性。
3. **多樣性**：提供多組反事實，讓使用者有選擇空間。

```python
def diverse_counterfactuals(model, x0, target_pred, n_cf=5):
    """Generate diverse counterfactuals."""
    cfs = []
    for seed in range(n_cf * 10):
        np.random.seed(seed)
        x_cf, _ = counterfactual_search(
            model, x0, target_pred,
            feature_names=names, feature_ranges=ranges,
            lr=0.02, n_steps=500
        )
        if abs(model(x_cf) - target_pred) < 0.05:
            # Check diversity
            is_diverse = True
            for existing in cfs:
                if np.linalg.norm(x_cf - existing) < 0.1 * len(x0):
                    is_diverse = False
                    break
            if is_diverse:
                cfs.append(x_cf)
                if len(cfs) >= n_cf:
                    break
    return cfs
```

## 反事實解釋的理論保證

Wachter et al.（2017）提出了反事實解釋的三個要求：**接近性**（與事實點相近）、**有效性**（確實改變預測）、**可理解性**（人類可以理解）。2026 年的最新研究加入了**因果約束**——反事實變更必須遵循因果圖的結構，而不是任意方向的最佳化。

## 結語

反事實解釋是 XAI 中最人性化的方法——它直接回答「我該怎麼做才能得到不同的結果？」。從金融貸款被拒後的改善建議，到醫療診斷中的「如果早點治療」，反事實推理正在讓 AI 從評判者轉變為顧問。

---

**延伸閱讀**
- [Wachter et al. - Counterfactual Explanations](https://www.google.com/search?q=Wachter+counterfactual+explanations+without+opening+the+black+box)
- [反事實推理在因果 AI 中的角色](https://www.google.com/search?q=counterfactual+reasoning+causal+AI+explainability)
- [DiCE - Diverse Counterfactual Explanations](https://www.google.com/search?q=DiCE+diverse+counterfactual+explanations+Python)
