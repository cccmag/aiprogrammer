# 邏輯迴歸與分類

## 問題設定

我們用一個經典問題示範邏輯迴歸：根據腫瘤的特徵判斷其為良性還是惡性。

## 資料準備

使用 scikit-learn 內建的乳癌資料集：

```python
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# 載入資料
data = load_breast_cancer()
X, y = data.data, data.target

print(f"資料形狀: {X.shape}")
print(f"類別: {data.target_names}")
```

## 訓練邏輯迴歸模型

```python
# 分割資料
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 建立模型
clf = LogisticRegression(max_iter=10000, random_state=42)
clf.fit(X_train, y_train)

# 預測
y_pred = clf.predict(X_test)
y_proba = clf.predict_proba(X_test)
```

## 評估結果

```python
acc = accuracy_score(y_test, y_pred)
print(f"準確率: {acc:.3f}")

print("混淆矩陣:")
print(confusion_matrix(y_test, y_pred))

print("\n分類報告:")
print(classification_report(y_test, y_pred, target_names=data.target_names))
```

## 機率預測

邏輯迴歸的一大優勢是能輸出機率：

```python
for i in range(5):
    prob = y_proba[i]
    pred = y_pred[i]
    print(f"樣本 {i}: 良性={prob[0]:.3f}, 惡性={prob[1]:.3f} → 預測={data.target_names[pred]}")
```

## 決策邊界可視化

為了可視化決策邊界，我們只使用兩個特徵：

```python
import numpy as np
import matplotlib.pyplot as plt

# 只使用前兩個特徵
X_2d = X[:, :2]
X_train_2d, X_test_2d, y_train_2d, y_test_2d = train_test_split(
    X_2d, y, test_size=0.2, random_state=42
)

clf_2d = LogisticRegression(max_iter=10000)
clf_2d.fit(X_train_2d, y_train_2d)

# 在二維平面上繪製決策邊界
x_min, x_max = X_2d[:, 0].min() - 1, X_2d[:, 0].max() + 1
y_min, y_max = X_2d[:, 1].min() - 1, X_2d[:, 1].max() + 1
xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.5),
                     np.arange(y_min, y_max, 0.5))

Z = clf_2d.predict(np.c_[xx.ravel(), yy.ravel()])
Z = Z.reshape(xx.shape)

plt.contourf(xx, yy, Z, alpha=0.8)
plt.scatter(X_2d[:, 0], X_2d[:, 1], c=y, edgecolors='k')
plt.xlabel(data.feature_names[0])
plt.ylabel(data.feature_names[1])
plt.title("邏輯迴歸決策邊界")
plt.show()
```

## 正則化

邏輯迴歸支援正則化防止過擬合：

```python
# L2 正則化（預設）
l2 = LogisticRegression(penalty='l2', C=1.0)

# L1 正則化（產生稀疏模型）
l1 = LogisticRegression(penalty='l1', solver='liblinear', C=1.0)

# ElasticNet（L1 + L2 混合）
enet = LogisticRegression(penalty='elasticnet', solver='saga', l1_ratio=0.5, C=1.0)
```

`C` 值是正則化強度的倒數。值越小，正則化越強，模型越簡單。

## 多類別分類

邏輯迴歸透過 OvR（One-vs-Rest）或 Softmax 支援多類別：

```python
# Softmax（多項式邏輯迴歸）
multi_clf = LogisticRegression(multi_class='multinomial', solver='lbfgs')
```

## 實作建議

- **標準化特徵**：邏輯迴歸對特徵尺度敏感
- **處理不平衡資料**：設定 `class_weight='balanced'`
- **收斂問題**：增加 `max_iter` 或使用不同的 solver
- **特徵選擇**：L1 正則化可以自動進行特徵選擇

邏輯迴歸雖然簡單，但在許多實際應用中表現出色，尤其適合需要機率解釋的場景。

---

## 延伸閱讀

- [scikit-learn 邏輯迴歸](https://www.google.com/search?q=scikit-learn+logistic+regression)
- [邏輯迴歸與正則化](https://www.google.com/search?q=logistic+regression+regularization)
- [多類別分類方法](https://www.google.com/search?q=multiclass+classification+ovr+softmax)
