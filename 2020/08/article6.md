# Attention 機制的數學原理

## 前言

Attention 機制是 Transformer 的核心。本文深入解析其數學原理。

---

## 一、基本概念

### 查詢-鍵-值 (QKV) 比喻

```
查詢 (Query): "我在找什麼？"
鍵 (Key): "我有哪些特徵？"
值 (Value): "我的實際內容是什麼？"
```

### 核心公式

```
Attention(Q, K, V) = softmax(QK^T / √d_k) V
```

---

## 二、詳細推導

### 步驟 1：計算相似度

```python
# Q, K 形狀: (batch, heads, seq_len, d_k)
# 計算 Q 和 K 的點積

scores = np.matmul(Q, K.transpose(-2, -1))  # (batch, heads, seq_len, seq_len)

# 每個 query 對每個 key 的相似度
# scores[b, h, i, j] = query[i] · key[j]
```

### 步驟 2：縮放

```python
# 為何要除以 √d_k？
# 當 d_k 很大時，點積的值會很大
# 導致 softmax 进入飽和區域，梯度變小

scaled_scores = scores / np.sqrt(d_k)
```

### 步驟 3：Softmax

```python
def softmax(x):
    exp_x = np.exp(x - np.max(x, axis=-1, keepdims=True))
    return exp_x / (np.sum(exp_x, axis=-1, keepdims=True) + 1e-8)

attn_weights = softmax(scaled_scores)  # (batch, heads, seq_len, seq_len)
# attn_weights[b, h, i, j] = P(key_j | query_i)
```

### 步驟 4：加權求和

```python
# V 形狀: (batch, heads, seq_len, d_v)
output = np.matmul(attn_weights, V)  # (batch, heads, seq_len, d_v)

# output[b, h, i, :] = Σ_j attn_weights[b, h, i, j] * V[b, h, j, :]
```

---

## 三、幾何意義

### QK^T 的幾何含義

QK^T 的第 (i, j) 個元素是查詢向量 q_i 和鍵向量 k_j 的點積：

```
q_i · k_j = ||q_i|| ||k_j|| cos(θ)
```

這衡量了兩個向量的相似度。

### 為何除以 √d_k？

當 d_k 較大時，向量的點積可能很大：

假設 q 和 k 的每個分量是均值 0、方差 1 的隨機變數，則：
- E[q · k] = 0
- Var(q · k) = d_k

除以 √d_k 後：
- Var(q · k / √d_k) = 1

---

## 四、多頭注意力

```python
class MultiHeadAttention:
    def __init__(self, d_model, num_heads):
        self.num_heads = num_heads
        self.d_k = d_model // num_heads
    
    def forward(self, Q, K, V):
        # 線性投影到 num_heads 個子空間
        batch_size = Q.shape[0]
        
        # Q, K, V 各自投影後分頭
        Q = self.split_heads(Q)  # (batch, heads, seq, d_k)
        K = self.split_heads(K)
        V = self.split_heads(V)
        
        # 分別計算每個頭的注意力
        head_outputs = []
        for h in range(self.num_heads):
            attn_out = attention(Q[:, h], K[:, h], V[:, h])
            head_outputs.append(attn_out)
        
        # 拼接並輸出投影
        concat = np.concatenate(head_outputs, axis=-1)
        output = np.dot(concat, self.W_O)
        
        return output
```

### 多頭的幾何解釋

每個頭在不同的子空間中學習相關性：

| 頭 | 專注關係類型 |
|----|-------------|
| 頭 1 | 語法結構 |
| 頭 2 | 語義相似 |
| 頭 3 | 指代關係 |
| ... | ... |

---

## 五、Mask 機制

### Padding Mask

遮罩無效位置：

```python
def create_padding_mask(seq):
    # 假設 pad token 的 id 為 0
    mask = (seq != 0).unsqueeze(1).unsqueeze(2)  # (batch, 1, 1, seq_len)
    return mask

# 應用：將這些位置設為 -inf
scores = scores.masked_fill(mask == 0, -1e9)
```

### Sequence Mask (Decoder)

確保解碼器只能看到之前的 token：

```python
def create_causal_mask(seq_len):
    # 上三角矩陣（不含對角線）為 1
    mask = torch.triu(torch.ones(seq_len, seq_len), diagonal=1)
    return mask == 0  # 轉換為 True=可注意，False=不可注意

# 應用：確保 position i 只注意 position <= i
scores = scores.masked_fill(mask == 0, -1e9)
```

---

## 六、複雜度分析

### 標準注意力

| 操作 | 複雜度 | 說明 |
|------|--------|------|
| QK^T | O(n² · d) | n=序列長度，d=維度 |
| Softmax | O(n²) | - |
| 輸出計算 | O(n² · d) | - |
| **總計** | **O(n² · d)** | 主要瓶頸在 n² |

### 與 RNN 比較

| 架構 | 時間複雜度 | 空間複雜度 | 並行化 |
|------|-----------|-----------|--------|
| RNN | O(n · d) | O(d) | 困難 |
| CNN | O(n · d · k) | O(d) | 容易 |
| Attention | O(n² · d) | O(n²) | 容易 |

---

## 結語

Attention 機制的數學原理清晰優雅。透過 QKV 計算、多頭注意力和 Mask 機制，Transformer 實現了高效且強大的序列建模能力。

---

*延伸閱讀：[attention+mechanism+mathematics+deep+learning](https://www.google.com/search?q=attention+mechanism+mathematics+transformer+explained)*