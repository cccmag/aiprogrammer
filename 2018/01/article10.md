# Matplotlib 資料視覺化

## 簡介

Matplotlib 是 Python 最流行的資料視覺化庫，可用來建立各種靜態、動態、互動式的圖表。

## 安裝與基本使用

```bash
pip install matplotlib
```

```python
import matplotlib.pyplot as plt
import numpy as np

# 基本圖表
plt.plot([1, 2, 3, 4], [1, 4, 2, 3])
plt.show()
```

## 基本圖表類型

### 折線圖

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 100)
y = np.sin(x)

plt.figure(figsize=(10, 6))
plt.plot(x, y, 'b-', label='sin(x)', linewidth=2)
plt.xlabel('X 軸')
plt.ylabel('Y 軸')
plt.title('Sin 函式圖形')
plt.legend()
plt.grid(True)
plt.show()
```

### 散佈圖

```python
import matplotlib.pyplot as plt
import numpy as np

np.random.seed(42)
n = 50
x = np.random.rand(n) * 100
y = np.random.rand(n) * 100
colors = np.random.rand(n)
sizes = np.random.rand(n) * 500

plt.figure(figsize=(10, 6))
plt.scatter(x, y, c=colors, s=sizes, alpha=0.6, cmap='viridis')
plt.colorbar()
plt.xlabel('X 軸')
plt.ylabel('Y 軸')
plt.title('散佈圖範例')
plt.show()
```

### 長條圖

```python
import matplotlib.pyplot as plt

categories = ['Python', 'JavaScript', 'Java', 'C++', 'Go']
votes = [35, 25, 20, 15, 5]

plt.figure(figsize=(10, 6))
plt.bar(categories, votes, color=['yellowgreen', 'gold', 'lightcoral', 'lightskyblue', 'plum'])
plt.xlabel('程式語言')
plt.ylabel('投票數')
plt.title('最受歡迎程式語言')
plt.show()
```

### 圓餅圖

```python
import matplotlib.pyplot as plt

sizes = [30, 25, 20, 15, 10]
labels = ['Python', 'JavaScript', 'Java', 'C++', '其他']
colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#ff99cc']
explode = (0.1, 0, 0, 0, 0)  # 突出顯示第一塊

plt.figure(figsize=(10, 8))
plt.pie(sizes, explode=explode, labels=labels, colors=colors,
        autopct='%1.1f%%', shadow=True, startangle=90)
plt.title('程式語言使用分布')
plt.axis('equal')
plt.show()
```

### 直方圖

```python
import matplotlib.pyplot as plt
import numpy as np

np.random.seed(42)
data = np.random.normal(100, 15, 1000)  # 平均100, 標準差15

plt.figure(figsize=(10, 6))
plt.hist(data, bins=30, color='steelblue', edgecolor='black', alpha=0.7)
plt.xlabel('數值')
plt.ylabel('頻率')
plt.title('常態分布直方圖')
plt.show()
```

## 子圖（Subplots）

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 100)

fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# 子圖 1
axes[0, 0].plot(x, np.sin(x), 'b-')
axes[0, 0].set_title('Sin')

# 子圖 2
axes[0, 1].plot(x, np.cos(x), 'r-')
axes[0, 1].set_title('Cos')

# 子圖 3
axes[1, 0].plot(x, np.tan(x), 'g-')
axes[1, 0].set_title('Tan')
axes[1, 0].set_ylim(-5, 5)

# 子圖 4
axes[1, 1].plot(x, np.exp(x), 'm-')
axes[1, 1].set_title('Exp')
axes[1, 1].set_yscale('log')

plt.tight_layout()
plt.show()
```

## 進階設定

### 線條樣式

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 100)

plt.figure(figsize=(12, 6))
plt.plot(x, x, 'r-', label='solid', linewidth=2)
plt.plot(x, x+1, 'b--', label='dashed', linewidth=2)
plt.plot(x, x+2, 'g:', label='dotted', linewidth=2)
plt.plot(x, x+3, 'm-.', label='dashdot', linewidth=2)
plt.legend()
plt.grid(True)
plt.show()
```

### 文字與註解

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 100)
y = np.sin(x)

plt.figure(figsize=(12, 6))
plt.plot(x, y)

# 添加文字
plt.text(5, 0.5, 'y = sin(x)', fontsize=14, ha='center')

# 添加註解
plt.annotate('峰值', xy=(np.pi/2, 1), xytext=(np.pi/2+1, 0.5),
             arrowprops=dict(arrowstyle='->', color='red'),
             fontsize=12)

plt.grid(True)
plt.show()
```

### 雙 Y 軸

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 100)
y1 = np.sin(x)
y2 = np.exp(x)

fig, ax1 = plt.subplots(figsize=(12, 6))

color = 'tab:blue'
ax1.set_xlabel('X 軸')
ax1.set_ylabel('sin(x)', color=color)
ax1.plot(x, y1, color=color)
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()
color = 'tab:red'
ax2.set_ylabel('exp(x)', color=color)
ax2.plot(x, y2, color=color)
ax2.tick_params(axis='y', labelcolor=color)

plt.title('雙 Y 軸範例')
fig.tight_layout()
plt.show()
```

## 保存圖表

```python
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))
plt.plot([1, 2, 3], [1, 4, 2])
plt.title('保存圖表示例')

# 保存為 PNG
plt.savefig('plot.png', dpi=300, bbox_inches='tight')

# 保存為 PDF
plt.savefig('plot.pdf')

plt.close()
```

## 中文顯示

```python
import matplotlib.pyplot as plt

# 設定中文字體
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False

plt.figure(figsize=(10, 6))
plt.title('中文標題')
plt.xlabel('X 軸')
plt.ylabel('Y 軸')
plt.plot([1, 2, 3], [1, 4, 2])
plt.show()
```

## 練習題

1. 繪製一個包含三條線的折線圖
2. 創建一個散佈圖，根據資料大小調整點的大小
3. 繪製資料分布的直方圖
4. 使用子圖顯示四種不同的圖表類型