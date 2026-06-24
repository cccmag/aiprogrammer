# 主題五：CLIP 與對比學習

## 文字-圖像對齊

### 1. CLIP 簡介

2021 年 1 月，OpenAI 發表 CLIP（Contrastive Language-Image Pre-Training），這是一種能夠理解和連接文字與圖像的多模態模型。

CLIP 的核心思想：通過對比學習，讓文字和圖像在向量空間中對齊。

### 2. 對比學習原理

對比學習的目標是讓相似的樣本在向量空間中靠近，不相似的樣本遠離：

```python
def clip_loss(logits):
    """CLIP 對比損失"""
    batch_size = logits.shape[0]
    labels = torch.arange(batch_size, device=logits.device)

    loss_i = F.cross_entropy(logits, labels)
    loss_t = F.cross_entropy(logits.t(), labels)

    return (loss_i + loss_t) / 2
```

### 3. CLIP 的訓練

CLIP 使用 4 億對文字-圖像對進行訓練：

```python
class CLIPModel(nn.Module):
    def __init__(self, image_encoder, text_encoder, embed_dim=512):
        super().__init__()
        self.image_encoder = image_encoder
        self.text_encoder = text_encoder
        self.image_projection = nn.Linear(image_encoder.output_dim, embed_dim)
        self.text_projection = nn.Linear(text_encoder.output_dim, embed_dim)

        self.temperature = nn.Parameter(torch.ones([]) * 0.07)

    def forward(self, images, texts):
        image_features = F.normalize(self.image_projection(self.image_encoder(images)))
        text_features = F.normalize(self.text_projection(self.text_encoder(texts)))

        logits = torch.matmul(image_features, text_features.t()) * torch.exp(self.temperature)

        loss = clip_loss(logits)
        return loss, logits
```

### 4. CLIP 的應用

**零樣本分類**：
```python
def zero_shot_classify(image, class_names, model):
    text_descriptions = [f"A photo of a {c}" for c in class_names]
    text_features = model.encode_text(text_descriptions)

    image_features = model.encode_image(image)
    similarity = torch.matmul(image_features, text_features.t())

    return class_names[similarity.argmax()]
```

**圖像搜尋**：
- 根據文字描述搜尋相關圖像
- 根據圖像搜尋相似文字描述

**圖像生成引導**：
- 與生成模型結合，控制圖像生成

### 5. CLIP 的創新點

**突破傳統分類**：
- 傳統模型需要固定的類別集合
- CLIP 可以理解任意的文字描述

**遷移學習能力**：
- 在各種視覺任務上表現優異
- 減少了任務特定的訓練需求

**避免人工標註**：
- 訓練資料來自網路上直接可用的文字-圖像對
- 不需要專家標註

### 6. CLIP 的局限性

- 複雜的視覺關係理解有限
- 對細粒度物體分類有挑戰
- 可能繼承訓練資料的偏見

### 7. 對比學習的發展

CLIP 之後，出現了更多類似的方法：

- **ALIGN**：更大規模的訓練
- **Florence**：更通用的視覺表示
- **BLIP**：統一的視覺-語言理解

---

## 延伸閱讀

- [CLIP 論文](https://www.google.com/search?q=CLIP+connecting+text+and+images+OpenAI+2021)
- [對比學習綜述](https://www.google.com/search?q=contrastive+learning+self-supervised+vision)
- [多模態學習](https://www.google.com/search?q=multimodal+learning+vision+language+2021)