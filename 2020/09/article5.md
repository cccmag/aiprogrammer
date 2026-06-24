# 模型部署與優化

## 前言

訓練模型只是第一步，將模型部署到生產環境同樣重要。本文介紹各種模型部署和優化技術。

---

## 一、模型導出

### TorchScript

```python
import torch

model = MyModel()
model.eval()

# 追蹤
example_input = torch.randn(1, 3, 224, 224)
traced_model = torch.jit.trace(model, example_input)
traced_model.save('model_traced.pt')

# 腳本化
scripted_model = torch.jit.script(model)
scripted_model.save('model_scripted.pt')
```

### ONNX

```python
import torch.onnx

model = MyModel()
model.eval()
example_input = torch.randn(1, 3, 224, 224)

torch.onnx.export(
    model,
    example_input,
    'model.onnx',
    input_names=['input'],
    output_names=['output'],
    dynamic_axes={'input': {0: 'batch_size'}, 'output': {0: 'batch_size'}}
)
```

---

## 二、模型量化

### 動態量化

```python
import torch.quantization

model = MyModel()
model.eval()

# 動態量化（最簡單）
quantized_model = torch.quantization.quantize_dynamic(
    model,
    {nn.Linear, nn.Conv2d},
    dtype=torch.qint8
)
```

### 訓練後靜態量化

```python
model = MyModel()
model.eval()

# Fuse layers (if applicable)
model = torch.quantization.fuse_modules(model, [['conv1', 'bn1', 'relu']])

# 設定量化
model.qconfig = torch.quantization.get_default_qconfig('fbgemm')
torch.quantization.prepare(model, inplace=True)

# 校正（需要代表性資料）
# calibrate(model, calibration_data)

# 轉換
quantized_model = torch.quantization.convert(model, inplace=False)
```

---

## 三、模型剪枝

### 結構化剪枝

```python
import torch.nn.utils.prune as prune

model = MyModel()

# L1 剪枝
prune.l1_unstructured(model.conv1, name='weight', amount=0.3)
prune.l1_unstructured(model.conv1, name='bias', amount=0.3)
```

### 產出稀疏模型

```python
# 移除剪枝 mask
prune.remove(model.conv1, 'weight')
prune.remove(model.conv1, 'bias')
```

---

## 四、TFLite 部署

### PyTorch -> TFLite

```python
# 1. PyTorch -> ONNX
torch.onnx.export(model, dummy_input, 'model.onnx')

# 2. ONNX -> TFLite (使用 onnx-tf)
import onnx
from onnx_tf.backend import prepare

onnx_model = onnx.load('model.onnx')
tf_rep = prepare(onnx_model)
tf_rep.export_graph('model.pb')

# 3. 轉換為 TFLite
# 使用 TensorFlow Lite Converter
```

---

## 五、TorchServe

部署 PyTorch 模型：

```bash
# 安裝
pip install torchserve

# 導出模型
torch-model-archiver --model-name my_model \
    --version 1.0 \
    --serialized-file model.pth \
    --handler image_classifier \
    --extra-files index_to_name.json \
    --export-path model_store

# 啟動服務
torchserve --start --model-store model_store --models my_model=my_model.mar
```

---

## 六、效能優化技巧

### 批次處理

```python
# 使用動態 batch
def collate_fn(batch):
    images, labels = zip(*batch)
    images = torch.stack(images)
    return images, torch.tensor(labels)
```

### 混合精度

```python
from torch.cuda.amp import autocast, GradScaler

scaler = GradScaler()

with autocast():
    outputs = model(images)
    loss = criterion(outputs, labels)

scaler.scale(loss).backward()
scaler.step(optimizer)
scaler.update()
```

### 快取中間結果

```python
# 在推論時快取不變的計算
cached_features = None

def inference(images):
    global cached_features
    if cached_features is None:
        cached_features = feature_extractor(images)
    return head(cached_features)
```

---

## 七、邊緣部署

### NVIDIA Jetson

```bash
# 使用 TensorRT
trtexec --onnx=model.onnx --saveEngine=model.engine
```

### 行動裝置

- Core ML (iOS)
- TFLite (Android)
- ONNX Runtime (跨平台)

---

## 結語

模型部署是將 AI 應用落地的關鍵。從 TorchScript 到 ONNX，從量化到剪枝，有多種技術可以幫助我們優化模型以適應不同的部署環境。

---

*延伸閱讀：[model+deployment+optimization+PyTorch+2020](https://www.google.com/search?q=model+deployment+optimization+PyTorch+2020)*