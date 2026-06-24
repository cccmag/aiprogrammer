# 2. 監督式學習基礎

## 監督式學習概念

監督式學習是機器學習中最常見的類型。訓練資料包含輸入特徵與對應的正確輸出（標籤），模型學習輸入與輸出之間的映射關係。

## 分類問題

分類問題的目標是預測類別標籤。

### 二分類（Binary Classification）

```python
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

X, y = make_classification(n_samples=1000, n_features=2,
                           n_informative=2, n_redundant=0,
                           random_state=42)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

clf = LogisticRegression()
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)

print(f"準確率: {accuracy_score(y_test, y_pred):.2%}")
print(classification_report(y_test, y_pred))
```

### 多分類（Multiclass Classification）

```python
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier

iris = load_iris()
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(iris.data, iris.target)

predictions = clf.predict(iris.data[:5])
print(f"預測類別: {predictions}")
print(f"實際類別: {iris.target[:5]}")
```

## 迴歸問題

迴歸問題的目標是預測連續數值。

### 線性迴歸（Linear Regression）

```python
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

np.random.seed(42)
X = np.random.randn(100, 1) * 2
y = 3 * X + 5 + np.random.randn(100, 1) * 2

model = LinearRegression()
model.fit(X, y)

print(f"斜率: {model.coef_[0][0]:.2f}")
print(f"截距: {model.intercept_[0]:.2f}")

X_new = np.array([[1], [2], [3]])
y_pred = model.predict(X_new)
print(f"預測值: {y_pred.flatten()}")
```

### 多項式迴歸（Polynomial Regression）

```python
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline

degree = 3
model = make_pipeline(PolynomialFeatures(degree), LinearRegression())
model.fit(X, y)

X_test = np.linspace(-5, 5, 100).reshape(-1, 1)
y_pred = model.predict(X_test)
```

## 常見分類演算法

| 演算法 | 適用場景 | 優點 |
|--------|----------|------|
| 邏輯斯迴歸 | 二分類 | 機率輸出，可解釋性 |
| 決策樹 | 多類分類 | 可解釋，處理類別特徵 |
| SVM | 高維資料 | 泛化能力強 |
| KNN | 小型資料集 | 簡單，無訓練過程 |
| 隨機森林 | 大型資料 | 抗過擬合 |

## 模型評估指標

### 分類指標

- **準確率（Accuracy）**：正確預測的比例
- **精確率（Precision）**：預測為正的樣本中真正為正的比例
- **召回率（Recall）**：所有正樣本中被正確預測的比例
- **F1 分數**：精確率與召回率的調和平均

```python
from sklearn.metrics import precision_score, recall_score, f1_score

precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)

print(f"精確率: {precision:.2%}")
print(f"召回率: {recall:.2%}")
print(f"F1 分數: {f1:.2%}")
```

### 迴歸指標

- **MAE（Mean Absolute Error）**：平均絕對誤差
- **MSE（Mean Squared Error）**：均方誤差
- **R²（R-squared）**：決定係數

```python
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"MAE: {mae:.2f}")
print(f"MSE: {mse:.2f}")
print(f"R²: {r2:.2%}")
```

## 參考資源

- https://www.google.com/search?q=supervised+learning+classification+regression+Python+scikit-learn+2019
- https://www.google.com/search?q=logistic+regression+linear+regression+scikit-learn+example+2019
- https://www.google.com/search?q=machine+learning+evaluation+metrics+accuracy+precision+recall+f1+2019