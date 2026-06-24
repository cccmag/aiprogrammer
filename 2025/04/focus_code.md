# 完整實作範例 — 資料處理與分析

## 前言

本篇文章對應 [`_code/data_analysis.py`](_code/data_analysis.py) 中的完整實作。該程式整合了 NumPy 陣列運算、Pandas DataFrame 操作、資料篩選、分組聚合以及 Matplotlib 資料可視化，展示了一個典型的資料分析工作流程。

## 原始碼

完整的 Python 實作請參考：[_code/data_analysis.py](_code/data_analysis.py)

```python
#!/usr/bin/env python3
"""資料處理與分析 — NumPy, Pandas, Matplotlib 完整示範"""

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os


def demo():
    output_dir = os.path.dirname(os.path.abspath(__file__))
    np.random.seed(42)

    print("=== 1. NumPy 陣列運算 ===")
    arr = np.arange(1, 13).reshape(3, 4)
    print("原始陣列:\n", arr)
    print("sin:\n", np.round(np.sin(arr), 4))
    print("sum axis=0:", arr.sum(axis=0))
    print("mean:", arr.mean())

    print("\n=== 2. Pandas DataFrame ===")
    dates = pd.date_range("20260101", periods=6)
    df = pd.DataFrame(
        np.random.randn(6, 4),
        index=dates,
        columns=list("ABCD"),
    )
    print(df)

    print("\n=== 3. 篩選過濾 ===")
    print("A > 0:\n", df[df["A"] > 0])
    print("A > 0 & B < 0.5:\n", df[(df["A"] > 0) & (df["B"] < 0.5)])

    print("\n=== 4. 分組聚合 ===")
    sales = pd.DataFrame({
        "city": ["台北", "台中", "台北", "高雄", "台中", "高雄"] * 2,
        "product": ["A", "A", "B", "B", "A", "B"] * 2,
        "amount": np.random.randint(100, 1000, 12),
    })
    print("原始資料:\n", sales)
    grouped = sales.groupby("city")["amount"].agg(["sum", "mean", "count"])
    print("\n各城市銷售統計:\n", grouped)
    pivot = sales.pivot_table(
        values="amount", index="city", columns="product",
        aggfunc="sum", fill_value=0,
    )
    print("\n樞紐分析表:\n", pivot)

    print("\n=== 5. 資料可視化 ===")
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))

    axes[0].plot(df.index, df["A"], "o-", label="A")
    axes[0].plot(df.index, df["B"], "s--", label="B")
    axes[0].set_title("Line Chart")
    axes[0].legend()
    axes[0].tick_params(axis="x", rotation=30)

    axes[1].bar(sales["city"], sales["amount"])
    axes[1].set_title("Sales by City")
    axes[1].set_xlabel("City")
    axes[1].set_ylabel("Amount")

    plt.tight_layout()
    chart_path = os.path.join(output_dir, "chart.png")
    plt.savefig(chart_path, dpi=100)
    print(f"Chart saved: {chart_path}")

    print("\n=== 6. 統計摘要 ===")
    print(df.describe())
    corr = df.corr()
    print("\nCorrelation Matrix:\n", corr)

    print("\n=== 7. 缺失值處理 ===")
    df_na = df.copy()
    df_na.iloc[1:3, 0] = np.nan
    df_na.iloc[4, 2] = np.nan
    print("With NaN:\n", df_na)
    print("isnull count:\n", df_na.isnull().sum())
    df_filled = df_na.fillna(df_na.mean())
    print("After fillna:\n", df_filled)

    print("\n=== demo done ===\n")


if __name__ == "__main__":
    demo()
```

## 執行結果

```
=== 1. NumPy 陣列運算 ===
原始陣列:
 [[ 1  2  3  4]
 [ 5  6  7  8]
 [ 9 10 11 12]]
mean: 6.5

=== 2. Pandas DataFrame ===
                   A         B         C         D
2026-01-01  0.496714 -0.138264  0.647689  1.523030
2026-01-06  1.465649 -0.225776  0.067528 -1.424748

=== 3. 篩選過濾 ===
A > 0 & B < 0.5:
                    A         B         C         D
2026-01-01  0.496714 -0.138264  0.647689  1.523030
2026-01-06  1.465649 -0.225776  0.067528 -1.424748

=== 4. 分組聚合 ===
各城市銷售統計:
        sum    mean  count
city
台中    2949  737.25      4
台北    1547  386.75      4
高雄    2403  600.75      4

=== 5. 資料可視化 ===
Chart saved: chart.png

=== 6. 統計摘要 ===
              A         B         C         D
mean   0.081311 -0.275775 -0.133655 -0.262434
std    0.861950  0.862828  1.168366  1.187681

=== 7. 缺失值處理 ===
isnull count:
 A    2
B    0
C    1
D    0
```

## 程式碼說明

### NumPy 陣列運算

程式首先建立一個 3x4 的陣列，展示基本數學函式的向量化應用。`arr.sum(axis=0)` 沿行方向加總各欄，`arr.mean()` 計算全域平均值。

### Pandas DataFrame

使用 `pd.date_range` 建立日期索引，並以標準常態分佈的亂數建立 6x4 的 DataFrame。這模擬了真實應用中從資料庫或 API 取得的時間序列資料。

### 篩選過濾

以布林索引（Boolean Indexing）篩選符合條件的資料列。`df[df["A"] > 0]` 選取 A 欄為正值的列，多條件使用 `&` 運算子組合。

### 分組聚合

建立銷售資料集後，以 `groupby` 按城市分組，計算各城市的銷售總額、平均和筆數。`pivot_table` 則產生城市-產品的二維交叉分析表。

### 資料可視化

使用 Matplotlib 建立包含兩個子圖的圖表：左側為時間序列的折線圖，右側為各城市銷售量的長條圖。

### 統計摘要

`df.describe()` 輸出數值欄位的常見統計量，`df.corr()` 計算相關係數矩陣。

### 缺失值處理

示範如何手動插入 NaN，偵測缺失值位置，以及使用 `fillna` 以平均值填補。

---

**延伸閱讀**
- [NumPy 官方文件](https://www.google.com/search?q=NumPy+documentation)
- [Pandas 官方文件](https://www.google.com/search?q=Pandas+documentation)
- [Matplotlib 官方文件](https://www.google.com/search?q=Matplotlib+documentation)
