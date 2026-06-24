# 管線與網格搜索

## 為什麼需要管線？

在真實的機器學習專案中，資料預處理和模型訓練是一個整體。傳統的做法是分別進行：
1. 標準化資料
2. 使用標準化後的資料訓練模型

但這種做法存在一個嚴重的問題：**資料洩漏（Data Leakage）**。如果在交叉驗證之前就對整個資料集進行標準化，驗證資料的訊息會洩漏到訓練過程中，導致效能評估過於樂觀。

## Pipeline 基本用法

```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.svm import SVC

pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("pca", PCA(n_components=10)),
    ("svm", SVC(kernel="rbf")),
])

pipeline.fit(X_train, y_train)
y_pred = pipeline.predict(X_test)
```

管線確保在交叉驗證的每次摺疊中，預處理器（如 StandardScaler）只使用訓練摺疊的資料來擬合。

## ColumnTransformer

真實資料集通常包含不同類型的特徵：

```python
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer

numeric_features = ["age", "salary", "years_experience"]
categorical_features = ["department", "education"]

preprocessor = ColumnTransformer([
    ("num", Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
    ]), numeric_features),
    ("cat", Pipeline([
        ("imputer", SimpleImputer(strategy="constant", fill_value="missing")),
        ("onehot", OneHotEncoder(handle_unknown="ignore")),
    ]), categorical_features),
])
```

## GridSearchCV 深入

```python
from sklearn.model_selection import GridSearchCV

pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("svm", SVC()),
])

param_grid = {
    "svm__C": [0.01, 0.1, 1, 10],
    "svm__gamma": [0.001, 0.01, 0.1, 1],
    "svm__kernel": ["rbf", "poly"],
}

grid = GridSearchCV(
    pipeline, param_grid,
    cv=5,
    scoring="f1_macro",
    n_jobs=-1,
    verbose=1,
)

grid.fit(X_train, y_train)
print(f"Best parameters: {grid.best_params_}")
print(f"Best CV score: {grid.best_score_:.3f}")
```

## RandomizedSearchCV

當參數空間很大時，隨機搜尋比網格搜尋更高效：

```python
from sklearn.model_selection import RandomizedSearchCV
from scipy.stats import loguniform, randint

param_dist = {
    "svm__C": loguniform(1e-3, 1e3),
    "svm__gamma": loguniform(1e-4, 1e1),
    "svm__kernel": ["rbf", "poly"],
}

random_search = RandomizedSearchCV(
    pipeline, param_dist,
    n_iter=50,
    cv=5,
    n_jobs=-1,
    random_state=42,
)
```

## 自訂轉換器

```python
from sklearn.base import BaseEstimator, TransformerMixin

class LogTransformer(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return np.log1p(X)

pipeline = Pipeline([
    ("log", LogTransformer()),
    ("scaler", StandardScaler()),
    ("model", RandomForestRegressor()),
])
```

## 管線的序列化

```python
import joblib

# 儲存完整管線
joblib.dump(grid.best_estimator_, "pipeline.pkl")

# 載入使用
loaded = joblib.load("pipeline.pkl")
loaded.predict(X_new)
```

## 延伸閱讀

- [scikit-learn Pipeline 教學](https://www.google.com/search?q=scikit-learn+pipeline+tutorial)
- [ColumnTransformer 文件](https://www.google.com/search?q=scikit-learn+ColumnTransformer)
- [GridSearchCV 最佳實踐](https://www.google.com/search?q=GridSearchCV+best+practices)
