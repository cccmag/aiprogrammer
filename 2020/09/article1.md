# 用 Python 實作簡單的 CNN

## 前言

本文將用 Python 和 NumPy 從零實作一個簡單的卷積神經網路，幫助讀者理解 CNN 的核心概念。

---

## 一、卷積操作

### 什麼是卷積？

卷積通過一個小型矩陣（卷積核）在輸入圖像上滑動，提取特徵：

```python
import numpy as np

def conv2d(image, kernel, stride=1, padding=0):
    """
    2D convolution without batching
    image: (H, W)
    kernel: (K, K)
    """
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
            output[i, j] = np.sum(
                image[h_start:h_start+kh, w_start:w_start+kw] * kernel
            )

    return output
```

---

## 二、池化操作

### 最大池化

```python
def max_pool(image, kernel_size, stride):
    ih, iw = image.shape
    kh, kw = kernel_size, kernel_size

    out_h = (ih - kh) // stride + 1
    out_w = (iw - kw) // stride + 1
    output = np.zeros((out_h, out_w))

    for i in range(out_h):
        for j in range(out_w):
            h_start = i * stride
            w_start = j * stride
            output[i, j] = np.max(
                image[h_start:h_start+kh, w_start:w_start+kw]
            )

    return output
```

---

## 三、激活函數

### ReLU

```python
def relu(x):
    return np.maximum(0, x)

def relu_grad(x):
    return (x > 0).astype(float)
```

### Softmax

```python
def softmax(x):
    exp_x = np.exp(x - np.max(x))
    return exp_x / np.sum(exp_x)
```

---

## 四、簡單 CNN 架構

```python
class SimpleCNN:
    def __init__(self, input_shape=(1, 28, 28), num_classes=10):
        self.input_shape = input_shape
        self.num_classes = num_classes

        # 初始化權重
        np.random.seed(42)
        self.conv1_W = np.random.randn(8, 1, 3, 3) * 0.1
        self.conv1_b = np.zeros(8)

        self.conv2_W = np.random.randn(16, 8, 3, 3) * 0.1
        self.conv2_b = np.zeros(16)

        self.fc_W = np.random.randn(16 * 5 * 5, 128) * 0.1
        self.fc_b = np.zeros(128)

        self.out_W = np.random.randn(128, num_classes) * 0.1
        self.out_b = np.zeros(num_classes)

    def forward(self, x):
        # Conv 1
        x = self._conv2d(x, self.conv1_W, self.conv1_b)
        x = relu(x)
        x = max_pool(x, (2, 2), 2)

        # Conv 2
        x = self._conv2d(x, self.conv2_W, self.conv2_b)
        x = relu(x)
        x = max_pool(x, (2, 2), 2)

        # Flatten
        x = x.reshape(1, -1)

        # FC 1
        x = np.dot(x, self.fc_W) + self.fc_b
        x = relu(x)

        # Output
        x = np.dot(x, self.out_W) + self.out_b
        x = softmax(x)

        return x

    def _conv2d(self, image, kernel, bias):
        # Simplified conv2d implementation
        output = np.zeros((image.shape[0] - 2, image.shape[1] - 2, kernel.shape[0]))

        for k in range(kernel.shape[0]):
            for i in range(image.shape[0] - 2):
                for j in range(image.shape[1] - 2):
                    output[i, j, k] = np.sum(
                        image[i:i+3, j:j+3] * kernel[k, 0]
                    ) + bias[k]

        return output

    def get_num_params(self):
        params = 0
        params += self.conv1_W.size + self.conv1_b.size
        params += self.conv2_W.size + self.conv2_b.size
        params += self.fc_W.size + self.fc_b.size
        params += self.out_W.size + self.out_b.size
        return params
```

---

## 五、使用範例

```python
def demo():
    print("=" * 50)
    print("Simple CNN Demo")
    print("=" * 50)

    # 建立模型
    model = SimpleCNN()
    print(f"\nTotal parameters: {model.get_num_params()}")

    # 創建測試輸入 (28x28 圖像)
    test_image = np.random.randn(28, 28)
    print(f"Input shape: {test_image.shape}")

    # 前向傳播
    output = model.forward(test_image)
    print(f"Output shape: {output.shape}")
    print(f"Output sum: {output.sum():.4f}")
    print(f"Predicted class: {np.argmax(output)}")

    # 邊緣檢測範例
    print("\n--- Edge Detection Demo ---")
    edge_kernel = np.array([[-1, -1, -1],
                            [-1,  8, -1],
                            [-1, -1, -1]])

    result = conv2d(test_image, edge_kernel)
    print(f"Edge detection result shape: {result.shape}")

    print("\n" + "=" * 50)
    print("Demo completed!")
    print("=" * 50)

if __name__ == "__main__":
    demo()
```

---

## 結語

本文用 NumPy 實作了簡單的 CNN，涵蓋了卷積、池化、激活函數等核心組件。這個實作雖然簡化，但清楚地展示了 CNN 的工作原理。

---

*延伸閱讀：[CNN+implementation+Python+NumPy+2020](https://www.google.com/search?q=CNN+implementation+Python+NumPy+2020)*