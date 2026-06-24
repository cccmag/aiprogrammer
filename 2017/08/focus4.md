# 物體偵測演算法

## 物體偵測的挑戰

物體偵測需要同時完成：
1. **分類**：判断物體類別
2. **定位**：找出物體位置（邊界框）

## 兩階段偵測器（Two-stage）

先產生候選區域，再進行分類。

### R-CNN (2014)

Region-based CNN，開創性的兩階段方法。

```
輸入圖像
    ↓
Selective Search → 產生 ~2000 候選框
    ↓
 warp/ resize 每個候選框
    ↓
 CNN 特徵提取（每個候選框獨立）
    ↓
 SVM 分類
    ↓
 邊界框回歸
```

缺點：太慢（每張圖 ~50 秒）

### Fast R-CNN (2015)

改進 R-CNN 的效率問題。

```python
# Fast R-CNN 核心思想
# 1. 整張圖通過 CNN 一次（共用特徵）
# 2. RoI Pooling 從特徵圖取候選區域特徵
# 3. 統一的全連接層分類 + 回歸
```

速度提升至 ~2 秒/圖。

### Faster R-CNN (2015)

用 Region Proposal Network (RPN) 取代 Selective Search。

```python
# Faster R-CNN 架構概念

# Backbone: ResNet / VGG 提取特徵

# RPN (Region Proposal Network)
# - 在特徵圖每個位置產生 anchor boxes
# - 判斷每個 anchor 是否有物體
# - 回歸邊界框偏移

# RoI Pooling
# - 從特徵圖取出候選區域
# - 統一尺寸後分類

def faster_rcnn(image):
    features = backbone(image)  # ResNet/VGG

    # RPN
    proposals = rpn(features)  # ~300 候選框

    # 分類 + 回歸
    class_scores, boxes = detection_head(features, proposals)

    return class_scores, boxes
```

## 一階段偵測器（One-stage）

直接從特徵圖預測類別與位置。

### YOLO (You Only Look Once)

將圖像分割成網格，直接預測邊界框。

```
輸入圖像 → 網格分割（7x7）
    ↓
 每格預測：2 個邊界框 + 類別機率
    ↓
 全圖預測一次（hence "You Only Look Once"）
```

### SSD (Single Shot MultiBox Detector)

多尺度特徵圖偵測。

```python
# SSD 概念

# 不同層度的特徵圖偵測不同大小的物體
feature_maps = [
    conv4_3,   # 小物體
    fc7,       # 中小物體
    conv6_2,   # 中物體
    conv7_2,   # 中大物體
    conv8_2,   # 大物體
]

predictions = [predict_boxes(fm) for fm in feature_maps]
```

## 比較

| 方法 | mAP | 速度 (FPS) |
|------|-----|-----------|
| R-CNN | 66.0 | 0.5 |
| Fast R-CNN | 70.0 | 2.0 |
| Faster R-CNN | 73.2 | 5.0 |
| YOLO | 63.4 | 45 |
| SSD300 | 77.2 | 46 |
| SSD500 | 78.1 | 19 |

## Anchor Boxes

現代偵測器的核心概念。

```python
# Anchor boxes 範例
anchor_sizes = [32, 64, 128, 256, 512]
aspect_ratios = [0.5, 1.0, 2.0]

# 產生的 anchor 數量
# 5 sizes × 3 ratios = 15 anchors per position
```

每個位置產生多個不同大小和形狀的 anchor，預測相對於 anchor 的偏移量。

## 非極大值抑制（NMS）

去除重複的偵測框。

```python
import numpy as np

def nms(boxes, scores, iou_threshold=0.5):
    # boxes: Nx4 (x1, y1, x2, y2)
    # scores: N

    indices = np.argsort(scores)[::-1]  # 從高分到低分

    keep = []
    while len(indices) > 0:
        current = indices[0]
        keep.append(current)

        if len(indices) == 1:
            break

        # 計算 IoU
        current_box = boxes[current]
        rest_boxes = boxes[indices[1:]]

        ious = compute_iou(current_box, rest_boxes)

        # 移除 IoU 過高的框
        indices = indices[1:][ious < iou_threshold]

    return keep

def compute_iou(box, boxes):
    # 計算一個 box 與多個 boxes 的 IoU
    x1 = np.maximum(box[0], boxes[:, 0])
    y1 = np.maximum(box[1], boxes[:, 1])
    x2 = np.minimum(box[2], boxes[:, 2])
    y2 = np.minimum(box[3], boxes[:, 3])

    intersection = np.maximum(0, x2 - x1) * np.maximum(0, y2 - y1)

    area1 = (box[2] - box[0]) * (box[3] - box[1])
    area2 = (boxes[:, 2] - boxes[:, 0]) * (boxes[:, 3] - boxes[:, 1])

    union = area1 + area2 - intersection

    return intersection / (union + 1e-6)
```

## 評估指標：IoU

Intersection over Union，衡量偵測框準確度。

```python
def compute_iou(box1, box2):
    x1 = max(box1[0], box2[0])
    y1 = max(box1[1], box2[1])
    x2 = min(box1[2], box2[2])
    y2 = min(box1[3], box2[3])

    intersection = max(0, x2 - x1) * max(0, y2 - y1)

    area1 = (box1[2] - box1[0]) * (box1[3] - box1[1])
    area2 = (box2[2] - box2[0]) * (box2[3] - box2[1])
    union = area1 + area2 - intersection

    return intersection / (union + 1e-6)
```

## 總結

物體偵測從兩階段方法（R-CNN 系列）發展到一階段方法（YOLO、SSD）。Faster R-CNN 實現了高精度，YOLO/SSD 實現了實時性。選擇哪種方法取決於應用場景的需求。