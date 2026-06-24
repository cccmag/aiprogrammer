# 文章 5：資料視覺化與 Matplotlib

## 前言

Matplotlib 是 Python 最流行的資料視覺化庫。本章節介紹 Matplotlib 的基本用法，幫助讀者建立視覺化能力。

## 基本繪圖

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 2*np.pi, 100)
y = np.sin(x)

plt.figure(figsize=(10, 6))
plt.plot(x, y)
plt.xlabel('x')
plt.ylabel('sin(x)')
plt.title('Sine Wave')
plt.grid(True)
plt.show()
```

## 圖表類型

### 散點圖

```python
plt.scatter(x, y, c=labels, cmap='viridis')
plt.colorbar()
```

### 長條圖

```python
categories = ['A', 'B', 'C', 'D']
values = [10, 25, 15, 30]
plt.bar(categories, values)
```

### 直方圖

```python
data = np.random.randn(1000)
plt.hist(data, bins=30, edgecolor='black')
```

### 子圖

```python
fig, axes = plt.subplots(2, 2, figsize=(12, 8))

axes[0, 0].plot(x, np.sin(x))
axes[0, 1].plot(x, np.cos(x))
axes[1, 0].plot(x, np.tan(x))
axes[1, 1].plot(x, x**2)

plt.tight_layout()
```

## 樣式設定

```python
plt.style.use('seaborn-v0_8-darkgrid')

plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['font.size'] = 12
plt.rcParams['lines.linewidth'] = 2
```

## 機器學習視覺化

### 損失曲線

```python
epochs = range(1, 101)
train_loss = [...]
val_loss = [...]

plt.plot(epochs, train_loss, label='Training Loss')
plt.plot(epochs, val_loss, label='Validation Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()
plt.title('Training Progress')
```

### 決策邊界

```python
def plot_decision_boundary(model, X, y):
    h = 0.02
    x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                         np.arange(y_min, y_max, h))
    Z = model.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)
    plt.contourf(xx, yy, Z, alpha=0.4)
    plt.scatter(X[:, 0], X[:, 1], c=y)
```

## 儲存圖表

```python
plt.savefig('figure.png', dpi=300, bbox_inches='tight')
plt.savefig('figure.pdf')
```

## 總結

Matplotlib 是資料科學不可或缺的工具。良好的視覺化能幫助理解模型行為與數據特性。

## 延伸閱讀

- https://www.google.com/search?q=Matplotlib+tutorial+Python+visualization
- https://www.google.com/search?q=matplotlib+machine+learning+plots