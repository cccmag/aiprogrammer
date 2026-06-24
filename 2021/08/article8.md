# Vision Transformer 詳解

ViT 將 Transformer 應用於圖像分類。

## 1. 圖像作為序列

ViT 將圖像劃分為 patches，每個 patch 作為一個「單詞」：

```python
class PatchEmbed(nn.Module):
    def forward(self, x):
        x = self.proj(x)
        x = x.flatten(2).transpose(1, 2)
        return x
```

## 2. Transformer Encoder

標准的 Transformer Encoder 應用於 patch 序列。

## 3. 與 CNN 的比較

- ViT 需要更多資料
- ViT 有更強的全局建模能力
- CNN 有更強的局部特徵提取能力

---

## 延伸閱讀

- [ViT 論文](https://www.google.com/search?q=AN+IMAGE+IS+WORTH+16X16+WORDS+Vision+Transformer+Dosovitskiy)
- [Swin Transformer](https://www.google.com/search?q=Swin+Transformer+shifted+windows+Liu)