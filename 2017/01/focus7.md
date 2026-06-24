# Python 在 AI 領域的應用：深度學習前的準備工作

## 前言

Python 是 AI 和機器學習領域最流行的程式語言。本篇文章介紹 Python 生態系中與 AI 相關的核心工具，以及在學習 TensorFlow 等深度學習框架之前需要掌握的 Python 技能。

## AI 開發環境的 Python 棧

### 必需的基礎技能

```
Python 基礎
    ├── 語法和資料結構
    ├── 函式和模組
    ├── 物件導向編程
    └── 檔案和網路操作

科學計算
    ├── NumPy（陣列運算）
    ├── SciPy（科學計算）
    └── Pandas（資料處理）

機器學習
    ├── scikit-learn（傳統 ML）
    ├── Matplotlib（視覺化）
    └── 統計基礎

深度學習
    ├── TensorFlow / Theano
    ├── Keras（高層 API）
    └── PyTorch（動態計算圖）
```

## NumPy：深度學習的基礎

### 為什麼深度學習需要 NumPy？

深度學習涉及大量的矩陣和張量運算，NumPy 提供了高效的实现：

```python
import numpy as np

# 模擬神經網路的權重
W = np.random.randn(784, 128) * 0.01  # 輸入層到隱藏層
b = np.zeros((1, 128))                  # 偏差項

# 類神經網路前向傳播
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def relu(x):
    return np.maximum(0, x)

# 輸入（模擬 64 個樣本，每個 784 維）
X = np.random.randn(64, 784)

# 線性變換 + 激活函數
Z1 = np.dot(X, W) + b
A1 = relu(Z1)

print(f"Input shape: {X.shape}")
print(f"Weights shape: {W.shape}")
print(f"Output shape: {A1.shape}")
```

### 常見的深度學習運算

```python
import numpy as np

# Softmax 函數（分類網路輸出層）
def softmax(x):
    exp_x = np.exp(x - np.max(x, axis=1, keepdims=True))
    return exp_x / np.sum(exp_x, axis=1, keepdims=True)

# 交叉熵損失
def cross_entropy_loss(y_pred, y_true):
    m = y_true.shape[0]
    p = np.clip(y_pred, 1e-10, 1 - 1e-10)
    return -np.sum(y_true * np.log(p)) / m

# L2 正規化
def l2_regularization(weights, lambda_):
    return lambda_ * np.sum(weights ** 2) / 2
```

## Matplotlib：視覺化神經網路訓練

### 訓練過程視覺化

```python
import matplotlib.pyplot as plt

# 模擬訓練過程
epochs = range(1, 101)
train_loss = [1.0 / e + np.random.randn() * 0.1 for e in epochs]
val_loss = [1.2 / e + np.random.randn() * 0.15 for e in epochs]
train_acc = [1 - 0.5/e + np.random.randn() * 0.02 for e in epochs]
val_acc = [1 - 0.6/e + np.random.randn() * 0.03 for e in epochs]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

# 損失曲線
ax1.plot(epochs, train_loss, 'b-', label='Training Loss')
ax1.plot(epochs, val_loss, 'r-', label='Validation Loss')
ax1.set_xlabel('Epoch')
ax1.set_ylabel('Loss')
ax1.set_title('Training and Validation Loss')
ax1.legend()
ax1.grid(True)

# 準確率曲線
ax2.plot(epochs, train_acc, 'b-', label='Training Accuracy')
ax2.plot(epochs, val_acc, 'r-', label='Validation Accuracy')
ax2.set_xlabel('Epoch')
ax2.set_ylabel('Accuracy')
ax2.set_title('Training and Validation Accuracy')
ax2.legend()
ax2.grid(True)

plt.tight_layout()
plt.show()
```

## scikit-learn：機器學習基礎

### 機器學習工作流

```python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

# 生成模擬數據
np.random.seed(42)
X = np.random.randn(200, 2)
y = (X[:, 0] + X[:, 1] > 0).astype(int)
X[y == 1] += 2

# 分割數據
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 標準化
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# 訓練模型
model = LogisticRegression()
model.fit(X_train, y_train)

# 預測和評估
y_pred = model.predict(X_test)
print(f"Accuracy: {accuracy_score(y_test, y_pred):.3f}")
print(classification_report(y_test, y_pred))
```

### 常用的 ML 演算法

| 演算法 | 用途 | sklearn 類別 |
|--------|------|-------------|
| 線性迴歸 | 迴歸 | `LinearRegression` |
| 羅吉斯迴歸 | 分類 | `LogisticRegression` |
| 決策樹 | 分類/迴歸 | `DecisionTreeClassifier` |
| 隨機森林 | 分類/迴歸 | `RandomForestClassifier` |
| SVM | 分類 | `SVC` |
| K-means | 聚類 | `KMeans` |
| PCA | 降維 | `PCA` |

## 深度學習框架前的準備

### TensorFlow 1.0（2017 年 2 月發布）

在學習 TensorFlow 之前，需要熟悉：

1. Python 基礎知識
2. NumPy 陣列操作
3. 基本的線性代數（矩陣乘法、向量）
4. 基本的微積分概念（梯度、導數）

```python
# TensorFlow 1.0 的基本語法
import tensorflow as tf

# 創建常數
a = tf.constant(2)
b = tf.constant(3)

# 運算
c = a + b

# Session 是 TensorFlow 1.x 的核心概念
with tf.Session() as sess:
    result = sess.run(c)
    print(f"Result: {result}")
```

### Keras：高層 API 的便利

Keras 以其簡潔的 API 設計降低了深度學習的門檻：

```python
# Keras 順序模型
from keras.models import Sequential
from keras.layers import Dense, Dropout

model = Sequential([
    Dense(128, activation='relu', input_shape=(784,)),
    Dropout(0.2),
    Dense(64, activation='relu'),
    Dense(10, activation='softmax')
])

model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)
```

## 結論

Python 為 AI 開發提供了完整的工具鏈：

1. **NumPy**：矩陣和張量運算的基礎
2. **Matplotlib**：資料和模型訓練的視覺化
3. **scikit-learn**：傳統機器學習的完整解決方案
4. **Pandas**：資料處理和預處理
5. **TensorFlow/Keras**：深度學習框架

建議的學習路徑：
- Python 基礎 → NumPy → Matplotlib → Pandas
- 統計基礎 → scikit-learn → 機器學習理論
- 深度學習理論 → Keras/TensorFlow → 實作專案

---

## 延伸閱讀

- [NumPy 深度學習教程](https://www.google.com/search?q=NumPy+deep+learning+tutorial)
- [scikit-learn 教程](https://www.google.com/search?q=scikit-learn+tutorial+machine+learning+Python)
- [Keras 官方教程](https://www.google.com/search?q=Keras+tutorial+deep+learning+Python)
- [深度學習+Python+入門](https://www.google.com/search?q=deep+learning+Python+tutorial+2017)

---

*本篇文章為「AI 程式人雜誌 2017 年 1 月號」焦點系列之一。*