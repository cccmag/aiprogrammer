# 電腦視覺進展：ResNet, 物體檢測, 語義分割

## 前言

2017 年，電腦視覺領域延續了深度學習帶來的革命性進步。ResNet 繼續主導物體識別，同時物體檢測和語義分割也取得了顯著突破。

## ResNet 的持續影響

### ResNet 的成功

2015 年提出的 ResNet 在 2017 年已成為電腦視覺的標準骨幹：

```python
# PyTorch 中的 ResNet
import torchvision.models as models

# 預訓練 ResNet
resnet18 = models.resnet18(pretrained=True)
resnet50 = models.resnet50(pretrained=True)
resnet152 = models.resnet152(pretrained=True)

# 迁移學習
for param in resnet18.parameters():
    param.requires_grad = False

resnet18.fc = nn.Linear(512, num_classes)
```

### 殘差連接的意義

```
┌─────────────────────────────────────────────────────────┐
│              殘差學習的優勢                               │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  傳統網路挑戰：                                         │
│  - 更深 = 梯度消失/爆炸                                  │
│  - 收斂困難                                            │
│                                                         │
│  ResNet 解決方案：                                       │
│  - 捷徑連接允許梯度直接流動                              │
│  - 可以訓練 1000+ 層的網路                              │
│  - 恆等映射保證起碼不比淺層差                           │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## 物體檢測的突破

### YOLO9000 (YOLOv2)

2017 年 12 月，Joseph Redmon 發布了 YOLO9000，可以即時檢測 9000 類物體：

```python
# YOLO 的核心思想
class YOLOv2(nn.Module):
    def __init__(self, num_anchors, num_classes):
        super().__init__()
        # 骨幹網路：Darknet-19
        self.backbone = Darknet19()

        # 檢測頭
        self.detection = nn.Sequential(
            nn.Conv2d(1024, 1024, 3, padding=1),
            nn.BatchNorm2d(1024),
            nn.LeakyReLU(0.1),

            # 預測層
            nn.Conv2d(1024, num_anchors * (5 + num_classes), 1)
        )

    def forward(self, x):
        # 骨幹特徵
        features = self.backbone(x)

        # 檢測
        output = self.detection(features)

        # 輸出形狀：[batch, anchors, h, w, 5+classes]
        # 5 = [x, y, w, h, confidence]
        return output
```

### Faster R-CNN

Region Proposal Network (RPN) 讓兩階段檢測更高效：

```python
# Faster R-CNN 架構
class FasterRCNN(nn.Module):
    def __init__(self):
        self.backbone = ResNet50()
        self.rpn = RegionProposalNetwork()
        self.roi_pooling = ROIPooling(output_size=(7, 7))
        self.head = FastRCNNHead(num_classes=80)

    def forward(self, x, gt_boxes=None):
        # 特徵提取
        features = self.backbone(x)

        # 生成 region proposals
        proposals, rpn_loss = self.rpn(features, gt_boxes)

        # ROI pooling
        pooled_features = self.roi_pooling(features, proposals)

        # 最終分類和回歸
        class_logits, box_regression = self.head(pooled_features)

        return class_logits, box_regression
```

## 語義分割

### DeepLabv3

Google 發布的 DeepLabv3 採用空洞卷積（Atrous Convolution）：

```python
class ASPP(nn.Module):
    """
    Atrous Spatial Pyramid Pooling
    使用不同 dilation rate 的卷積捕捉多尺度特徵
    """
    def __init__(self, in_channels, out_channels):
        super().__init__()
        self.atrous_block1 = nn.Conv2d(in_channels, out_channels, 1)
        self.atrous_block2 = nn.Conv2d(in_channels, out_channels, 3, padding=6, dilation=6)
        self.atrous_block3 = nn.Conv2d(in_channels, out_channels, 3, padding=12, dilation=12)
        self.atrous_block4 = nn.Conv2d(in_channels, out_channels, 3, padding=18, dilation=18)

        self.global_pool = nn.AdaptiveAvgPool2d(1)

    def forward(self, x):
        size = x.size()[2:]
        feat1 = self.atrous_block1(x)
        feat2 = self.atrous_block2(x)
        feat3 = self.atrous_block3(x)
        feat4 = self.atrous_block4(x)

        global_feat = self.global_pool(x)
        global_feat = F.interpolate(global_feat, size, mode='bilinear')

        return torch.cat([feat1, feat2, feat3, feat4, global_feat], dim=1)
```

## 2017 年重要模型時間線

```
┌─────────────────────────────────────────────────────────┐
│              2017 年電腦視覺模型                          │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  物體識別:                                            │
│  - ResNet (2015) → 標準骨幹                           │
│  - SENet (2017) - Squeeze-and-Excitation               │
│                                                         │
│  物體檢測:                                            │
│  - Faster R-CNN (2015) - 雨刷階段檢測                  │
│  - SSD (2015) - 單階段檢測                             │
│  - YOLO9000 (2017) - 9000 類檢測                       │
│  - RetinaNet (2017) - Focal Loss 解決類別不平衡        │
│                                                         │
│  語義分割:                                            │
│  - FCN (2015) - 全捲積網路                             │
│  - DeepLabv3 (2017) - 空洞卷積                        │
│  - PSPNet (2017) - 金字塔池化                         │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## 預訓練模型使用

```python
# 使用預訓練模型進行遷移學習
import torchvision.models as models

# 物體識別
model = models.resnet50(pretrained=True)
model.fc = nn.Linear(2048, num_classes)

# 語義分割
model = models.segmentation.deeplabv3_resnet50(pretrained=True)

# 實例分割
model = models.detection.mask_rcnn(pretrained=True)
```

## 對應用領域的影響

```
┌─────────────────────────────────────────────────────────┐
│              電腦視覺應用領域                            │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  自動駕駛：                                            │
│  - 車道線檢測                                          │
│  - 障礙物識別                                          │
│  - 交通標誌識別                                        │
│                                                         │
│  醫療影像：                                            │
│  - 腫瘤檢測                                            │
│  - 器官分割                                            │
│  - 病變分類                                            │
│                                                         │
│  人臉識別：                                            │
│  - 人臉偵測                                            │
│  - 特徵比對                                            │
│  - 情緒分析                                            │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## 總結

2017 年電腦視覺的發展特點：

1. **ResNet 成為標準**：幾乎所有新模型都基於殘差連接
2. **單階段檢測崛起**：YOLO、SSD 在速度和精度間取得平衡
3. **多尺度感知**：空洞卷積、金字塔池化成為主流
4. **遷移學習普及**：預訓練模型大幅減少訓練需求

---

**延伸閱讀**

- [ResNet Paper (He et al., 2016)](https://www.google.com/search?q=ResNet+He+2016)
- [YOLO9000 (Redmon & Farhadi, 2017)](https://www.google.com/search?q=YOLO9000+2017)
- [DeepLabv3 (Chen et al., 2017)](https://www.google.com/search?q=DeepLabv3+2017)

---

*本篇文章為「AI 程式人雜誌 2017 年 12 月號」年終回顧系列之一。*