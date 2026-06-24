# 模型評估與驗證

## 為什麼需要評估？

建立模型只是第一步，更重要的是知道模型在真實世界中的表現如何。機器學習的核心挑戰是：模型在訓練資料上表現好不一定在未見過的資料上表現好。這就是泛化（Generalization）問題。

## 混淆矩陣

對於分類問題，混淆矩陣（Confusion Matrix）是最基礎的評估工具：

```
                實際值
              正   |   負
        ┌──────┬──────────┐
預 正   │  TP  │   FP     │
測      │ 真陽 │  假陽    │
值      ├──────┼──────────┤
   負   │  FN  │   TN     │
        │ 假陰 │  真陰    │
        └──────┴──────────┘
```

## 關鍵評估指標

### 準確率（Accuracy）

```
準確率 = (TP + TN) / (TP + TN + FP + FN)
```

最直觀的指標，但對於不平衡資料集可能誤導。

### 精確率（Precision）

```
精確率 = TP / (TP + FP)
```

「預測為正的樣本中有多少是真正的正樣本」。在垃圾郵件檢測中，高精確率意味著誤判為垃圾郵件的正常郵件很少。

### 召回率（Recall）

```
召回率 = TP / (TP + FN)
```

「真正的正樣本中有多少被正確預測出來」。在疾病篩查中，高召回率意味著盡可能不遺漏病人。

### F1 分數

F1 是精確率和召回率的調和平均：

```
F1 = 2 × (精確率 × 召回率) / (精確率 + 召回率)
```

在精確率和召回率之間取得平衡。

## 訓練/測試集分割

最簡單的評估方法是將資料分為訓練集和測試集：

```python
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
```

- **訓練集**：用來訓練模型
- **測試集**：用來評估模型在未見過資料上的表現

常見分割比例：80/20 或 70/30。`random_state` 確保結果可重現。

## 交叉驗證

訓練/測試集分割的一個問題是結果對分割方式敏感。K-Fold 交叉驗證解決了這個問題：

```
Fold 1: [訓練│訓練│訓練│訓練│測試]
Fold 2: [訓練│訓練│訓練│測試│訓練]
Fold 3: [訓練│訓練│測試│訓練│訓練]
Fold 4: [訓練│測試│訓練│訓練│訓練]
Fold 5: [測試│訓練│訓練│訓練│訓練]
```

1. 將資料分成 K 等份
2. 每次用 K-1 份訓練，1 份測試
3. 重複 K 次，取平均分數

```python
from sklearn.model_selection import cross_val_score

scores = cross_val_score(model, X, y, cv=5)
print(f"平均準確率: {scores.mean():.3f}")
```

## 過擬合與欠擬合

### 欠擬合（Underfitting）

模型過於簡單，無法捕捉資料中的模式。在訓練集和測試集上表現都差。

**解決方案**：增加模型複雜度、增加特徵。

### 過擬合（Overfitting）

模型過於複雜，記住了訓練資料中的雜訊。在訓練集上表現極好，但在測試集上表現差。

**解決方案**：簡化模型、增加訓練資料、正則化、早停。

### 學習曲線

繪製訓練集和驗證集的誤差隨訓練規模的變化，可以診斷擬合狀態。訓練誤差遠低於驗證誤差表示過擬合；兩者都高表示欠擬合。

---

## 延伸閱讀

- [混淆矩陣說明](https://www.google.com/search?q=confusion+matrix+explained)
- [交叉驗證教學](https://www.google.com/search?q=cross+validation+k+fold)
- [過擬合與欠擬合](https://www.google.com/search?q=overfitting+vs+underfitting)
