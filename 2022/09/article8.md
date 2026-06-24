# 注意力在 CV 的應用

## 從 NLP 到 CV

注意力機制原本是為自然語言處理設計的，但它的影響很快就擴展到了電腦視覺（CV）領域。從 2018 年開始，研究人員發現注意力機制不僅可以替代卷積神經網路，還能在多個視覺任務上超越它。

## Vision Transformer（ViT）

### 從像素到 Patch

2020 年，Dosovitskiy 等人發表了 Vision Transformer（ViT），首次證明了純 Transformer 架構可以在圖像分類任務上達到或超越最先進的 CNN。

ViT 的核心思想是：將圖像切割成固定大小的 patch（如 16×16 像素），將每個 patch 視為一個「詞」，然後在 patch 序列上應用標準的 Transformer 編碼器。

```
輸入圖像 (224×224)
    │
    ▼
分割成 196 個 patch (每個 16×16)
    │
    ▼
展開為向量序列 (196, 768)
    │
    ▼
加入位置編碼
    │
    ▼
Transformer 編碼器 × L 層
    │
    ▼
分類頭
```

### ViT 的注意力模式

ViT 的注意力模式與 BERT 有顯著的不同：

- **底層**：patch 主要關注相鄰的 patch（局部性）
- **中層**：開始關注語義相關的 patch（如動物的不同身體部位）
- **高層**：[CLS] token 整合來自所有 patch 的資訊

### 縮放挑戰

ViT 的計算量與 patch 數量的平方成正比。對於高解析度圖像（如 1024×1024），patch 數量可能達到 4096，注意力計算的開銷極大。

解決方案：
- **分層架構**：Swin Transformer 使用移動視窗，逐步降低解析度
- **高效注意力**：使用稀疏或線性注意力變體
- **混合架構**：CNN + Transformer 的混合設計

## Swin Transformer

Swin Transformer（Liu 等人，2021）是目前最成功的視覺 Transformer 之一。它的關鍵創新是「移動視窗注意力」（Shifted Window Attention）。

### 移動視窗注意力

Swin 將圖像劃分為不重疊的視窗（如 7×7），只在視窗內部計算注意力。然後在下一層移動視窗的劃分，使不同視窗之間能夠通信。

```
層 L：視窗 A | 視窗 B
       ────┼────
       視窗 C | 視窗 D

層 L+1：移動後的視窗
       視窗 A' 跨越原視窗的邊界
```

這種設計不僅將計算複雜度從 O(n²) 降低到 O(n·w²)（w 是視窗大小），還透過視窗移動實現了跨視窗的資訊流通。

### 分層特徵圖

Swin 透過 patch merging 逐步降低解析度，形成類似 CNN 的金字塔結構：
```
Stage 1: H/4 × W/4 × C
Stage 2: H/8 × W/8 × 2C
Stage 3: H/16 × W/16 × 4C
Stage 4: H/32 × W/32 × 8C
```

這使得 Swin 可以自然地應用於物體偵測和語意分割等需要多尺度特徵的任務。

## 物體偵測中的注意力

### DETR：端到端物體偵測

DETR（Carion 等人，2020）使用 Transformer 實現了第一個端到端的物體偵測系統：

1. CNN 骨幹提取圖像特徵
2. Transformer 編碼器處理特徵圖
3. Transformer 解碼器使用 object queries 預測物體

DETR 的關鍵是「object queries」——這是一組可學習的嵌入向量，每個 query 負責偵測圖像中的一個物體。

解碼器中的 Cross-Attention 讓每個 object query 關注圖像中對應的區域，實現了類似於「注意力偵測」的效果。

### DETR 注意力的可視化

DETR 的 Cross-Attention 權重可以直接可視化為物體檢測框：

```
Object Query 1: 關注人物區域 ──► 檢測到「人」
Object Query 2: 關注車輛區域 ──► 檢測到「車」
Object Query 3: 關注背景 ──► 無檢測結果
```

## 注意力在圖像生成中的應用

### Diffusion Transformer（DiT）

DiT（Peebles & Xie，2023）使用 Transformer 替代傳統的 U-Net 作為擴散模型的骨幹，在圖像生成品質上取得了顯著提升。

DiT 中的注意力機制用於：
- patch 之間的資訊交換
- 條件資訊（如文字提示、類別標籤）的整合
- 多尺度特徵的融合

### 文字到圖像生成中的注意力

Stable Diffusion 使用 Cross-Attention 來實現文字引導的圖像生成：

```
# 每個去噪步驟
for each timestep:
    image_features ← UNet(latent, timestep)
    for each cross_attn layer:
        image_features = CrossAttention(
            query=image_features,
            key=text_embeddings,
            value=text_embeddings
        )
    latent ← denoise_step(latent, image_features)
```

## 結論

注意力機制在電腦視覺中的應用證明了它不僅僅是 NLP 的工具，而是一種通用的「關係學習」機制。從 ViT 的 patch 級別注意力到 Swin 的視窗注意力，從 DETR 的物件查詢到 DiT 的擴散注意力，注意力正在重新定義視覺計算的邊界。

未來，視覺注意力模型將與 CNN 更深度地融合，產生更高效、更強大的混合架構。

---

**延伸閱讀**
- [ViT: An Image is Worth 16x16 Words](https://www.google.com/search?q=Vision+Transformer+ViT+2020)
- [Swin Transformer: Hierarchical Vision Transformer](https://www.google.com/search?q=Swin+Transformer+2021)
- [DETR: End-to-End Object Detection with Transformers](https://www.google.com/search?q=DETR+transformer+object+detection)
