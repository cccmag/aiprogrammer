# 主題六：DALL-E 與生成式圖像

## 文字生成圖像

### 1. DALL-E 簡介

2021 年 1 月，OpenAI 發表 DALL-E，這是一種能夠根據文字描述生成圖像的模型。DALL-E 的名字源於 WALL-E（機器人總動員）和 Salvador Dalí（超現實主義藝術家）。

### 2. DALL-E 的架構

DALL-E 基於 GPT-3 的架構，但應用於圖像生成：

**兩階段訓練**：
1. 自動回歸解碼器：根據文字生成圖像
2. VQ-VAE：離散 VAE 用於圖像壓縮

```python
class DALL_E(nn.Module):
    def __init__(self, image_vqgan, text_encoder, gpt_decoder):
        super().__init__()
        self.image_vqgan = image_vqgan
        self.text_encoder = text_encoder
        self.gpt_decoder = gpt_decoder

    def forward(self, text, image=None):
        text_features = self.text_encoder(text)

        if image is not None:
            image_tokens = self.image_vqgan.encode(image)
            output = self.gpt_decoder(text_features, image_tokens)
        else:
            output = self.gpt_decoder.generate(text_features)

        return output

    def generate(self, text, num_samples=1):
        text_features = self.text_encoder(text)
        image_tokens = self.gpt_decoder.generate(text_features, num_samples)
        images = self.image_vqgan.decode(image_tokens)
        return images
```

### 3. 文字到圖像的挑戰

**創意與多樣性**：
- 同一描述可以有多種合理圖像
- 模型需要展示創造力

**細節理解**：
- 精確的空間關係
- 正確的屬性绑定

**世界知識**：
- 理解常見物體的樣子
- 處理抽象概念

### 4. DALL-E 的能力

DALL-E 展示了多種令人驚艷的能力：

**物體组合**：
- 將不同物體以新穎方式组合
- 如「方形的蘋果」、「用叉子做的雲」

**場景合成**：
- 根據文字描述創建複雜場景
- 處理視角、光照等細節

**風格轉換**：
- 將藝術風格應用於物體
- 如「用梵谷風格畫的蘋果」

**文字渲染**：
- 在圖像中渲染文字
- 這對大多數模型來說很困難

### 5. 圖像生成的發展

**GAN 時代**：
- StyleGAN：高质量人脸生成
- BigGAN：更大規模的 GAN

**Transformer 時代**：
- DALL-E：文字到圖像
-Imagen：更真實的圖像生成（2022）
- Stable Diffusion：開源的 Latent Diffusion（2022）

### 6. 離散變分自編碼器 (VQ-VAE)

DALL-E 使用 VQ-VAE 進行圖像壓縮：

```python
class VQVAE(nn.Module):
    def __init__(self, encoder, decoder, codebook_size=8192, embed_dim=256):
        super().__init__()
        self.encoder = encoder
        self.decoder = decoder
        self.codebook = nn.Embedding(codebook_size, embed_dim)
        self.embed_dim = embed_dim

    def encode(self, x):
        z = self.encoder(x)
        batch_size, channels, h, w = z.shape
        z_flattened = z.permute(0, 2, 3, 1).reshape(-1, channels)

        distances = torch.cdist(z_flattened, self.codebook.weight)
        indices = distances.argmin(dim=1)

        quantized = self.codebook(indices)
        quantized = quantized.reshape(batch_size, h, w, channels).permute(0, 3, 1, 2)

        return indices.reshape(batch_size, h, w), quantized

    def decode(self, indices):
        z = self.codebook(indices)
        return self.decoder(z.permute(0, 3, 1, 2))
```

### 7. 應用與倫理

**應用場景**：
- 創意設計辅助
- 藝術創作
- 遊戲和娛樂

**倫理考量**：
- 深度偽造風險
- 著作權問題
- 偏見和刻板印象

---

## 延伸閱讀

- [DALL-E 官方網站](https://www.google.com/search?q=DALL-E+creating+images+from+text+OpenAI)
- [VQ-VAE 論文](https://www.google.com/search?q=VQ-VAE+neural+discrete+representation+learning)
- [生成對抗網路](https://www.google.com/search?q=GAN+generative+adversarial+networks+introduction)