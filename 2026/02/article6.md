# 隨機森林實戰

## 為什麼用隨機森林？

單一決策樹有兩個主要問題：

1. **高變異數**：訓練資料的小變化可能導致完全不同的樹
2. **容易過擬合**：樹可以長到完美記憶訓練資料

隨機森林透過整合多棵樹解決了這些問題。它的概念很簡單：一群普通人投票的結果往往優於單一專家。

## 隨機森林核心概念

### 1. Bagging（Bootstrap Aggregating）

從訓練資料中有放回地抽樣，建立多個子資料集。每個子資料集用於訓練一棵決策樹。由於抽樣是「有放回」的，同一個樣本可能被多次選中。

### 2. 隨機特徵選擇

在每個節點分割時，只考慮隨機選取的部分特徵（通常是 `sqrt(n_features)` 或 `log2(n_features)`）。這確保了樹之間的多樣性。

### 3. 投票/平均

- 分類：每棵樹投票，取眾數
- 迴歸：每棵樹輸出加權平均

## 實戰範例：客戶流失預測

```python
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix

# 模擬客戶資料（1000 位客戶，10 個特徵）
np.random.seed(42)
n_samples = 1000
n_features = 10

X = np.random.randn(n_samples, n_features)
y = (X[:, 0] + X[:, 2] - X[:, 5] + np.random.randn(n_samples) * 0.5 > 0).astype(int)

# 分割資料
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
```

## 訓練與調參

```python
rf = RandomForestClassifier(
    n_estimators=200,     # 樹的數量
    max_depth=10,          # 每棵樹的最大深度
    min_samples_split=5,   # 內部節點最小樣本數
    min_samples_leaf=2,    # 葉節點最小樣本數
    max_features='sqrt',   # 每個節點考慮的特徵數
    random_state=42,
    n_jobs=-1              # 使用所有 CPU 核心
)

rf.fit(X_train, y_train)
y_pred = rf.predict(X_test)
```

## 評估結果

```python
print("分類報告:")
print(classification_report(y_test, y_pred))

print("混淆矩陣:")
print(confusion_matrix(y_test, y_pred))

print(f"\n訓練集準確率: {rf.score(X_train, y_train):.3f}")
print(f"測試集準確率: {rf.score(X_test, y_test):.3f}")
```

## 特徵重要性分析

隨機森林天然支援特徵重要性分析：

```python
importances = rf.feature_importances_
indices = np.argsort(importances)[::-1]

print("特徵重要性排序:")
for i, idx in enumerate(indices):
    print(f"  第 {i+1} 名: 特徵 {idx} — {importances[idx]:.4f}")
```

這可以幫助你了解哪些特徵對預測最關鍵，進而指導資料收集和特徵工程。

## OOB 評分

隨機森林支援 OOB（Out-of-Bag）評分，不需額外分割驗證集：

```python
rf_oob = RandomForestClassifier(n_estimators=200, oob_score=True, random_state=42)
rf_oob.fit(X_train, y_train)
print(f"OOB 分數: {rf_oob.oob_score_:.3f}")
```

## 參數調優建議

```python
from sklearn.model_selection import GridSearchCV

param_grid = {
    'n_estimators': [100, 200, 300],
    'max_depth': [5, 10, 15],
    'min_samples_split': [2, 5, 10],
}

grid = GridSearchCV(
    RandomForestClassifier(random_state=42),
    param_grid,
    cv=5,
    n_jobs=-1
)

grid.fit(X_train, y_train)
print(f"最佳參數: {grid.best_params_}")
```

## 實戰注意事項

- **樹的數量**：越多越好，但回報遞減。100-500 棵通常足夠
- **深度限制**：隨機森林不太需要深度限制（Bagging 已降低變異數）
- **特徵尺度**：樹模型不需標準化
- **類別不平衡**：設定 `class_weight='balanced'`

隨機森林在各類 ML 競賽中長期表現出色，是入門者必學的強力模型。

---

## 延伸閱讀

- [隨機森林演算法詳解](https://www.google.com/search?q=random+forest+algorithm+explained)
- [scikit-learn 隨機森林](https://www.google.com/search?q=sklearn+random+forest)
- [隨機森林調參指南](https://www.google.com/search?q=random+forest+hyperparameter+tuning)
