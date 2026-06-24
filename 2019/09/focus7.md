# TensorFlow.js 與張量 flow.js

## 瀏覽器中的深度學習

TensorFlow.js（之前稱為 DeepLearn.js）讓深度學習可以在瀏覽器中運行，開闢了新的應用場景。

---

## TensorFlow.js 簡介

### 什麼是 TensorFlow.js？

TensorFlow.js 是一個用 JavaScript 編寫的開源庫，允許在瀏覽器和 Node.js 中訓練和運行機器學習模型。

```javascript
// 在瀏覽器中使用 TensorFlow.js
import * as tf from '@tensorflow/tfjs';

const model = tf.sequential({
    layers: [
        tf.layers.dense({ inputShape: [784], units: 128, activation: 'relu' }),
        tf.layers.dense({ units: 10, activation: 'softmax' })
    ]
});

model.compile({
    optimizer: 'adam',
    loss: 'categoricalCrossentropy',
    metrics: ['accuracy']
});
```

### 支援的環境

```
┌─────────────────────────────────────────────────────┐
│              TensorFlow.js 支援環境                   │
├─────────────────────────────────────────────────────┤
│                                                     │
│   瀏覽器                                           │
│   - WebGL 加速                                      │
│   - WebAssembly (WASM)                              │
│                                                     │
│   Node.js                                          │
│   - 原生 C++ 綁定                                   │
│   - CUDA 加速（需要 NVIDIA GPU）                    │
│                                                     │
│   行動裝置                                         │
│   - iOS Safari                                     │
│   - Android Chrome                                 │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## 模型轉換

### 從 Python TensorFlow 到 TF.js

```python
# Python: 保存 Keras 模型
model.save('model.h5')

# 轉換為 TF.js 格式
!tensorflowjs_converter \
    --input_format=keras \
    --output_format=tfjs_graph_model \
    model.h5 \
    /path/to/tfjs_model
```

### 在 JavaScript 中加載

```javascript
// 加載轉換後的模型
const model = await tf.loadGraphModel('/path/to/model.json');

// 或使用 Layers API 格式
const model = await tf.loadLayersModel('/path/to/model.json');
```

---

## 在瀏覽器中訓練

### 完整示例：MNIST 分類

```html
<!DOCTYPE html>
<html>
<head>
    <title>MNIST in Browser</title>
</head>
<body>
    <canvas id="canvas" width="280" height="280"></canvas>
    <button onclick="train()">訓練模型</button>
    <button onclick="predict()">預測</button>
    <script src="https://cdn.jsdelivr.net/npm/@tensorflow/tfjs@2.0.0/dist/tf.min.js"></script>
    <script>
        let model;

        async function buildModel() {
            model = tf.sequential({
                layers: [
                    tf.layers.dense({ inputShape: [784], units: 128, activation: 'relu' }),
                    tf.layers.dropout({ rate: 0.2 }),
                    tf.layers.dense({ units: 10, activation: 'softmax' })
                ]
            });

            model.compile({
                optimizer: 'adam',
                loss: 'categoricalCrossentropy',
                metrics: ['accuracy']
            });
        }

        async function train() {
            // 假設有訓練數據
            const xTrain = tf.randomNormal([1000, 784]);
            const yTrain = tf.randomUniform([1000, 10]);

            await model.fit(xTrain, yTrain, {
                epochs: 10,
                batchSize: 32,
                validationSplit: 0.1
            });
        }
    </script>
</body>
</html>
```

---

## Transfer Learning

### 使用預訓練模型

```javascript
import * as tf from '@tensorflow/tfjs';
import * as mobilenet from '@tensorflow-models/mobilenet';

// 加載 MobileNet
const model = await mobilenet.load();

// 預測
const predictions = await model.classify(document.getElementById('image'));
console.log(predictions);
```

### 自定義特徵提取

```javascript
// 使用 MobileNet 作為特徵提取器
const mobilenet = await mobilenet.load({ version: 2, alpha: 1.0 });
const featureModel = tf.model({
    inputs: mobilenet.inputs,
    outputs: mobilenet.outputs  // 特徵
});

const features = featureModel.predict(myImageTensor);
```

---

## Node.js 中的 TensorFlow.js

### 安裝

```bash
npm install @tensorflow/tf-node
```

### 使用

```javascript
const tf = require('@tensorflow/tf-node');

const model = tf.sequential({
    layers: [
        tf.layers.dense({ units: 128, activation: 'relu', inputShape: [100] }),
        tf.layers.dense({ units: 1, activation: 'sigmoid' })
    ]
});

model.compile({
    optimizer: 'adam',
    loss: 'binaryCrossentropy',
    metrics: ['accuracy']
});

const x = tf.randomNormal([1000, 100]);
const y = tf.randomUniform([1000, 1]);

model.fit(x, y, { epochs: 10 });
```

---

## 應用場景

### 1. 瀏覽器內即時分類

```javascript
// 實時物體分類
navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {
        video.srcObject = stream;
        setInterval(() => {
            const img = captureImage(video);
            const predictions = model.predict(img);
            displayResults(predictions);
        }, 100);
    });
```

### 2. 手勢辨識

```javascript
// 使用 WebGL 進行手部追蹤
// 結合 TensorFlow.js 進行手勢分類
```

### 3. 語音辨識

```javascript
// 使用 Speech Commands 模型
// 識別簡單的語音指令
```

---

## 結語

TensorFlow.js 讓深度學習走出了伺服器，來到了用戶的瀏覽器中。這開闢了新的應用場景：

- **隱私保護**：數據不需要離開用戶設備
- **低延遲**：本地推理，無網路延遲
- **離線支援**：不需要網路連接
- **跨平台**：統一代碼運行在瀏覽器和伺服器

---

**延伸閱讀**

- [TensorFlow.js Official](https://www.google.com/search?q=TensorFlow.js+official)
- [TensorFlow.js+tutorial](https://www.google.com/search?q=TensorFlow.js+tutorial)
- [Browser+deep+learning](https://www.google.com/search?q=browser+deep+learning+TensorFlow.js)

---

*本篇文章為「AI 程式人雜誌 2019 年 9 月號」TensorFlow 2.0 系列之七。*