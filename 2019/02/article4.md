# 線性迴歸實作

## 線性迴歸概念

線性迴歸尋找輸入特徵與連續輸出之間的線性關係。

## 從零實作線性迴歸

```python
import numpy as np

class LinearRegression:
    def __init__(self, learning_rate=0.01, n_iterations=1000):
        self.lr = learning_rate
        self.n_iterations = n_iterations
        self.weights = None
        self.bias = None

    def fit(self, X, y):
        n_samples, n_features = X.shape
        self.weights = np.zeros(n_features)
        self.bias = 0

        for _ in range(self.n_iterations):
            y_pred = np.dot(X, self.weights) + self.bias

            dw = (1/n_samples) * np.dot(X.T, (y_pred - y))
            db = (1/n_samples) * np.sum(y_pred - y)

            self.weights -= self.lr * dw
            self.bias -= self.lr * db

    def predict(self, X):
        return np.dot(X, self.weights) + self.bias
```

## 使用實作

```python
np.random.seed(42)
X = 2 * np.random.rand(100, 1)
y = 4 + 3 * X + np.random.randn(100, 1)

model = LinearRegression(learning_rate=0.1, n_iterations=1000)
model.fit(X, y.ravel())

print(f"預期參數: 截距=4, 斜率=3")
print(f"實際參數: 截距={model.bias:.2f}, 斜率={model.weights[0]:.2f}")

X_new = np.array([[0], [2]])
y_pred = model.predict(X_new)
print(f"預測值: {y_pred}")
```

## 使用 scikit-learn

```python
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = LinearRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"均方誤差: {mse:.4f}")
print(f"R² 分數: {r2:.4f}")
print(f"係數: {model.coef_}")
print(f"截距: {model.intercept_}")
```

## 多元線性迴歸

```python
from sklearn.datasets import make_regression

X, y = make_regression(n_samples=100, n_features=5, noise=10, random_state=42)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = LinearRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

print(f"R² 分數: {r2_score(y_test, y_pred):.4f}")
```

## 多項式迴歸

```python
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline

X = np.linspace(0, 4, 50).reshape(-1, 1)
y = 2 * X**2 + 3 * X + 1 + np.random.randn(50, 1) * 5

degrees = [1, 2, 5]
for degree in degrees:
    model = make_pipeline(PolynomialFeatures(degree), LinearRegression())
    model.fit(X, y)
    y_pred = model.predict(X)

    mse = mean_squared_error(y, y_pred)
    print(f"Degree {degree}: MSE = {mse:.2f}")
```

## 正規化線性迴歸

### Ridge 迴歸

```python
from sklearn.linear_model import Ridge

ridge = Ridge(alpha=1.0)
ridge.fit(X_train, y_train)
print(f"Ridge 係數: {ridge.coef_}")
```

### Lasso 迴歸

```python
from sklearn.linear_model import Lasso

lasso = Lasso(alpha=0.1)
lasso.fit(X_train, y_train)
print(f"Lasso 係數: {lasso.coef_}")
```

### ElasticNet

```python
from sklearn.linear_model import ElasticNet

elastic = ElasticNet(alpha=0.1, l1_ratio=0.5)
elastic.fit(X_train, y_train)
print(f"ElasticNet 係數: {elastic.coef_}")
```

## 視覺化

```python
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))
plt.scatter(X, y, color='blue', alpha=0.5, label='資料點')
plt.plot(X_new, y_pred, color='red', linewidth=2, label='預測線')
plt.xlabel('X')
plt.ylabel('y')
plt.title('線性迴歸')
plt.legend()
plt.show()
```

## 參考資源

- https://www.google.com/search?q=linear+regression+Python+implementation+from+scratch+2019
- https://www.google.com/search?q=scikit-learn+linear+regression+Ridge+Lasso+ElasticNet+2019
- https://www.google.com/search?q=polynomial+regression+Python+scikit-learn+tutorial+2019