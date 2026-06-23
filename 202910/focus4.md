# 透明度與可解釋性報告

## SHAP、LIME、Model Cards（2023-2029）

### 可解釋性的三個層次

AI 可解釋性可分為三個層次：**全局解釋**（模型整體邏輯）、**局部解釋**（單個預測原因）、**反事實解釋**（改變哪些輸入會改變結果）。

### SHAP（SHapley Additive exPlanations）

SHAP 基於賽局理論的 Shapley 值，計算每個特徵對預測的邊際貢獻：

```python
import numpy as np

class ShapExplainer:
    def __init__(self, model, background_data: np.ndarray):
        self.model = model
        self.background = background_data  # 背景資料集

    def _predict(self, x):
        return self.model(x)

    def explain(self, instance: np.ndarray, n_samples: int = 1000) -> dict:
        """近似計算每個特徵的 SHAP 值"""
        n_features = instance.shape[0]
        shap_values = np.zeros(n_features)

        for _ in range(n_samples):
            bg_sample = self.background[np.random.randint(0, len(self.background))]
            mask = np.random.binomial(1, 0.5, size=n_features)

            with_features = instance * mask + bg_sample * (1 - mask)
            without_feature = instance.copy()
            j = np.random.randint(0, n_features)
            without_feature[j] = bg_sample[j]

            pred_with = self._predict(with_features.reshape(1, -1))
            pred_without = self._predict(without_feature.reshape(1, -1))
            shap_values[j] += float(pred_with - pred_without)

        shap_values /= n_samples
        return dict(zip([f"f{i}" for i in range(n_features)], shap_values))
```

### LIME（Local Interpretable Model-agnostic Explanations）

LIME 在預測點附近訓練一個簡單的可解釋模型（如線性迴歸）來近似局部決策邊界：

```python
from sklearn.linear_model import Ridge

class LimeExplainer:
    def __init__(self, model, kernel_width: float = 0.75):
        self.model = model
        self.kernel_width = kernel_width

    def explain(self, instance: np.ndarray, n_perturb: int = 500) -> list:
        n_features = instance.shape[0]
        perturbations = np.random.normal(0, 0.1, (n_perturb, n_features))
        distances = np.linalg.norm(perturbations, axis=1)
        weights = np.exp(-distances**2 / self.kernel_width**2)

        samples = instance + perturbations
        preds = self.model(samples)

        linear = Ridge(alpha=1.0)
        linear.fit(samples, preds, sample_weight=weights)

        coefs = linear.coef_.flatten() if len(linear.coef_.shape) > 1 else linear.coef_
        return sorted(
            [(f"f{i}", float(coefs[i])) for i in range(n_features)],
            key=lambda x: abs(x[1]), reverse=True
        )
```

### Model Cards 透明度報告

Google 在 2019 年提出 Model Cards 概念——每一張 Model Card 就像 AI 模型的身份證：

```python
# Model Card 生成器
class ModelCard:
    def __init__(self, name: str, version: str):
        self.card = {
            "model_details": {"name": name, "version": version},
            "intended_use": "",
            "training_data": {},
            "evaluation": {},
            "fairness": {},
            "limitations": "",
        }

    def add_fairness_report(self, metrics: dict):
        self.card["fairness"] = {
            "demographic_parity": metrics.get("dp", "N/A"),
            "equal_opportunity": metrics.get("eo", "N/A"),
            "equalized_odds": metrics.get("eodds", "N/A"),
        }

    def generate_report(self) -> str:
        lines = [f"# Model Card: {self.card['model_details']['name']}"]
        for section, content in self.card.items():
            if isinstance(content, dict):
                lines.append(f"\n## {section}")
                for k, v in content.items():
                    lines.append(f"- **{k}**: {v}")
            elif content:
                lines.append(f"\n## {section}\n{content}")
        return "\n".join(lines)
```

### 2025 年的透明度標準

歐盟 AI Act 要求高風險 AI 系統提供「有意義的解釋」，但什麼算「有意義」仍在討論中。Google DeepMind 在 2025 年提出「可解釋性的分級標準」：Level 1（黑箱）到 Level 5（完全可理解），為法規提供了參考框架。

---

**下一步**：[AI 問責機制](focus5.md)

## 延伸閱讀

- [SHAP 論文](https://www.google.com/search?q=SHAP+unified+approach+explain)
- [LIME 論文](https://www.google.com/search?q=LIME+local+interpretable+explanations)
- [Model Cards](https://www.google.com/search?q=Model+Cards+Google+AI)
