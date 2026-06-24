# 訓練與測試：過擬合、正則化與交叉驗證

## 前言

機器學習的核心目標是讓模型能夠泛化（generalize）到新的、未見過的資料上。如果模型只是在訓練資料上表現良好，但在新資料上表現很差，那就是發生了過擬合（Overfitting）。本文將探討如何正確地訓練和測試模型。

## 資料集划分

### 基礎划分

將資料分為三部分：
- **訓練集（Training Set）**：用於訓練模型
- **驗證集（Validation Set）**：用於調整超參數
- **測試集（Test Set）**：用於最終評估模型效能

```
┌─────────────────────────────────────────────────────┐
│                   資料集划分                         │
├─────────────────────────────────────────────────────┤
│                                                     │
│  全部資料                                           │
│  ┌───────────┬───────────┬───────────┐            │
│  │  訓練集   │  驗證集   │  測試集   │            │
│  │  (60-80%) │  (10-20%) │  (10-20%) │            │
│  └───────────┴───────────┴───────────┘            │
│                                                     │
│  用途      訓練模型    調參數    最終評估             │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### 簡單划分

```python
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
```

### 分層抽樣

當類別不平衡時，使用分層抽樣確保各集合中類別比例一致：

```python
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)
```

## 過擬合與欠擬合

### 過擬合（Overfitting）

模型在訓練資料上表現很好，但在測試資料上表現很差。
- 模型太複雜，記憶了訓練資料的噪聲
- 訓練資料太少

### 欠擬合（Underfitting）

模型在訓練資料和測試資料上表現都不好。
- 模型太簡單，無法捕捉資料的複雜模式

```
┌─────────────────────────────────────────────────────┐
│              過擬合 vs 欠擬合                        │
├─────────────────────────────────────────────────────┤
│                                                     │
│   訓練 loss                                         │
│      │                                              │
│      │    ╭── 訓練 loss                             │
│      │   ╱╲                                         │
│      │  ╱  ╲    ╭── 驗證 loss                       │
│      │ ╱    ╲  ╱                                    │
│      │╱      ╲╱                                     │
│      └──────────────────────►  模型複雜度            │
│           欠擬合   理想   過擬合                     │
│                                                     │
└─────────────────────────────────────────────────────┘
```

## 正則化（Regularization）

正則化是防止過擬合的主要技術之一。

### L1 正則化（Lasso）

懲罰項是權重的絕對值總和：
```
L1 = α * Σ|w|
```
特點：會將不重要特徵的權重設為 0，實現特徵選擇。

### L2 正則化（Ridge）

懲罰項是權重的平方和：
```
L2 = α * Σw²
```
特點：會讓權重趨近於 0但不為 0，所有特徵都會被考慮。

### Elastic Net

結合 L1 和 L2 正則化：
```
Elastic Net = α * (ρ * Σ|w| + (1-ρ) * Σw² / 2)
```

### Python 實作

```python
from sklearn.linear_model import Ridge, Lasso, ElasticNet

# Ridge 回歸（L2 正則化）
ridge = Ridge(alpha=1.0)
ridge.fit(X_train, y_train)

# Lasso 回歸（L1 正則化）
lasso = Lasso(alpha=1.0)
lasso.fit(X_train, y_train)

# Elastic Net（L1 + L2）
elastic = ElasticNet(alpha=1.0, l1_ratio=0.5)
elastic.fit(X_train, y_train)
```

## 交叉驗證（Cross-Validation）

交叉驗證是評估模型泛化能力的標準方法。

### K-Fold 交叉驗證

將資料分成 K 份，輪流使用其中一份作為測試集：

```python
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LogisticRegression

model = LogisticRegression(max_iter=200)

# 5-Fold 交叉驗證
scores = cross_val_score(model, X, y, cv=5)

