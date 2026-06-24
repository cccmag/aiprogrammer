# Matplotlib 視覺化

## 基本繪圖

```python
import matplotlib.pyplot as plt
import numpy as np

# 簡單線圖
x = [1, 2, 3, 4, 5]
y = [2, 4, 6, 8, 10]

plt.plot(x, y)
plt.show()
```

## 常用圖表

### 散點圖

```python
x = np.random.rand(50)
y = np.random.rand(50)
colors = np.random.rand(50)
sizes = 100 * np.random.rand(50)

plt.scatter(x, y, c=colors, s=sizes, alpha=0.6)
plt.colorbar()
plt.show()
```

### 直方圖

```python
data = np.random.randn(1000)

plt.hist(data, bins=30, alpha=0.7, color='blue')
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.title('Histogram')
plt.show()
```

### 柱狀圖

```python
categories = ['A', 'B', 'C', 'D']
values = [3, 7, 2, 5]

plt.bar(categories, values, color=['red', 'green', 'blue', 'orange'])
plt.show()
```

### 子圖

```python
fig, axes = plt.subplots(2, 2, figsize=(10, 8))

# 第一個子圖
axes[0, 0].plot(x, y)
axes[0, 0].set_title('Line')

# 第二個子圖
axes[0, 1].scatter(x, y)
axes[0, 1].set_title('Scatter')

# 第三個子圖
axes[1, 0].hist(data, bins=20)
axes[1, 0].set_title('Histogram')

# 第四個子圖
axes[1, 1].bar(categories, values)
axes[1, 1].set_title('Bar')

plt.tight_layout()
plt.show()
```

## 自定義

```python
plt.figure(figsize=(10, 6))

plt.plot(x, y,
         color='red',
         linewidth=2,
         linestyle='--',
         marker='o',
         markersize=8,
         label='Data')

plt.xlabel('X Axis', fontsize=14)
plt.ylabel('Y Axis', fontsize=14)
plt.title('Customized Plot', fontsize=16)
plt.legend()
plt.grid(True, alpha=0.3)

plt.xlim(0, 6)
plt.ylim(0, 12)

plt.show()
```

## 3D 繪圖

```python
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

x = np.linspace(-5, 5, 100)
y = np.linspace(-5, 5, 100)
X, Y = np.meshgrid(x, y)
Z = np.sin(np.sqrt(X**2 + Y**2))

ax.plot_surface(X, Y, Z, cmap='viridis')
plt.show()
```

## 儲存圖表

```python
plt.savefig('plot.png', dpi=300, bbox_inches='tight')
plt.savefig('plot.pdf')
```

## 總結

Matplotlib 是 Python 資料視覺化的核心。掌握基本繪圖、 子圖佈局與自定義選項，可有效呈現資料分析結果。