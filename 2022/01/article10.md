# 深度學習開發流程

## 概述

一個完整的深度學習專案從概念到部署通常包含六個階段。本文以圖像分類為例，介紹標準的開發流程。

## 階段一：問題定義

### 需求分析

- **任務類型**：分類、檢測、生成、回歸？
- **效能指標**：準確率、召回率、F1、延遲？
- **資源約束**：GPU 記憶體、推理時間、模型大小？

### 可行性評估

```python
# 確認硬體可用
import torch
print(f"CUDA available: {torch.cuda.is_available()}")
print(f"GPU count: {torch.cuda.device_count()}")
print(f"GPU name: {torch.cuda.get_device_name(0)}")
```

## 階段二：資料準備

### 資料收集

```python
import torchvision
from torchvision import transforms

dataset = torchvision.datasets.ImageFolder(
    root='data/train',
    transform=transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
    ])
)
```

### 資料劃分

```
訓練集：60-70%   用於模型訓練
驗證集：15-20%   用於超參數調整和模型選擇
測試集：15-20%   用於最終效能評估
```

### 資料增強

```python
train_transform = transforms.Compose([
    transforms.RandomResizedCrop(224),
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(10),
    transforms.ColorJitter(brightness=0.2, contrast=0.2),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225])
])
```

## 階段三：模型選擇

### 選擇策略

根據問題類型選擇基準模型：

- **圖像分類**：ResNet、EfficientNet、ViT
- **目標檢測**：YOLO、Faster R-CNN、DETR
- **語義分割**：UNet、DeepLab
- **文字分類**：BERT、RoBERTa

```python
import torchvision.models as models

model = models.resnet18(pretrained=True)
model.fc = nn.Linear(512, num_classes)
```

### 模型大小與效能權衡

| 模型 | 參數 | 準確率 | 推理時間 | 適用場景 |
|------|------|-------|---------|---------|
| ResNet-18 | 11M | 69.8% | 1x | 邊緣裝置 |
| ResNet-50 | 25M | 76.1% | 2x | 伺服器 |
| ResNet-152 | 60M | 78.3% | 4x | 準確優先 |
| EfficientNet-B7 | 66M | 84.3% | 8x | 高效能 |

## 階段四：訓練與調優

### 訓練腳本模板

```python
def train_model(model, train_loader, val_loader, epochs=30):
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.AdamW(model.parameters(), lr=1e-4)
    scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=epochs)
    
    best_acc = 0.0
    for epoch in range(epochs):
        model.train()
        for images, labels in train_loader:
            images, labels = images.cuda(), labels.cuda()
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
        
        # 驗證
        model.eval()
        acc = evaluate(model, val_loader)
        print(f"Epoch {epoch}: Val Acc {acc:.2f}%")
        
        if acc > best_acc:
            best_acc = acc
            torch.save(model.state_dict(), 'best_model.pth')
        
        scheduler.step()
```

### 超參數調優

關鍵超參數及其影響：

```
學習率：    1e-5 ~ 1e-3   影響收斂速度和穩定性
批次大小：  16 ~ 256       影響記憶體使用和梯度品質
優化器：    Adam / SGD     影響收斂特性
權重衰減：  1e-5 ~ 1e-3    L2 正則化強度
Dropout：   0.1 ~ 0.5      正則化強度
```

## 階段五：評估

### 模型分析

```python
# 混淆矩陣
from sklearn.metrics import confusion_matrix, classification_report

y_true, y_pred = [], []
model.eval()
with torch.no_grad():
    for images, labels in test_loader:
        outputs = model(images.cuda())
        _, predicted = torch.max(outputs, 1)
        y_true.extend(labels.cpu().numpy())
        y_pred.extend(predicted.cpu().numpy())

print(classification_report(y_true, y_pred))
print(confusion_matrix(y_true, y_pred))
```

### 錯誤分析

對錯誤分類的樣本進行分析，尋找模式：
- 哪些類別容易混淆？
- 哪些類型（光照、角度）的樣本容易出錯？
- 資料標註是否正確？

## 階段六：部署

### 模型轉換

```python
# 轉換為 TorchScript
model.eval()
example = torch.randn(1, 3, 224, 224).cuda()
traced_model = torch.jit.trace(model, example)
traced_model.save('model.pt')

# 轉換為 ONNX
torch.onnx.export(model, example, 'model.onnx',
                  input_names=['input'],
                  output_names=['output'],
                  dynamic_axes={'input': {0: 'batch_size'}})
```

### 部署選項

| 方式 | 延遲 | 吞吐量 | 靈活性 |
|------|------|-------|-------|
| PyTorch Serving | 低 | 高 | 好 |
| ONNX Runtime | 極低 | 極高 | 中 |
| TensorRT | 極低 | 極高 | 差 |
| TFLite（行動端） | 低 | 中 | 中 |

### API 服務

```python
from flask import Flask, request, jsonify
import torch

app = Flask(__name__)
model = torch.jit.load('model.pt').cuda().eval()

@app.route('/predict', methods=['POST'])
def predict():
    image = preprocess(request.files['image'])
    with torch.no_grad():
        output = model(image.unsqueeze(0))
        _, predicted = torch.max(output, 1)
    return jsonify({'class': predicted.item()})
```

## 最佳實踐總結

1. **先建立基準**：先使用預訓練模型快速建立基準線
2. **迭代改進**：逐步增加複雜度，觀察改進效果
3. **自動記錄**：使用 TensorBoard 或 WandB 記錄實驗
4. **程式碼版本控制**：使用 Git 管理程式碼和實驗配置
5. **隨機種子固定**：確保實驗可重現
6. **逐步增加**：先在小資料子集上驗證，再擴展到完整資料集

---

## 延伸閱讀

- [PyTorch 官方教學](https://www.google.com/search?q=PyTorch+official+tutorial)
- [MLOps 實務指南](https://www.google.com/search?q=MLOps+best+practices)
- [模型部署最佳實踐](https://www.google.com/search?q=deep+learning+model+deployment+guide)

*本篇文章為「AI 程式人雜誌 2022 年 1 月號」精選文章。*
