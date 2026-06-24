# KV Cache 與注意力最佳化（2023-2028）

## Transformer 推論的瓶頸

Transformer 的自注意力機制在生成每個 token 時，需要重新計算所有先前 token 的 Key 和 Value 向量。隨著序列長度增加，計算量呈二次增長——這就是 LLM 推論延遲的核心問題。

## KV Cache 的基本原理

KV Cache 的直覺很簡單：既然 Key 和 Value 在前面的步驟已經算過了，為什麼不存下來？

```python
class KVCache:
    def __init__(self, max_seq=2048, d_k=64):
        self.k_cache = np.zeros((max_seq, d_k), dtype=np.float16)
        self.v_cache = np.zeros((max_seq, d_k), dtype=np.float16)
        self.pos = 0
    
    def update(self, k, v):
        n = k.shape[0]  # 當前批次 token 數
        self.k_cache[self.pos:self.pos+n] = k
        self.v_cache[self.pos:self.pos+n] = v
        self.pos += n
        return self.k_cache[:self.pos], self.v_cache[:self.pos]
```

## 記憶體壓力分析

KV Cache 的記憶體消耗驚人：

```
GPT-3 175B, 序列長度 2048, FP16:
每層: 2 × 2048 × 12288 × 2 bytes = 96 MB
96 層: ≈ 9.2 GB

batch size = 64 → 約 590 GB！
```

這就是為什麼 KV Cache 最佳化至關重要。

## PagedAttention

vLLM 的核心貢獻——將虛擬記憶體分頁概念引入 KV Cache：

```
傳統: [Seq0: ████████][Seq1: ████░░░░][Seq2: ██░░░░░░]
      每個序列連續儲存，碎片嚴重

PagedAttention:
Block Table:
┌──────┬──────┬──────┬──────┐
│ Seq0 │ Seq0 │ Seq1 │ Seq2 │
├──────┼──────┼──────┼──────┤
│ Seq1 │ Seq0 │ Seq3 │ Seq3 │
└──────┴──────┴──────┴──────┘
分頁管理，利用率接近 100%
```

## Multi-Query Attention（MQA）

MQA 是 2023 年出現的關鍵最佳化。原始 MHA（Multi-Head Attention）每個 head 有自己的 K 和 V，MQA 讓所有 head 共用 K 和 V：

```
MHA:     12 heads × 12 KV pairs = 12 KV
MQA:     12 heads ×  1 KV pair  =  1 KV
GQA:     12 heads ×  4 KV pairs =  4 KV (折衷方案)
```

## FlashAttention

FlashAttention 通過 IO-aware 演算法減少高頻寬記憶體（HBM）的讀寫：

```python
# 概念示意：分塊計算注意力
def flash_attention(Q, K, V, block_size=128):
    n = Q.shape[0]
    output = np.zeros_like(Q)
    for i in range(0, n, block_size):
        Q_block = Q[i:i+block_size]
        for j in range(0, n, block_size):
            K_block = K[j:j+block_size]
            V_block = V[j:j+block_size]
            # 在 SRAM 中計算區域注意力
            S_block = Q_block @ K_block.T
            P_block = softmax(S_block)
            output[i:i+block_size] += P_block @ V_block
    return output
```

## 2025-2028 前沿

KV Cache 的未來方向包括：稀疏注意力（只在特定位置儲存 KV）、量化 KV Cache（INT4/INT2）、以及用線性注意力完全取代傳統注意力機制。

## 延伸閱讀

- [FlashAttention: Fast and Memory-Efficient Attention](https://www.google.com/search?q=FlashAttention+fast+memory+efficient+attention)
- [PagedAttention: vLLM Architecture](https://www.google.com/search?q=PagedAttention+vLLM+architecture)
- [Multi-Query Attention in LLMs](https://www.google.com/search?q=multi+query+attention+transformer)

---

*本篇文章為「AI 程式人雜誌 2026 年 6 月號」焦點系列之五。*
