# 類神經網路：早期研究

## 概述

類神經網路（Neural Networks）的起源可以追溯到 1940 年代。2007 年，深度學習尚未興起，但傳統類神經網路在模式識別、預測等領域已有廣泛應用。

## 類神經網路基礎

```python
"""
類神經網路概念展示
展示傳統神經網路的原理
"""

def demo():
    print("=" * 50)
    print("類神經網路概念展示")
    print("=" * 50)

    print("\n--- 網路結構 ---")
    print("""
典型的三層神經網路：

輸入層 (3 節點)     隱藏層 (4 節點)     輸出層 (2 節點)

    o x1              o
    |  \\             / \\
    |   \\           /   \\
    o----o----o----o     o---- y1
   x2    \\  /    / \\   /
    |     \\/     /   \\ /
    o------o----o-----o---- y2
   x3                 /
                     /
                    o
""")

    print("\n--- 前饋傳播 ---")
    forward_code = """
# 簡化前饋傳播
def forward(X, W1, W2, b1, b2):
    # 隱藏層線性組合 + 激活
    z1 = X @ W1 + b1
    a1 = sigmoid(z1)

    # 輸出層線性組合 + 激活
    z2 = a1 @ W2 + b2
    a2 = softmax(z2)

    return a2

# Sigmoid 激活函數
def sigmoid(z):
    return 1 / (1 + exp(-z))

# Softmax 輸出
def softmax(z):
    exp_z = exp(z - max(z))
    return exp_z / sum(exp_z)
"""
    print(forward_code)

    print("\n--- 反向傳播 ---")
    backprop = """
# 梯度計算
def backward(Y_true, Y_pred, a1, z2, W2):
    # 輸出層梯度
    delta_output = Y_pred - Y_true

    # 權重梯度
    grad_W2 = a1.T @ delta_output

    # 反向傳播到隱藏層
    delta_hidden = delta_output @ W2.T * sigmoid_derivative(z1)

    # 隱藏層權重梯度
    grad_W1 = X.T @ delta_hidden

    return grad_W1, grad_W2

# 權重更新
W1 -= learning_rate * grad_W1
W2 -= learning_rate * grad_W2
"""
    print(backprop)

    print("\n--- 激活函數 ---")
    activations = [
        ("Sigmoid", "0-1 之間，常用於輸出層", "1/(1+e^-x)"),
        ("Tanh", "-1 到 1 之間，零中心化", "(e^x - e^-x)/(e^x + e^-x)"),
        ("ReLU", "計算高效，避免梯度消失", "max(0, x)"),
    ]
    for name, desc, formula in activations:
        print(f"  {name}: {desc}")
        print(f"    公式: {formula}")

    print("\n--- 應用領域 ---")
    applications = [
        ("影像辨識", "手寫字識別、人臉辨識"),
        ("語音處理", "語音識別、說話者辨識"),
        ("時間序列", "股價預測、氣象預測"),
        ("自然語言", "文字分類、情感分析"),
    ]
    for cat, desc in applications:
        print(f"  {cat}: {desc}")

    print("\n" + "=" * 50)
    print("類神經網路概念展示完成")

if __name__ == "__main__":
    demo()