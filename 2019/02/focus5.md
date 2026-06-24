# 5. 資料預處理

## 資料預處理的重要性

機器學習模型的效能很大程度上取決於資料品質。資料預處理是機器學習工作流程中最耗時但也最關鍵的步驟。

## 處理缺失值

### 刪除缺失值

```python
import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer

df = pd.DataFrame({
    'A': [1, 2, np.nan, 4],
    'B': [5, np.nan, np.nan, 8],
    'C': [9, 10, 11, 12]
})

print(f"缺失值數量:\n{df.isnull().sum()}")

imputer = SimpleImputer(strategy='mean')
df_imputed = pd.DataFrame(
    imputer.fit_transform(df),
    columns=df.columns
)
print(f"填補後:\n{df_imputed}")
```

### 常見填補策略

```python
from sklearn.impute import SimpleImputer

strategies = ['mean', 'median', 'most_frequent', 'constant']
for strategy in strategies:
    imputer = SimpleImputer(strategy=strategy)
    result = imputer.fit_transform(df)
    print(f"{strategy}: {result[1]}")
```

## 特徵縮放

### 標準化（Standardization）

將特徵調整為均值為 0、標準差為 1 的分佈。

```python
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print(f"標準化後均值: {X_scaled.mean(axis=0)}")
print(f"標準化後標準差: {X_scaled.std(axis=0)}")
```

### 歸一化（Normalization）

將特徵縮放到指定範圍（通常是 0 到 1）。

```python
from sklearn.preprocessing import MinMaxScaler

normalizer = MinMaxScaler()
X_normalized = normalizer.fit_transform(X_train)
print(f"歸一化後範圍: [{X_normalized.min()}, {X_normalized.max()}]")
```

### RobustScaler

對異常值更具魯棒性的縮放方法。

```python
from sklearn.preprocessing import RobustScaler

robust = RobustScaler()
X_robust = robust.fit_transform(X_train)
```

## 類別特徵編碼

### 標籤編碼（Label Encoding）

```python
from sklearn.preprocessing import LabelEncoder

labels = ['貓', '狗', '鳥', '貓', '狗']
encoder = LabelEncoder()
encoded = encoder.fit_transform(labels)
print(f"編碼結果: {encoded}")
print(f"類別映射: {dict(zip(encoder.classes_, range(len(encoder.classes_))))}")
```

### 獨熱編碼（One-Hot Encoding）

```python
from sklearn.preprocessing import OneHotEncoder
import numpy as np

categories = np.array([['紅'], ['藍'], ['綠'], ['藍']]).reshape(-1, 1)
encoder = OneHotEncoder(sparse_output=False)
onehot = encoder.fit_transform(categories)
print(f"獨熱編碼:\n{onehot}")
```

### pandas get_dummies

```python
df = pd.DataFrame({'顏色': ['紅', '藍', '綠', '藍']})
df_encoded = pd.get_dummies(df, columns=['顏色'])
print(df_encoded)
```

## 訓練/測試集分割

```python
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print(f"訓練集大小: {len(X_train)}")
print(f"測試集大小: {len(X_test)}")
```

## 處理類別不平衡

```python
from sklearn.utils import resample
from sklearn.datasets import make_classification

X, y = make_classification(n_samples=1000, weights=[0.9, 0.1], random_state=42)

X_majority = X[y == 0]
X_minority = X[y == 1]
y_majority = y[y == 0]
y_minority = y[y == 1]

X_minority_upsampled = resample(
    X_minority, y_minority,
    replace=True, n_samples=len(X_majority), random_state=42
)

X_balanced = np.vstack([X_majority, X_minority_upsampled])
y_balanced = np.hstack([y_majority, np.ones(len(X_minority_upsampled))])
```

## 特徵選擇

```python
from sklearn.feature_selection import SelectKBest, f_classif

selector = SelectKBest(f_classif, k=3)
X_selected = selector.fit_transform(X_train, y_train)
X_test_selected = selector.transform(X_test)

print(f"選擇的特徵索引: {selector.get_support(indices=True)}")
print(f"特徵分數: {selector.scores_}")
```

## 參考資源

- https://www.google.com/search?q=data+preprocessing+machine+learning+Python+scikit-learn+2019
- https://www.google.com/search?q=feature+scaling+standardization+normalization+Python+2019
- https://www.google.com/search?q=one+hot+encoding+label+encoding+Python+pandas+scikit+2019