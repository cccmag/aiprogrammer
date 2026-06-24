# Transformer 架構的崛起

## 前言

Transformer 架構在 2017 年被提出，經過 2018-2019 年的發展，已經成為 NLP 和 AI 領域的核心架構。

## Transformer 的核心

### 自注意力機制

Transformer 的核心是自注意力機制：

```python
def attention(query, keys, values):
    scores = torch.matmul(query, keys.transpose(-2, -1))
    scores = scores / math.sqrt(d_k)
    weights = torch.softmax(scores, dim=-1)
    return torch.matmul(weights, values)
```

### 架構類型

| 類型 | 代表模型 | 應用 |
|------|----------|------|
| Encoder only | BERT, RoBERTa | 理解任務 |
| Decoder only | GPT, GPT-2 | 生成任務 |
| Encoder-Decoder | T5, BART | 序列到序列 |

## Transformer 的影響

### NLP 領域

Transformer 徹底改變了 NLP：

```
影響：
- 幾乎所有 NLP 任務的效能大幅提升
- 預訓練+微調成為標準
- 各類模型相繼湧現
```

### 其他領域

Transformer 的影響正在擴展到其他領域：

```
擴展：
- 電腦視覺（Vision Transformer）
- 語音處理
- 多模態學習
```

## 結論

Transformer 架構已經成為 AI 領域的基礎構建模組。它的影響力將持續擴大。

---

**延伸閱讀**

- [Transformer+architecture](https://www.google.com/search?q=Transformer+architecture+NLP)
- [Attention+mechanism](https://www.google.com/search?q=attention+mechanism+2019)