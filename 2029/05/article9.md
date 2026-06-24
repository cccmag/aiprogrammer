# 評估指標選擇指南

## 指標選擇的重要性

不同的評估指標反映模型不同面向的能力。選擇錯誤的指標可能導致誤導性的結論。本篇文章介紹常見評估指標及其適用場景。

## 分類任務指標

```python
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, confusion_matrix
)
import numpy as np

def evaluate_classification(y_true, y_pred):
    metrics = {
        "accuracy": accuracy_score(y_true, y_pred),
        "precision_macro": precision_score(y_true, y_pred,
                                            average="macro"),
        "recall_macro": recall_score(y_true, y_pred,
                                      average="macro"),
        "f1_macro": f1_score(y_true, y_pred, average="macro")
    }

    # 混淆矩陣
    cm = confusion_matrix(y_true, y_pred)

    # 每類別精確率與召回率
    per_class = {}
    for i in range(len(np.unique(y_true))):
        per_class[f"class_{i}"] = {
            "precision": precision_score(y_true, y_pred,
                                          labels=[i], average="micro"),
            "recall": recall_score(y_true, y_pred,
                                   labels=[i], average="micro")
        }

    return {"overall": metrics, "per_class": per_class,
            "confusion_matrix": cm.tolist()}
```

## 生成任務指標

```python
import evaluate

class GenerationMetrics:
    def __init__(self):
        self.bleu = evaluate.load("bleu")
        self.rouge = evaluate.load("rouge")
        self.bertscore = evaluate.load("bertscore")

    def compute_all(self, predictions, references):
        results = {}

        # BLEU：適合翻譯與摘要
        results["bleu"] = self.bleu.compute(
            predictions=predictions,
            references=references
        )

        # ROUGE：適合摘要評估
        results["rouge"] = self.rouge.compute(
            predictions=predictions,
            references=references
        )

        # BERTScore：語義相似度
        results["bertscore"] = self.bertscore.compute(
            predictions=predictions,
            references=references,
            lang="zh"
        )

        return results
```

## 何時使用何種指標

```python
metric_guide = {
    "classification": {
        "balanced": "accuracy",
        "imbalanced": "F1-macro"
    },
    "generation": {
        "translation": "BLEU",
        "summarization": "ROUGE-L"
    },
    "code": {"functional": "pass@k"},
    "qa": {"extractive": "F1 / EM"}
}
```

## 結語

Google 搜尋「Evaluation Metrics NLP Guide」可深入了解各指標的數學定義與適用條件。選擇正確的評估指標，才能得到有意義的結論。
