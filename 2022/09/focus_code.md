# 注意力機制 Python 實作

## 前言

本篇文章將完整實作三種核心注意力機制：Bahdanau Attention（加法注意力）、Luong Attention（乘法注意力）、以及 Self-Attention（自我注意力）。所有實作均使用 Python + NumPy，不依賴深度學習框架，以便讀者理解注意力的數學原理。

---

## 原始碼

完整的 Python 實作請參考：[_code/attention.py](_code/attention.py)

```python
import numpy as np

def softmax(x, axis=-1):
    e = np.exp(x - np.max(x, axis=axis, keepdims=True))
    return e / np.sum(e, axis=axis, keepdims=True)

def bahdanau_score(query, keys, W_q, W_k, v):
    query_trans = W_q @ query
    keys_trans = W_k @ keys.T
    energies = v @ np.tanh(query_trans[:, None] + keys_trans)
    return energies

def bahdanau_attention(query, keys, values, W_q, W_k, v):
    scores = bahdanau_score(query, keys, W_q, W_k, v)
    weights = softmax(scores)
    context = weights @ values
    return context, weights

def luong_score(query, keys, method="dot"):
    if method == "dot":
        return query @ keys.T
    elif method == "general":
        W = np.random.randn(len(query), len(query)) * 0.1
        return (W @ query) @ keys.T
    elif method == "concat":
        W = np.random.randn(len(query), len(query)) * 0.1
        v = np.random.randn(len(query)) * 0.1
        return v @ np.tanh(W @ (query[:, None] + keys))

def luong_attention(query, keys, values, method="dot"):
    scores = luong_score(query, keys, method)
    weights = softmax(scores)
    context = weights @ values
    return context, weights

def self_attention(Q, K, V, mask=None):
    d_k = K.shape[-1]
    scores = Q @ K.T / np.sqrt(d_k)
    if mask is not None:
        scores = np.where(mask, -1e9, scores)
    weights = softmax(scores, axis=-1)
    output = weights @ V
    return output, weights
```

---

## 執行結果

```
[Bahdanau Attention]
  context shape: (8,)
  weights: [0.167 0.162 0.167 0.17  0.169 0.164]

[Luong Attention (dot)]
  context shape: (8,)
  weights: [0.001 0.001 0.09  0.005 0.109 0.794]

[Self-Attention]
  output shape: (6, 8)
  weights shape: (6, 6)
  weights:
[[0.164 0.204 0.112 0.12  0.307 0.093]
 [0.194 0.096 0.143 0.316 0.109 0.142]
 [0.268 0.199 0.17  0.199 0.094 0.071]
 [0.321 0.126 0.141 0.172 0.025 0.215]
 [0.135 0.165 0.074 0.142 0.298 0.187]
 [0.019 0.073 0.385 0.327 0.022 0.174]]

[Causal Self-Attention]
  masked weights:
[[1.    0.    0.    0.    0.    0.   ]
 [0.668 0.332 0.    0.    0.    0.   ]
 [0.421 0.312 0.267 0.    0.    0.   ]
 [0.422 0.166 0.186 0.226 0.    0.   ]
 [0.166 0.203 0.09  0.174 0.366 0.   ]
 [0.019 0.073 0.385 0.327 0.022 0.174]]
```

---

## Bahdanau Attention（加法注意力）

Bahdanau Attention 由 Bahdanau 等人於 2014 年提出，是第一個成功應用於 Seq2Seq 模型的注意力機制。

**核心公式：**
```
score(q, k_i) = v^T tanh(W_q q + W_k k_i)
```

其中 W_q、W_k 和 v 是可學習的參數。由於使用了加法操作和 tanh 激活函數，這種注意力也被稱為「加法注意力」（Additive Attention）。

**關鍵特性：**
- 使用可學習的參數計算注意力分數
- 每個查詢-鍵對都需要計算一個非線性變換
- 靈活性高，但計算相對較慢

## Luong Attention（乘法注意力）

Luong Attention 由 Luong 等人於 2015 年提出，簡化了注意力分數的計算方式。

**三種評分函數：**

| 方法 | 公式 | 特點 |
|------|------|------|
| dot | score = q · k | 最簡單，無參數 |
| general | score = q^T W k | 加入可學習矩陣 |
| concat | score = v^T tanh(W [q; k]) | 類似 Bahdanau |

**關鍵特性：**
- dot 方法使用純點積，計算最快
- general 方法加入可學習投影
- 整體效率高於 Bahdanau

## Self-Attention（自我注意力）

Self-Attention 是 Transformer 架構的核心，於 2017 年由 Vaswani 等人提出。

**核心公式：**
```
Attention(Q, K, V) = softmax(Q K^T / sqrt(d_k)) V
```

**關鍵特性：**
- 縮放因子 sqrt(d_k) 防止 softmax 進入梯度極小區域
- 支援批量和並行計算
- 可以加入 Mask 控制資訊流（因果注意力）

---

## 延伸閱讀

- [Bahdanau 2014: Neural Machine Translation by Jointly Learning to Align and Translate](https://www.google.com/search?q=Bahdanau+attention+2014)
- [Luong 2015: Effective Approaches to Attention-based Neural Machine Translation](https://www.google.com/search?q=Luong+attention+2015)
- [Vaswani 2017: Attention Is All You Need](https://www.google.com/search?q=Attention+Is+All+You+Need+2017)
