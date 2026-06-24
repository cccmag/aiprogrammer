# 自監督學習與對比學習：YOLO、SimCLR、CLIP

## 前言

2020 年，自監督學習和對比學習成為 AI 領域的主流方法。這些技術減少了對標籤資料的依賴，讓模型能從海量未標記資料中學習。

## 對比學習核心概念

```
對比學習原理：
────────────────────────────────

目標：讓相似的樣本距離近，不相似的距離遠

正樣本對：同一張影像的不同增強
負樣本對：不同影像

對比損失：最大化正樣本相似度，最小化負樣本相似度
```

## SimCLR

```python
# SimCLR 概念

class SimCLR:
    """
    Simple Contrastive Learning of Visual Representations
    """
    def __init__(self, encoder, projection_head):
        self.encoder = encoder
        self.projection_head = projection_head
    
    def contrastive_loss(self, z_i, z_j, temperature=0.5):
        # z_i, z_j 是同一張圖的兩個增強
        similarity = torch.mm(z_i, z_j.T) / temperature
        
        # 對角是正樣本，其他是負樣本
        labels = torch.arange(len(z_i)).to(z_i.device)
        
        loss = F.cross_entropy(similarity, labels)
        return loss

# 數據增強
transforms = [
    RandomCrop(),
    RandomHorizontalFlip(),
    ColorJitter(),
    # ...
]
```

## CLIP

```python
# CLIP - 對比語言-影像預訓練

class CLIP:
    """
    Connect text and images through contrastive learning
    """
    def __init__(self, image_encoder, text_encoder):
        self.image_encoder = image_encoder
        self.text_encoder = text_encoder
    
    def forward(self, images, texts):
        # 編碼影像和文字
        image_features = self.image_encoder(images)
        text_features = self.text_encoder(texts)
        
        # 投影到共同空間
        image_features = self.image_projection(image_features)
        text_features = self.text_projection(text_features)
        
        # 對比學習
        logits = torch.mm(image_features, text_features.T)
        labels = torch.arange(len(images))
        
        loss = F.cross_entropy(logits, labels) + \
               F.cross_entropy(logits.T, labels)
        
        return loss
```

## YOLO 的發展

```
YOLO (You Only Look Once)：
────────────────────────────────

YOLO 系列發展：
- YOLO (2016): 單次檢測，速度快
- YOLOv3 (2018): 多尺度檢測
- YOLOv4 (2020): 大量優化，CSPDarknet
- YOLOv5 (2020): PyTorch 實現

YOLOv4 發布（2020年4月）：
- 突破性的檢測速度和精度
- 廣泛的應用
```

## 延伸閱讀

- [SimCLR 論文](https://www.google.com/search?q=SimCLR+contrastive+learning)
- [CLIP OpenAI](https://www.google.com/search?q=CLIP+OpenAI+contrastive+language+image)
- [YOLOv4 論文](https://www.google.com/search?q=YOLOv4+2020+paper)

---

*本篇文章為「AI 程式人雜誌 2020 年 12 月號」年度回顧系列之一。*