# 行動 AI 的發展

## 前言

2016 年見證了行動 AI 應用的爆發式成長。從語音助理到圖像識別，AI 能力正在成為行動裝置的標準配置。

## 行動 AI 概述

```python
mobile_ai_2016 = {
    '語音助理': 'Siri, Google Assistant, Cortana',
    '圖像識別': 'Google Photos, 華為Mate 9',
    'AR/VR': 'Pokemon GO, ARKit (預告)',
    '相機增強': '場景識別, HDR+, 人像模式',
    '健康': '心率監測, 睡眠追蹤',
}
```

## 行動端的深度學習

### 為何要在行動端執行 AI？

```python
mobile_ai_benefits = {
    '延遲': '本地處理，無需網路往返',
    '離線': '網路不穩定時仍可使用',
    '隱私': '資料不上傳雲端',
    '成本': '減少伺服器負載和頻寬消耗',
    '體驗': '即時回饋，更流暢的使用者體驗',
}
```

### 挑戰

```python
mobile_constraints = {
    '計算資源': '有限的 CPU/GPU 能力',
    '記憶體': '行動裝置記憶體有限',
    '電力': 'AI 運算消耗大量電量',
    '儲存': '模型大小受限',
    '散熱': '長時間 AI 運算導致發熱',
}
```

## 移動端框架

### TensorFlow Lite

```python
# TensorFlow Lite 模型轉換
import tensorflow as tf

# 轉換 Keras 模型
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()

# 儲存
with open('model.tflite', 'wb') as f:
    f.write(tflite_model)
```

```kotlin
// Android 使用 TensorFlow Lite
class ImageClassifier {
    private var interpreter: Interpreter? = null

    fun classify(image: ByteBuffer): String {
        val output = Array(1) { FloatArray(CLASS_COUNT) }
        interpreter?.run(image, output)
        return getLabel(output[0].argMax())
    }
}
```

### Core ML (iOS)

```swift
// Core ML 模型使用
import CoreML
import Vision

let model = try MobileNetV2(configuration: MLModelConfiguration())
let request = VNCoreMLRequest(model: model) { request, error in
    if let results = request.results as? [VNClassificationObservation] {
        print(results[0].identifier, results[0].confidence)
    }
}

let handler = VNImageRequestHandler(cgImage: image, options: [:])
try handler.perform([request])
```

### Caffe2 Mobile

```python
# Caffe2 移動端部署
from caffe2.python import workspace, model_helper
import caffe2.python.predictor.mobile_exporter

# 匯出為行動端格式
predictor = mobile_exporter.Export(
    workspace,
    model,
    [db_type='minidb']
)

with open('myapp.pb', 'wb') as f:
    f.write(predictor.predictor_net.SerializeToString())
```

## 邊緣 AI 應用

### 場景識別

```python
class SceneClassifier:
    """場景分類模型"""
    def __init__(self):
        self.model = self.load_model('mobilenet_v2')
        self.labels = ['indoor', 'outdoor', 'beach', 'mountain', 'city']

    def classify(self, image):
        """分類圖像場景"""
        # 預處理
        tensor = self.preprocess(image)

        # 推論
        logits = self.model.predict(tensor)

        # 後處理
        prob = self.softmax(logits)
        return self.labels[prob.argmax()]

class ObjectDetector:
    """即時物體檢測"""
    def __init__(self):
        self.model = self.load_model('ssd_mobilenet')

    def detect(self, frame):
        """檢測視頻幀中的物體"""
        boxes, scores, labels = self.model.predict(frame)

        # 過濾低置信度
        keep = scores > 0.5
        return boxes[keep], scores[keep], labels[keep]
```

### 語音辨識

```python
class MobileASR:
    """離線語音辨識"""
    def __init__(self):
        self.encoder = self.load_encoder('deepspeech')
        self.decoder = self.load_decoder()

    def transcribe(self, audio):
        """將語音轉為文字"""
        # 特徵提取
        features = self.extract_mfcc(audio)

        # CTC 解碼
        text = self.decoder.decode(features)

        return text
```

### 自然語言處理

```python
class MobileNLP:
    """離線 NLP 模型"""
    def __init__(self):
        self.tokenizer = self.load_tokenizer()
        self.model = self.load_model('bert_mini')

    def analyze_sentiment(self, text):
        """情感分析"""
        tokens = self.tokenizer.tokenize(text)
        embedding = self.model.embed(tokens)
        sentiment = self.classifier.predict(embedding)
        return sentiment

    def generate_response(self, query):
        """生成回應"""
        tokens = self.tokenizer.tokenize(query)
        context = self.model.embed(tokens)
        response = self.generator.generate(context)
        return self.tokenizer.detokenize(response)
```

## 模型優化

### 量化

```python
# 模型量化減少大小和加速
import torch

# 動態量化
quantized_model = torch.quantization.quantize_dynamic(
    model, {torch.nn.Linear}, dtype=torch.qint8
)

# 訓練後量化
model.eval()
model.qconfig = torch.quantization.get_default_qconfig('fbgemm')
torch.quantization.prepare(model, inplace=True)
torch.quantization.convert(model, inplace=True)
```

### 剪枝

```python
def prune_weights(weights, threshold=0.01):
    """移除小權重"""
    mask = np.abs(weights) > threshold
    pruned_weights = weights * mask
    return pruned_weights, mask

def iterative_pruning(model, epochs=10, sparsity=0.5):
    """迭代剪枝"""
    for epoch in range(epochs):
        # 訓練
        model.train()

        # 剪枝
        for name, param in model.named_parameters():
            if 'weight' in name:
                param.data, mask = prune_weights(param.data, threshold=0.01)

        # 微調
        model.fit()
```

### 知識蒸餾

```python
def distill(teacher, student, train_loader, temperature=4, alpha=0.7):
    """知識蒸餾"""
    optimizer = torch.optim.Adam(student.parameters())

    for data, target in train_loader:
        teacher_logits = teacher(data)
        student_logits = student(data)

        # 蒸餾損失
        soft_target = torch.softmax(teacher_logits / temperature, dim=1)
        distill_loss = F.kl_div(
            torch.log_softmax(student_logits / temperature, dim=1),
            soft_target,
            reduction='batchmean'
        ) * (temperature ** 2)

        # 標準損失
        hard_loss = F.cross_entropy(student_logits, target)

        # 總損失
        loss = alpha * hard_loss + (1 - alpha) * distill_loss

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
```

## 聯邦學習

```python
federated_learning = """
聯邦學習：保護隱私的分散式訓練

客戶端                   伺服器
  │                        │
  ├─ 收到全球模型 ────────►│
  │                        │
  │  訓練本地資料          │
  │                        │
  ├─ 傳送模型更新 ────────►│
  │                        │
  │                    聚合更新
  │                        │
  │  接收新模型 ◄──────────┘
  │                        │
  └────────────────────────┘

優點：
- 資料不離開設備
- 減少網路傳輸
- 保護使用者隱私
"""
```

## 小結

2016 年是行動 AI 的起點。隨著硬體能力的提升和模型優化技術的進步，越來越多的 AI 能力可以在行動裝置上運行。TensorFlow Lite、Core ML 和 Caffe2 等框架為開發者提供了便捷的工具，使得離線 AI 應用成為可能。

---

**延伸閱讀**

- [TensorFlow Lite](https://www.google.com/search?q=TensorFlow+Lite)
- [Core ML Documentation](https://www.google.com/search?q=Core+ML+documentation)
- [Mobile AI Research](https://www.google.com/search?q=mobile+AI+deep+learning+optimization)