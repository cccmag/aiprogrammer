# 交叉驗證

## 為什麼需要交叉驗證？

單次訓練/測試集分割的問題：結果可能對分割方式非常敏感。運氣好時測試集簡單，分數高；運氣差時測試集困難，分數低。

交叉驗證（Cross-Validation）透過多次分割、多次評估來解決這個問題，讓評估結果更穩定可靠。

## K-Fold 交叉驗證

K-Fold 是最常用的交叉驗證方法：

```
Fold 1: [測試][訓練][訓練][訓練][訓練] → 分數 1
Fold 2: [訓練][測試][訓練][訓練][訓練] → 分數 2
Fold 3: [訓練][訓練][測試][訓練][訓練] → 分數 3
Fold 4: [訓練][訓練][訓練][測試][訓練] → 分數 4
Fold 5: [訓練][訓練][訓練][訓練][測試] → 分數 5
                                       → 平均 = 最終分數
```

### 基本用法

```python
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_iris

iris = load_iris()
clf = RandomForestClassifier(n_estimators=100, random_state=42)

scores = cross_val_score(clf, iris.data, iris.target, cv=5)

print(f"各折分數: {scores}")
print(f"平均分數: {scores.mean():.3f}")
print(f"標準差: {scores.std():.3f}")
```

### 選擇 K 值

- **K=5**：最常用，平衡偏差與變異數
- **K=10**：更穩定（變異數更小），但計算成本更高
- **K=3**：計算快速但評估可能不穩定
- **Leave-One-Out (K=N)**：極端情況，每個樣本單獨作為測試集

```python
from sklearn.model_selection import LeaveOneOut

loo = LeaveOneOut()
scores_loo = cross_val_score(clf, iris.data, iris.target, cv=loo)
print(f"LOO 平均分數: {scores_loo.mean():.3f}")
```

## 分層 K-Fold

對於分類問題，分層 K-Fold 保持每次折疊中的類別比例與原始資料一致：

```python
from sklearn.model_selection import StratifiedKFold

skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
scores = cross_val_score(clf, iris.data, iris.target, cv=skf)
```

對不平衡資料集，分層 K-Fold 是必要選擇。

## 自定義評估指標

```python
from sklearn.metrics import make_scorer, f1_score

f1_scorer = make_scorer(f1_score, average='macro')
scores = cross_val_score(clf, iris.data, iris.target, cv=5, scoring=f1_scorer)
```

## 使用交叉驗證調參

```python
from sklearn.model_selection import GridSearchCV

param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [3, 5, None]
}

grid = GridSearchCV(
    RandomForestClassifier(random_state=42),
    param_grid,
    cv=5,
    scoring='accuracy',
    n_jobs=-1
)

grid.fit(iris.data, iris.target)
print(f"最佳參數: {grid.best_params_}")
print(f"最佳分數: {grid.best_score_:.3f}")
```

## 交叉驗證的優點與缺點

### 優點

- **更穩定的評估**：降低單次分割的隨機性
- **更有效利用資料**：所有資料都被用來訓練和測試
- **更可靠的參數選擇**：調參結果不易過擬合

### 缺點

- **計算成本高**：K 倍訓練時間
- **不適用時間序列**：隨機分割會破壞時間順序

## 時間序列的特殊處理

時間序列資料需使用 TimeSeriesSplit：

```python
from sklearn.model_selection import TimeSeriesSplit

tscv = TimeSeriesSplit(n_splits=5)
for train_idx, test_idx in tscv.split(X):
    print(f"訓練: {train_idx[0]}-{train_idx[-1]}, 測試: {test_idx[0]}-{test_idx[-1]}")
```

## 實作建議

1. **資料量大時**：K=5 就足夠
2. **資料量小時**：K=10 或 Leave-One-Out
3. **分類問題**：使用 StratifiedKFold
4. **時間序列**：使用 TimeSeriesSplit
5. **搭配 Pipeline**：避免資料洩漏

```python
from sklearn.pipeline import Pipeline

pipe = Pipeline([
    ('scaler', StandardScaler()),
    ('clf', RandomForestClassifier())
])

scores = cross_val_score(pipe, X, y, cv=5)
```

交叉驗證是機器學習中最重要的評估技術之一。掌握它，你就能對模型效能有更客觀的判斷。

---

## 延伸閱讀

- [交叉驗證介紹](https://www.google.com/search?q=cross+validation+machine+learning)
- [scikit-learn 交叉驗證](https://www.google.com/search?q=sklearn+cross+validation)
- [K-Fold 與 Stratified K-Fold](https://www.google.com/search?q=kfold+vs+stratified+kfold)
