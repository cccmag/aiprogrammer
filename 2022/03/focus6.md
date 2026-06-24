# Scikit-learn 機器學習管線

## 機器學習的標準化介面

Scikit-learn 是 Python 生態系中最著名的機器學習函式庫，由 David Cournapeau 在 2007 年發起，後續由 INRIA 團隊（特別是 Fabian Pedregosa 和 Gaël Varoquaux）持續開發。它的核心貢獻在於定義了一套統一的 Estimator API，讓使用者可以用一致的介面使用不同的機器學習演算法。

## Estimator API

Scikit-learn 的所有模型都遵循同一個 API 模式：

```python
# 所有估計器都實作這三個方法：
model.fit(X, y)       # 訓練模型
model.predict(X)      # 進行預測
model.score(X, y)     # 評估模型
```

這種一致性讓使用者可以輕鬆地在不同演算法之間切換：

```python
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression

for Model in [SVC, RandomForestClassifier, LogisticRegression]:
    model = Model()
    model.fit(X_train, y_train)
    print(f"{Model.__name__}: {model.score(X_test, y_test):.3f}")
```

## 預處理與特徵工程

真實資料從不乾淨。scikit-learn 的 `preprocessing` 模組提供了完整的資料轉換工具：

```python
from sklearn.preprocessing import StandardScaler, OneHotEncoder

# 標準化（Z-score）
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 類別特徵編碼
encoder = OneHotEncoder()
X_encoded = encoder.fit_transform(categorical_features)
```

## 管線（Pipeline）

管線是 scikit-learn 最具革命性的設計之一。它將預處理和模型訓練封裝為一個單一物件：

```python
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC

pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("svm", SVC(kernel="rbf")),
])

pipeline.fit(X_train, y_train)
y_pred = pipeline.predict(X_test)
```

管線的好處：
- **避免資料洩漏**：標準化的參數只在訓練集上擬合
- **簡化程式碼**：預處理和模型一步到位
- **支援網格搜尋**：可以直接搜尋管線中的超參數

## 網格搜尋（GridSearchCV）

```python
from sklearn.model_selection import GridSearchCV

param_grid = {
    "svm__C": [0.1, 1, 10, 100],
    "svm__gamma": [0.001, 0.01, 0.1, 1],
}

grid = GridSearchCV(pipeline, param_grid, cv=5)
grid.fit(X_train, y_train)

print(f"Best params: {grid.best_params_}")
print(f"Best CV score: {grid.best_score_:.3f}")
```

## 交叉驗證

Scikit-learn 提供了多種交叉驗證策略：

```python
from sklearn.model_selection import cross_val_score

scores = cross_val_score(model, X, y, cv=5, scoring="accuracy")
print(f"CV scores: {scores.mean():.3f} ± {scores.std():.3f}")

# 自訂交叉驗證
from sklearn.model_selection import StratifiedKFold
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
```

## 評估指標

```python
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, confusion_matrix, classification_report
)

print(classification_report(y_test, y_pred))
```

## 延伸閱讀

- [scikit-learn 官方教學](https://www.google.com/search?q=scikit-learn+tutorial)
- [scikit-learn Pipeline 指南](https://www.google.com/search?q=scikit-learn+pipeline)
- [scikit-learn 模型選擇](https://www.google.com/search?q=scikit-learn+model+selection)

---

*本篇文章為「AI 程式人雜誌 2022 年 3 月號」歷史回顧系列之一。*
