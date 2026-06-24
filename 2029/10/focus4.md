# 透明度與可解釋性報告

## SHAP、LIME、Model Cards 實戰（2023-2029）

### 前言

當 AI 系統做出影響人生的決定——貸款審核、疾病診斷、求職篩選——使用者有權知道「為什麼」。可解釋性 AI（XAI）正是為此而生。2023 年以來，解釋性方法從學術工具演變為法規要求。

### SHAP：基於合作賽局理論的解釋

SHAP（SHapley Additive exPlanations）是目前最理論完備的解釋方法：

```python
import numpy as np
import pandas as pd

class SimpleShapExplainer:
    """簡化版 SHAP 解釋器（示意核心概念）"""
    
    def __init__(self, model, X_train: np.ndarray):
        self.model = model
        self.X_train = X_train
        self.base_value = X_train.mean(axis=0)
    
    def _predict(self, X):
        return self.model.predict(X)
    
    def explain(self, x: np.ndarray) -> dict:
        """計算每個特徵的 SHAP 值
        
        SHAP 值 = 該特徵對預測的邊際貢獻
        """
        n_features = len(x)
        shap_values = np.zeros(n_features)
        
        for i in range(n_features):
            # 模擬：特徵 i 存在與不存在的預測差異
            with_feature = self._predict(x.reshape(1, -1))[0]
            
            x_without = x.copy()
            x_without[i] = self.base_value[i]
            without_feature = self._predict(x_without.reshape(1, -1))[0]
            
            shap_values[i] = with_feature - without_feature
        
        return {
            'base_value': self._predict(self.base_value.reshape(1, -1))[0],
            'shap_values': shap_values,
            'features': x,
        }

# 使用範例
class DummyModel:
    def predict(self, X):
        return X.sum(axis=1)

model = DummyModel()
X_train = np.random.randn(100, 4)
explainer = SimpleShapExplainer(model, X_train)
x_test = np.array([1.0, 2.0, 3.0, 4.0])
result = explainer.explain(x_test)
print(f"SHAP values: {result['shap_values']}")
print(f"Base value: {result['base_value']:.2f}")
```

### LIME：局部可解釋模型

LIME 在預測點附近訓練一個簡單的可解釋模型：

```python
from sklearn.linear_model import Ridge

class LimeExplainer:
    """LIME：局部可解釋模型（簡化版）"""
    
    def __init__(self, model, kernel_width: float = 0.75):
        self.model = model
        self.kernel_width = kernel_width
    
    def _generate_neighborhood(self, x: np.ndarray, n_samples: int = 1000):
        """在 x 周圍生成擾動樣本"""
        perturbations = np.random.normal(0, 0.1, (n_samples, len(x)))
        return x + perturbations
    
    def _kernel(self, distances: np.ndarray):
        """指數核函數：距離越近權重越高"""
        return np.sqrt(np.exp(-(distances ** 2) / self.kernel_width ** 2))
    
    def explain(self, x: np.ndarray, n_features: int = 2) -> dict:
        """解釋單一預測"""
        neighborhood = self._generate_neighborhood(x)
        distances = np.linalg.norm(neighborhood - x, axis=1)
        weights = self._kernel(distances)
        
        preds = self.model.predict(neighborhood)
        
        # 訓練加權線性模型
        surrogate = Ridge(alpha=1.0)
        surrogate.fit(neighborhood, preds, sample_weight=weights)
        
        # 取得最重要的特徵
        importance = np.abs(surrogate.coef_)
        top_indices = np.argsort(importance)[-n_features:][::-1]
        
        return {
            'intercept': surrogate.intercept_,
            'coefficients': surrogate.coef_,
            'top_features': top_indices,
            'local_prediction': self.model.predict(x.reshape(1, -1))[0],
        }
```

### Model Cards：模型文件化標準

Model Cards 是 Google 提出的模型文件化格式：

```python
from dataclasses import dataclass, field
from datetime import date

@dataclass
class ModelCard:
    """Model Card 標準格式（簡化版）"""
    
    # 基本資訊
    model_name: str
    version: str
    release_date: date
    model_type: str
    
    # 用途
    intended_use: str
    intended_users: str
    out_of_scope_uses: str
    
    # 評估
    training_data: str
    evaluation_data: str
    metrics: dict = field(default_factory=dict)
    
    # 公平性
    fairness_evaluation: str = ""
    identified_risks: list = field(default_factory=list)
    
    # 限制
    known_limitations: list = field(default_factory=list)
    recommended_mitigations: list = field(default_factory=list)
    
    def generate_report(self) -> str:
        """產生 Model Card 文字報告"""
        lines = [
            f"# Model Card: {self.model_name} v{self.version}",
            f"**Release Date**: {self.release_date}",
            f"**Model Type**: {self.model_type}",
            "",
            "## Intended Use",
            self.intended_use,
            "",
            "## Performance Metrics",
        ]
        for k, v in self.metrics.items():
            lines.append(f"- {k}: {v}")
        
        lines.extend([
            "",
            "## Fairness Evaluation",
            self.fairness_evaluation,
            "",
            "## Known Limitations",
        ])
        for lim in self.known_limitations:
            lines.append(f"- {lim}")
        
        return "\n".join(lines)

# 實例
card = ModelCard(
    model_name="credit-scorer-v2",
    version="2.1.0",
    release_date=date(2025, 6, 1),
    model_type="Gradient Boosted Tree",
    intended_use="信用貸款核准輔助決策",
    intended_users="銀行授信人員",
    out_of_scope_uses="不得用於人種篩選或歧視性目的",
    metrics={'accuracy': 0.92, 'equal_opportunity_diff': 0.03},
    fairness_evaluation="經交叉性分析，種族×性別組合無顯著差異",
    known_limitations=["僅適用於成年申請人", "資料來自特定地區"],
)
print(card.generate_report())
```

### 透明度演進時間線

| 年份 | 里程碑 |
|------|--------|
| 2023 | 歐盟 AI Act 要求高風險系統提供解釋 |
| 2024 | Model Cards 被多家監管機構推薦 |
| 2025 | SHAP/LIME 成為標準稽核工具 |
| 2026 | 自動化解釋報告生成工具 |
| 2027 | 即時互動式解釋系統 |
| 2029 | 反事實解釋成為法規基本要求 |

### 小結

可解釋性不是可有可無的附加功能。從 SHAP 的數學嚴謹性到 Model Cards 的文件標準，2029 年的 AI 系統必須能回答「為什麼」——不只是為了法規遵循，更是為了建立使用者信任。

---

**下一步**：[AI 問責機制](focus5.md)

## 延伸閱讀

- [SHAP 論文](https://www.google.com/search?q=SHAP+Shapley+Additive+exPlanations)
- [LIME 論文](https://www.google.com/search?q=LIME+local+interpretable+model)
- [Model Cards](https://www.google.com/search?q=Google+Model+Cards)
- [XAI 綜述](https://www.google.com/search?q=explainable+AI+survey+2024)
