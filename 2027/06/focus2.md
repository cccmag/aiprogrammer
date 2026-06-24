# 注意力機制的奧秘（2015-2026）

## 從 Seq2Seq + Bahdanau Attention 到 Self-Attention

注意力機制並非 Transformer 的發明。2015 年，Bahdanau 等人首次將注意力引入 Seq2Seq 模型，解決了編碼器固定長度向量的瓶頸。

### Bahdanau Attention（加法注意力）

在 RNN Seq2Seq 中，解碼器每一步會回頭關注編碼器的所有隱藏狀態：

```
y_1, y_2, ..., y_T = Decoder(
    Context_1, Context_2, ..., Context_T
)
其中 Context_t = sum(α_tj × h_j)
```

注意力權重 α_tj 由一個小型神經網路計算：e_tj = v^T tanh(W h_j + U s_t)

### Luong Attention（乘法注意力）

2015 年稍晚，Luong 提出了乘法注意力，使用 dot product 計算分數——這比 Bahdanau 的加法注意力更快且更容易訓練。

### Self-Attention（自注意力）

2017 年 Transformer 引入的 Self-Attention 讓序列中的每個位置關注所有其他位置。與 RNN 不同，這允許：

- **並行計算**：不需要逐步遞迴
- **全域視野**：一步到位看到完整序列
- **遠程依賴**：O(1) 路徑長度捕獲長距離關係

## 多頭注意力的直觀理解

多頭注意力讓模型「同時從不同角度理解序列」：

```python
class MultiHeadAttention:
    def __init__(self, d_model=512, n_heads=8):
        self.d_k = d_model // n_heads
        # 每個頭有不同的投影權重
        self.W_q = [random(d_model, self.d_k) for _ in range(n_heads)]
        self.W_k = [random(d_model, self.d_k) for _ in range(n_heads)]
        self.W_v = [random(d_model, self.d_k) for _ in range(n_heads)]

    def forward(self, x):
        heads = []
        for h in range(self.n_heads):
            Q = x @ self.W_q[h]  # 頭 1: 關注語法
            K = x @ self.W_k[h]  # 頭 2: 關注語義
            V = x @ self.W_v[h]  # 頭 3: 關注位置 ...
            scores = Q @ K.T / sqrt(self.d_k)
            heads.append(softmax(scores) @ V)
        return concat(heads) @ W_o  # 混合所有頭的資訊
```

每個頭學習不同的關注模式：
- 某些頭關注語法關係（主詞-動詞）
- 某些頭關注位置鄰近性
- 某些頭關注語義相似性

## 注意力遮罩

實務中需要三種遮罩控制注意力範圍：

**Padding Mask** — 忽略填充的 [PAD] token：
```
原始序列: ["我", "愛", "AI", [PAD], [PAD]]
注意力權重:
 我   愛   AI   [PAD] [PAD]
[1.0, 0.0, 0.0, -inf, -inf]  ← "我" 不看 [PAD]
[0.0, 1.0, 0.0, -inf, -inf]  ← "愛" 不看 [PAD]
```

**Causal Mask**（因果遮罩）— 防止看到未來 token：
```
 我   愛   AI
[1,   -inf, -inf]  ← "我" 只看自己
[0.3, 0.7, -inf]  ← "愛" 看 "我" 和 "愛"
[0.2, 0.3, 0.5]   ← "AI" 看全部
```

## Flash Attention 高效實作

傳統注意力需要將完整的 N×N 注意力矩陣存入 HBM（高頻寬記憶體），對長序列（N > 4096）極不友好。

Flash Attention（2022, Dao et al.）的關鍵洞察：**不要計算完整的注意力矩陣**。透過 tiling 和 recomputation：

```
傳統方式：
計算 QK^T (N×N) → 寫入 HBM → 讀取 → softmax → 寫入 HBM → 讀取 → ×V

Flash Attention：
將 Q、K、V 分塊載入 SRAM → 區塊內計算注意力 → 逐步合併結果
```

這將注意力計算的記憶體讀寫從 O(N²) 降為 O(N)，在長序列上獲得 2-4 倍加速。

2025-2026 年，Flash Attention 已成為所有 LLM 推論/訓練框架的標準元件，支援長達百萬 token 的上下文。

---

## 延伸閱讀

- [Bahdanau Attention 原始論文](https://www.google.com/search?q=Neural+Machine+Translation+by+Jointly+Learning+to+Align+and+Translate)
- [The Illustrated Transformer](https://www.google.com/search?q=illustrated+transformer+attention+visualization)
- [Flash Attention 論文](https://www.google.com/search?q=Flash+Attention+Fast+and+Memory-Efficient+Exact+Attention)
- [注意力可視化工具](https://www.google.com/search?q=bertviz+attention+visualization+tool)

---

*AI 程式人雜誌 2026 年 7 月號 — 大型語言模型實戰*
