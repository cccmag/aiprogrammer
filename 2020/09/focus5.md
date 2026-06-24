# 物體檢測的進展

## 從 R-CNN 到 YOLO

### 歷史回顧

物體檢測經歷了從傳統方法到深度學習的根本性轉變。

---

## 一、兩階段檢測器

### R-CNN (2014)

首個基於 CNN 的物體檢測器：

```
輸入圖像
  ↓
選擇性搜索 (Selective Search) 生成候選區域
  ↓
對每個候選區域裁剪並變換大小
  ↓
CNN 提取特徵
  ↓
SVM 分類 + 邊界框回歸
```

問題：非常慢，每張圖像需要 47 秒。

### Fast R-CNN (2015)

加速版本：

```
輸入圖像
  ↓
CNN 特徵提取（整張圖像一次）
  ↓
感興趣區域 (RoI) 池化
  ↓
分類和邊界框回歸
```

訓練從多階段變為單一階段。

### Faster R-CNN (2015)

引入 Region Proposal Network (RPN)：

```
輸入圖像
  ↓
CNN 特徵提取
  ↓
RPN 生成候選區域
  ↓
RoI 池化 + 分類/回歸
```

---

## 二、單階段檢測器

### YOLO (You Only Look Once, 2016)

將檢測視為迴歸問題：

```
輸入圖像劃分為 S×S 網格
  ↓
每個網格預測 B 個邊界框 + 信心分數 + 類別機率
  ↓
NMS 非極大值抑制
  ↓
最終檢測結果
```

```python
# YOLO 的輸出
# [S, S, B*5 + C] 其中 5 = (x, y, w, h, confidence)
```

### SSD (Single Shot MultiBox Detector, 2016)

多尺度特徵圖檢測：

```
輸入圖像
  ↓
不同尺度的特徵圖（38x38, 19x19, 10x10, ...）
  ↓
每層特徵圖的 Default Boxes
  ↓
分類和位置回歸
```

---

## 三、YOLO 版本演化

| 版本 | 年份 | 主要改進 |
|------|------|---------|
| YOLOv1 | 2016 | 單階段檢測 |
| YOLOv2 | 2017 | 更好更快，添加先驗框 |
| YOLOv3 | 2018 | 多尺度，FPN，Darknet-53 |
| YOLOv4 | 2020 | CSPDarknet, PAN, Mosaic |
| YOLOv5 | 2020 | 超引數進化，工程優化 |

### YOLOv4 (2020) 的創新

```python
# 骨幹網路：CSPDarknet53
# 脖頸部：SPP, PAN
# 頭部：YOLOv3

# 訓練技巧
- Mosaic 資料增強
- 標籤平滑
- CIOU 損失
- DropBlock 正則化
```

---

## 四、比較

| 方法 | mAP | FPS | 優缺點 |
|------|-----|-----|--------|
| Faster R-CNN | 高 | 慢 | 高精度、適合小物體 |
| YOLOv3 | 中高 | 快 | 平衡 |
| SSD | 中 | 快 | 適合多尺度 |
| EfficientDet | 高 | 中 | 效率良好 |

---

## 五、2020 年的進展

### EfficientDet (2020)

Google 的複合縮放方法應用於檢測：

```python
# BiFPN：雙向特徵金字塔網路
# 複合縮放：骨幹網路、特征網路、盒/類別預測網路
```

### 關鍵突破

1. **Anchor-free 方法**：FCOS、CenterNet
2. **Transformer-based**：DETR (2020)

### DETR (2020)

使用 Transformer 的端到端檢測：

```python
# 流程
圖像 -> CNN 骨幹 -> Transformer Encoder-Decoder -> 物件集合預測

# 優點：移除 NMS 等後處理
# 缺點：收斂慢，小物體表現不佳
```

---

**下一步**：[語義分割與實例分割](focus6.md)

## 延伸閱讀

- [object+detection+R-CNN+YOLO+SSD+2020](https://www.google.com/search?q=object+detection+R-CNN+YOLO+SSD+2020)
- [Faster+R-CNN+region+proposal+network](https://www.google.com/search?q=Faster+R-CNN+region+proposal+network)