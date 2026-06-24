# DeepMind 發布 WaveNet：原始音訊生成模型

## 前言

DeepMind 於 2017 年發布了 WaveNet，這是一種革命性的原始音訊生成神經網路。WaveNet 可以生成極為逼真的人類語音，為文字轉語音（TTS）系統帶來突破性提升。

## WaveNet 的創新

### dilated Causal Convolutions

WaveNet 使用了一種特殊的卷積結構——dilated causal convolutions：

```
┌─────────────────────────────────────────────────────────┐
│         Dilated Convolutions 的運作方式                  │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Dilated rate = 1:  [x0][x1][x2][x3][x4][x5]           │
│                         │                               │
│  Dilated rate = 2:  [x0][x1][x2][x3][x4][x5]           │
│                           │                             │
│  Dilated rate = 4:  [x0][x1][x2][x3][x4][x5]           │
│                               │                         │
│  感受野隨指數成長                                      │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

```python
class WaveNet(nn.Module):
    def __init__(self, num_channels=256, residual_channels=256,
                 skip_channels=256, dilation_channels=256,
                 num_repeat=30):
        super().__init__()
        self.net = nn.ModuleList()

        for _ in range(num_repeat):
            for dilation in [1, 2, 4, 8, 16, 32, 64, 128]:
                self.net.append(ResidualBlock(
                    dilation_channels,
                    residual_channels,
                    skip_channels,
                    dilation
                ))
```

### PixelCNN 思想

WaveNet 借鑒了 PixelCNN 的思想，將音訊生成視為序列生成問題：

```python
# 音訊被量化為 16-bit 樣本
# 每個時間步預測下一個樣本

# 損失函數
def wavenet_loss(output, target):
    # output: (batch, 256, time)
    # 256 是因為 8-bit μ-law 量化
    return nn.functional.cross_entropy(
        output, target, reduction='none'
    ).mean()
```

## 架構詳解

```python
class ResidualBlock(nn.Module):
    def __init__(self, dilation_channels, residual_channels,
                 skip_channels, dilation):
        super().__init__()
        self.filter_conv = nn.Conv1d(
            residual_channels,
            dilation_channels,
            2 * dilation,
            dilation=dilation
        )
        self.gate_conv = nn.Conv1d(
            residual_channels,
            dilation_channels,
            2 * dilation,
            dilation=dilation
        )
        self.residual_conv = nn.Conv1d(
            dilation_channels,
            residual_channels,
            1
        )
        self.skip_conv = nn.Conv1d(
            dilation_channels,
            skip_channels,
            1
        )

    def forward(self, x):
        filter = torch.tanh(self.filter_conv(x))
        gate = torch.sigmoid(self.gate_conv(x))
        out = filter * gate

        skip = self.skip_conv(out)
        residual = self.res_conv(out)

        return x + residual, skip
```

## 效能與品質

### 語音品質評估

```
┌─────────────────────────────────────────────────────────┐
│         WaveNet 語音品質 (MOS 分數)                     │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  方法                  MOS 分數                         │
│  ───────────────────────────────────────────────────   │
│  真人錄音            4.7                               │
│  WaveNet             4.0                               │
│  參數化 TTS          3.5                               │
│  拼接 TTS            3.0                               │
│                                                         │
│  MOS: Mean Opinion Score (1-5 分，5 為最高)             │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## 應用

### 文字轉語音

```python
# WaveNet 可以將文字轉換為自然語音
class TTSWaveNet:
    def synthesize(self, text):
        # 文字 → 語音特徵 → WaveNet → 波形
        text_encoded = self.text_encoder(text)
        mel_spectrogram = self.predict_mel(text_encoded)
        waveform = self.wavenet.generate(mel_spectrogram)
        return waveform
```

### 音樂生成

相同的架構也可以用於音樂生成：

```python
# 生成鋼琴音樂
music_wavenet = WaveNet(num_classes=128)  # 128 種音符
generated_notes = music_wavenet.sample()
```

## 後續發展

### Parallel WaveNet

原始 WaveNet 速度很慢，後來提出了 Parallel WaveNet：

```python
# 使用 flow-based 模型加速
class ParallelWaveNet:
    """
    使用 Inverse Autoregressive Flow (IAF)
    實現並行生成
    """
    def forward(self, noise):
        return self.flow(noise)  # 單次前向傳播即可生成
```

### WaveRNN

2018 年提出了更高效能的 WaveRNN：

```python
# 使用 RNN 的輕量級模型
class WaveRNN(nn.Module):
    def __init__(self):
        self.rnn = nn.GRU(256, 512, batch_first=True)
        self.fc = nn.Linear(512, 256)

    def forward(self, x, hidden=None):
        out, hidden = self.rnn(x, hidden)
        out = self.fc(out)
        return out, hidden
```

## 對 AI 的影響

WaveNet 的意義：

1. **生成品質**：展示了深度學習生成高質量音訊的潛力
2. **遷移學習**：Dilated convolution 被廣泛採用
3. **TTS 革命**：推動了 Google Assistant 等產品的語音品質提升

## 結論

WaveNet 代表了生成模型在音訊領域的重大突破。它的架構創新，特別是 dilated convolutions，對後來的模型產生了深遠影響。

---

**延伸閱讀**

- [WaveNet Paper (van den Oord et al., 2016)](https://www.google.com/search?q=WaveNet+Oord+2016)
- [DeepMind WaveNet Blog](https://www.google.com/search?q=DeepMind+WaveNet+blog)
- [Audio Generation with GANs](https://www.google.com/search?q=audio+generation+neural+network)

---

*本篇文章為「AI 程式人雜誌 2017 年 10 月號」AI 相關文章之一。*