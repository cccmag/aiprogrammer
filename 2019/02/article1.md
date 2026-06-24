# 資料視覺化基礎

## Matplotlib 簡介

Matplotlib 是 Python 最廣泛使用的資料視覺化庫，可以建立各種靜態、動態與互動式圖表。

## 基本繪圖

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 2 * np.pi, 100)
y = np.sin(x)

plt.figure(figsize=(10, 6))
plt.plot(x, y, 'b-', linewidth=2)
plt.title('Sin Wave')
plt.xlabel('x')
plt.ylabel('sin(x)')
plt.grid(True)
plt.show()
```

## 子圖（Subplots）

```python
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

x = np.linspace(0, 4 * np.pi, 100)

axes[0, 0].plot(x, np.sin(x))
axes[0, 0].set_title('sin(x)')

axes[0, 1].plot(x, np.cos(x), 'r-')
axes[0, 1].set_title('cos(x)')

axes[1, 0].plot(x, np.tan(x))
axes[1, 0].set_title('tan(x)')
axes[1, 0].set_ylim(-5, 5)

axes[1, 1].plot(x, np.exp(-x/10) * np.sin(x))
axes[1, 1].set_title('Damped Sine')

plt.tight_layout()
plt.show()
```

## 散點圖（Scatter Plot）

```python
np.random.seed(42)
x = np.random.randn(100)
y = np.random.randn(100)
colors = np.random.rand(100)
sizes = 100 * np.random.rand(100)

plt.figure(figsize=(10, 8))
scatter = plt.scatter(x, y, c=colors, s=sizes, alpha=0.6, cmap='viridis')
plt.colorbar(scatter, label='Color Scale')
plt.title('Scatter Plot with Colors and Sizes')
plt.xlabel('X')
plt.ylabel('Y')
plt.grid(True)
plt.show()
```

## 長條圖（Bar Chart）

```python
categories = ['Python', 'JavaScript', 'Java', 'C++', 'Go']
popularity = [29.8, 17.9, 15.4, 7.8, 5.6]

plt.figure(figsize=(10, 6))
bars = plt.bar(categories, popularity, color=['#3776ab', '#f7df1e', '#ed8b00', '#00599c', '#00add8'])
plt.title('Programming Language Popularity 2019')
plt.xlabel('Language')
plt.ylabel('Popularity (%)')
plt.xticks(rotation=45)

for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height,
            f'{height:.1f}%', ha='center', va='bottom')

plt.tight_layout()
plt.show()
```

## 直方圖（Histogram）

```python
np.random.seed(42)
data = np.random.normal(loc=170, scale=10, size=1000)

plt.figure(figsize=(10, 6))
plt.hist(data, bins=30, color='steelblue', edgecolor='white', alpha=0.7)
plt.title('Height Distribution')
plt.xlabel('Height (cm)')
plt.ylabel('Frequency')
plt.axvline(data.mean(), color='red', linestyle='--', label=f'Mean: {data.mean():.1f}')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()
```

## 箱線圖（Box Plot）

```python
np.random.seed(42)
data = [np.random.normal(0, std, 100) for std in range(1, 5)]

plt.figure(figsize=(10, 6))
bp = plt.boxplot(data, labels=['Group 1', 'Group 2', 'Group 3', 'Group 4'],
                 patch_artist=True)
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
for patch, color in zip(bp['boxes'], colors):
    patch.set_facecolor(color)
    patch.set_alpha(0.6)

plt.title('Box Plot Example')
plt.ylabel('Value')
plt.grid(True, alpha=0.3)
plt.show()
```

## 熱力圖（Heatmap）

```python
import pandas as pd

data = np.random.rand(10, 10)
df = pd.DataFrame(data, index=[f'Row {i}' for i in range(10)],
                  columns=[f'Col {i}' for i in range(10)])

plt.figure(figsize=(10, 8))
plt.imshow(df.values, cmap='YlOrRd')
plt.colorbar(label='Value')
plt.xticks(range(10), df.columns, rotation=45)
plt.yticks(range(10), df.index)
plt.title('Heatmap Example')

for i in range(10):
    for j in range(10):
        plt.text(j, i, f'{data[i, j]:.2f}', ha='center', va='center',
                color='white' if data[i, j] > 0.7 else 'black')

plt.tight_layout()
plt.show()
```

## 3D 繪圖

```python
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

X = np.arange(-5, 5, 0.25)
Y = np.arange(-5, 5, 0.25)
X, Y = np.meshgrid(X, Y)
Z = np.sin(np.sqrt(X**2 + Y**2))

surf = ax.plot_surface(X, Y, Z, cmap='coolwarm')
fig.colorbar(surf, shrink=0.5, aspect=5)
ax.set_title('3D Surface Plot')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
plt.show()
```

## 保存圖表

```python
plt.savefig('plot.png', dpi=300, bbox_inches='tight')
plt.savefig('plot.pdf', bbox_inches='tight')
plt.savefig('plot.svg', format='svg')
```

## 參考資源

- https://www.google.com/search?q=matplotlib+tutorial+Python+visualization+2019
- https://www.google.com/search?q=matplotlib+scatter+plot+bar+chart+histogram+Python+2019
- https://www.google.com/search?q=matplotlib+3d+plot+heatmap+Python+tutorial+2019