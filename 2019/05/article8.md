# 遷移學習：利用預訓練模型

## 前言

遷移學習允許我們使用在大規模資料上預訓練的模型，快速適應特定任務。

## PyTorch 遷移學習

```python
import torchvision.models as models

# 載入預訓練 ResNet
model = models.resnet50(pretrained=True)

# 凍結晶層
for param in model.parameters():
    param.requires_grad = False

# 替換最後的全連接層
num_features = model.fc.in_features
model.fc = nn.Linear(num_features, 2)

# 訓練
for images, labels in dataloader:
    outputs = model(images)
    loss = criterion(outputs, labels)
    loss.backward()
    optimizer.step()
```

## Keras 遷移學習

```python
from keras.applications import ResNet50

base_model = ResNet50(weights='imagenet', include_top=False)
model = Sequential([
    base_model,
    GlobalAveragePooling2D(),
    Dense(1024, activation='relu'),
    Dense(num_classes, activation='softmax')
])

# 凍結晶層
for layer in base_model.layers:
    layer.trainable = False

model.compile(optimizer='adam', loss='categorical_crossentropy')
```

## 常用預訓練模型

| 模型 | 資料集 | 參數 |
|-----|--------|------|
| ResNet-50 | ImageNet | 26M |
| VGG-16 | ImageNet | 138M |
| InceptionV3 | ImageNet | 23M |
| MobileNet | ImageNet | 4.2M |

## 微調策略

1. **凍結晶層**：只訓練新增的層
2. **逐步解凍**：先訓練新增層，再逐步解凍
3. **全部訓練**：如果資料量大，可訓練全部層

## 延伸閱讀

- [PyTorch TorchVision](https://www.google.com/search?q=pytorch+transfer+learning+tutorial)
- [Keras Applications](https://www.google.com/search?q=keras+transfer+learning)