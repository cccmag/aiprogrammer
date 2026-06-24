# 6. 模型評估與驗證

## 模型評估的重要性

正確評估模型效能對於選擇最佳模型、避免過擬合至關重要。本章介紹各種評估方法與指標。

## 訓練/測試分割

```python
from sklearn.model_selection import train_test_split
from sklearn.datasets import make_classification

X, y = make_classification(n_samples=1000, n_features=20,
                           random_state=42, flip_y=0.05)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"訓練集: {X_train.shape[0]} 樣本")
print(f"測試集: {X_test.shape[0]} 樣本")
```

## 交叉驗證（Cross-Validation）

### K 折交叉驗證

```python
from sklearn.model_selection import cross_val_score, KFold
from sklearn.linear_model import LogisticRegression

model = LogisticRegression(max_iter=1000)

scores = cross_val_score(model, X, y, cv=5)
print(f"5折交叉驗證分數: {scores}")
print(f"平均分數: {scores.mean():.2%}")
print(f"標準差: {scores.std():.2%}")
```

### 分層 K 折交叉驗證

```python
from sklearn.model_selection import StratifiedKFold

skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
scores = cross_val_score(model, X, y, cv=skf)
print(f"分層5折交叉驗證: {scores}")
```

### 留一法交叉驗證（LOOCV）

```python
from sklearn.model_selection import LeaveOneOut

loo = LeaveOneOut()
scores = cross_val_score(model, X, y, cv=loo)
print(f"LOOCV 平均分數: {scores.mean():.2%}")
```

## 混淆矩陣

```python
from sklearn.metrics import confusion_matrix
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression

X, y = make_classification(n_samples=200, n_features=10, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

cm = confusion_matrix(y_test, y_pred)
print(f"混淆矩陣:\n{cm}")
```

## ROC 曲線與 AUC

```python
from sklearn.metrics import roc_curve, auc, roc_auc_score
import matplotlib.pyplot as plt

y_prob = model.predict_proba(X_test)[:, 1]
fpr, tpr, thresholds = roc_curve(y_test, y_prob)
roc_auc = auc(fpr, tpr)

plt.figure(figsize=(8, 6))
plt.plot(fpr, tpr, color='darkorange', lw=2,
         label=f'ROC curve (AUC = {roc_auc:.2f})')
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve')
plt.legend()
plt.grid(True)
plt.show()

print(f"AUC 分數: {roc_auc:.2%}")
```

## 學習曲線

```python
import numpy as np
from sklearn.model_selection import learning_curve
import matplotlib.pyplot as plt

train_sizes, train_scores, test_scores = learning_curve(
    LogisticRegression(max_iter=1000), X, y,
    train_sizes=np.linspace(0.1, 1.0, 10),
    cv=5, scoring='accuracy'
)

train_mean = train_scores.mean(axis=1)
train_std = train_scores.std(axis=1)
test_mean = test_scores.mean(axis=1)
test_std = test_scores.std(axis=1)

plt.figure(figsize=(8, 6))
plt.plot(train_sizes, train_mean, 'o-', color='r', label='Training score')
plt.plot(train_sizes, test_mean, 'o-', color='g', label='Cross-validation score')
plt.fill_between(train_sizes, train_mean - train_std, train_mean + train_std, alpha=0.1, color='r')
plt.fill_between(train_sizes, test_mean - test_std, test_mean + test_std, alpha=0.1, color='g')
plt.xlabel('Training Size')
plt.ylabel('Accuracy')
plt.title('Learning Curve')
plt.legend()
plt.grid(True)
plt.show()
```

## 驗證曲線

```python
from sklearn.model_selection import validation_curve

param_range = [0.001, 0.01, 0.1, 1, 10, 100]
train_scores, test_scores = validation_curve(
    LogisticRegression(max_iter=1000), X, y,
    param_name='C', param_range=param_range, cv=5
)

plt.figure(figsize=(8, 6))
plt.semilogx(param_range, train_scores.mean(axis=1), 'o-', label='Training score')
plt.semilogx(param_range, test_scores.mean(axis=1), 'o-', label='Cross-validation score')
plt.xlabel('C')
plt.ylabel('Score')
plt.title('Validation Curve')
plt.legend()
plt.grid(True)
plt.show()
```

## 過擬合與欠擬合

- **過擬合（Overfitting）**：模型在訓練集表現良好但在測試集表現差
- **欠擬合（Underfitting）**：模型在訓練集與測試集都表現不佳

處理方法：

```python
from sklearn.linear_model import Ridge
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import Pipeline

degrees = [1, 3, 15]
for degree in degrees:
    model = Pipeline([
        ('poly', PolynomialFeatures(degree)),
        ('ridge', Ridge(alpha=0.1))
    ])
    scores = cross_val_score(model, X, y, cv=5)
    print(f"Degree {degree}: {scores.mean():.2%}")
```

## 參考資源

- https://www.google.com/search?q=model+evaluation+machine+learning+cross+validation+Python+2019
- https://www.google.com/search?q=confusion+matrix+ROC+curve+AUC+Python+scikit-learn+2019
- https://www.google.com/search?q=overfitting+underfitting+learning+curve+validation+curve+2019