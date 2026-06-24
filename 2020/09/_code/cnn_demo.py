#!/usr/bin/env python3
"""CNN Demo: Convolution, Pooling, and Image Classification"""

import numpy as np

def relu(x):
    return np.maximum(0, x)

def relu_grad(x):
    return (x > 0).astype(float)

def softmax(x):
    exp_x = np.exp(x - np.max(x, axis=-1, keepdims=True))
    return exp_x / np.sum(exp_x, axis=-1, keepdims=True)

def max_pool(image, kernel_size, stride):
    ih, iw = image.shape[:2]
    kh, kw = kernel_size, kernel_size
    out_h = (ih - kh) // stride + 1
    out_w = (iw - kw) // stride + 1
    output = np.zeros((out_h, out_w))
    for i in range(out_h):
        for j in range(out_w):
            h_start = i * stride
            w_start = j * stride
            output[i, j] = np.max(image[h_start:h_start+kh, w_start:w_start+kw])
    return output

def conv2d(image, kernel, stride=1, padding=0):
    if padding > 0:
        image = np.pad(image, padding, mode='constant')
    ih, iw = image.shape
    kh, kw = kernel.shape
    out_h = (ih - kh) // stride + 1
    out_w = (iw - kw) // stride + 1
    output = np.zeros((out_h, out_w))
    for i in range(out_h):
        for j in range(out_w):
            h_start = i * stride
            w_start = j * stride
            output[i, j] = np.sum(image[h_start:h_start+kh, w_start:w_start+kw] * kernel)
    return output

class SimpleCNN:
    def __init__(self):
        np.random.seed(42)
        self.conv1_W = np.random.randn(8, 3, 3) * 0.1
        self.conv1_b = np.zeros(8)
        self.conv2_W = np.random.randn(16, 8, 3, 3) * 0.1
        self.conv2_b = np.zeros(16)
        self.fc_W = np.random.randn(10, 16 * 5 * 5) * 0.1
        self.fc_b = np.zeros(10)

    def forward(self, x):
        x = conv2d(x, self.conv1_W) + self.conv1_b.reshape(-1, 1, 1)
        x = relu(x)
        x = max_pool(x, (2, 2), 2)
        x = conv2d(x, self.conv2_W[0], padding=1)
        x = relu(x)
        x = max_pool(x, (2, 2), 2)
        x = x.reshape(1, -1)
        x = np.dot(x, self.fc_W.T) + self.fc_b
        x = softmax(x)
        return x

    def get_num_params(self):
        return (self.conv1_W.size + self.conv1_b.size +
                self.conv2_W.size + self.conv2_b.size +
                self.fc_W.size + self.fc_b.size)

def edge_detection(image):
    kernel = np.array([[-1, -1, -1],
                       [-1,  8, -1],
                       [-1, -1, -1]])
    return conv2d(image, kernel)

def blur(image):
    kernel = np.ones((3, 3)) / 9
    return conv2d(image, kernel)

def demo():
    print("=" * 50)
    print("CNN Demo: Image Processing and Classification")
    print("=" * 50)

    model = SimpleCNN()
    print(f"\n1. Simple CNN Architecture:")
    print("-" * 30)
    print(f"   Conv1: 3x3 -> 8 channels")
    print(f"   Conv2: 3x3 -> 16 channels")
    print(f"   FC: 16*5*5 -> 10")
    print(f"   Total parameters: {model.get_num_params()}")

    test_image = np.random.randn(28, 28)
    print(f"\n2. Input Image:")
    print("-" * 30)
    print(f"   Shape: {test_image.shape}")
    print(f"   Value range: [{test_image.min():.2f}, {test_image.max():.2f}]")

    output = model.forward(test_image)
    print(f"\n3. Forward Pass:")
    print("-" * 30)
    print(f"   Output shape: {output.shape}")
    print(f"   Output sum: {output.sum():.4f}")
    print(f"   Predicted class: {np.argmax(output)}")
    print(f"   Class probabilities: {output[0]}")

    print(f"\n4. Convolution Operations:")
    print("-" * 30)
    edge_result = edge_detection(test_image)
    blur_result = blur(test_image)
    print(f"   Edge detection result shape: {edge_result.shape}")
    print(f"   Blur result shape: {blur_result.shape}")

    print(f"\n5. Edge Detection Kernel:")
    print("-" * 30)
    kernel = np.array([[-1, -1, -1],
                       [-1,  8, -1],
                       [-1, -1, -1]])
    print(f"   Kernel:\n{kernel}")

    print(f"\n6. Pooling Example:")
    print("-" * 30)
    pool_result = max_pool(test_image, (2, 2), 2)
    print(f"   Input: {test_image.shape}")
    print(f"   Output: {pool_result.shape}")

    print("\n" + "=" * 50)
    print("Demo completed!")
    print("=" * 50)

if __name__ == "__main__":
    demo()