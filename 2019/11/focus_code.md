# 語言模型實作

## 前言

本篇文章將介紹一個簡化的語言模型實作，幫助讀者理解 GPT-2 等模型的基本原理。

## 原始碼

完整的 Python 實作請參考：[_code/gpt2_simplified.py](_code/gpt2_simplified.py)

```python
#!/usr/bin/env python3
import math
import torch
import torch.nn as nn

class PositionalEncoding(nn.Module):
    def __init__(self, d_model, max_len=5000):
        super().__init__()
        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len).unsqueeze(1).float()
        div_term = torch.exp(torch.arange(0, d_model, 2).float() * (-math.log(10000.0) / d_model))
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        pe = pe.unsqueeze(0)
        self.register_buffer('pe', pe)

    def forward(self, x):
        return x + self.pe[:, :x.size(1)]

class TransformerLM(nn.Module):
    def __init__(self, vocab_size, d_model, num_heads, num_layers):
        super().__init__()
        self.token_embedding = nn.Embedding(vocab_size, d_model)
        self.position_encoding = PositionalEncoding(d_model)

        self.decoder_layers = nn.ModuleList([
            nn.TransformerDecoderLayer(d_model, num_heads, dim_feedforward=d_model * 4, dropout=0.1)
            for _ in range(num_layers)
        ])

        self.fc = nn.Linear(d_model, vocab_size)

    def forward(self, x, memory_mask=None):
        x = self.token_embedding(x) * math.sqrt(x.size(-1))
        x = self.position_encoding(x)

        for layer in self.decoder_layers:
            x = layer(x, x, tgt_mask=None, tgt_key_padding_mask=None)

        return self.fc(x)

def demo():
    print("Simplified Transformer Language Model Demo")
    print("=" * 50)

    vocab_size = 10000
    d_model = 256
    num_heads = 8
    num_layers = 6

    torch.manual_seed(42)

    model = TransformerLM(vocab_size, d_model, num_heads, num_layers)
    model.eval()

    seq_len = 10
    batch_size = 2
    x = torch.randint(0, vocab_size, (batch_size, seq_len))

    print(f"Vocabulary size: {vocab_size}")
    print(f"Model dimension: {d_model}")
    print(f"Number of heads: {num_heads}")
    print(f"Number of layers: {num_layers}")
    print()
    print(f"Input sequence shape: {x.shape}")

    with torch.no_grad():
        output = model(x)
        logits = output[:, -1, :]
        probabilities = torch.softmax(logits, dim=-1)
        next_token = torch.argmax(probabilities, dim=-1)

    print(f"Output shape: {output.shape}")
    print(f"Next token probabilities shape: {probabilities.shape}")
    print(f"Predicted next tokens: {next_token.tolist()}")
    print()
    print("Note: This is a simplified implementation.")
    print("The actual GPT-2 model uses:")
    print("- 48 layers, 1600 hidden dimension, 25 heads")
    print("- 1.5B parameters total")
    print("- Learned positional embeddings")

if __name__ == "__main__":
    demo()
```

---

## 執行結果

```
Simplified Transformer Language Model Demo
==================================================
Vocabulary size: 10000
Model dimension: 256
Number of heads: 8
Number of layers: 6

Input sequence shape: torch.Size([2, 10])
Output shape: torch.Size([2, 10, 10000])
Next token probabilities shape: torch.Size([2, 10000])
Predicted next tokens: [7823, 2156]

Note: This is a simplified implementation.
The actual GPT-2 model uses:
- 48 layers, 1600 hidden dimension, 25 heads
- 1.5B parameters total
- Learned positional embeddings
```

---

## 語言模型的核心概念

### 語言建模目標

語言模型的目標是預測下一個 token：

```python
# 語言模型目標
# P(w_t | w_{<t})
# 給定前面的詞，預測下一個詞
```

### Transformer 解碼器

GPT-2 使用 Transformer 解碼器：

```
Transformer 解碼器的特點：
- 使用遮蔽自注意力（Masked Self-Attention）
- 每個位置只能看到之前的 token
- 適合生成式任務
```

### 注意力機制

遮蔽自注意力的工作方式：

```
位置 0：只能看到位置 0
位置 1：只能看到位置 0, 1
位置 2：只能看到位置 0, 1, 2
...
```

---

## GPT-2 與簡化實現的對比

| 方面 | 簡化實現 | GPT-2 |
|------|----------|-------|
| 層數 | 6 | 48 |
| 隱藏維度 | 256 | 1600 |
| 注意力頭數 | 8 | 25 |
| 參數量 | ~10M | 1.5B |

---

## 結論

本篇文章介紹了語言模型的基本原理和一個簡化的 Transformer 語言模型實現。雖然真正的 GPT-2 模型規模要大得多，但其核心架構是相似的。希望這個簡化的實現能幫助讀者更好地理解 GPT-2 等大型語言模型的工作原理。

---

**延伸閱讀**

- [GPT-2+Architecture](https://www.google.com/search?q=GPT-2+architecture+explained)
- [Transformer+Language+Model](https://www.google.com/search?q=transformer+language+model+tutorial)
- [Language+Model+from+Scratch](https://www.google.com/search?q=language+model+from+scratch+python)