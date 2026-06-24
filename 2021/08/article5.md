# 物件偵測演算法

物件偵測是電腦視覺的重要任務，本文介紹經典演算法。

## 1. 兩階段偵測器

**Faster R-CNN**：
- Region Proposal Network (RPN)
- ROI Pooling
- 分類和邊界框回歸

```python
class FasterRCNN(nn.Module):
    def __init__(self, backbone, num_classes):
        super().__init__()
        self.rpn = RPN(backbone.output_dim)
        self.roi_head = ROIHead(backbone.output_dim, num_classes)

    def forward(self, images, targets=None):
        features = self.backbone(images)
        proposals = self.rpn(features, targets)
        detections = self.roi_head(features, proposals, targets)
        return detections
```

## 2. 單階段偵測器

**YOLO (You Only Look Once)**：
- 直接預測邊界框和類別
- 速度快，適合即時應用

```python
class YOLOv1(nn.Module):
    def __init__(self, S=7, B=2, C=20):
        super().__init__()
        self.S = S
        self.B = B
        self.C = C
        self.backbone = DarknetBackbone()
        self.head = YOLOHead(S, B, C + 5 * B)

    def forward(self, x):
        features = self.backbone(x)
        predictions = self.head(features)
        return predictions
```

## 3. 評估指標

- mAP (mean Average Precision)
- IoU (Intersection over Union)
- FPS (Frames Per Second)

---

## 延伸閱讀

- [Faster R-CNN 論文](https://www.google.com/search?q=Faster+R-CNN+towards+real-time+object+detection)
- [YOLO 官方網站](https://www.google.com/search?q=YOLO+object+detection+you+only+look+once)