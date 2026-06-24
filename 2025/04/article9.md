# 折線圖與長條圖

## 前言

折線圖和長條圖是資料可視化中最基礎也最常用的兩種圖表。折線圖擅長展示時間序列的變化趨勢，長條圖則適合比較不同類別之間的數值差異。掌握這兩種圖表，就能應對絕大多數的視覺化需求。

## 折線圖 (Line Chart)

折線圖透過連接資料點的線段來展示資料的連續變化：

```python
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

np.random.seed(42)
dates = pd.date_range("2026-01-01", periods=30)
values = np.random.randn(30).cumsum() + 100

# 基本折線圖
plt.figure(figsize=(10, 5))
plt.plot(dates, values, marker="o", linestyle="-", linewidth=2, markersize=4)
plt.title("每日銷售趨勢")
plt.xlabel("日期")
plt.ylabel("銷售額")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
```

### 多線條折線圖

```python
# 多條折線比較
data = pd.DataFrame({
    "Product_A": np.random.randn(30).cumsum() + 100,
    "Product_B": np.random.randn(30).cumsum() + 95,
    "Product_C": np.random.randn(30).cumsum() + 105,
}, index=dates)

plt.figure(figsize=(12, 5))
for col in data.columns:
    plt.plot(data.index, data[col], marker="o", label=col, linewidth=1.5)

plt.title("各產品銷售趨勢比較")
plt.xlabel("日期")
plt.ylabel("銷售額")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
```

### 面積圖 (填滿區域)

```python
plt.figure(figsize=(10, 5))
plt.fill_between(dates, values, alpha=0.3)
plt.plot(dates, values, "o-", color="blue")
plt.title("面積圖")
plt.tight_layout()
plt.show()
```

## 長條圖 (Bar Chart)

長條圖用長條的高度來表示數值大小：

```python
categories = ["A", "B", "C", "D", "E"]
values = [23, 45, 56, 78, 34]

plt.figure(figsize=(8, 5))
plt.bar(categories, values, color="skyblue", edgecolor="navy")
plt.title("各類別銷售量")
plt.xlabel("類別")
plt.ylabel("銷售量")
plt.tight_layout()
plt.show()
```

### 水平長條圖

```python
plt.figure(figsize=(8, 5))
plt.barh(categories, values, color="lightgreen")
plt.title("水平長條圖")
plt.xlabel("銷售量")
plt.ylabel("類別")
plt.tight_layout()
plt.show()
```

### 分組長條圖

```python
data = {
    "產品": ["A", "B", "C"],
    "Q1": [100, 120, 90],
    "Q2": [110, 115, 105],
    "Q3": [130, 140, 95],
}
df = pd.DataFrame(data)

x = np.arange(len(df))
width = 0.25

plt.figure(figsize=(10, 5))
plt.bar(x - width, df["Q1"], width, label="Q1")
plt.bar(x, df["Q2"], width, label="Q2")
plt.bar(x + width, df["Q3"], width, label="Q3")

plt.xticks(x, df["產品"])
plt.title("各產品季度銷售比較")
plt.legend()
plt.tight_layout()
plt.show()
```

### 堆疊長條圖

```python
plt.figure(figsize=(8, 5))
plt.bar(categories, values_a, label="Part A")
plt.bar(categories, values_b, bottom=values_a, label="Part B")
plt.legend()
plt.show()
```

## 樣式客製化

```python
# 使用專業樣式
plt.style.use("seaborn-v0_8-darkgrid")

# 在長條上標註數值
bars = plt.bar(categories, values)
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, height,
             f"{height:.0f}", ha="center", va="bottom")
```

---

**延伸閱讀**
- [Matplotlib 折線圖教學](https://www.google.com/search?q=Matplotlib+line+chart+tutorial)
- [Matplotlib 長條圖教學](https://www.google.com/search?q=Matplotlib+bar+chart+tutorial)
