# 模型評估指標：準確率、Precision、Recall、F1

## 1. 混淆矩陣

```python
from sklearn.metrics import confusion_matrix
import numpy as np

y_true = [1, 0, 1, 1, 0, 1, 0, 0, 1, 0]
y_pred = [1, 0, 1, 0, 0, 1, 1, 0, 1, 0]

cm = confusion_matrix(y_true, y_pred)
print(cm)
# [[4 1]
#  [1 4]]
```

- **True Positive (TP)**：實際陽性和預測陽性
- **True Negative (TN)**：實際陰性和預測陰性
- **False Positive (FP)**：實際陰性但預測陽性（假警報）
- **False Negative (FN)**：實際陽性但預測陰性（漏檢）

## 2. 準確率（Accuracy）

```python
def accuracy(y_true, y_pred):
    return np.sum(y_true == y_pred) / len(y_true)

# 或使用 sklearn
from sklearn.metrics import accuracy_score
accuracy_score(y_true, y_pred)
```

- **適用場景**：類別平衡時
- **缺點**：類別不平衡時會有誤導性

## 3. Precision（精確率）

```python
def precision(y_true, y_pred):
    tp = np.sum((y_true == 1) & (y_pred == 1))
    fp = np.sum((y_true == 0) & (y_pred == 1))
    return tp / (tp + fp)

# sklearn
from sklearn.metrics import precision_score
precision_score(y_true, y_pred)
```

- **意義**：預測為正的樣本中，有多少是真正的正
- **適用場景**：假警報代價高的場景（如垃圾郵件判斷）

## 4. Recall（召回率）

```python
def recall(y_true, y_pred):
    tp = np.sum((y_true == 1) & (y_pred == 1))
    fn = np.sum((y_true == 1) & (y_pred == 0))
    return tp / (tp + fn)

# sklearn
from sklearn.metrics import recall_score
recall_score(y_true, y_pred)
```

- **意義**：真正的正樣本中，有多少被預測出來
- **適用場景**：漏檢代價高的場景（如疾病診斷）

## 5. F1 分數

```python
def f1_score(y_true, y_pred):
    p = precision(y_true, y_pred)
    r = recall(y_true, y_pred)
    return 2 * (p * r) / (p + r)

# sklearn
from sklearn.metrics import f1_score
f1_score(y_true, y_pred)
```

F1 是 Precision 和 Recall 的調和平均，平衡兩者。

## 6. 多分類擴展

```python
from sklearn.metrics import classification_report

# 每個類別的 Precision、Recall、F1
print(classification_report(y_true, y_pred))

#                precision    recall  f1-score   support
#
#            0       0.80      0.80      0.80         5
#            1       0.80      0.80      0.80         5
#
#     accuracy                           0.80        10
#    macro avg       0.80      0.80      0.80        10
#weighted avg       0.80      0.80      0.80        10
```

## 7. ROC 曲線與 AUC

```python
from sklearn.metrics import roc_curve, auc
import matplotlib.pyplot as plt

# 假設 y_pred_proba 是預測機率
fpr, tpr, thresholds = roc_curve(y_true, y_pred_proba)
roc_auc = auc(fpr, tpr)

plt.plot(fpr, tpr, label=f'AUC = {roc_auc:.2f}')
plt.plot([0, 1], [0, 1], 'k--')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.legend()
```

## 8. 選擇指標的考量

| 場景 | 優先指標 |
|------|----------|
| 類別平衡的分類 | Accuracy |
| 假警報代價高 | Precision |
| 漏檢代價高 | Recall |
| 需要平衡 Precision/Recall | F1 |
| 排名/機率任務 | AUC |

## 9. 小結

模型評估不能只看準確率，特別是類別不平衡時。選擇適當的指標能更準確反映模型的實際效用。

---

**參考資料**
- [Classification Metrics Guide](https://www.google.com/search?q=classification+metrics+precision+recall+f1)
- [ROC AUC Explained](https://www.google.com/search?q=ROC+curve+AUC+explained)