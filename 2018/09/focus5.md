# 物件偵測：R-CNN 到 YOLO

## 1. 物件偵測任務

```python
# 任務輸入：一張影像
# 任務輸出：
# - 多個邊界框（bounding boxes）
# - 每個框的類別標籤
# - 每個框的信心度
```

## 2. R-CNN（2014）

### 流程

```python
# R-CNN 流程
# 1. 候選區域生成（Selective Search）
# 2. 對每個候選區域裁剪並變換大小
# 3. CNN 特徵萃取（AlexNet）
# 4. SVM 分類 + 邊界框回歸

# 問題：太慢（每張圖幾十秒）
```

## 3. Fast R-CNN（2015）

### 改進

```python
# Fast R-CNN 流程
# 1. 候選區域生成（共用卷積特徵）
# 2. 對整張圖提取特徵圖（一次 CNN）
# 3. ROI Pooling 從特徵圖中取出候選區域
# 4. 單一網路同時預測類別和邊界框
```

### ROI Pooling

```python
# 將不同大小的候選區域pooling到固定大小
def roi_pooling(feature_map, roi, output_size=7):
    # feature_map: (C, H, W)
    # roi: (x1, y1, x2, y2)
    # 輸出: (C, output_size, output_size)
```

## 4. Faster R-CNN（2016）

### Region Proposal Network

```python
# Faster R-CNN 流程
# 1. 骨幹網路提取特徵圖
# 2. RPN 網路生成候選框
# 3. ROI Head 進行分類和邊界框回歸

# 幾乎端到端訓練，速度大幅提升
```

## 5. YOLO（2016）

### 核心思想

```python
# YOLO 流程
# 1. 將輸入影像劃分為 SxS 網格
# 2. 每個網格預測 B 個邊界框 + 信心度 + C 類機率
# 3. 一次性輸出所有預測

# 單次網路前向傳播，實現即時偵測
```

### YOLOv1 輸出

```python
# S=7, B=2, C=20（Pascal VOC）
# 輸出張量：7x7x(2*5+20) = 7x7x30

# 每個邊界框：(x, y, w, h, confidence)
# 5 個值 × 2 個框 + 20 個類別 = 30
```

## 6. SSD（2016）

### 多尺度特徵圖

```python
# SSD 流程
# 1. 骨幹網路（VGG）
# 2. 多尺度特徵圖（如 38x38, 19x19, 10x10...）
# 3. 每層特徵圖預測不同大小的物件

# 比 YOLO 更準確，比 Faster R-CNN 更快
```

## 7. YOLOv2 / YOLO9000（2016）

### 改進

```python
# YOLOv2 改進
# - 預設框（Anchor Boxes）
# - 維度聚類（K-means 自動學習 anchor）
# - 多尺度訓練
# - Batch Normalization
# - 移除全連接層
```

## 8. 比較表

| 方法 | mAP | FPS | 優點 | 缺點 |
|------|-----|-----|------|------|
| R-CNN | 66.0% | 0.03 | 簡單 | 慢 |
| Fast R-CNN | 70.0% | 0.5 | 統一框架 | 仍需外部 RP |
| Faster R-CNN | 73.3% | 7 | 幾乎端到端 | 複雜 |
| SSD300 | 77.2% | 46 | 多尺度 | 小物體 |
| YOLOv1 | 63.4% | 45 | 非常快 | 精度一般 |
| YOLOv2 | 78.6% | 40 | 速度與精度平衡 | 中小物體 |

## 9. 小結

從 R-CNN 到 YOLO，物件偵測經歷了從慢到快、從多階段到端到端的發展歷程。Faster R-CNN 適合高精度需求，YOLO 適合即時應用。

---

**下一步**：[語義分割：FCN 與 U-Net](focus6.md)