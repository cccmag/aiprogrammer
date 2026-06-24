import sys
import os


def demo():
    print("=" * 56)
    print("機器學習框架基礎展示")
    print("=" * 56)

    print("\n[1] NumPy 基礎（所有框架的基礎）")
    import numpy as np
    a = np.random.randn(3, 4)
    b = np.random.randn(4, 5)
    c = np.dot(a, b)
    print(f"    陣列 a: shape {a.shape}")
    print(f"    矩陣乘法結果 c: shape {c.shape}")

    print("\n[2] 自動微分概念（純 Python 實現）")
    def simple_gradient(x):
        return x ** 2

    h = 0.0001
    x = 3.0
    numerical_grad = (simple_gradient(x + h) - simple_gradient(x)) / h
    print(f"    函式 f(x) = x^2")
    print(f"    在 x=3 的梯度 approx: {numerical_grad:.6f}")

    print("\n[3] 簡單神經網路（NumPy 實現）")
    def sigmoid(x):
        return 1 / (1 + np.exp(-x))

    W1 = np.random.randn(784, 128) * 0.01
    b1 = np.zeros((1, 128))
    W2 = np.random.randn(128, 10) * 0.01
    b2 = np.zeros((1, 10))

    x_sample = np.random.randn(1, 784)
    h = sigmoid(np.dot(x_sample, W1) + b1)
    output = sigmoid(np.dot(h, W2) + b2)
    print(f"    輸入 shape: (1, 784)")
    print(f"    隱藏層 output shape: {h.shape}")
    print(f"    輸出 shape: {output.shape}")

    print("\n[4] 框架檢測")
    frameworks = {
        "NumPy": "ok",
        "TensorFlow": "需要 pip install tensorflow",
        "PyTorch": "需要 pip install torch",
        "JAX": "需要 pip install jax jaxlib"
    }
    for name, status in frameworks.items():
        try:
            if name == "NumPy":
                print(f"    {name}: {np.__version__}")
            elif name == "TensorFlow":
                import tensorflow as tf
                print(f"    {name}: {tf.__version__}")
            elif name == "PyTorch":
                import torch
                print(f"    {name}: {torch.__version__}")
            elif name == "JAX":
                import jax
                import jax.numpy as jnp
                print(f"    {name}: {jax.__version__}")
        except ImportError:
            print(f"    {name}: 未安裝 ({status})")

    print(f"\n{'=' * 56}")
    print("展示完成")
    print("=" * 56)


if __name__ == "__main__":
    demo()