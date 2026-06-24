# 語義分割與實例分割

## 像素級分類的演进

### 分割任務的類型

| 類型 | 說明 | 範例 |
|------|------|------|
| 語義分割 | 為每個像素分配類別 | 道路、建筑 |
| 實例分割 | 區分同類別的不同個體 | 人1、人2 |
| 全景分割 | 語義+實例 | 統一框架 |

---

## 一、語義分割

###FCN (Fully Convolutional Network, 2015)

將 CNN 的全連接層替換為卷積層：

```
輸入圖像
  ↓
CNN 特徵提取
  ↓
1x1 卷積 (不改變空間維度)
  ↓
上採樣 (轉置卷積)
  ↓
像素級分類
```

### U-Net (2015)

編碼器-解碼器架構 + 跳躍連接：

```python
class UNet(nn.Module):
    def __init__(self):
        # 編碼器（下採樣）
        self.enc1 = DoubleConv(3, 64)
        self.enc2 = DoubleConv(64, 128)
        self.enc3 = DoubleConv(128, 256)
        self.enc4 = DoubleConv(256, 512)

        # 瓶頸
        self.bottleneck = DoubleConv(512, 1024)

        # 解碼器（上採樣）+ 跳躍連接
        self.up4 = nn.ConvTranspose2d(1024, 512, 2, stride=2)
        self.dec4 = DoubleConv(1024, 512)
        # ... 更多解碼器層
```

### DeepLab 系列

使用 Atrous Convolution（空洞卷積）擴大感受野：

```python
# 空洞卷積
conv = nn.Conv2d(in_channels, out_channels, kernel_size=3,
                 padding=dilation, dilation=dilation)
```

DeepLabv3+ 使用 ASPP（Atrous Spatial Pyramid Pooling）：

```
輸入
  ↓
並列空洞卷積 (dilation=6, 12, 18)
  ↓
Global Average Pooling
  ↓
拼接 + 1x1 卷積
```

---

## 二、實例分割

### Mask R-CNN (2017)

在 Faster R-CNN 基礎上添加分割頭：

```python
class MaskRCNN(nn.Module):
    def __init__(self):
        # Faster R-CNN 組件
        self.rpn = RPN()
        self.roi_heads = ROIHeads()

        # 新增：分割頭
        self.mask_head = nn.Sequential(
            nn.Conv2d(256, 256, 3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(256, 256, 3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(256, num_classes, 1)  # 每類別一個 mask
        )

    def forward(self, images, targets):
        # ... RPN 和 ROI pooling
        mask_logits = self.mask_head(roi_features)
        masks = F.sigmoid(mask_logits)
        return masks
```

### 技術流程

```
輸入圖像
  ↓
CNN 特徵提取 (ResNet + FPN)
  ↓
RPN 生成候選區域
  ↓
RoI Align
  ↓
並行分支：
  - 類別分類
  - 邊界框回歸
  - 二值分割 Mask
```

---

## 三、關鍵技術

### RoI Align

解決 RoI Pooling 的對齊問題：

```python
# RoI Pooling：量化導致精度損失
# RoI Align：雙線性插值，無量化
def roi_align(features, rois, output_size):
    # 對每個 RoI 進行雙線性採樣
    # 保持空間精度
```

### 損失函數

```python
# Mask R-CNN 的損失
total_loss = (
    classification_loss +          # 類別分類
    box_regression_loss +         # 邊界框
    mask_loss                     # 分割 (BCE)
)
```

---

## 四、評估指標

| 指標 | 說明 |
|------|------|
| IoU (Intersection over Union) | 預測與真實的交集/並集 |
| mAP | 平均精度均值 |
| mIoU | Mean IoU（語義分割常用） |

```python
def iou(pred, target):
    intersection = (pred & target).sum()
    union = (pred | target).sum()
    return intersection / union

def miou(predictions, targets, num_classes):
   ious = []
    for cls in range(num_classes):
        pred_cls = (predictions == cls)
        target_cls = (targets == cls)
        ious.append(iou(pred_cls, target_cls))
    return np.mean(ious)
```

---

## 五、2020 年的進展

### SOLO (Segmenting Objects by Locations, 2019) 和 SOLOv2

anchor-free 實例分割：

```python
# 核心思想：根據位置預測實例 mask
# 將圖像劃分為網格，每個位置預測該位置的實例
```

### PointRend (2020)

將渲染思想應用於分割：

```
在粗糙預測上選擇不確定的點
  ↓
對這些點進行細緻預測
  ↓
迭代細化
```

---

**下一步**：[未來展望：視覺的 Transformer 時代](focus7.md)

## 延伸閱讀

- [semantic+segmentation+U-Net+FCN+2020](https://www.google.com/search?q=semantic+segmentation+U-Net+FCN+2020)
- [instance+segmentation+Mask+RCNN+2020](https://www.google.com/search?q=instance+segmentation+Mask+RCNN+2020)