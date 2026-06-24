# 因果注意力（掩碼）

## 什麼是因果注意力？

因果注意力（Causal Attention），也稱為 Masked Attention 或 Autoregressive Attention，是 Transformer 解碼器的核心機制。它的目的是防止模型在生成當前位置的輸出時「看到」未來的資訊。

在自迴歸生成中，模型應該按照序列順序逐個生成 token：t₁, t₂, t₃, ...。當生成 t₂ 時，模型只能使用 t₁ 和之前的資訊，不能看到 t₃ 或之後的 token。

## 因果遮罩的實現

### 上三角遮罩

因果遮罩的實現非常簡單：將注意力分數矩陣的上三角部分設為 -∞（在 softmax 後對應的權重為 0）：

```
位置    1    2    3    4    5
1      [1,   0,   0,   0,   0]   ← 位置 1 只能關注自己
2      [0.5, 0.5, 0,   0,   0]   ← 位置 2 只能關注 1 和 2
3      [0.3, 0.3, 0.4, 0,   0]   ← 位置 3 只能關注 1,2,3
4      [0.2, 0.2, 0.3, 0.3, 0]   ← 位置 4 只能關注 1-4
5      [0.1, 0.2, 0.3, 0.2, 0.2] ← 位置 5 能關注所有位置
```

在程式碼中：
```python
def causal_mask(size):
    mask = torch.triu(torch.ones(size, size), diagonal=1).bool()
    return mask  # True 表示需要被遮蔽的位置

# 應用遮罩
scores = scores.masked_fill(mask, float('-inf'))
weights = F.softmax(scores, dim=-1)
```

### 代碼實現

```python
def self_attention_with_causal_mask(Q, K, V):
    d_k = Q.shape[-1]
    scores = Q @ K.T / np.sqrt(d_k)
    n = Q.shape[0]
    mask = np.triu(np.ones((n, n)), k=1).astype(bool)
    scores = np.where(mask, -1e9, scores)
    weights = softmax(scores, axis=-1)
    output = weights @ V
    return output, weights
```

## 因果注意力的數學特性

### 三角性質

因果注意力的注意力權重矩陣是一個下三角矩陣（包括對角線）。這意味著：

- 位置 i 可以關注位置 j，當且僅當 j ≤ i
- 注意力矩陣是三角的，但不是對稱的

### 機率性質

遮罩後，每行的注意力權重仍然滿足：
- Σ_j α_{ij} = 1（所有可見位置的權重和為 1）
- 0 ≤ α_{ij} ≤ 1

## 在 Transformer 解碼器中的應用

### 標準 Transformer 解碼器

Transformer 解碼器由三層組成：
1. **Masked Self-Attention**：使用因果遮罩，防止看到未來 token
2. **Cross-Attention**：不使用遮罩，關注編碼器所有位置
3. **Feed-Forward Network**：逐位置的全連接層

### 訓練與推論的差異

**訓練階段**：
- 使用 Teacher Forcing，一次性計算所有位置的注意力
- 透過因果遮罩確保自迴歸性質
- 高度並行化

**推論階段**：
- 逐個生成 token，無法並行化
- 使用 KV Cache 儲存已計算的 Key 和 Value
- 每次只計算新增 token 的注意力

## 因果注意力的變體

### Prefix 注意力

Prefix Attention（或 Prefix LM）讓序列前綴可以互相關注所有位置，而後綴使用因果遮罩。這在編碼器-解碼器統一模型中很常見：

```
Prefix: 所有位置雙向關注
位置    1    2    3    4    5    6
1      [1,   0.5, 0.3, 0,   0,   0]
2      [0.4, 0.6, 0.2, 0,   0,   0]
3      [0.2, 0.3, 0.5, 0,   0,   0]
4      [0.1, 0.2, 0.3, 0.4, 0,   0]  ← mask 從這裡開始
5      [0.1, 0.1, 0.2, 0.3, 0.3, 0]
6      [0.1, 0.1, 0.1, 0.2, 0.3, 0.2]
```

### 稀疏因果注意力

在稀疏注意力中，因果遮罩可以與稀疏模式結合，只計算部分 < i 的注意力：

- **Strided 模式**：關注 i-w 到 i-1 的連續範圍 + 間隔關注更早的位置
- **壓縮模式**：對歷史資訊進行壓縮後再關注

## KV Cache：因果注意力的效率優化

### 為什麼需要 KV Cache？

在推論時，如果每次生成一個 token 都重新計算所有位置的注意力，計算量會非常大：

```
生成第 t 個 token：
標準方法：計算 t×t 的注意力矩陣，然後只看最後一行
KV Cache：只計算最後一行（之前行的 K 和 V 已快取）
```

### 記憶體消耗

對於長序列生成（如 n=4096），KV Cache 的記憶體消耗為：

```
每層：2 × n × d_k × 頭數 × 精度
總計：層數 × 每層消耗
```

以 Llama 2 7B 為例：32 層 × 2 × 4096 × 128 × 8 × 2 bytes ≈ 2.6 GB

## 結論

因果注意力是 Transformer 解碼器能夠進行自迴歸生成的關鍵設計。它的優雅之處在於：透過一個簡單的遮罩矩陣，就實現了對序列順序的嚴格控制，同時保持了訓練時的高度並行化。

---

**延伸閱讀**
- [Transformer 解碼器因果注意力](https://www.google.com/search?q=transformer+decoder+causal+attention+mask)
- [KV Cache 與高效推論](https://www.google.com/search?q=KV+cache+transformer+inference)
- [Prefix LM 注意力](https://www.google.com/search?q=prefix+language+model+attention+mask)
