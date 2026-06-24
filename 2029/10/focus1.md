# 負責任 AI 框架

## Google、Microsoft、IBM 的責任 AI 實踐（2019-2029）

### 前言

負責任 AI（Responsible AI）並非單一技術，而是一整套從設計到部署的治理框架。2019 年之後，各大科技公司陸續發布了各自的責任 AI 原則與工具，試圖將「公平、透明、可解釋、隱私、安全」等抽象理念落地為可操作的流程。

### Google 的 Responsible AI 路徑

Google 在 2019 年發布了 AI 原則，並在 2022 年推出 Cloud Responsible AI 工具組：

```python
# Google 的責任 AI 工具包示意：偏見偵測掃描
import pandas as pd
from sklearn.model_selection import train_test_split

def compute_subgroup_accuracy(y_true, y_pred, group_mask):
    """計算子群體的準確率，用於偏見掃描"""
    mask = group_mask.astype(bool)
    if mask.sum() == 0:
        return None
    correct = (y_true[mask] == y_pred[mask]).mean()
    return correct

# 模擬：檢查不同族群間的準確率差異
data = pd.DataFrame({
    'score': range(1000),
    'label': [1 if x > 500 else 0 for x in range(1000)],
    'group': ['A'] * 700 + ['B'] * 300,
})

for g in ['A', 'B']:
    mask = data['group'] == g
    acc = compute_subgroup_accuracy(
        data['label'][mask],
        data['label'][mask],  # 模擬完美預測
        mask
    )
    print(f"Group {g} accuracy: {acc:.3f}")
```

Google 的工具矩陣包括：
- **What-If Tool**：互動式模型行為分析
- **Model Card Toolkit**：模型文件化
- **TensorFlow Fairness Indicators**：公平性指標儀表板
- **Explainable AI**：可解釋性 API

### Microsoft 的 Responsible AI 儀表板

Microsoft 在 2021 年推出 Responsible AI Dashboard，整合在 Azure ML 中：

```python
# Microsoft 的責任 AI 儀表板元件示意
from dataclasses import dataclass

@dataclass
class ModelReport:
    model_name: str
    overall_accuracy: float
    fairness_metrics: dict
    explainer_shap: list
    error_analysis: dict

def generate_report(model, X_test, y_test, sensitive_features):
    """模擬 Microsoft Responsible AI Dashboard 的報告流程"""
    # 1. 錯誤分析
    errors = {
        'overall': 0.05,
        'by_group': {
            'group_A': 0.03,
            'group_B': 0.08,  # 較高錯誤率 -> 需要關注
        }
    }
    
    # 2. 公平性指標
    fairness = {
        'demographic_parity': 0.92,
        'equal_opportunity': 0.88,
        'disparate_impact': 0.85,
    }
    
    # 3. SHAP 解釋
    explanations = [0.12, -0.05, 0.34, 0.02, -0.18]
    
    return ModelReport(
        model_name=model.__class__.__name__,
        overall_accuracy=0.94,
        fairness_metrics=fairness,
        explainer_shap=explanations,
        error_analysis=errors,
    )
```

### IBM 的 AI Fairness 360

IBM 的 AIF360 是開源領域最完整的公平性工具包：

```python
# AIF360 的核心流程示意
from aif360.datasets import BinaryLabelDataset
from aif360.metrics import BinaryLabelDatasetMetric
from aif360.algorithms.preprocessing import Reweighing

# 定義受保護屬性
protected_attribute = 'race'

# 計算原始資料的公平性指標
dataset = BinaryLabelDataset(...)
metric = BinaryLabelDatasetMetric(
    dataset,
    unprivileged_groups=[{'race': 0}],
    privileged_groups=[{'race': 1}]
)

print(f"Disparate Impact: {metric.disparate_impact():.3f}")
print(f"Statistical Parity Difference: {metric.statistical_parity_difference():.3f}")

# 使用 Reweighing 進行前處理緩解
RW = Reweighing(
    unprivileged_groups=[{'race': 0}],
    privileged_groups=[{'race': 1}]
)
dataset_transf = RW.fit_transform(dataset)
```

### 框架演進時間線

| 年份 | 事件 |
|------|------|
| 2019 | Google 發布 AI 原則，禁止武器 AI |
| 2020 | IBM 開源 AIF360 |
| 2021 | Microsoft 推出 Responsible AI Dashboard |
| 2022 | Google Cloud RAI 工具組 GA |
| 2023 | 歐盟 AI Act 草案通過歐洲議會 |
| 2025 | 各國強制性 AI 稽核要求 |
| 2027 | ISO/IEC 42001 AI 管理系統標準普及 |
| 2029 | 負責任 AI 成為業界標配 |

### 小結

從 2019 到 2029，負責任 AI 從自願性原則走向強制性規範。Google、Microsoft、IBM 提供的工具逐步成熟，但真正的挑戰不在工具，而在組織文化——如何讓公平性檢測像單元測試一樣成為開發流程的一環。

---

**下一步**：[偏見檢測與緩解](focus2.md)

## 延伸閱讀

- [Google Responsible AI](https://www.google.com/search?q=Google+Responsible+AI+framework)
- [Microsoft Responsible AI Dashboard](https://www.google.com/search?q=Microsoft+Responsible+AI+Dashboard)
- [IBM AI Fairness 360](https://www.google.com/search?q=IBM+AI+Fairness+360)
- [What-If Tool](https://www.google.com/search?q=What+If+Tool+Google)
