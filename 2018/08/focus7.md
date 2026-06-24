# PyTorch 預訓練模型庫

## torchvision.models

### 常用預訓練模型

```python
from torchvision import models

# 影像分類
resnet = models.resnet18(pretrained=True)
resnet = models.resnet34(pretrained=True)
resnet = models.resnet50(pretrained=True)
resnet = models.resnet101(pretrained=True)

vgg = models.vgg16(pretrained=True)
vgg = models.vgg19(pretrained=True)

densenet = models.densenet121(pretrained=True)

inception = models.inception_v3(pretrained=True)
```

### 修改預訓練模型

```python
# 修改最後一層用於自己的分類任務
num_features = resnet.fc.in_features
resnet.fc = nn.Linear(num_features, 10)  # 10 類分類

# 移除最後一層作為特徵萃取器
resnet = models.resnet18(pretrained=True)
resnet = nn.Sequential(*list(resnet.children())[:-1])  # 移除分類頭
```

### TorchVision 模型對照表

| 模型 | Top-1 錯誤率 | 參數數量 | 適合場景 |
|------|-------------|----------|----------|
| ResNet18 | 30.43% | 11.7M | 入門首選 |
| ResNet50 | 24.01% | 25.6M | 一般用途 |
| VGG16 | 28.50% | 138M | 遷移學習 |
| DenseNet121 | 25.02% | 8.0M | 記憶體受限 |
| InceptionV3 | 22.55% | 23.9M | 高精度需求 |

### 影像特徵萃取

```python
from torchvision import transforms
from torch.autograd import Variable

preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

img = Image.open('cat.jpg')
img_tensor = preprocess(img).unsqueeze(0)

# 萃取特徵
resnet = models.resnet18(pretrained=True)
resnet.eval()
with torch.no_grad():
    features = resnet(img_tensor)
```

### 模型結構檢視

```python
# 顯示模型結構
print(resnet)

# 只看卷積層
conv_layers = [m for m in resnet.modules() if isinstance(m, nn.Conv2d)]
print(f"共 {len(conv_layers)} 個卷積層")

# 計算 FLOPs
from torchvision.models.resnet import resnet18
model = resnet18(pretrained=True)
print(f"參數數量: {sum(p.numel() for p in model.parameters())}")
```

### TorchVision 0.3 新增模型（2018）

```python
# SSD（單發多框檢測）
ssd = models.ssd300_vgg16(pretrained=True)

# Segmentation 模型
fcn = models.fcn_resnet101(pretrained=True)
deeplab = models.deeplabv3_resnet101(pretrained=True)
```

### 小結

torchvision.models 提供了豐富的預訓練模型，是遷移學習的強大工具。合理利用這些模型可以大幅減少訓練時間和計算資源。

---

**下一步**：[程式實作：PyTorch 神經網路建構實務](focus_code.md)

## 延伸閱讀

- [TorchVision Models](https://www.google.com/search?q=torchvision+pretrained+models+2018)
- [Transfer Learning Tutorial](https://www.google.com/search?q=pytorch+transfer+learning+tutorial)