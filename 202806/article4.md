# Flash Attention 演算法

## 注意力機制的記憶體瓶頸

標準注意力計算 $Attention(Q,K,V) = softmax(QK^T / \sqrt{d}) V$ 需要：

1. 計算 $S = QK^T$ — 產生 $N \times N$ 的矩陣
2. 將 $S$ 寫回 HBM（高頻寬記憶體）
3. 讀取 $S$ 做 softmax
4. 乘以 $V$ 寫回

對於序列長度 $N=4096$ 和 32 頭注意力，$S$ 矩陣佔 **512 MB**。當 $N=8192$ 時躍升為 **2 GB**。HBM 讀寫是主瓶頸。

## Flash Attention 的核心技巧

Flash Attention 將注意力計算**分塊（tiling）**，讓中間矩陣 $S$ 始終留在 SRAM 中：

```python
import math

def flash_attention_tile(Q, K, V, block_size=128):
    """Simulated Flash Attention with tiling"""
    N, d = Q.shape
    output = [[0.0] * d for _ in range(N)]

    for i in range(0, N, block_size):
        q_tile = Q[i:i + block_size]
        for j in range(0, N, block_size):
            k_tile = K[j:j + block_size]
            v_tile = V[j:j + block_size]

            # Compute S = Q * K^T in SRAM
            s_tile = [[0.0] * len(k_tile) for _ in range(len(q_tile))]
            for qi in range(len(q_tile)):
                for kj in range(len(k_tile)):
                    s_tile[qi][kj] = sum(q_tile[qi][t] * k_tile[kj][t] for t in range(d))

            # Softmax + multiply V
            for qi in range(len(q_tile)):
                max_v = max(s_tile[qi])
                exp_sum = sum(math.e ** (s_tile[qi][kj] - max_v) for kj in range(len(k_tile)))
                for t in range(d):
                    acc = 0.0
                    for kj in range(len(v_tile)):
                        attn = math.e ** (s_tile[qi][kj] - max_v) / exp_sum
                        acc += attn * v_tile[kj][t]
                    output[i + qi][t] += acc

    return output
```

## 軟體重計算（Recomputation）

反向傳播時，Flash Attention **不儲存 $S$ 矩陣**，而是在反向時重新計算。雖然增加了計算量，但減少了 HBM 存取：

```python
def flash_attention_forward(Q, K, V, block_size=128):
    """Forward pass — don't store S matrix, only output"""
    N = len(Q)
    O = [[0.0] * len(V[0]) for _ in range(N)]

    for i in range(0, N, block_size):
        for j in range(0, N, block_size):
            q_tile = Q[i:i + block_size]
            k_tile = K[j:j + block_size]
            v_tile = V[j:j + block_size]
            # Compute on the fly, store only output
            ...

    # Store only Q, K, V for backward
    return O, (Q, K, V, block_size)
```

## 效能比較

| 方法 | HBM 存取 | 速度 (N=4096) |
|------|---------|-------------|
| 標準注意力 | $O(N^2)$ | 1x |
| Flash Attention v1 | $O(N^2/s)$ | 2-4x |
| Flash Attention v2 | $O(N^2/s)$ | 3-6x |

## 延伸閱讀

- [Flash Attention 論文](https://www.google.com/search?q=Flash+Attention+fast+memory+efficient)
- [Flash Attention v2](https://www.google.com/search?q=Flash+Attention+v2)
- [Tri Dao 的實作](https://www.google.com/search?q=Flash+Attention+Tri+Dao)

Flash Attention 在不犧牲精度的前提下，透過分塊計算與軟體重計算，將注意力機制的速度提升 2-6 倍。它讓長序列 Transformer 訓練與推理變得實際可行。
