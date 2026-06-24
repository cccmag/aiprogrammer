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
    axes[0].set_title("折線圖")
    axes[0].legend()
    axes[0].tick_params(axis="x", rotation=30)

    axes[1].bar(sales["city"], sales["amount"])
    axes[1].set_title("各城市銷售量")
    axes[1].set_xlabel("城市")
    axes[1].set_ylabel("金額")

    plt.tight_layout()
    chart_path = os.path.join(output_dir, "chart.png")
    plt.savefig(chart_path, dpi=100)
    print(f"圖表已儲存: {chart_path}")

    print("\n=== 6. 統計摘要 ===")
    print(df.describe())
    corr = df.corr()
    print("\n相關係數矩陣:\n", corr)

    print("\n=== 7. 缺失值處理 ===")
    df_na = df.copy()
    df_na.iloc[1:3, 0] = np.nan
    df_na.iloc[4, 2] = np.nan
    print("含缺失值:\n", df_na)
    print("isnull 計數:\n", df_na.isnull().sum())
    df_filled = df_na.fillna(df_na.mean())
    print("補值後:\n", df_filled)

    print("\n=== demo 完成 ===\n")


if __name__ == "__main__":
    demo()
