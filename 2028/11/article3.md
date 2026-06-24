# WebNN/WebGPU 瀏覽器 AI

## 1. 瀏覽器中的 AI

過去的 AI 推論需要下載模型到本機或依賴雲端 API。WebNN（Web Neural Network API）與 WebGPU 讓瀏覽器直接利用 GPU 和 NPU 執行機器學習推論，無需任何外掛。

## 2. WebNN 基本用法

WebNN 提供標準化 API，底層自動對應到 DirectML、CoreML 或 OpenVINO：

```python
# 模擬 WebNN 行為的 Python 範例
import numpy as np

class WebNNBackend:
    def __init__(self):
        self.ops = {
            'relu': lambda x: np.maximum(0, x),
            'sigmoid': lambda x: 1 / (1 + np.exp(-x)),
            'conv2d': lambda x, w: np.apply_along_axis(
                lambda v: np.sum(v * w), axis=0, arr=x)
        }

    def build_graph(self, operations):
        self.graph = operations

    def compute(self, input_data, weights):
        x = input_data
        for op, params in self.graph:
            if op == 'conv2d':
                x = self.ops[op](x, weights[params])
            elif op in self.ops:
                x = self.ops[op](x)
        return x

# 模擬執行
backend = WebNNBackend()
backend.build_graph([
    ('conv2d', 'w1'),
    ('relu', None),
    ('sigmoid', None)
])
result = backend.compute(np.array([0.5, 0.3, 0.8]), {'w1': 0.2})
print(f'WebNN 模擬結果: {result}')
```

## 3. WebGPU 加速

WebGPU 提供底層 GPU 計算能力，適合大規模平行推論：

```python
# 使用 wgpu-py 模擬 WebGPU 計算
import wgpu  # pip install wgpu-py
import numpy as np

def gpu_relu(x):
    return np.maximum(0, x)

def gpu_softmax(x):
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum()

logits = np.array([2.0, 1.0, 0.1, -0.5])
activated = gpu_relu(logits)
probs = gpu_softmax(activated)
print(f'WebGPU 模擬 Softmax 結果: {probs}')
```

## 4. 應用場景

WebNN/WebGPU 特別適合即時視訊處理、網頁端 OCR、語言翻譯等應用。Google Chrome 和 Microsoft Edge 已全面支援。

## 5. 結語

瀏覽器 AI 讓網頁應用也能享有本地端推論的即時性與隱私保障。更多資訊請參考 https://www.google.com/search?q=WebNN+WebGPU+browser+machine+learning
