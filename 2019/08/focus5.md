# Positional Encoding

## 為序列添加位置資訊

Transformer 的自注意力機制本身是 permutation equivariant 的——它對輸入順序不變。這意味著如果我們打亂輸入序列的順序，輸出也會以相同方式被打亂，但內容不變。

然而，序列順序在語言和時間序列中至關重要。我們需要一種方式來告訴 Transformer 這些資訊——這就是位置編碼（Positional Encoding）。

---

## 問題背景

### 自注意力忽略位置

```python
# 自注意力的計算
# output = softmax(QK^T / sqrt(d)) V
# 這個計算與順序無關！

x1 = embedding("cat")
x2 = embedding("sat")
# "cat sat" 和 "sat cat" 會得到相同的注意力權重
```

### 解決方案

有兩種常見的方法：

1. **絕對位置編碼**：為每個位置分配一個獨特的向量
2. **相對位置編碼**：編碼位置之間的相對距離

---

## 正弦/餘弦位置編碼

### 原始 Transformer 論文中的設計

```python
import math
import torch

class PositionalEncoding(nn.Module):
    def __init__(self, d_model, max_len=5000):
        super().__init__()

        # 創建位置編碼矩陣
        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len, dtype=torch.float).unsqueeze(1)
        div_term = torch.exp(
            torch.arange(0, d_model, 2).float() * (-math.log(10000.0) / d_model)
        )

        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)

        pe = pe.unsqueeze(0)  # [1, max_len, d_model]
        self.register_buffer('pe', pe)

    def forward(self, x):
        # x: [batch, seq_len, d_model]
        return x + self.pe[:, :x.size(1)]
```

### 為什麼選擇正弦/餘弦函式？

```
┌─────────────────────────────────────────────────────┐
│         正弦/餘弦位置編碼的可視化                     │
├─────────────────────────────────────────────────────┤
│                                                     │
│   維度 0 (sin):                                    │
│   pos=0:  sin(0) = 0                               │
│   pos=1:  sin(1) = 0.84                            │
│   pos=2:  sin(2) = 0.91                            │
│   pos=3:  sin(3) = 0.14                            │
│                                                     │
│   維度 1 (cos):                                    │
│   pos=0:  cos(0) = 1                               │
│   pos=1:  cos(1) = 0.54                            │
│   pos=2:  cos(2) = -0.42                           │
│   pos=3:  cos(3) = -0.99                           │
│                                                     │
│   每個位置有一個獨特的編碼                           │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### 數學性質

```python
# 為什麼有效？

# 公式
PE(pos, 2i) = sin(pos / 10000^(2i/d_model))
PE(pos, 2i+1) = cos(pos / 10000^(2i/d_model))

# 性質 1：每個位置的編碼是獨特的
# 性質 2：編碼是周期性的，週期為 10000^(2i/d_model)
# 性質 3：可以表示任意長度的位置
```

---

## 位置編碼的可視化

### 編碼模式

```python
# 可視化位置編碼
# 每個位置是一個 d_model 維的向量

# 圖示（d_model = 4，max_len = 20）
# 每一行是一個位置的編碼

位置 0: [0,  1,    0,     1   ]
位置 1: [0.84, 0.54, 0.09, 0.99]
位置 2: [0.91, -0.42, 0.17, 0.98]
...
```

### 不同頻率的週期

```python
# 不同維度有不同的週期
# i=0: 週期 = 2π * 10000^0 = 2π
# i=1: 週期 = 2π * 10000^(1/d_model)
# i=2: 週期 = 2π * 10000^(2/d_model)
# ...
# i=d/2-1: 週期 = 2π * 10000
```

這確保了：
- 較低頻率捕獲較遠距離
- 較高頻率捕獲較近距離

---

## 學習的位置編碼

### 替代方案：可學習的參數

```python
class LearnedPositionalEncoding(nn.Module):
    def __init__(self, d_model, max_len):
        super().__init__()
        self.pe = nn.Embedding(max_len, d_model)

    def forward(self, x):
        batch, seq_len = x.size()
        positions = torch.arange(seq_len, device=x.device)
        return x + self.pe(positions)
