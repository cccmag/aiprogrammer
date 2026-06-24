# LIME 與局部解釋：信任單一預測

## 前言

當銀行拒絕你的貸款申請、AI 診斷系統判你為高風險——你需要知道「為什麼」。LIME（Local Interpretable Model-agnostic Explanations）正是為此而生：它在單一預測點的鄰近區域訓練一個簡單的可解釋模型，模擬黑箱模型的行為。

## LIME 的核心思想

與 SHAP 從博弈論出發不同，LIME 的邏輯更直觀：在一個預測點 x 附近，取樣一組擾動點，用它們的預測值訓練一個線性模型或決策樹，然後解釋這個「局部代理模型」。

```python
import numpy as np
import random
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler


def lime_explain(model, x: dict, n_samples: int = 5000,
                 kernel_width: float = 0.75) -> dict:
    features = list(x.keys())
    n_features = len(features)

    # 1. Generate perturbed samples
    perturbations = []
    original = np.array([x[f] for f in features])
    for _ in range(n_samples):
        noise = np.random.normal(0, kernel_width, n_features)
        perturbed = original + noise * np.abs(original + 1e-8)
        perturbations.append(perturbed)
    perturbations = np.array(perturbations)

    # 2. Get model predictions
    preds = []
    for p in perturbations:
        x_p = {features[j]: p[j] for j in range(n_features)}
        preds.append(model(x_p))
    preds = np.array(preds)

    # 3. Compute exponential kernel weights (distance to original)
    distances = np.sqrt(((perturbations - original) ** 2).sum(axis=1))
    weights = np.exp(-(distances ** 2) / (kernel_width ** 2))

    # 4. Train interpretable ridge regression
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(perturbations)
    reg = Ridge(alpha=1.0)
    reg.fit(X_scaled, preds, sample_weight=weights)

    # 5. Return feature coefficients (in original space)
    coefs = {}
    for j, f in enumerate(features):
        coefs[f] = reg.coef_[j] / scaler.scale_[j]
    coefs["intercept"] = reg.intercept_
    coefs["r2"] = reg.score(X_scaled, preds, sample_weight=weights)
    return coefs


def dummy_classifier(x: dict) -> float:
    """Simulate a loan approval model."""
    score = 0.3 * x.get("income", 0) / 100000
    score += 0.2 * min(x.get("credit_score", 0) / 800, 1.0)
    score -= 0.1 * x.get("debt_ratio", 0)
    score -= 0.05 * x.get("late_payments", 0)
    return max(0.0, min(1.0, score))


x_instance = {"income": 85000, "credit_score": 720,
              "debt_ratio": 0.35, "late_payments": 1}
explanation = lime_explain(dummy_classifier, x_instance)

print("LIME Explanation:")
for f, c in sorted(explanation.items(), key=lambda t: -abs(t[1])):
    print(f"  {f}: {c:+.4f}")
print(f"\nModel local R²: {explanation['r2']:.3f}")
```

## LIME 的超參數選擇

LIME 的結果高度依賴兩個參數：

- **擾動幅度（kernel_width）**：決定「局部」的範圍。太小則模型不穩定，太大則代理模型無法捕捉局部非線性。
- **樣本數量（n_samples）**：至少需要特徵數的 10 倍，否則線性回歸容易過擬合。

實務上建議對不同 kernel_width 進行敏感度分析，觀察解釋的穩定性。

## LIME vs SHAP 的關鍵差異

| 面向 | LIME | SHAP |
|------|------|------|
| 理論基礎 | 局部代理模型 | Shapley Value |
| 計算速度 | 較快（線性回歸） | 較慢（需枚舉特徵組合） |
| 一致性 | 無保證（對擾動敏感） | 滿足一致性公理 |
| 可解釋性 | 係數直觀 | 需理解基準值概念 |
| 適用場景 | 快速除錯、互動探索 | 法規報告、嚴謹歸因 |

## 2026 年的 LIME 生態

LIME 的原始論文（Ribeiro et al., 2016）已累積超過兩萬次引用。2026 年的改進方向包括：

- **TabularLIME**：專門為表格式資料設計的變體，內建類別變數處理。
- **SP-LIME**：選擇代表性解釋的子模組化最佳化，解決多實例解釋的冗餘問題。
- **LIME with Do-Calculus**：最新研究將干預概念引入局部解釋，讓 LIME 不只解釋「模型看到什麼」，更解釋「如果改變特徵會怎樣」。

## 結語

LIME 的價值在於它的模型不可知（model-agnostic）特性——無論是隨機森林還是千層 Transformer，LIME 都能給出人類可讀的解釋。但它的不穩定性也是一把雙面刃：同一個預測點在不同擾動下可能產生不同解釋。因此，LIME 最適合用於探索性分析，而正式報告則建議以 SHAP 為輔助驗證。

---

**延伸閱讀**
- [LIME 原始論文 - Ribeiro et al.](https://www.google.com/search?q=LIME+local+interpretable+model+agnostic+explanations)
- [LIME Python 套件](https://www.google.com/search?q=LIME+Python+library+github)
- [LIME vs SHAP 對比分析](https://www.google.com/search?q=LIME+vs+SHAP+explainable+AI+comparison)
