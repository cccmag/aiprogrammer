# 模型評估指標：準確率、精確率、召回率與 F1 分數

## 前言

選擇正確的評估指標對於機器學習專案至關重要。不同的問題需要不同的指標。一個在所有情況下都適用的「萬能指標」並不存在。

## 分類問題的評估指標

### 混淆矩陣（Confusion Matrix）

混淆矩陣是評估分類模型的基本工具：

```
┌─────────────────────────────────────────────────────┐
│                   混淆矩陣                           │
├─────────────────────────────────────────────────────┤
│                         預測                          │
│                      正例    負例                     │
│      ┌─────────┬─────────┬─────────┐              │
│   實  │  真陽性  │  假陰性  │         │              │
│   際  │  (TP)   │  (FN)   │         │              │
│      ├─────────┼─────────┼─────────┤              │
│   正  │         │         │         │              │
│   例  ├─────────┼─────────┼─────────┤              │
│      │  假陽性  │  真陰性  │         │              │
│   負  │  (FP)   │  (TN)   │         │              │
│   例  └─────────┴─────────┴─────────┘              │
│                                                     │
└─────────────────────────────────────────────────────┘
```

- **True Positive (TP)**：實際為正，預測為正（正確）
- **False Negative (FN)**：實際為正，預測為負（錯誤）
- **False Positive (FP)**：實際為負，預測為正（錯誤）
- **True Negative (TN)**：實際為負，預測為負（正確）

### 準確率（Accuracy）

最直觀的指標，但當類別不平衡時可能誤導：

```
Accuracy = (TP + TN) / (TP + TN + FP + FN)
```

```python
from sklearn.metrics import accuracy_score

y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f'準確率: {accuracy:.4f}')
```

### 精確率（Precision）

在所有預測為正的樣本中，實際為正的比例：

```
Precision = TP / (TP + FP)
```

適用場景：假陽性代價高（如垃圾郵件過濾，誤標正常郵件）

### 召回率（Recall）

在所有實際為正的樣本中，被正確預測為正的比例：

```
Recall = TP / (TP + FN)
```

適用場景：假陰性代價高（如疾病篩檢，漏診）

### F1 分數

精確率和召回率的調和平均數：

```
F1 = 2 * (Precision * Recall) / (Precision + Recall)
```

```python
from sklearn.metrics import precision_score, recall_score, f1_score

precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)

print(f'精確率: {precision:.4f}')
print(f'召回率: {recall:.4f}')
print(f'F1 分數: {f1:.4f}')
```

### 完整報告

```python
from sklearn.metrics import classification_report

print(classification_report(y_test, y_pred,
                            target_names=['負例', '正例']))
```

輸出：
```
              precision    recall  f1-score   support

         負例       0.92      0.95      0.93       100
         正例       0.87      0.82      0.84        50

    accuracy                           0.90       150
   macro avg       0.89      0.88      0.89       150
weighted avg       0.90      0.90      0.90       150
```

## ROC 曲線與 AUC

### ROC 曲線

ROC（Receiver Operating Characteristic）曲線顯示了在不同閾值下，真陽率（TPR）與假陽率（FPR）的權衡。

```
TPR (True Positive Rate) = TP / (TP + FN) = Recall
FPR (False Positive Rate) = FP / (FP + TN)
```

### AUC

AUC（Area Under the Curve）是 ROC 曲線下的面積，值域為 0 到 1：
- AUC = 0.5：隨機猜測
- AUC = 1.0：完美分類器
- AUC > 0.9：優秀
- AUC > 0.7：良好

```python
from sklearn.metrics import roc_curve, auc
import matplotlib.pyplot as plt

# 獲取預測機率
y_prob = model.predict_proba(X_test)[:, 1]

# 計算 ROC 曲線
fpr, tpr, thresholds = roc_curve(y_test, y_prob)
roc_auc = auc(fpr, tpr)

# 繪製
plt.figure()
plt.plot(fpr, tpr, color='darkorange', lw=2,
         label=f'ROC curve (AUC = {roc_auc:.2f})')
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic')
plt.legend()
plt.show()
```

## 迴歸問題的評估指標

### 均方誤差（MSE）

```
MSE = (1/n) * Σ(y_pred - y_true)²
```

對大誤差更敏感（因為平方）。

### 均方根誤差（RMSE）

```
RMSE = √MSE
```

與目標變數同單位，更容易解釋。

### 平均絕對誤差（MAE）

```
MAE = (1/n) * Σ|y_pred - y_true|
```

對 outliers 更魯棒。

### 決定係數（R²）

```
R² = 1 - (SS_res / SS_tot)
```

其中：
- SS_res = Σ(y_pred - y_true)²
- SS_tot = Σ(y_true - y_mean)²

R² = 1 表示完美擬合，R² = 0 表示僅預測平均值。

```python
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

y_pred = model.predict(X_test)

mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f'MSE: {mse:.4f}')
print(f'RMSE: {rmse:.4f}')
print(f'MAE: {mae:.4f}')
print(f'R²: {r2:.4f}')
```

## 多類別分類

### Macro 與 Micro 平均

- **Macro 平均**：先計算每個類別的指標，再平均
- **Micro 平均**：先聚合所有類別的 TP、FP、FN，再計算指標

```python
from sklearn.metrics import precision_score

# Micro 平均（對所有類別的預測結果進行全局計算）
precision_micro = precision_score(y_test, y_pred, average='micro')

# Macro 平均（每個類別單獨計算後取平均）
precision_macro = precision_score(y_test, y_pred, average='macro')

# Weighted 平均（依類別樣本數加權）
precision_weighted = precision_score(y_test, y_pred,
                                     average='weighted')
```

## 選擇正確的指標

| 問題類型 | 推薦指標 | 原因 |
|----------|----------|------|
| 類別平衡 | 準確率 | 簡單直觀 |
| 類別不平衡 | F1、Precision、Recall | 關注少數類別 |
| 疾病篩檢 | Recall | 避免漏診 |
| 垃圾郵件 | Precision | 避免誤標 |
| 排名問題 | AUC | 不依賴閾值 |

## 結語

選擇正確的評估指標是機器學習專案成功的關鍵之一。要根據業務需求和資料特性來選擇最適合的指標。在類別不平衡的問題中，準確率往往會誤導我們，這時應該使用 F1 分數、ROC-AUC 等指標。

下一篇文章將介紹 scikit-learn 的使用方法，這是 Python 生態系統中最受歡迎的機器學習庫。

---

## 延伸閱讀

- [scikit-learn 評估指標文檔](https://www.google.com/search?q=sklearn+metrics+documentation)
- [ROC 曲線與 AUC 詳解](https://www.google.com/search?q=ROC+curve+AUC+explained)
- [機器學習評估指標](https://www.google.com/search?q=machine+learning+evaluation+metrics)

---

*本篇文章為「AI 程式人雜誌 2018 年 4 月號」機器學習基礎系列之一。*