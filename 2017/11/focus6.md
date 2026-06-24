# 遷移學習與微調

## 前言

遷移學習允許我們利用在大規模資料集（如 ImageNet）上預訓練的模型，快速構建针对特定任務的模型。這是深度學習中最重要的技術之一，大幅減少了訓練所需的資料和時間。

## 遷移學習的原理

```
┌─────────────────────────────────────────────────────────┐
│           ImageNet 預訓練模型的遷移                      │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ImageNet (1.2M 圖像, 1000 類)                         │
│                                                         │
│  ┌─────────────────────────────────────────────────┐   │
│  │           預訓練模型                             │   │
│  │  [Conv blocks] → [Pooling] → [FC layers]       │   │
│  │       ↑                                       │   │
│  │    學習通用特徵                                 │   │
│  │    (邊、紋理、形狀)                             │   │
│  └─────────────────────────────────────────────────┘   │
│                          │                             │
│                          │ 遷移                         │
│                          ▼                             │
│  ┌─────────────────────────────────────────────────┐   │
│  │           Fine-tuning                           │   │
│  │  [Frozen Conv] → [Pooling] → [New FC]         │   │
│  │                                       ↑        │   │
│  │                                   學習新任務   │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
│  新任務 (如醫學影像分類)                                │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## 微調策略

### 1. 特徵提取（Frozen）

```python
import torchvision.models as models

# 載入預訓練模型
model = models.resnet18(pretrained=True)

# 凍住所有參數
for param in model.parameters():
    param.requires_grad = False

# 替換最後的全連接層
num_features = model.fc.in_features
model.fc = nn.Linear(num_features, num_classes)

# 只訓練新的 FC 層
optimizer = optim.Adam(model.fc.parameters(), lr=0.001)
```

### 2. 微調所有層

```python
# 不凍住任何層
model = models.resnet18(pretrained=True)
model.fc = nn.Linear(num_features, num_classes)

# 使用較小的學習率訓練所有層
optimizer = optim.Adam([
    {'params': model.conv1.parameters(), 'lr': 1e-5},
    {'params': model.layer4.parameters(), 'lr': 1e-4},
    {'params': model.fc.parameters(), 'lr': 1e-3}
])
```

### 3. 分層學習率

```python
def get_layerwise_lr(model, base_lr=1e-3):
    """為不同層設置不同的學習率"""
    params = []
    for name, param in model.named_parameters():
        if 'conv1' in name:
            lr = base_lr * 0.1
        elif 'layer4' in name:
            lr = base_lr * 0.5
        else:
            lr = base_lr
        params.append({'params': param, 'lr': lr})
    return params

optimizer = optim.Adam(get_layerwise_lr(model))
```

## 實用技巧

### 資料增強

預訓練模型需要與預訓練時相同的資料分佈：

```python
# ImageNet 預訓練模型使用的標準增強
train_transform = transforms.Compose([
    transforms.RandomResizedCrop(224),
    transforms.RandomHorizontalFlip(),
    transforms.ColorJitter(0.2, 0.2),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])
```

### 學習率 schedule

```python
# 對於微調，通常使用較小的學習率和衰減
scheduler = optim.lr_scheduler.StepLR(
    optimizer,
    step_size=10,
    gamma=0.1
)

# 或者使用 cosine annealing
scheduler = optim.lr_scheduler.CosineAnnealingLR(
    optimizer,
    T_max=30
)
```

## 預訓練模型庫

### torchvision.models

```python
# 影像模型
resnet18 = models.resnet18(pretrained=True)
resnet50 = models.resnet50(pretrained=True)
vgg16 = models.vgg16(pretrained=True)
densenet121 = models.densenet121(pretrained=True)
mobilenet_v2 = models.mobilenet_v2(pretrained=True)

# 可用於特徵提取的模型
alexnet = models.alexnet(pretrained=True)
```

### 其他模型庫

```python
# TIMM (PyTorch Image Models)
import timm
model = timm.create_model('efficientnet_b0', pretrained=True)

# TensorFlow Keras
# from tensorflow.keras.applications import ResNet50
# model = ResNet50(weights='imagenet')
```

## 實驗結果

```python
#!/usr/bin/env python3
"""Transfer learning demonstration"""

import torch
import torch.nn as nn
import torchvision.models as models

def demo():
    print("Transfer Learning Demo")
    print("=" * 50)

    # 載入預訓練 ResNet18
    print("\n1. Loading pretrained ResNet18:")
    model = models.resnet18(pretrained=True)
    print(f"   Total parameters: {sum(p.numel() for p in model.parameters()):,}")

    # 策略 1: 特徵提取
    print("\n2. Feature Extraction (freeze backbone):")
    for param in model.parameters():
        param.requires_grad = False

    num_features = model.fc.in_features
    model.fc = nn.Linear(num_features, 10)

    trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
    print(f"   Trainable parameters: {trainable:,}")

    # 策略 2: 微調所有層
    print("\n3. Fine-tuning (all layers):")
    model = models.resnet18(pretrained=True)
    model.fc = nn.Linear(num_features, 10)

    trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
    print(f"   Trainable parameters: {trainable:,}")

    # 策略 3: 分層學習率
    print("\n4. Layer-wise learning rate:")
    params = []
    for name, param in model.named_parameters():
        if 'conv1' in name:
            lr = 1e-5
        elif 'layer4' in name:
            lr = 1e-4
        else:
            lr = 1e-3
        params.append({'params': param, 'lr': lr})
        print(f"   {name[:30]:30s} lr={lr:.0e}")

    print("\nDemo completed!")

if __name__ == "__main__":
    demo()
```

## 領域適應

當源領域和目標領域差異較大時：

```python
# 1. 領域對抗訓練
class DomainAdversarialModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.feature_extractor = FeatureExtractor()
        self.label_classifier = LabelClassifier()
        self.domain_classifier = DomainClassifier()

    def forward(self, x, alpha=1.0):
        features = self.feature_extractor(x)
        class_pred = self.label_classifier(features)
        domain_pred = self.domain_classifier(features)

        # 領域對抗損失
        return class_pred, domain_pred

# 2. 逐步微調
def progressive_fine_tune(model, train_loader, epochs_list):
    """逐步解冻更多層"""
    for epochs, num_layers_frozen in epochs_list:
        freeze_layers(model, num_layers_frozen)
        train(model, train_loader, epochs)
```

## 總結

遷移學習是深度學習的關鍵技術：

1. **節省時間**：不需要從頭訓練
2. **減少資料**：通常只需少量目標領域資料
3. **更好的泛化**：預訓練模型學習了通用特徵

最佳實踐：
- 選擇與目標任務相關的預訓練模型
- 從凍住大部分層開始，逐步解凍
- 使用較小的學習率
- 應用任務相關的資料增強

---

**延伸閱讀**

- [CS231n Transfer Learning](https://www.google.com/search?q=CS231n+transfer+learning)
- [Pretrained Models](https://www.google.com/search?q=pretrained+models+imageNet)
- [Domain Adaptation](https://www.google.com/search?q=domain+adaptation+deep+learning)