# Vision Transformer (ViT) 的興起

## 2020 年：Transformer 進軍視覺領域

### 論文資訊

- **標題**：An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale
- **作者**：Dosovitskiy et al.
- **發布**：ICLR 2021（2020年提交）

---

## 一、將 Transformer 應用於圖像

### 核心思想

將圖像視為 16x16 像素的補丁序列：

```
圖像 (H x W x C)
     ↓
分割為 N 個補丁 (16 x 16)
     ↓
每個補丁線性嵌入為向量
     ↓
添加位置編碼
     ↓
輸入標準 Transformer Encoder
```

### 補丁化 (Patch Embedding)

```python
class PatchEmbed(nn.Module):
    def __init__(self, img_size=224, patch_size=16, in_channels=3, embed_dim=768):
        self.img_size = img_size
        self.patch_size = patch_size
        self.num_patches = (img_size // patch_size) ** 2

        # 補丁嵌入：每個補丁通過一個線性層
        self.proj = nn.Conv2d(in_channels, embed_dim,
                              kernel_size=patch_size, stride=patch_size)

    def forward(self, x):
        # x: (B, C, H, W)
        x = self.proj(x)  # (B, embed_dim, num_patches_h, num_patches_w)
        x = x.flatten(2)  # (B, embed_dim, num_patches)
        x = x.transpose(1, 2)  # (B, num_patches, embed_dim)
        return x
```

### 位置編碼

```python
class PositionalEncoding(nn.Module):
    def __init__(self, num_patches, embed_dim, dropout=0.1):
        super().__init__()
        self.pe = nn.Parameter(torch.randn(1, num_patches + 1, embed_dim))
        # +1 for CLS token
        self.dropout = nn.Dropout(dropout)

    def forward(self, x):
        x = x + self.pe[:, :x.size(1)]
        return self.dropout(x)
```

---

## 二、ViT 架構

### 完整流程

```
輸入圖像
  ↓
補丁線性嵌入 + 位置編碼
  ↓
添加 [CLS] token
  ↓
N × Transformer Encoder
  ↓
[CLS] token 輸出
  ↓
分類頭
```

### Encoder 區塊

```python
class TransformerEncoder(nn.Module):
    def __init__(self, embed_dim, num_heads, num_layers, mlp_ratio=4):
        super().__init__()
        self.layers = nn.ModuleList([
            EncoderBlock(embed_dim, num_heads, int(embed_dim * mlp_ratio))
            for _ in range(num_layers)
        ])

    def forward(self, x):
        for layer in self.layers:
            x = layer(x)
        return x

class EncoderBlock(nn.Module):
    def __init__(self, embed_dim, num_heads, mlp_dim):
        super().__init__()
        self.norm1 = nn.LayerNorm(embed_dim)
        self.attn = nn.MultiheadAttention(embed_dim, num_heads)
        self.norm2 = nn.LayerNorm(embed_dim)
        self.mlp = nn.Sequential(
            nn.Linear(embed_dim, mlp_dim),
            nn.GELU(),
            nn.Linear(mlp_dim, embed_dim)
        )

    def forward(self, x):
        x = x + self.attn(self.norm1(x), self.norm1(x), self.norm1(x))[0]
        x = x + self.mlp(self.norm2(x))
        return x
```

---

## 三、與 CNN 的比較

| 方面 | CNN | ViT |
|------|-----|-----|
| 歸納偏置 | 局部性、平移不變性 | 無 |
| 資料需求 | 較少（10M 參數） | 較多（需要大規模預訓練） |
| 計算效率 | 高 | 低（尤其在小圖像） |
| 可解釋性 | 中等 | 較強（注意力可視化） |
| 規模擴展性 | 邊際效益遞減 | 線性擴展 |

---

## 四、ViT 的變體

| 變體 | 改進 |
|------|------|
| DeiT | 加入蒸餾token |
| Swin Transformer | 階層結構、局部注意力 |
| BEiT | 雙向上下文建模 |
| MAE | 遮罩自動編碼器 |

### Swin Transformer（2021）

```
圖像
  ↓
分割為小視窗 (7x7)
  ↓
視窗內注意力 + Shifted Window
  ↓
階層結構（类似 CNN）
```

---

## 五、2020 年的發展狀態

### ViT 的發布時間線

- 2020年10月：ViT 論文發布（ICLR 2021）
- 2020年底：開源程式碼和預訓練模型
- 2020年：DeiT 等改進相繼發布

### 當時的影響

ViT 證明了 Transformer 可以直接應用於影像是可行的，但：
- 需要大規模訓練資料
- 計算成本較高
- CNN 仍然是主力

---

**下一步**：[物體檢測的進展](focus5.md)

## 延伸閱讀

- [Vision+Transformer+ViT+ICLR+2021](https://www.google.com/search?q=Vision+Transformer+ViT+ICLR+2021)
- [ViT+image+recognition+patch+embedding](https://www.google.com/search?q=ViT+image+recognition+patch+embedding+2020)