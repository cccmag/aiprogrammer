# Transformer 架構的勝利：從 NLP 到多模態

## 前言

Transformer 架構在 2017 年被提出後，迅速成為深度學習的核心。2020 年，這一趨勢更加明顯——Transformer 從 NLP 擴展到電腦視覺等多個領域。

## Transformer 核心概念

```python
# Transformer Self-Attention

class SelfAttention(nn.Module):
    def __init__(self, hidden_size, num_heads):
        super().__init__()
        self.num_heads = num_heads
        self.head_size = hidden_size // num_heads
        
        self.query = nn.Linear(hidden_size, hidden_size)
        self.key = nn.Linear(hidden_size, hidden_size)
        self.value = nn.Linear(hidden_size, hidden_size)
        self.output = nn.Linear(hidden_size, hidden_size)
    
    def forward(self, x, mask=None):
        # 線性投射
        Q = self.query(x)
        K = self.key(x)
        V = self.value(x)
        
        # 分頭
        batch_size = x.size(0)
        Q = Q.view(batch_size, -1, self.num_heads, self.head_size).transpose(1, 2)
        K = K.view(batch_size, -1, self.num_heads, self.head_size).transpose(1, 2)
        V = V.view(batch_size, -1, self.num_heads, self.head_size).transpose(1, 2)
        
        # 注意力分數
        scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(self.head_size)
        
        if mask is not None:
            scores = scores.masked_fill(mask == 0, -1e9)
        
        attn_weights = F.softmax(scores, dim=-1)
        context = torch.matmul(attn_weights, V)
        
        return self.output(context)
```

## 2020 年的 Transformer 模型

```
2020 年重要 Transformer 模型：
────────────────────────────────

NLP 領域：
- GPT-3 (1750 億參數) - 5月
- T5 (110 億參數) - 3月
- BERT 系列持續優化

電腦視覺：
- ViT (Vision Transformer) - 10月
  - 純 Transformer 架構
  - 超越 CNN 在大資料集上

多模態：
- CLIP (OpenAI) - 1月
- DALL-E (OpenAI) - 12月
```

## Vision Transformer (ViT)

```python
# ViT 概念

class VisionTransformer(nn.Module):
    def __init__(self, image_size=224, patch_size=16, num_classes=1000):
        super().__init__()
        num_patches = (image_size // patch_size) ** 2
        
        self.patch_embedding = nn.Conv2d(3, 768, patch_size, patch_size)
        self.cls_token = nn.Parameter(torch.randn(1, 1, 768))
        self.pos_embedding = nn.Parameter(torch.randn(1, num_patches + 1, 768))
        
        self.transformer = nn.Transformer(768, 12, 12)
        self.head = nn.Linear(768, num_classes)
    
    def forward(self, x):
        # 分割影像為補丁
        x = self.patch_embedding(x)  # [B, 768, 14, 14]
        x = x.flatten(2).transpose(1, 2)  # [B, 196, 768]
        
        # 加入分類 token
        cls_tokens = self.cls_token.expand(x.size(0), -1, -1)
        x = torch.cat([cls_tokens, x], dim=1)
        
        # 加入位置嵌入
        x = x + self.pos_embedding
        
        # 通過 Transformer
        x = self.transformer(x)
        
        # 分類
        return self.head(x[:, 0])
```

## 延伸閱讀

- [Attention Is All You Need](https://www.google.com/search?q=attention+is+all+you+need+paper+transformer)
- [ViT 論文](https://www.google.com/search?q=vision+transformer+ViT+paper)
- [GPT-3 論文](https://www.google.com/search?q=GPT-3+paper+language+models)

---

*本篇文章為「AI 程式人雜誌 2020 年 12 月號」年度回顧系列之一。*