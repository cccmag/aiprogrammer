# 主題四：Vision Transformer (ViT)

## Transformer 進軍電腦視覺

### 1. 背景

Transformer 在 NLP 領域取得巨大成功後，研究者開始探索將其應用於電腦視覺。2020 年，Google 發表 Vision Transformer (ViT)，首次將標準 Transformer 應用於圖像分類。

### 2. 圖像 Patch 化

ViT 的核心思想是將圖像劃分為固定大小的 patches：

```python
import torch
import torch.nn as nn
from einops import rearrange

class PatchEmbed(nn.Module):
    def __init__(self, img_size=224, patch_size=16, in_channels=3, embed_dim=768):
        super().__init__()
        self.img_size = img_size
        self.patch_size = patch_size
        self.num_patches = (img_size // patch_size) ** 2

        self.proj = nn.Conv2d(
            in_channels, embed_dim,
            kernel_size=patch_size,
            stride=patch_size
        )

    def forward(self, x):
        x = self.proj(x)
        x = x.flatten(2).transpose(1, 2)
        return x
```

### 3. 位置編碼

```python
class PositionalEncoding(nn.Module):
    def __init__(self, num_patches, embed_dim, dropout=0.1):
        super().__init__()
        self.pos_embed = nn.Parameter(torch.zeros(1, num_patches + 1, embed_dim))
        self.cls_token = nn.Parameter(torch.zeros(1, 1, embed_dim))
        self.dropout = nn.Dropout(dropout)

        nn.init.trunc_normal_(self.pos_embed, std=0.02)
        nn.init.trunc_normal_(self.cls_token, std=0.02)

    def forward(self, x):
        batch_size = x.size(0)
        cls_tokens = self.cls_token.expand(batch_size, -1, -1)
        x = torch.cat([cls_tokens, x], dim=1)
        x = x + self.pos_embed
        return self.dropout(x)
```

### 4. Transformer Encoder

```python
class TransformerEncoder(nn.Module):
    def __init__(self, embed_dim, num_heads, num_layers, mlp_ratio=4, dropout=0.1):
        super().__init__()
        self.layers = nn.ModuleList([
            EncoderLayer(embed_dim, num_heads, mlp_ratio, dropout)
            for _ in range(num_layers)
        ])

    def forward(self, x):
        for layer in self.layers:
            x = layer(x)
        return x

class EncoderLayer(nn.Module):
    def __init__(self, embed_dim, num_heads, mlp_ratio, dropout):
        super().__init__()
        self.norm1 = nn.LayerNorm(embed_dim)
        self.attn = nn.MultiheadAttention(embed_dim, num_heads, dropout, batch_first=True)
        self.norm2 = nn.LayerNorm(embed_dim)

        mlp_hidden_dim = int(embed_dim * mlp_ratio)
        self.mlp = nn.Sequential(
            nn.Linear(embed_dim, mlp_hidden_dim),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(mlp_hidden_dim, embed_dim),
            nn.Dropout(dropout)
        )

    def forward(self, x):
        x = x + self.attn(self.norm1(x), self.norm1(x), self.norm1(x))[0]
        x = x + self.mlp(self.norm2(x))
        return x
```

### 5. 完整 ViT 架構

```python
class VisionTransformer(nn.Module):
    def __init__(self, img_size=224, patch_size=16, in_channels=3,
                 num_classes=1000, embed_dim=768, depth=12, num_heads=12):
        super().__init__()
        self.patch_embed = PatchEmbed(img_size, patch_size, in_channels, embed_dim)
        self.pos_embed = PositionalEncoding(self.patch_embed.num_patches, embed_dim)
        self.transformer = TransformerEncoder(embed_dim, num_heads, depth)

        self.head = nn.Linear(embed_dim, num_classes)

    def forward(self, x):
        x = self.patch_embed(x)
        x = self.pos_embed(x)
        x = self.transformer(x)
        x = x[:, 0]
        return self.head(x)
```

### 6. ViT 與 CNN 的比較

| 特性 | CNN | ViT |
|------|-----|-----|
| 歸納偏置 | 局部性、權重共用 | 較少 |
| 資料需求 | 較少 | 較多 |
| 计算量 | 較少 | 較多 |
| 可解釋性 | 有限 | Attention 可視化 |

### 7. ViT 的優勢與挑戰

**優勢**：
- 更强的全局建模能力
- 更好的遷移學習能力
- 適用於各種視覺任務

**挑戰**：
- 需要更多訓練資料
- 計算成本較高
- 對小目標物體效果較差

---

## 延伸閱讀

- [Vision Transformer 論文](https://www.google.com/search?q=Vision+Transformer+ViT+AN+IMAGE+IS+WORTH+16X16+WORDS)
- [DETR 物體偵測](https://www.google.com/search?q=DETR+end-to-end+object+detection+transformer)
- [Swin Transformer](https://www.google.com/search?q=Swin+Transformer+shifted+windows)