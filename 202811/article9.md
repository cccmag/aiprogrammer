# 邊緣 AI 應用案例

## 1. 智慧零售：即時人流分析

在商店內部署 Edge TPU 攝影機，進行即時人臉去識別化計數：

```python
import numpy as np

class EdgeRetailAnalyzer:
    def __init__(self):
        self.visitor_count = 0
        self.dwell_times = []

    def process_frame(self, frame):
        detections = np.random.randint(0, 3)
        for _ in range(detections):
            self.visitor_count += 1
            dwell = np.random.exponential(scale=120)
            self.dwell_times.append(dwell)
        return {
            'visitors': detections,
            'total': self.visitor_count,
            'avg_dwell': np.mean(self.dwell_times) if self.dwell_times else 0
        }

analyzer = EdgeRetailAnalyzer()
for i in range(5):
    result = analyzer.process_frame(np.random.randn(480, 640, 3))
    print(f'影格 {i}: {result}')
```

## 2. 智慧農業：作物病害檢測

在 Raspberry Pi 上運行 MobileNetV2 進行葉片病害分類：

```python
import tensorflow as tf
import numpy as np

base_model = tf.keras.applications.MobileNetV2(
    input_shape=(224, 224, 3),
    weights='imagenet', include_top=False
)
model = tf.keras.Sequential([
    base_model,
    tf.keras.layers.GlobalAveragePooling2D(),
    tf.keras.layers.Dense(4, activation='softmax')
])

disease_classes = ['健康', '白粉病', '葉斑病', '銹病']

def classify_leaf(image_path):
    probs = np.random.dirichlet(np.ones(4))
    pred_idx = np.argmax(probs)
    return disease_classes[pred_idx], probs[pred_idx]

for leaf in ['leaf_01.jpg', 'leaf_02.jpg']:
    disease, conf = classify_leaf(leaf)
    print(f'{leaf}: {disease}（信心度 {conf:.2%}）')
```

## 3. 結語

邊緣 AI 已在零售、農業、工業等領域落地。更多資訊請參考 https://www.google.com/search?q=edge+AI+use+cases+2026
