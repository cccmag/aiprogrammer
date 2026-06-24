# 文章 8：監督式學習基礎

## 前言

監督式學習是最常見的機器學習範式。本章節介紹監督式學習的核心概念與常見演算法。

## 監督式學習框架

訓練資料：
```
D = {(x₁, y₁), (x₂, y₂), ..., (xₙ, yₙ)}
```

目標：學習一個函數 f，使得 f(x) ≈ y

## 分類問題

輸出是離散的類別標籤。

### K 近鄰（K-Nearest Neighbors, KNN）

```python
from sklearn.neighbors import KNeighborsClassifier

model = KNeighborsClassifier(n_neighbors=5)
model.fit(X_train, y_train)
predictions = model.predict(X_test)
```

### 邏輯迴歸（Logistic Regression）

```python
from sklearn.linear_model import LogisticRegression

model = LogisticRegression()
model.fit(X_train, y_train)
predictions = model.predict(X_test)
```

### 決策樹（Decision Tree）

```python
from sklearn.tree import DecisionTreeClassifier

model = DecisionTreeClassifier(max_depth=10)
model.fit(X_train, y_train)
predictions = model.predict(X_test)
```

## 迴歸問題

輸出是連續的數值。

### 線性迴歸（Linear Regression）

```python
from sklearn.linear_model import LinearRegression

model = LinearRegression()
model.fit(X_train, y_train)
predictions = model.predict(X_test)
```

### 嶺迴歸（Ridge Regression）

帶 L2 正則化的線性迴歸，防止過擬合：

```python
from sklearn.linear_model import Ridge

model = Ridge(alpha=1.0)
model.fit(X_train, y_train)
```

## 模型評估指標

### 分類指標

```python
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

accuracy = accuracy_score(y_test, predictions)
precision = precision_score(y_test, predictions, average='weighted')
recall = recall_score(y_test, predictions, average='weighted')
f1 = f1_score(y_test, predictions, average='weighted')
```

### 迴歸指標

```python
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

mse = mean_squared_error(y_test, predictions)
mae = mean_absolute_error(y_test, predictions)
r2 = r2_score(y_test, predictions)
```

## 過擬合與欠擬合

### 過擬合（Overfitting）

模型擬合訓練資料太好，但泛化能力差。

解決方法：
- 增加訓練數據
- 正則化
- 減少模型複雜度
- Dropout

### 欠擬合（Underfitting）

模型連訓練資料都擬合不好。

解決方法：
- 增加模型複雜度
- 增加訓練輪數
- 增加特徵

## 總結

監督式學習涵蓋分類與迴歸問題。選擇適當的演算法與評估指標是解決實際問題的關鍵。

## 延伸閱讀

- https://www.google.com/search?q=supervised+learning+classification+regression
- https://www.google.com/search?q=overfitting+underfitting+machine+learning