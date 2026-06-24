# 混淆矩陣與指標

## 從準確率談起

準確率（Accuracy）是最直觀的評估指標：預測正確的樣本數除以總樣本數。但它可能誤導。

想像一個醫療篩查系統，實際患病率只有 1%。一個永遠預測「健康」的系統準確率高達 99%，但完全沒有篩查價值。

這就是為什麼需要更全面的評估指標。

## 混淆矩陣

混淆矩陣是分類問題評估的基礎。以二元分類為例：

```
                實際值
              正 (P)  │ 負 (N)
        ┌──────┬──────────┬──────┐
預 正   │  TP   │   FP     │ PPV  │
測 (P)  │ 真陽  │  假陽    │精確率│
        ├──────┼──────────┼──────┤
值 負   │  FN   │   TN     │ NPV  │
   (N)  │ 假陰  │  真陰    │      │
        ├──────┼──────────┴──────┤
        │ TPR  │   TNR            │
        │召回率│  特異性          │
        └──────┴──────────────────┘
```

### 四種結果

- **TP（真陽性）**：正確預測為正
- **TN（真陰性）**：正確預測為負
- **FP（假陽性）**：錯誤預測為正（誤報）
- **FN（假陰性）**：錯誤預測為負（漏報）

## 核心指標

### 精確率（Precision）

```
精確率 = TP / (TP + FP)
```

當模型預測為正時，有多大概率是對的？適合「不要打擾我」的場景（如郵件過濾，誤判正常郵件為垃圾郵件很糟糕）。

### 召回率（Recall）

```
召回率 = TP / (TP + FN)
```

真正的正樣本中有多少被找出來了？適合「不要遺漏」的場景（如疾病篩查，漏掉病人很嚴重）。

### F1 分數

```
F1 = 2 × (Precision × Recall) / (Precision + Recall)
```

精確率和召回率的調和平均。當兩者都很重要時使用。

### 特異性（Specificity）

```
特異性 = TN / (TN + FP)
```

真正的負樣本中有多少被正確識別。

## 程式實作

```python
from sklearn.metrics import (
    confusion_matrix,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report
)

y_true = [1, 0, 1, 1, 0, 1, 0, 0, 1, 0]
y_pred = [1, 0, 1, 0, 0, 1, 0, 1, 1, 0]

cm = confusion_matrix(y_true, y_pred)
print("混淆矩陣:")
print(cm)

print(f"準確率: {accuracy_score(y_true, y_pred):.2f}")
print(f"精確率: {precision_score(y_true, y_pred):.2f}")
print(f"召回率: {recall_score(y_true, y_pred):.2f}")
print(f"F1 分數: {f1_score(y_true, y_pred):.2f}")

# 一次輸出所有指標
print("\n分類報告:")
print(classification_report(y_true, y_pred))
```

## 多類別分類的擴展

混淆矩陣可以擴展到多類別。每個類別都有自己的精確率、召回率和 F1：

```python
from sklearn.metrics import confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

# 假設有三個類別
y_true = [0, 1, 2, 0, 1, 2, 0, 0, 1, 2]
y_pred = [0, 1, 1, 0, 1, 2, 0, 1, 1, 2]

cm = confusion_matrix(y_true, y_pred)

# 視覺化
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
plt.xlabel('預測值')
plt.ylabel('實際值')
plt.title('多類別混淆矩陣')
plt.show()
```

### 平均方法

多類別時有三種平均方式：

- **micro**：計算總體 TP/FP/FN
- **macro**：每個類別獨立計算後平均（不考慮樣本數）
- **weighted**：每個類別加權平均（考慮樣本數）

```python
print(f"Macro F1: {f1_score(y_true, y_pred, average='macro'):.2f}")
print(f"Weighted F1: {f1_score(y_true, y_pred, average='weighted'):.2f}")
```

## ROC 曲線與 AUC

ROC 曲線顯示不同閾值下的 TPR 與 FPR。AUC（曲線下面積）衡量模型區分正負樣本的能力：

```python
from sklearn.metrics import RocCurveDisplay

# 繪製 ROC 曲線
RocCurveDisplay.from_estimator(clf, X_test, y_test)
plt.title("ROC 曲線")
plt.show()
```

AUC 範圍 [0, 1]，0.5 等同隨機猜測，1.0 為完美分類。

## 選擇合適的指標

| 場景 | 優先指標 | 原因 |
|------|----------|------|
| 垃圾郵件過濾 | 精確率 | 不想誤刪正常郵件 |
| 疾病篩查 | 召回率 | 不想漏掉病人 |
| 模型綜合比較 | F1 | 平衡精確率和召回率 |
| 平衡資料集 | 準確率 | 簡單直觀 |

常見建議：先看混淆矩陣了解錯誤類型，再用合適的單一指標做比較。

---

## 延伸閱讀

- [混淆矩陣導覽](https://www.google.com/search?q=confusion+matrix+explained)
- [精確率與召回率](https://www.google.com/search?q=precision+recall+tradeoff)
- [ROC 與 AUC 介紹](https://www.google.com/search?q=roc+auc+curve+explained)