```

### 對比

| 特性 | 正弦/餘弦 | 學習的 |
|------|-----------|--------|
| 參數 | 固定，無需訓練 | 可訓練 |
| 推廣 | 可處理任意長度 | 受限於訓練長度 |
| 理論基礎 | 有數學解釋 | 經驗結果 |
| 常用場景 | Transformer 原始設計 | 某些改進版本 |

---

## 相對位置編碼

### Shaw 等人的設計

2018 年，Shaw 等人提出了相對位置編碼：

```python
class RelativePositionalEncoding(nn.Module):
    def __init__(self, d_model, max_rel_pos=16):
        super().__init__()
        self.max_rel_pos = max_rel_pos
        self.rel_embeddings = nn.Embedding(2 * max_rel_pos + 1, d_model)

    def forward(self, length):
        # 創建相對位置索引
        range_vec = torch.arange(length)
        rel_pos = range_vec.unsqueeze(1) - range_vec.unsqueeze(0)
        rel_pos = rel_pos.clamp(-self.max_rel_pos, self.max_rel_pos)
        rel_pos += self.max_rel_pos  # 偏移為非負
        return self.rel_embeddings(rel_pos)
```

### 優勢

1. **建模相對關係**：語言中相對位置往往更重要
2. **更好的泛化**：可以處理訓練時未見過的距離
3. **語法結構**：適合捕捉句法關係

---

## 其他位置編碼變體

### 旋轉位置編碼（RoPE）

2021 年提出的方法，使用旋轉矩陣：

```python
def apply_rotary_pos_emb(x, cos, sin):
    x1, x2 = x[..., :x.size(-1)//2], x[..., x.size(-1)//2:]
    return torch.cat([x1 * cos - x2 * sin, x2 * cos + x1 * sin], dim=-1)
```

### ALiBi（Attention with Linear Biases）

避免使用位置編碼，改用注意力偏置：

```python
# ALiBi 的注意力分數偏移
score = score - |i - j| * m
# m 是一個根據頭索引遞減的斜率
```

### 混合位置編碼

結合絕對和相對位置編碼。

---

## 在實際應用中的注意事項

### 1. 序列長度規劃

```python
# 規劃最大序列長度
MAX_SEQ_LEN = 512  # BERT, GPT-2
MAX_SEQ_LEN = 2048  # GPT-3
MAX_SEQ_LEN = 4096  # LLaMA
MAX_SEQ_LEN = 100000  # Longformer
```

### 2. 內存考慮

注意力機制本身是 O(n²) 複雜度：
```python
# 長序列的內存消耗
# n = 1000:  1M 元素
# n = 5000:  25M 元素
# n = 10000: 100M 元素
```

### 3. 與其他技術的結合

```python
# 位置編碼 + 閒時填充
class PositionalEncodingWithPadding(nn.Module):
    def __init__(self, d_model, max_len, padding_idx):
        super().__init__()
        self.pe = PositionalEncoding(d_model, max_len)
        self.padding_idx = padding_idx

    def forward(self, x, mask=None):
        output = self.pe(x)
        if mask is not None:
            output = output.masked_fill(mask.unsqueeze(-1), 0)
        return output
```

---

## 總結

位置編碼是 Transformer 的重要組成部分：

1. **必要性**：自注意力本身不考慮位置
2. **正弦/餘弦**：通用、可以處理任意長度
3. **可學習的**：靈活但受限於訓練長度
4. **相對位置編碼**：更适合捕捉語法關係

位置編碼的選擇會影響模型捕捉位置關係的能力，需要根據任務特點選擇。

---

## 延伸閱讀

- [Positional Encoding Transformer](https://www.google.com/search?q=positional+encoding+transformer)
- [Relative position encoding](https://www.google.com/search?q=relative+position+encoding)
- [Rotary+position+embedding](https://www.google.com/search?q=rotary+position+embedding)

---

*本篇文章為「AI 程式人雜誌 2019 年 8 月號」注意力機制系列之五。*