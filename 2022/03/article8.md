# 特徵工程與預處理

## 資料決定上限

在機器學習領域有一個廣為流傳的說法：「更好的資料勝過更好的模型。」這正是特徵工程（Feature Engineering）的重要性所在。良好的特徵工程往往比複雜的模型更能提升預測效能。

## 資料清洗

特徵工程的第一步永遠是資料清洗：

```python
import pandas as pd
import numpy as np

df = pd.read_csv("raw_data.csv")

# 處理缺失值
df = df.dropna(subset=["critical_column"])
df["numeric_col"] = df["numeric_col"].fillna(df["numeric_col"].median())
df["categorical_col"] = df["categorical_col"].fillna("unknown")

# 處理異常值
def cap_outliers(series, n_std=3):
    mean, std = series.mean(), series.std()
    lower, upper = mean - n_std * std, mean + n_std * std
    return series.clip(lower, upper)

df["income"] = cap_outliers(df["income"])
```

## scikit-learn 預處理器

```python
from sklearn.preprocessing import (
    StandardScaler,
    MinMaxScaler,
    RobustScaler,
    OneHotEncoder,
    LabelEncoder,
    OrdinalEncoder,
)
```


### 標準化（Z-score）

```python
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
# 結果：平均值=0，標準差=1
```

### 歸一化（Min-Max）

```python
scaler = MinMaxScaler()
X_normalized = scaler.fit_transform(X)
# 結果：範圍 [0, 1]
```

### 穩健標準化（RobustScaler）

使用中位數和 IQR，對異常值更魯棒：

```python
scaler = RobustScaler()
X_robust = scaler.fit_transform(X)
```

## 類別變數編碼

```python
# One-Hot Encoding
encoder = OneHotEncoder(sparse_output=False, handle_unknown="ignore")
X_encoded = encoder.fit_transform(categorical_features)

# Label Encoding
encoder = LabelEncoder()
y_encoded = encoder.fit_transform(y)
```

## 數值轉換

```python
from sklearn.preprocessing import PowerTransformer, QuantileTransformer

# Box-Cox 轉換（要求正值）
pt = PowerTransformer(method="box-cox")
X_boxcox = pt.fit_transform(X_positive)

# 分位數轉換（任意分佈 → 均勻分佈或常態分佈）
qt = QuantileTransformer(output_distribution="normal")
X_quantile = qt.fit_transform(X)
```

## 特徵建立

```python
# 多項式特徵
from sklearn.preprocessing import PolynomialFeatures
poly = PolynomialFeatures(degree=2, include_bias=False)
X_poly = poly.fit_transform(X)

# 分箱
df["age_group"] = pd.cut(df["age"], bins=[0, 18, 35, 55, 100],
                          labels=["youth", "adult", "middle", "senior"])

# 交互特徵
df["income_per_age"] = df["income"] / df["age"]
```

## 特徵選擇

```python
from sklearn.feature_selection import (
    SelectKBest,
    SelectPercentile,
    f_classif,
    mutual_info_classif,
)

# 選擇 k 個最佳特徵
selector = SelectKBest(score_func=f_classif, k=5)
X_selected = selector.fit_transform(X, y)

# 特徵重要性
from sklearn.ensemble import RandomForestClassifier
rf = RandomForestClassifier()
rf.fit(X, y)
importances = pd.Series(rf.feature_importances_, index=feature_names)
```

## 延伸閱讀

- [scikit-learn 預處理文件](https://www.google.com/search?q=scikit-learn+preprocessing+tutorial)
- [特徵工程實務](https://www.google.com/search?q=feature+engineering+practical+guide)
- [Kaggle 特徵工程競賽技巧](https://www.google.com/search?q=Kaggle+feature+engineering)
