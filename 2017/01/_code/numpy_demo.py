#!/usr/bin/env python3
"""NumPy 基礎操作示範"""

import numpy as np

def demo():
    print("=" * 60)
    print("NumPy 基礎操作示範")
    print("=" * 60)

    print("\n1. 創建陣列：")
    a = np.array([1, 2, 3, 4, 5])
    print(f"   a = np.array([1, 2, 3, 4, 5]) → {a}")
    print(f"   a.shape = {a.shape}, a.dtype = {a.dtype}")

    b = np.zeros((3, 4))
    print(f"   np.zeros((3, 4)) =\n{b}")

    c = np.arange(0, 10, 2)
    print(f"   np.arange(0, 10, 2) = {c}")

    d = np.random.randn(2, 3)
    print(f"   np.random.randn(2, 3) =\n{d}")

    print("\n2. 基本運算：")
    x = np.array([1, 2, 3])
    y = np.array([4, 5, 6])
    print(f"   x = {x}, y = {y}")
    print(f"   x + y = {x + y}")
    print(f"   x * y = {x * y}")
    print(f"   x @ y = {x @ y} (dot product)")

    print("\n3. 矩陣運算：")
    A = np.array([[1, 2], [3, 4]])
    B = np.array([[5, 6], [7, 8]])
    print(f"   A @ B = \n{A @ B}")
    print(f"   A.T = \n{A.T}")

    print("\n4. 索引與切片：")
    arr = np.arange(12).reshape(3, 4)
    print(f"   arr (3x4):\n{arr}")
    print(f"   arr[1, 2] = {arr[1, 2]}")
    print(f"   arr[:, 1] = {arr[:, 1]}")
    print(f"   arr[arr > 5] = {arr[arr > 5]}")

if __name__ == "__main__":
    demo()