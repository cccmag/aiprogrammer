# 生成式 AI 的興起：從 GAN 到文字生成

## 前言

生成式 AI 是目前 AI 領域最熱門的方向之一。從圖像生成到文字創作，生成模型正在改變我們對 AI 的認知。

## 生成對抗網路（GAN）

### 基本原理

GAN 由 Ian Goodfellow 在 2014 年提出，包含兩個神經網路：
- **生成器（Generator）**：生成假樣本
- **判別器（Discriminator）**：區分真假樣本

```
┌─────────────────────────────────────────────────────┐
│                   GAN 結構                          │
├─────────────────────────────────────────────────────┤
│                                                     │
│   生成器 ──────► 假樣本 ──────┐                    │
│      ▲                        │                    │
│      │                        ▼                    │
│      │              ┌──────────────┐               │
│      │              │   判別器     │               │
│      │              │  輸出: 真/假  │               │
│      │              └──────────────┘               │
│      │                        ▲                    │
│      └────────────────────────┘                    │
│         真實資料                                    │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### 對抗訓練

```python
# 損失函數
# 判別器：最大化真假樣本的分類準確率
# 生成器：最小化判別器正確識別假樣本的能力

D_loss = -log(D(real)) - log(1 - D(G(z)))
G_loss = -log(D(G(z)))
```

### GAN 的應用

1. **圖像生成**：逼真的人臉、藝術作品
2. **圖像翻譯**：風格遷移、夏冬轉換
3. **資料增強**：生成訓練樣本
4. **超解析度**：將低解析度轉為高解析度

## 文字生成

### 文字生成的方法

在 GPT 之前，文字生成主要基於：

1. **N-gram 模型**：簡單但效果有限
2. **RNN/LSTM**：能生成較連貫的文字
3. **Seq2seq + Attention**：機器翻譯、摘要生成

### GPT 的貢獻

GPT 展示了預訓練語言模型在文字生成上的強大能力。給定一個開頭，GPT 可以生成連貫的續寫。

```python
# GPT 文字生成示例
def generate_text(model, start_text, max_length=50):
    input_ids = tokenize(start_text)
    for _ in range(max_length):
        logits = model(input_ids)
        next_token_logits = logits[-1, :]
        probs = F.softmax(next_token_logits, dim=-1)
        next_token = torch.multinomial(probs, num_samples=1)
        input_ids = torch.cat([input_ids, next_token])
    return detokenize(input_ids)
```

## 生成式 AI 的挑戰

1. **品質控制**：生成的內容可能不一致或有錯誤
2. **多樣性與保真度的平衡**：避免模式崩潰
3. **評估困難**：如何衡量「好」的生成結果
4. **倫理問題**：深度偽造、虛假資訊

## 結語

生成式 AI 正在快速發展。從 GPT 開始，預訓練語言模型成為文字生成的主流方法。

---

**延伸閱讀**

- [GAN 論文](https://www.google.com/search?q=GAN+generative+adversarial+network+2014)
- [GPT 論文](https://www.google.com/search?q=Improving+Language+Understanding+by+Generative+Pre-Training+2018)
- [文字生成模型](https://www.google.com/search?q=text+generation+neural+network)

---

*本篇文章為「AI 程式人雜誌 2018 年 6 月號」GPT 與生成式 AI 系列之一。*