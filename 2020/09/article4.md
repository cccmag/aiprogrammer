# 遷移學習實戰

## 前言

遷移學習讓我們可以使用預訓練模型來加速訓練並提高效能。本文介紹在 PyTorch 中如何使用遷移學習。

---

## 一、遷移學習原理

### 為何有效？

預訓練模型已經在大規模資料集（如 ImageNet）上學習了豐富的視覺特徵：
- 淺層：邊緣、紋理
- 中層：形狀、物體部件
- 深層：物體類別

### 策略選擇

| 策略 | 適用場景 |
|------|---------|
| 特徵提取 | 資料量少、GPU 資源有限 |
| 全模型微調 | 資料充足、訓練時間充裕 |
| 混合策略 | 部分層凍住、部分微調 |

---

## 二、特徵提取

### 只訓練分類頭

```python
import torchvision.models as models

# 載入預訓練模型
model = models.resnet18(pretrained=True)

# 凍住所有參數
for param in model.parameters():
    param.requires_grad = False

# 替換分類頭
model.fc = nn.Linear(model.fc.in_features, num_classes)

# 只優化新分類頭的參數
optimizer = optim.Adam(model.fc.parameters(), lr=0.001)
```

### 使用特徵提取器

```python
# 移除分類頭，獲取特徵
feature_extractor = nn.Sequential(*list(model.children())[:-1])

features = feature_extractor(images)  # (B, 512, 1, 1)
features = features.squeeze()  # (B, 512)
```

---

## 三、全模型微調

### 微調整個網路

```python
model = models.resnet18(pretrained=True)
model.fc = nn.Linear(model.fc.in_features, num_classes)

# 學習率設低一些
optimizer = optim.Adam([
    {'params': model.conv1.parameters(), 'lr': 1e-5},
    {'params': model.layer1.parameters(), 'lr': 1e-5},
    {'params': model.layer2.parameters(), 'lr': 1e-4},
    {'params': model.fc.parameters(), 'lr': 1e-3}
], lr=1e-3)
```

---

## 四、混合策略

### 部分層凍住

```python
model = models.resnet18(pretrained=True)

# 凍住前面的層
for param in model.conv1.parameters():
    param.requires_grad = False
for param in model.bn1.parameters():
    param.requires_grad = False

# 檢查哪些參數可訓練
trainable_params = [p for p in model.parameters() if p.requires_grad]
print(f"Trainable parameters: {sum(p.numel() for p in trainable_params):,}")
```

---

## 五、CIFAR-10 實戰

### 完整流程

```python
import torchvision.models as models
import torchvision.datasets as datasets
import torchvision.transforms as transforms

# 1. 資料載入
transform_train = transforms.Compose([
    transforms.RandomCrop(32, padding=4),
    transforms.RandomHorizontalFlip(),
    transforms.ToTensor(),
    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
])

train_dataset = datasets.CIFAR10(root='./data', train=True,
                                 transform=transform_train, download=True)

# 2. 模型
model = models.resnet18(pretrained=True)
model.fc = nn.Linear(model.fc.in_features, 10)

# 3. 訓練
criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(model.parameters(), lr=0.1, momentum=0.9, weight_decay=5e-4)
scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=30, gamma=0.1)

for epoch in range(90):
    train(model, train_loader, criterion, optimizer)
    scheduler.step()
```

---

## 六、使用不同預訓練模型

| 模型 | 參數量 | 特色 |
|------|--------|------|
| ResNet-18 | 11.7M | 輕量、平衡 |
| ResNet-50 | 25.6M | 中等效能 |
| EfficientNet-B0 | 5.3M | 高效率 |
| VGG-16 | 138M | 經典 |
| MobileNetV2 | 3.5M | 邊緣友好 |

---

## 七、注意事項

### 1. 資料集相似度

- 相似度高：浅層特徵直接可用，微調高層即可
- 相似度低：需要更多微調

### 2. 學習率設定

```python
# 預訓練層用較小學習率
optimizer = optim.Adam([
    {'params': model.feature.parameters(), 'lr': 1e-4},
    {'params': model.classifier.parameters(), 'lr': 1e-3}
])
```

### 3. 訓練時間

預訓練模型通常能大幅縮短訓練時間。

---

## 結語

遷移學習是實用且有效的方法。選擇合適的策略可以讓我們在有限資源下獲得良好的模型。

---

*延伸閱讀：[transfer+learning+PyTorch+vision+2020](https://www.google.com/search?q=transfer+learning+PyTorch+vision+2020)*