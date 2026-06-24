# 從零實作 CLIP 風格的對比學習

## 前言

CLIP（Contrastive Language-Image Pre-training）由 OpenAI 於 2021 年提出，核心概念是透過對比學習將文字與圖片映射到同一向量空間。本文將從零實作一個簡化的 CLIP 訓練流程，幫助讀者理解跨模態對比學習的數學原理與程式實現。

---

## 一、對比學習的核心：InfoNCE Loss

CLIP 使用 InfoNCE（Noise Contrastive Estimation）損失函數。給定一個 batch 的 `(text, image)` 配對，目標是讓正確配對的相似度 highest，錯誤配對的相似度最低：

```python
import torch
import torch.nn.functional as F

def infonce_loss(logits_per_image, temperature=0.07):
    # logits_per_image: shape (batch_size, batch_size)
    # 第 (i, j) 個元素 = image_i 與 text_j 的相似度
    batch_size = logits_per_image.shape[0]
    labels = torch.arange(batch_size)  # 正確配對在對角線

    loss_i = F.cross_entropy(logits_per_image / temperature, labels)
    loss_t = F.cross_entropy(logits_per_image.T / temperature, labels)
    return (loss_i + loss_t) / 2
```

## 二、簡化版 CLIP 模型

我們實作一個輕量級的雙塔結構：文字編碼器 + 圖片編碼器：

```python
import torch.nn as nn

class TextEncoder(nn.Module):
    def __init__(self, vocab_size, embed_dim=256, proj_dim=128):
        super().__init__()
        self.embed = nn.Embedding(vocab_size, embed_dim)
        self.encoder = nn.TransformerEncoder(
            nn.TransformerEncoderLayer(embed_dim, nhead=4, batch_first=True),
            num_layers=2
        )
        self.proj = nn.Linear(embed_dim, proj_dim)

    def forward(self, x):
        x = self.embed(x)
        x = self.encoder(x)
        x = x.mean(dim=1)  # 平均池化
        return self.proj(x)

class ImageEncoder(nn.Module):
    def __init__(self, img_channels=3, img_size=32, proj_dim=128):
        super().__init__()
        self.cnn = nn.Sequential(
            nn.Conv2d(img_channels, 64, 3, padding=1),
            nn.ReLU(),
            nn.AdaptiveAvgPool2d((1, 1)),
            nn.Flatten(),
            nn.Linear(64, proj_dim),
        )

    def forward(self, x):
        return self.cnn(x)
```

## 三、完整訓練循環

```python
from torch.utils.data import Dataset, DataLoader

class ImageTextDataset(Dataset):
    def __init__(self, captions, images):
        self.captions = captions  # list of token IDs
        self.images = images      # list of image tensors

    def __len__(self):
        return len(self.captions)

    def __getitem__(self, idx):
        return self.images[idx], self.captions[idx]

def train_clip(model, dataloader, optimizer, epochs=10):
    model.train()
    for epoch in range(epochs):
        total_loss = 0
        for images, texts in dataloader:
            optimizer.zero_grad()

            img_feat = model.image_encoder(images)
            txt_feat = model.text_encoder(texts)

            # 正規化
            img_feat = F.normalize(img_feat, dim=1)
            txt_feat = F.normalize(txt_feat, dim=1)

            logits = img_feat @ txt_feat.T  # 相似度矩陣
            loss = infonce_loss(logits)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()

        print(f"Epoch {epoch+1}, Loss: {total_loss/len(dataloader):.4f}")
```

## 四、零樣本分類

訓練完成後，CLIP 可以進行零樣本分類：將候選類別的文字嵌入與圖片嵌入比對相似度：

```python
def zero_shot_classify(model, image, class_names, tokenizer):
    # 嵌入圖片
    img_feat = F.normalize(model.image_encoder(image.unsqueeze(0)), dim=1)

    # 嵌入所有類別名稱
    text_feats = []
    for name in class_names:
        tokens = tokenizer(name)
        feat = F.normalize(model.text_encoder(tokens.unsqueeze(0)), dim=1)
        text_feats.append(feat)

    text_feats = torch.cat(text_feats)
    similarities = img_feat @ text_feats.T
    pred_idx = similarities.argmax().item()
    return class_names[pred_idx]
```

## 五、實戰注意事項

1. **Batch size 越大越好**：對比學習依賴大量負樣本，建議 batch size ≥ 256
2. **溫度參數**：`temperature` 控制相似度分布的 sharpness，通常設在 0.01–0.1 之間
3. **資料增強**：圖片側的資料增強（隨機裁切、色彩抖動）對學習效果至關重要
4. **超大規模訓練**：原始 CLIP 使用 4 億個 `(image, text)` 配對，這在一般環境難以複製

---

## 結語

CLIP 的對比學習框架已經成為多模態 AI 的基石。從 OpenAI 的 CLIP 到 Google 的 SigLIP、Apple 的 AIM，所有主流多模態模型都建立在相似的對比學習原理之上。理解 InfoNCE loss 和雙塔結構，是理解多模態 AI 的第一步。

---

**參考資料**

- CLIP 論文：https://arxiv.org/abs/2103.00020
- OpenAI CLIP 官方實作：https://github.com/openai/CLIP
- InfoNCE Loss 說明：https://www.google.com/search?q=InfoNCE+loss+contrastive+learning
- SigLIP：https://arxiv.org/abs/2303.15343
