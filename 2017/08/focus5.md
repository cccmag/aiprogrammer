# YOLO 即時物體偵測

## YOLO 設計理念

You Only Look Once (YOLO) 的核心思想：**將物體偵測當作迴歸問題**，在單一網路中直接預測邊界框和類別機率。

## YOLO v1 (2016) 原理

### 網格划分

將輸入圖像劃分為 S×S 網格（如 7×7）。每個網格負責預測該區域內的物體。

```python
# YOLO 網格概念
S = 7  # 7x7 網格
B = 2  # 每格 2 個候選框
C = 20  # Pascal VOC 20 類別

# 輸出張量: S × S × (B*5 + C) = 7 × 7 × (2*5 + 20) = 7 × 7 × 30
```

每個候選框包含：
- (x, y)：框的中心座標
- (w, h)：框的寬高（相對於圖像）
- confidence：框包含物體的信心度

### 損失函數

```python
# YOLO 損失包含多個部分
loss = (
    # 1. 包含物體的候選框座標損失
    lambda_coord * sum([(x - x_true)^2 + (y - y_true)^2
                       + (sqrt(w) - sqrt(w_true))^2 + (sqrt(h) - sqrt(h_true))^2
                       for obj in objects]),

    # 2. 不包含物體的候選框 confidence 損失（較小權重）
    + sum([(confidence - 0)^2 for no_obj in no_objects]),

    # 3. 包含物體的候選框 confidence 損失
    + sum([(confidence - 1)^2 for obj in objects]),

    # 4. 類別損失（只有負責該物體的網格才計算）
    + sum([(class_probs - class_true)^2 for obj in objects])
)
```

## YOLO v2 (2016) 改進

### 1. Batch Normalization

在每層卷積後加入 BN，收斂更快，泛化能力更強。

### 2. High Resolution Classifier

先用高解析度圖像微調分類器，再用檢測資料微調。

### 3. Anchor Boxes

使用 k-means 聚類自動學習 anchor boxes，取代手工設計。

```python
# k-means 產生 anchor
def kmeans_anchors(boxes, k=5):
    # 對邊界框尺寸進行 k-means 聚類
    # 使用 IoU 作為距離度量
    pass
```

### 4. Passthrough Layer

連結淺層特徵圖，幫助偵測小物體。

### 5. 多尺度訓練

不同 epoch 使用不同輸入尺寸，增強魯棒性。

## Darknet 框架

YOLO 使用的開源深度學習框架。

```bash
# 下載 Darknet
git clone https://github.com/pjreddie/darknet.git
cd darknet
make

# 下載預訓練權重
wget https://pjreddie.com/media/files/yolo.weights
```

### 使用 Darknet 進行偵測

```bash
# 圖像偵測
./darknet detect cfg/yolo.cfg yolo.weights data/dog.jpg

# 即時偵測（需要 webcam）
./darknet detect webcam
```

## YOLO v2 架構

```python
# Darknet-19 主幹網路（19 層卷積）
# 5 次最大池化
# 全域平均池化
# 1000 類分類器

# 修改用於檢測
# - 移除分類頭
# - 加入 detection head
# - 使用 anchor boxes
```

## Keras / TensorFlow 實作

### 簡化版 YOLO 概念

```python
import numpy as np

def yolo_predict(image, anchors, num_classes=20):
    """
    簡化版 YOLO 預測
    """
    # image: (416, 416, 3)
    # 輸出: (13, 13, num_anchors, 5+num_classes)

    grid_size = 13  # 416/32 = 13
    predictions = np.zeros((grid_size, grid_size, len(anchors), 5 + num_classes))

    for i in range(grid_size):
        for j in range(grid_size):
            for a, anchor in enumerate(anchors):
                # 預測偏移量
                tx, ty, tw, th, to = predictions[i, j, a, :5]

                # 轉換為實際座標
                x = (j + sigmoid(tx)) * 32  # 細胞左上角 + 偏移
                y = (i + sigmoid(ty)) * 32
                w = anchor[0] * exp(tw)
                h = anchor[1] * exp(th)

                # 信心度
                confidence = sigmoid(to)

                # 類別機率
                class_probs = softmax(predictions[i, j, a, 5:])

                predictions[i, j, a] = [x, y, w, h, confidence, *class_probs]

    return predictions

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def softmax(x):
    exp_x = np.exp(x - np.max(x))
    return exp_x / exp_x.sum()
```

### 實際使用 YOLO

```bash
pip install opencv-python

# 或使用 keras-yolo3
git clone https://github.com/qqwweee/keras-yolo3.git
cd keras-yolo3
python convert.py yolov3.cfg yolov3.weights model_data/yolo.h5
python yolo_video.py --image
```

## YOLO 的優勢

1. **速度快**：45-155 FPS（取決於版本）
2. **端到端**：單一網路，無需候選區域產生
3. **上下文感知**：能看到整張圖像，而非局部

## 限制

1. 對小物體偵測效果較差
2. 約束每格只能偵測一類物體（通常一類）
3. 輸入解析度固定（416×416 常見）

## YOLO v3 (2018) 預告

2018 年將發布的 v3 版本使用：
- 更大的 Darknet-53 主幹網路
- 多尺度偵測（小、中、大物體）
- 更好的 anchor matching

## 總結

YOLO 開創了一階段物體偵測的先河，實現了實時偵測的可能。從 v1 到 v2 不斷改進，平衡速度與精度。適用於需要即時性的場景。