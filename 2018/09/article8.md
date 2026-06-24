# 影像 Captioning 與 Attention

## 1. 影像描述任務

```python
# 輸入：影像
# 輸出：描述影像內容的文字

# 例如：
# 輸入：一張狗在草地上跑的圖
# 輸出："A dog is running on the grass"
```

## 2. Encoder-Decoder 架構

```python
# Encoder：CNN（如 ResNet）提取影像特徵
# Decoder：RNN/LSTM 生成文字

class ImageCaptioning(nn.Module):
    def __init__(self, vocab_size, embed_dim=256, hidden_dim=512):
        self.encoder = EncoderCNN(embed_dim)
        self.decoder = DecoderLSTM(vocab_size, embed_dim, hidden_dim)

    def forward(self, images, captions):
        features = self.encoder(images)
        outputs = self.decoder(features, captions)
        return outputs
```

## 3. Attention 機制

```python
# 讓模型在生成每個單詞時关注影像的不同區域

class Attention(nn.Module):
    def __init__(self, encoder_dim, decoder_dim):
        self.attn = nn.Linear(encoder_dim + decoder_dim, decoder_dim)
        self.v = nn.Parameter(torch.rand(decoder_dim))

    def forward(self, encoder_outputs, decoder_hidden):
        # encoder_outputs: (batch, num_pixels, encoder_dim)
        # decoder_hidden: (batch, decoder_dim)

        # 計算注意力權重
        energy = torch.tanh(self.attn(
            torch.cat([encoder_outputs, decoder_hidden.unsqueeze(1).expand(-1, encoder_outputs.size(1), -1)], dim=2)
        ))  # (batch, num_pixels, decoder_dim)

        attention = self.v.dot(energy, dim=2)  # (batch, num_pixels)

        weights = F.softmax(attention, dim=1)  # (batch, num_pixels)

        # 加權求和
        context = (weights.unsqueeze(2) * encoder_outputs).sum(dim=1)  # (batch, encoder_dim)

        return context, weights
```

## 4. Show, Attend and Tell

```python
# 完整的 Attention Captioning 模型
class AttentiveCaptioner(nn.Module):
    def __init__(self, vocab_size, embed_dim=256, encoder_dim=2048, decoder_dim=512):
        self.encoder = ResNetEncoder(encoder_dim)
        self.attention = Attention(encoder_dim, decoder_dim)
        self.decoder = DecoderWithAttention(vocab_size, embed_dim, encoder_dim, decoder_dim)

    def forward(self, images, captions):
        encoder_out = self.encoder(images)  # (batch, num_pixels, encoder_dim)
        decoder_out, _ = self.decoder(encoder_out, captions)
        return decoder_out
```

## 5. 小結

Attention 機制讓影像描述模型能夠「所見即所言」，大幅提升了描述的準確性和自然度。

---

**參考資料**
- [Show Attend and Tell Paper](https://www.google.com/search?q=show+attend+and+tell+paper)
- [Image Captioning with Attention](https://www.google.com/search?q=image+captioning+attention+PyTorch+tutorial)