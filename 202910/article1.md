# 偏見檢測工具實戰：用 Python 揪出模型中的不公平

## 前言

AI 模型的偏見問題已成為負責任 AI 的核心挑戰。從性別偏見到種族歧視，模型可能在訓練資料中學到有害的刻板印象。本文介紹如何用 Python 工具檢測模型偏見。

## 使用 AIF360 檢測偏見

IBM 的 AI Fairness 360（AIF360）是業界最成熟的偏見檢測工具。

```python
from aif360.datasets import BinaryLabelDataset
from aif360.metrics import BinaryLabelDatasetMetric
from aif360.algorithms.preprocessing import Reweighing

dataset = BinaryLabelDataset(
    df=load_data(),
    label_names=['income'],
    protected_attribute_names=['gender'],
    privileged_classes=[['男性']],
    unprivileged_classes=[['女性']]
)

metric = BinaryLabelDatasetMetric(
    dataset,
    unprivileged_groups=[{'gender': 0}],
    privileged_groups=[{'gender': 1}]
)

print(f"統計均差異: {metric.statistical_parity_difference():.4f}")
print(f"不利影響比: {metric.disparate_impact():.4f}")
```

## 使用 Fairlearn 進行儀表板分析

Microsoft 的 Fairlearn 提供視覺化儀表板：

```python
from fairlearn.metrics import MetricFrame
from fairlearn.metrics import selection_rate, equalized_odds_difference

y_true = labels
y_pred = model.predict(X_test)
sensitive_features = X_test['gender']

mf = MetricFrame(
    metrics={'selection_rate': selection_rate},
    y_true=y_true,
    y_pred=y_pred,
    sensitive_features=sensitive_features
)
print(mf.by_group)
```

## 使用 WIT（What-If Tool）互動探索

Google 的 What-If Tool 提供互動式偏見分析：

```python
from witwidget.notebook.visualization import WitWidget, WitConfigBuilder

config_builder = WitConfigBuilder(
    examples, feature_spec
).set_compare_model(model).set_target('income')

WitWidget(config_builder)
```

## 結語

偏見檢測應融入模型開發的每個環節。建議團隊建立自動化檢測管道，在 CI/CD 流程中加入公平性檢查，確保每次部署前都經過審核。

---

**延伸閱讀**

- [AIF360 官方文件](https://www.google.com/search?q=AIF360+IBM+fairness+360+Python)
- [Fairlearn 使用者指南](https://www.google.com/search?q=Fairlearn+Microsoft+fairness+tool)
- [What-If Tool 教學](https://www.google.com/search?q=What+If+Tool+Google+interactive+fairness)
- [ML 公平性概述](https://www.google.com/search?q=machine+learning+fairness+overview+bias+detection)