print(f'各折準確率: {scores}')
print(f'平均準確率: {scores.mean():.4f} ± {scores.std():.4f}')
```

```
┌─────────────────────────────────────────────────────┐
│              5-Fold 交叉驗證                        │
├─────────────────────────────────────────────────────┤
│                                                     │
│   Fold 1: [測試] [訓練] [訓練] [訓練] [訓練]       │
│   Fold 2: [訓練] [測試] [訓練] [訓練] [訓練]       │
│   Fold 3: [訓練] [訓練] [測試] [訓練] [訓練]       │
│   Fold 4: [訓練] [訓練] [訓練] [測試] [訓練]       │
│   Fold 5: [訓練] [訓練] [訓練] [訓練] [測試]       │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### 分層 K-Fold

保持每折中類別比例一致：

```python
from sklearn.model_selection import StratifiedKFold

skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

for train_idx, test_idx in skf.split(X, y):
    X_train, X_test = X[train_idx], X[test_idx]
    y_train, y_test = y[train_idx], y[test_idx]
    # 訓練和評估模型
```

## 學習曲線（Learning Curve）

學習曲線可以幫助診斷過擬合和欠擬合：

```python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import learning_curve

train_sizes, train_scores, val_scores = learning_curve(
    model, X, y, cv=5, n_jobs=-1,
    train_sizes=np.linspace(0.1, 1.0, 10)
)

train_mean = train_scores.mean(axis=1)
train_std = train_scores.std(axis=1)
val_mean = val_scores.mean(axis=1)
val_std = val_scores.std(axis=1)

plt.fill_between(train_sizes, train_mean - train_std,
                 train_mean + train_std, alpha=0.1, color='blue')
plt.fill_between(train_sizes, val_mean - val_std,
                 val_mean + val_std, alpha=0.1, color='orange')
plt.plot(train_sizes, train_mean, 'o-', color='blue', label='訓練分數')
plt.plot(train_sizes, val_mean, 'o-', color='orange', label='驗證分數')
plt.xlabel('訓練樣本數')
plt.ylabel('準確率')
plt.legend()
plt.show()
```

## Dropout（用於神經網路）

Dropout 是一種用於神經網路的正則化技術：

```python
# 在 Keras 中使用 Dropout
from keras.models import Sequential
from keras.layers import Dense, Dropout

model = Sequential([
    Dense(64, activation='relu', input_shape=(100,)),
    Dropout(0.5),  # 隨機丟棄 50% 的神經元
    Dense(64, activation='relu'),
    Dropout(0.5),
    Dense(10, activation='softmax')
])
```

## 模型選擇策略

### 網格搜索（Grid Search）

```python
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVC

param_grid = {
    'C': [0.1, 1, 10],
    'kernel': ['linear', 'rbf'],
    'gamma': [0.1, 1, 10]
}

grid_search = GridSearchCV(SVC(), param_grid, cv=5)
grid_search.fit(X_train, y_train)

print(f'最佳參數: {grid_search.best_params_}')
print(f'最佳分數: {grid_search.best_score_:.4f}')
```

### 隨機搜索（Random Search）

當參數空間很大時，隨機搜索比網格搜索更有效率：

```python
from sklearn.model_selection import RandomizedSearchCV
from scipy.stats import uniform, randint

param_dist = {
    'C': uniform(0.1, 10),
    'kernel': ['linear', 'rbf'],
    'gamma': uniform(0.01, 10)
}

random_search = RandomizedSearchCV(SVC(), param_dist,
                                    n_iter=50, cv=5)
random_search.fit(X_train, y_train)
```

## 結語

正確的訓練和測試流程是建立可靠機器學習模型的關鍵：
1. 永遠要將資料分為訓練集和測試集
2. 使用驗證集調整超參數
3. 使用交叉驗證獲得可靠的效能估計
4. 使用正則化防止過擬合
5. 繪製學習曲線診斷模型問題

下一篇文章將介紹各種模型評估指標，幫助你更全面地評價模型效能。

---

## 延伸閱讀

- [過擬合與正則化](https://www.google.com/search?q=overfitting+regularization+machine+learning)
- [交叉驗證詳解](https://www.google.com/search?q=cross+validation+sklearn+tutorial)
- [學習曲線分析](https://www.google.com/search?q=learning+curve+diagnosis+machine+learning)

---

*本篇文章為「AI 程式人雜誌 2018 年 4 月號」機器學習基礎系列之一。*