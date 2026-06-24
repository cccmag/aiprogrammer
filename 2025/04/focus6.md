# Matplotlib 資料可視化

## 為什麼需要可視化

人類的大腦擅長處理視覺資訊。一張設計良好的圖表，可以傳達數千行數字無法表達的洞察。從趨勢分析到異常值偵測，從分佈觀察到關聯性探索，可視化是資料分析不可或缺的一環。

## 繪圖基本流程

Matplotlib 提供了兩種使用風格：MATLAB 風格的 `pyplot` 介面，以及物件導向的 API。

```python
import matplotlib.pyplot as plt
import numpy as np

# 準備資料
x = np.linspace(0, 10, 100)
y = np.sin(x)

# 繪圖
plt.figure(figsize=(8, 4))
plt.plot(x, y, label="sin(x)", color="blue", linewidth=2)
plt.title("正弦曲線")
plt.xlabel("x")
plt.ylabel("sin(x)")
plt.legend()
plt.grid(True)
plt.show()
```

## 物件導向 API

對於複雜的圖表，物件導向 API 提供了更精細的控制：

```python
fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(x, y, label="sin(x)")
ax.set_title("正弦曲線")
ax.set_xlabel("x")
ax.legend()
ax.grid(True)
```

## 子圖與佈局

```python
# 建立 2x2 子圖
fig, axes = plt.subplots(2, 2, figsize=(10, 8))

# 在不同子圖上繪圖
axes[0, 0].plot(x, np.sin(x))
axes[0, 0].set_title("sin(x)")

axes[0, 1].plot(x, np.cos(x))
axes[0, 1].set_title("cos(x)")

axes[1, 0].plot(x, np.sin(x) * np.exp(-x * 0.1))
axes[1, 0].set_title("damped sin(x)")

axes[1, 1].scatter(x, np.sin(x) + np.random.randn(100) * 0.1)
axes[1, 1].set_title("noisy sin(x)")

plt.tight_layout()
plt.show()
```

## 常見圖表類型

### 折線圖 — 趨勢展示

```python
plt.plot(dates, values, marker="o", linestyle="-")
```

### 長條圖 — 類別比較

```python
categories = ["A", "B", "C", "D"]
values = [23, 45, 56, 78]
plt.bar(categories, values, color=["red", "blue", "green", "orange"])
```

### 直方圖 — 分佈觀察

```python
data = np.random.randn(1000)
plt.hist(data, bins=30, alpha=0.7, edgecolor="black")
```

### 散佈圖 — 相關性展示

```python
x = np.random.randn(200)
y = x * 0.5 + np.random.randn(200) * 0.3
plt.scatter(x, y, alpha=0.6)
```

## 樣式與客製化

```python
# 查看可用樣式
print(plt.style.available)

# 設定樣式
plt.style.use("seaborn-v0_8-darkgrid")

# 自訂顏色與標籤
plt.plot(x, y, color="#FF5733", linewidth=2, linestyle="--", label="資料")
plt.xlabel("時間", fontsize=12)
plt.ylabel("數值", fontsize=12)
```

## 儲存圖表

```python
plt.savefig("chart.png", dpi=300, bbox_inches="tight")
plt.savefig("chart.pdf", format="pdf")  # 向量格式
```

---

**延伸閱讀**
- [Matplotlib 官方教學](https://www.google.com/search?q=Matplotlib+official+tutorial)
- [Matplotlib 圖表範例](https://www.google.com/search?q=Matplotlib+gallery+examples)
