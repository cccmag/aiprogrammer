# Transformer 進軍視覺領域

## 前言

2020 年，Vision Transformer (ViT) 的論文發表，標誌著 Transformer 正式進入電腦視覺領域。本文回顧這一重要進展。

---

## 一、Vision Transformer (ViT)

### 核心思想

將圖像視為補丁序列，類似於文字序列：

```
圖像 → 補丁 → 線性嵌入 → Transformer Encoder → 分類
```

### 補丁化

```python
# 將 224x224 圖像分割為 16x16 補丁
# 得到 (224/16)² = 14² = 196 個補丁
# 每個補丁 16×16×3 = 768 維
```

### 架構

```
輸入補丁序列 + [CLS] token
  ↓
線性投影 + 位置嵌入
  ↓
L × Transformer Encoder
  ↓
[CLS] token → 分類頭
```

---

## 二、ViT 與 CNN 的比較

### 資料需求

| 模型 | 訓練資料 | 效能 |
|------|---------|------|
| ViT-B/16 | ImageNet-21k | 84.3% |
| ViT-L/16 | ImageNet-21k | 85.2% |
| ResNet-50 | ImageNet-1k | 76.1% |

ViT 需要更多資料才能發揮優勢。

### 計算效率

```
ViT: O(n² × d) 其中 n 是補丁數
CNN: O(k² × n × d) 其中 k 是卷積核大小
```

當圖像較大時，ViT 的計算量增长更快。

---

## 三、2020 年的相關進展

### DeiT (Data-efficient Image Transformer)

Facebook 在 2020 年發布：

- 使用蒸餾訓練
- 減少對資料的需求
- 在 ImageNet 上達到 SOTA

### SETR (2020)

將 Transformer 用於語義分割：

- 使用 ViT 作為編碼器
- 傳統解碼器用於分割

### CLIP (2021 初，但基礎在 2020)

對比語言-圖像預訓練：

- 文字-圖像配對學習
- 零樣本分類
- 預示了多模態的潜力

---

## 四、DETR (2020)

端到端物體檢測：

```python
# 流程
圖像 → CNN → Transformer Encoder-Decoder → 物件集合
```

### 創新

- 移除 NMS 等後處理
- 集合預測
- 全域注意力

### 限制

- 訓練收斂慢
- 小物體表現不佳

---

## 五、Swin Transformer（2021 初）

階層式 Vision Transformer：

```python
# 與 ViT 的主要區別
# 1. 視窗內注意力（降低計算）
# 2. 階層結構（多尺度）
# 3. 偏移視窗
```

---

## 六、為何 Transformer 在視覺有效？

### 1. 全域注意力

捕捉長距離依賴，勝過 CNN 的局部感受野。

### 2. 可擴展性

與語言模型相同的架構便於規模化。

### 3. 多模態統一

文字、圖像、音訊可以使用相同的架構處理。

---

## 七、挑戰與機會

### 挑戰

1. **計算效率**：對小圖像計算量大
2. **訓練穩定性**：需要較多資料和訓練技巧
3. **部署**：CNN 在邊緣設備上更高效

### 機會

1. **大規模預訓練**
2. **多模態學習**
3. **視覺-語言模型**

---

## 八、實驗建議

### 何時嘗試 ViT？

- 有足夠的訓練資料
- 需要在大規模預訓練上微調
- 對最新技術有興趣

### 建議配置

```python
# 使用 timm 庫
import timm

model = timm.create_model('vit_base_patch16_224', pretrained=True)
```

---

## 結語

Transformer 正在改變電腦視覺的格局。雖然 CNN 仍然是主力，但 Vision Transformer 提供了一個有前景的新方向。未來可能會看到 CNN 和 Transformer 的混合架構。

---

*延伸閱讀：[Vision+Transformer+ViT+2020](https://www.google.com/search?q=Vision+Transformer+ViT+2020+ICLR)
[DETR+end+to+end+object+detection](https://www.google.com/search?q=DETR+end+to+end+object+detection+transformer+2020)*