# 物體偵測

## RCNN、YOLO 與 Faster RCNN

物體偵測是電腦視覺的核心任務之一，需要同時定位和識別影像中的多個物體。

---

## 任務定義

```
輸入：圖像
輸出：邊界框 (Bounding Box) + 類別標籤

多個物體可能同時存在：
├── 車 (x1, y1, x2, y2) - 95% confidence
├── 人 (x1, y1, x2, y2) - 87% confidence
└── 狗 (x1, y1, x2, y2) - 78% confidence
```

---

## 兩階段 vs 單階段

| 類型 | 方法 | 特點 | 代表模型 |
|-----|------|------|---------|
| 兩階段 | 先提候選框，再分類 | 精確但慢 | RCNN, Fast RCNN, Faster RCNN |
| 單階段 | 直接預測 | 快但稍不精確 | YOLO, SSD |

---

## RCNN 系列

### RCNN（2014）

Region-based CNN：

```python
# RCNN 流程
# 1. 選擇性搜索（Selective Search）產生候選區域
# 2. 對每個區域運行 CNN 提取特徵
# 3. 使用 SVM 分類每個區域

def rcnn_detect(image):
    # 步驟 1: 產生 ~2000 個候選框
    proposals = selective_search(image)

    # 步驟 2: 對每個候選框提取 CNN 特徵
    features = []
    for prop in proposals:
        feat = cnn.extract(warped_image(prop))
        features.append(feat)

    # 步驟 3: SVM 分類
    predictions = svm_classify(features)

    return predictions
```

問題：
- 慢（每張圖像需要幾十秒）
- 不是端到端訓練

### Fast RCNN（2015）

改進：

```python
# 改進 1: 共享卷積計算
# 只對整張圖像跑一次 CNN

# 改進 2: RoI Pooling
def roi_pooling(feature_map, roi, output_size):
    # 將不同大小的候選框池化到相同大小
    h, w = output_size
    roi_h, roi_w = roi.height, roi.width

    # 劃分為 h×w 網格
    # 每個格子做 Max Pooling
    return pooled_features
```

### Faster RCNN（2016）

真正端到端的物體偵測：

```python
# Faster RCNN = RPN + Fast RCNN

class FasterRCNN(nn.Module):
    def __init__(self):
        self.backbone = ResNet()
        self.rpn = RegionProposalNetwork()  # 區域提議網路
        self.roi_pool = RoIPooling()
        self.classifier = FastRCNNHead()

    def forward(self, image):
        features = self.backbone(image)

        # RPN 產生候選框
        proposals = self.rpn(features)

        # 對候選框分類和邊界框回歸
        detections = self.classifier(self.roi_pool(features, proposals))

        return detections
```

### RPN（Region Proposal Network）

```python
#  Anchor 機制
# 在每個位置產生多個 anchor boxes
anchors = generate_anchors(base_size=16, ratios=[0.5, 1, 2], scales=[8, 16, 32])

# RPN 輸出
# 每個 anchor: 是否包含物體 + 邊界框精修
```

---

## YOLO 系列

### YOLOv1（2016）

單階段回歸方法：

```python
# 將影像劃分為 S×S 網格
# 每個格子預測 B 個邊界框 + C 個類別機率

# YOLOv1: S=7, B=2, C=20 (Pascal VOC)

class YOLO(nn.Module):
    def __init__(self):
        self.backbone = DarkNet()
        self.fc = nn.Linear(1024, 1470)  # 7*7*30

    def forward(self, x):
        # 7×7×(5*B + C) = 7×7×30
        output = self.fc(self.backbone(x))
        return output.view(-1, 7, 7, 30)
```

### YOLOv2（2017）

改進：

```python
# 1. 更好的骨幹網路（Darknet-19）
# 2. Anchor boxes（類似 Faster RCNN）
# 3. 階層式類別預測
# 4. 多尺度訓練
```

### YOLOv3（2018）

現代 YOLO：

```python
# 1. FPN（特徵金字塔網路）
# 2. 多尺度預測
# 3. 更好的骨幹（Darknet-53）
# 4. Logistic 回歸用於類別預測
```

### 比較

| 模型 | mAP | FPS |
|-----|-----|-----|
| Faster RCNN | 76.4% | 5 FPS |
| YOLOv2 | 76.8% | 67 FPS |
| YOLOv3 | 57.9% | 52 FPS (416x416) |

---

## SSD（Single Shot Detector）

```python
# SSD: 多尺度特徵圖 + Default boxes

class SSD(nn.Module):
    def __init__(self):
        self.base_network = VGG16()
        self.extra_layers = []  # 更多特徵圖
        self.conf_head = []     # 類別預測
        self.loc_head = []      # 位置預測

    def forward(self, x):
        # 多尺度特徵圖
        # 38x38, 19x19, 10x10, 5x5, 3x3, 1x1
        features = self.extract_features(x)

        # 在每個尺度預測
        predictions = []
        for feat in features:
            pred = self.predict(feat)
            predictions.append(pred)

        return predictions
```

---

## 評估指標

### IoU（Intersection over Union）

```python
def iou(box1, box2):
    """計算兩個邊界框的 IoU"""
    x1 = max(box1[0], box2[0])
    y1 = max(box1[1], box2[1])
    x2 = min(box1[2], box2[2])
    y2 = min(box1[3], box2[3])

    intersection = max(0, x2 - x1) * max(0, y2 - y1)
    area1 = (box1[2] - box1[0]) * (box1[3] - box1[1])
    area2 = (box2[2] - box2[0]) * (box2[3] - box2[1])

    return intersection / (area1 + area2 - intersection)
```

### mAP（mean Average Precision）

```python
# 對每個類別計算 AP，然後取平均
def calculate_map(all_detections, all_ground_truths):
    aps = []
    for class_id in classes:
        dets = all_detections[class_id]
        gts = all_ground_truths[class_id]
        ap = calculate_ap(dets, gts)
        aps.append(ap)
    return np.mean(aps)
```

---

## 延伸閱讀

- [RCNN 論文](https://www.google.com/search?q=RCNN+Girshick+2014)
- [YOLO 論文](https://www.google.com/search?q=YOLO+Redmon+2016)
- [Faster RCNN 論文](https://www.google.com/search?q=Faster+RCNN+Ren+2015)

---

*本篇文章為「AI 程式人雜誌 2019 年 5 月號」系列文章之一。*