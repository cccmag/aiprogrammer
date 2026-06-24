#!/usr/bin/env python3
"""Pandas 基礎操作示範"""

import pandas as pd
import numpy as np

def demo():
    print("=" * 60)
    print("Pandas 基礎操作示範")
    print("=" * 60)

    print("\n1. Series：")
    s = pd.Series([1, 3, 5, np.nan, 6, 8])
    print(f"   Series: {s.values}")
    print(f"   Index: {list(s.index)}")

    print("\n2. DataFrame：")
    df = pd.DataFrame({
        'name': ['Alice', 'Bob', 'Charlie', 'Diana'],
        'age': [25, 30, 35, 28],
        'score': [85.5, 90.0, 78.5, 92.0]
    })
    print(df)

    print("\n3. 基本操作：")
    print(f"   df['name'] = {list(df['name'])}")
    print(f"   df.describe():\n{df.describe()}")
    print(f"   df[df['age'] > 28]:\n{df[df['age'] > 28]}")

    print("\n4. 讀寫操作：")
    print("   pd.read_csv('file.csv')  # 讀取")
    print("   df.to_csv('output.csv')   # 寫入")

if __name__ == "__main__":
    demo()