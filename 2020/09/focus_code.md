# 實作：簡單的 CNN

## 程式概述

本程式中，我們將用 Python 和 NumPy 實作一個簡單的卷積神經網路（CNN），展示電腦視覺的基礎概念。

## 實作內容

1. **卷積操作**：提取圖像特徵
2. **池化操作**：減少空間尺寸
3. **前饋傳播**：完整的神經網路流程

```python
#!/usr/bin/env python3
"""Simple CNN Implementation using NumPy"""

import numpy as np

def im2col(image, kernel_size, stride):
    """Convert image to column format for efficient convolution"""
    batch_size, channels, height, width = image.shape
    k_h, k_w = kernel_size
    out_h = (height - k_h) // stride + 1
    out_w = (width - k_w) // stride + 1

    col = np.zeros((batch_size, channels, out_h, out_w, k_h, k_w))
    for i in range(out_h):
        for j in range(out_w):
            h_start = i * stride
            w_start = j * stride
            col[:, :, i, j] = image[:, :, h_start:h_start+k_h, w_start:w_start+k_w]

    col = col.reshape(batch_size, channels, out_h, out_w, -1)
    return col

def conv2d(image, kernel, stride=1, padding=0):
    """2D convolution operation"""
    if padding > 0:
        image = np.pad(image, ((0,0), (0,0), (padding, padding), (padding, padding)))

    batch_size, c_in, h, w = image.shape
    c_out, c_in_k, k_h, k_w = kernel.shape

    out_h = (h - k_h) // stride + 1
    out_w = (w - k_w) // stride + 1

    col_image = im2col(image, (k_h, k_w), stride)
    kernel_flat = kernel.reshape(c_out, -1)

    output = np.tensordot(col_image, kernel_flat, axes=([3, 1], [1, 0]))
    output = np.moveaxis(output, 0, 2)

    return output

def max_pool(image, kernel_size, stride):
    """Max pooling operation"""
    batch_size, channels, h, w = image.shape
    k_h, k_w = kernel_size
    out_h = (h - k_h) // stride + 1
    out_w = (w - k_w) // stride + 1

    output = np.zeros((batch_size, channels, out_h, out_w))

    for i in range(out_h):
        for j in range(out_w):
            h_start = i * stride
            w_start = j * stride
            patch = image[:, :, h_start:h_start+k_h, w_start:w_start+k_w]
            output[:, :, i, j] = np.max(patch, axis=(2, 3))

    return output

def relu(x):
    """ReLU activation function"""
    return np.maximum(0, x)

def softmax(x):
    """Softmax activation function"""
    exp_x = np.exp(x - np.max(x, axis=-1, keepdims=True))
    return exp_x / np.sum(exp_x, axis=-1, keepdims=True)

class SimpleCNN:
    def __init__(self):
        np.random.seed(42)

        self.conv1_weights = np.random.randn(16, 1, 3, 3) * 0.1
        self.conv1_bias = np.zeros(16)

        self.conv2_weights = np.random.randn(32, 16, 3, 3) * 0.1
        self.conv2_bias = np.zeros(32)

        self.fc1_weights = np.random.randn(128, 32 * 6 * 6) * 0.1
        self.fc1_bias = np.zeros(128)

        self.fc2_weights = np.random.randn(10, 128) * 0.1
        self.fc2_bias = np.zeros(10)

    def forward(self, x):
        """Forward pass through the network"""
        x = conv2d(x, self.conv1_weights) + self.conv1_bias.reshape(1, -1, 1, 1)
        x = relu(x)
        x = max_pool(x, (2, 2), 2)

        x = conv2d(x, self.conv2_weights) + self.conv2_bias.reshape(1, -1, 1, 1)
        x = relu(x)
        x = max_pool(x, (2, 2), 2)

        x = x.reshape(x.shape[0], -1)
        x = np.dot(x, self.fc1_weights.T) + self.fc1_bias
        x = relu(x)

        x = np.dot(x, self.fc2_weights.T) + self.fc2_bias
        x = softmax(x)

        return x

    def get_num_params(self):
        """Calculate total number of parameters"""
        params = 0
        params += self.conv1_weights.size + self.conv1_bias.size
        params += self.conv2_weights.size + self.conv2_bias.size
        params += self.fc1_weights.size + self.fc1_bias.size
        params += self.fc2_weights.size + self.fc2_bias.size
        return params

def demo():
    print("=" * 50)
    print("Simple CNN Demo with NumPy")
    print("=" * 50)

    batch_size = 4
    channels = 1
    height = 28
    width = 28

    cnn = SimpleCNN()
    print(f"\n1. Network Architecture:")
    print("-" * 30)
    print(f"   Conv1: 1 channel -> 16 channels, 3x3 kernel")
    print(f"   Conv2: 16 channels -> 32 channels, 3x3 kernel")
    print(f"   FC1: 32*6*6 -> 128")
    print(f"   FC2: 128 -> 10 (softmax)")
    print(f"   Total parameters: {cnn.get_num_params():,}")

    print(f"\n2. Input Data:")
    print("-" * 30)
    x = np.random.randn(batch_size, channels, height, width)
    print(f"   Input shape: {x.shape}")

    print(f"\n3. Convolution Properties:")
    print("-" * 30)
    conv1_out_h = (height - 3) // 1 + 1
    conv1_out_w = (width - 3) // 1 + 1
    pool1_out_h = conv1_out_h // 2
    pool1_out_w = conv1_out_w // 2
    print(f"   After Conv1: ({conv1_out_h}, {conv1_out_w})")
    print(f"   After Pool1: ({pool1_out_h}, {pool1_out_w})")

    conv2_out_h = (pool1_out_h - 3) // 1 + 1
    conv2_out_w = (pool1_out_w - 3) // 1 + 1
    pool2_out_h = conv2_out_h // 2
    pool2_out_w = conv2_out_w // 2
    print(f"   After Conv2: ({conv2_out_h}, {conv2_out_w})")
    print(f"   After Pool2: ({pool2_out_h}, {pool2_out_w})")

    print(f"\n4. Forward Pass:")
    print("-" * 30)
    output = cnn.forward(x)
    print(f"   Input shape: {x.shape}")
    print(f"   Output shape: {output.shape}")
    print(f"   Output sum (should be ~1.0): {output[0].sum():.4f}")
    print(f"   Predicted class probabilities: {output[0]}")

    print(f"\n5. Convolution Kernel Sample:")
    print("-" * 30)
    print(f"   Conv1 kernel[0,0] first row: {cnn.conv1_weights[0,0,0,:]}")
    print(f"   Conv1 kernel[0,0] shape: {cnn.conv1_weights[0,0].shape}")

    print(f"\n" + "=" * 50)
    print("Demo completed!")
    print("=" * 50)

if __name__ == "__main__":
    demo()