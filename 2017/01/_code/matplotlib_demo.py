#!/usr/bin/env python3
"""Matplotlib 基礎操作示範"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

def demo():
    print("=" * 60)
    print("Matplotlib 基礎操作示範")
    print("=" * 60)

    x = np.linspace(0, 2 * np.pi, 100)

    print("\n1. 創建圖表：")
    fig, axes = plt.subplots(2, 2, figsize=(10, 8))

    axes[0, 0].plot(x, np.sin(x), 'b-')
    axes[0, 0].set_title('Sin(x)')
    axes[0, 0].grid(True)

    axes[0, 1].plot(x, np.cos(x), 'r-')
    axes[0, 1].set_title('Cos(x)')
    axes[0, 1].grid(True)

    axes[1, 0].plot(x, x**2, 'g-')
    axes[1, 0].set_title('x^2')
    axes[1, 0].grid(True)

    axes[1, 1].scatter(np.random.randn(50), np.random.randn(50), alpha=0.5)
    axes[1, 1].set_title('Scatter Plot')
    axes[1, 1].grid(True)

    plt.tight_layout()
    plt.savefig('/tmp/matplotlib_demo.png')
    print("   圖表已保存到 /tmp/matplotlib_demo.png")

    print("\n2. 柱狀圖：")
    categories = ['A', 'B', 'C', 'D']
    values = [23, 45, 56, 78]
    plt.figure()
    plt.bar(categories, values, color=['red', 'green', 'blue', 'orange'])
    plt.title('Category Performance')
    plt.xlabel('Category')
    plt.ylabel('Value')
    plt.savefig('/tmp/bar_demo.png')
    print("   柱狀圖已保存到 /tmp/bar_demo.png")

    print("\n注意：如需顯示圖表，請使用 plt.show() 或在 Jupyter 中使用 %matplotlib inline")

if __name__ == "__main__":
    demo()