# 影像分割

## FCN、U-Net 與語意分割

影像分割是將影像劃分為具有不同語義含義的區域的任務。

---

## 任務類型

### 語意分割（Semantic Segmentation）

```
輸入：圖像
輸出：每個像素的類別標籤

車 車 車 車  草 草 草 草
車 車 車 車  草 草 草 草
人 人 人 人  樹 樹 樹 樹
人 人 人 人  樹 樹 樹 樹
```

### 實例分割（Instance Segmentation）

```
不僅區分不同類別
還區分同一類別的不同個體

車1 車1 車1 車1  草 草 草 草
車1 車1 車1 車1  草 草 草 草
車2 車2 車2 車2  草 草 草 草
車2 車2 車2 車2  草 草 草 草
```

### 全景分割（Panoptic Segmentation）

結合語意分割和實例分割。

---

## FCN（Fully Convolutional Network）

第一個端到端的語意分割網路。

### 核心思想

```python
# 用卷積層替換全連接層
# 輸出從分類結果變為熱力圖

class FCN(nn.Module):
    def __init__(self):
        self.backbone = VGG16()
        # 將 VGG 的 FC 層轉換為 conv 層
        self.score_fr = nn.Conv2d(4096, 21, 1)  # 21 類 Pascal VOC
        self.upscore = nn.ConvTranspose2d(21, 21, 64, stride=32)
```

### 上取樣

```python
# 反卷積（Transposed Convolution）
output = F.conv_transpose2d(input, weight, stride=32)

# 雙線性插值上取樣 + 卷積
output = F.interpolate(input, scale_factor=2, mode='bilinear')
```

### 跳躍連接

```python
# FCN-8s: 結合多個尺度
# pool5 → upsample 32x → prediction
# pool4 + prediction → upsample 16x → prediction
# pool3 + prediction → upsample 8x → final prediction
```

---

## U-Net（2015）

醫學影像分割的經典架構。

### 結構

```
       Encoder                    Decoder
       ───────                    ───────

    572x572               388x388
       │                       ▲
    Conv                     DeConv
       │                       ▲
    570x570                 392x392
       │                       ▲
    Pool                     Concat
       │                       ▲
    284x284                 784x784
       │                       ▲
    Conv                     DeConv
       │                       ▲
    282x282                 788x788
       │                       ▲
    Pool                     Concat
       │                       ▲
       ...                     ...
```

### U-Net 實現

```python
class UNet(nn.Module):
    def __init__(self, in_channels, out_channels):
        super().__init__()

        # Encoder
        self.enc1 = DoubleConv(in_channels, 64)
        self.enc2 = DoubleConv(64, 128)
        self.enc3 = DoubleConv(128, 256)
        self.enc4 = DoubleConv(256, 512)

        # Bottleneck
        self.bottleneck = DoubleConv(512, 1024)

        # Decoder
        self.up4 = nn.ConvTranspose2d(1024, 512, kernel_size=2, stride=2)
        self.dec4 = DoubleConv(1024, 512)

        self.up3 = nn.ConvTranspose2d(512, 256, kernel_size=2, stride=2)
        self.dec3 = DoubleConv(512, 256)

        self.up2 = nn.ConvTranspose2d(256, 128, kernel_size=2, stride=2)
        self.dec2 = DoubleConv(256, 128)

        self.up1 = nn.ConvTranspose2d(128, 64, kernel_size=2, stride=2)
        self.dec1 = DoubleConv(128, 64)

        # Output
        self.out = nn.Conv2d(64, out_channels, kernel_size=1)

    def forward(self, x):
        # Encoder
        e1 = self.enc1(x)
        e2 = self.enc2(F.max_pool2d(e1, 2))
        e3 = self.enc3(F.max_pool2d(e2, 2))
        e4 = self.enc4(F.max_pool2d(e3, 2))

        # Bottleneck
        b = self.bottleneck(F.max_pool2d(e4, 2))

        # Decoder with skip connections
        d4 = self.dec4(torch.cat([self.up4(b), e4], dim=1))
        d3 = self.dec3(torch.cat([self.up3(d4), e3], dim=1))
        d2 = self.dec2(torch.cat([self.up2(d3), e2], dim=1))
        d1 = self.dec1(torch.cat([self.up1(d2), e1], dim=1))

        return self.out(d1)
```

---

## 語意分割的關鍵技術

### 空洞卷積（Dilated/Atrous Convolution）

```python
# 空洞卷積增加感受野，不丟失解析度

def dilated_conv(x, in_channels, out_channels, rate=2):
    return nn.Conv2d(in_channels, out_channels, kernel_size=3,
                     padding=rate, dilation=rate)(x)
```

### 空間金字塔池化（ASPP）

```python
# 多尺度特徵
aspp_pool = nn.AdaptiveAvgPool2d(1)  # 全域池化
aspp_1x1 = nn.Conv2d(channels, 256, 1)
aspp_3x3_r6 = dilated_conv(channels, 256, 256, rate=6)
aspp_3x3_r12 = dilated_conv(channels, 256, 256, rate=12)
aspp_3x3_r18 = dilated_conv(channels, 256, 256, rate=18)
```

---

## Mask RCNN（實例分割）

在 Faster RCNN 基礎上新增分割分支。

```python
class MaskRCNN(nn.Module):
    def __init__(self):
        self.backbone = ResNet+FPN()
        self.rpn = RPN()
        self.roi_heads = nn.ModuleList([
            BoxHead(),   # 邊界框分類和回歸
            MaskHead()   # 實例分割
        ])

    def forward(self, image):
        features = self.backbone(image)
        proposals = self.rpn(features)

        # 對每個候選框
        box_pred = self.roi_heads[0](proposals, features)
        mask_pred = self.roi_heads[1](proposals, features)

        return box_pred, mask_pred
```

---

## 評估指標

### IoU（Intersection over Union）

```python
def compute_iou(pred_mask, gt_mask):
    intersection = np.logical_and(pred_mask, gt_mask).sum()
    union = np.logical_or(pred_mask, gt_mask).sum()
    return intersection / union
```

### Mean IoU

```python
def compute_mean_iou(predictions, targets, num_classes):
    ious = []
    for cls in range(num_classes):
        pred_cls = predictions == cls
        target_cls = targets == cls
        iou = compute_iou(pred_cls, target_cls)
        ious.append(iou)
    return np.mean(ious)
```

---

## 延伸閱讀

- [FCN 論文](https://www.google.com/search?q=FCN+Long+Shelhamer+Darrell+2015)
- [U-Net 論文](https://www.google.com/search?q=U-Net+Ronneberger+2015)
- [Mask RCNN 論文](https://www.google.com/search?q=Mask+RCNN+He+2017)

---

*本篇文章為「AI 程式人雜誌 2019 年 5 月號」系列文章之一。*