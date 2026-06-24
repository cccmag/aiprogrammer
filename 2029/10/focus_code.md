# 程式實作：公平性與透明度工具包

## 簡介

本實作建構一個 AI 公平性檢測工具，支援偏見測量、群體公平性評估和緩解策略。完整程式碼在 `_code/fairness_tool.py`。

## 核心元件

### 1. 偏見檢測

```python
detector = BiasDetector()
bias_report = detector.check_gender_bias(["The doctor is a man", "The nurse is a woman"])
```

### 2. 公平性指標

```python
eval = FairnessEvaluator()
report = eval.evaluate_fairness(predictions, sensitive_attr)
```

### 3. 緩解策略

```python
mitigator = BiasMitigator()
corrected = mitigator.reweight_training_data(data, sensitive_col)
```

### 4. 完整報告

```python
report = FairnessReport(
    demographic_parity=0.92,
    equal_opportunity=0.88,
    disparate_impact=1.15,
    biases=["gender_bias"],
    score=0.87
)
```

## 執行方式

```bash
cd _code
python3 fairness_tool.py
```

## 延伸練習

1. **整合 AIF360**：串接 IBM 公平性工具包
2. **模型卡片生成**：自動生成透明度報告
3. **交叉公平性**：分析多個敏感屬性的交織
4. **即時監控**：部署後的公平性持續追蹤
5. **緩解策略比較**：比較重加權與對抗性去偏
