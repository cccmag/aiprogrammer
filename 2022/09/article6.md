# 相對位置編碼

## 為什麼需要位置編碼？

Self-Attention 本質上是「置換等變」（permutation equivariant）的——如果我們打亂輸入序列的順序，輸出也會以相同的方式打亂。這是一個重要的性質，但對於序列建模來說，這也意味著 Self-Attention 完全失去了對位置資訊的感知。

換句話說，「我愛你」和「你愛我」在 Self-Attention 中的表示是相同的。

為了解決這個問題，Transformer 引入了位置編碼（Positional Encoding），讓模型能夠感知 token 在序列中的位置。

## 絕對位置編碼

### 正弦餘弦編碼

原始 Transformer 使用固定頻率的正弦和餘弦函數來編碼位置：

```
PE(pos, 2i)   = sin(pos / 10000^{2i/d_model})
PE(pos, 2i+1) = cos(pos / 10000^{2i/d_model})
```

其中 pos 是位置，i 是維度索引，d_model 是模型維度。

這種設計的優點：
- **無需學習**：不需要額外的參數
- **值域固定**：輸出始終在 [-1, 1] 範圍內
- **外推能力**：可以處理比訓練時更長的序列

### 可學習的位置編碼

BERT 使用可學習的位置嵌入（Positional Embedding），將每個位置映射為一個可訓練的向量：

```
PositionEmbedding(pos) = Embedding[pos]
```

這種方法的優點是可以透過訓練資料自適應地學習位置表示。缺點是無法處理比訓練時更長的序列。

## 相對位置編碼的動機

### 絕對位置的不足

絕對位置編碼假設模型需要知道 token 的「絕對位置」，但對於許多任務來說，真正重要的是 token 之間的「相對距離」。

例如，在語法分析中，動詞和它的賓語之間的距離（無論是 2 個詞還是 10 個詞）比它們的絕對位置更重要。

### 相對位置的優勢

相對位置編碼（Shaw 等人，2018）的關鍵洞見是：注意力應該基於位置之間的距離，而不是絕對位置。

```
「我喜歡吃蘋果」
   距離 2   距離 1
```

「喜歡」與「蘋果」的注意力計算應該基於距離 2，而不是它們的絕對位置 1 和 3。

## 相對位置編碼的實現

### Shaw 的方法（2018）

Shaw 的方法在注意力計算中引入了可學習的相對位置嵌入：

```
score(i, j) = (x_i W_q) (x_j W_k + a_{ij}^K)^T
```

其中 a_{ij}^K 是位置 i 和 j 之間的相對位置嵌入。

這種方法需要學習 2K+1 個嵌入向量（K 是最大截斷距離），對於超出範圍的距離，使用最近的嵌入。

### Transformer XL 的方法（2019）

Transformer XL 提出了一個更優雅的形式，將位置編碼完全轉化為相對形式：

```
score(i, j) = q_i^T k_j + q_i^T R_{i-j} W_k + u^T k_j + v^T R_{i-j} W_k
```

其中：
- q_i^T k_j：基於內容的注意力
- q_i^T R_{i-j} W_k：基於內容和位置的注意力
- u^T k_j：全域內容偏差
- v^T R_{i-j} W_k：全域位置偏差

R_{i-j} 是正弦編碼的相對位置矩陣。

### RoPE（ Rotary Position Embedding，2021）

RoPE 是目前最流行的相對位置編碼方法之一，被 Llama、Mistral 等模型採用。

RoPE 的核心思想是：對 Query 和 Key 進行旋轉變換，使得它們的點積自動編碼相對位置資訊。

```
f_q(x_m, m) = R_m W_q x_m
f_k(x_n, n) = R_n W_k x_n

score(m, n) = f_q(x_m, m)^T f_k(x_n, n)
           = (W_q x_m)^T R_{n-m} (W_k x_n)
```

其中 R_m 是旋轉矩陣。RoPE 的優點：
- 相對位置自然編碼在點積中
- 可以外推到更長的序列
- 支援線性注意力變體

### ALiBi（2022）

ALiBi（Attention with Linear Biases）提供了一個極簡的相對位置編碼方案：在注意力分數上直接加一個與距離成線性關係的偏置項：

```
score(i, j) = q_i k_j^T - m × |i - j|
```

其中 m 是每個注意力頭專屬的斜率參數。

ALiBi 的驚人之處在於：它不需要任何可學習的位置參數，也不需要位置嵌入，但在長序列任務上表現優異。

## 各種位置編碼的比較

| 方法 | 參數 | 外推能力 | 計算開銷 | 代表模型 |
|------|------|---------|---------|---------|
| 正弦編碼 | 0 | 好 | 低 | 原始 Transformer |
| 可學習嵌入 | O(n·d) | 無 | 低 | BERT |
| 相對編碼 | O(K·d) | 中等 | 中 | T5 |
| Transformer XL | O(K·d) | 好 | 中 | Transformer XL |
| RoPE | 0 | 好 | 低 | Llama, Mistral |
| ALiBi | h | 極好 | 極低 | BLOOM, MPT |

## 結論

位置編碼的演變反映了學界對序列建模理解的深化：從絕對位置到相對位置，從固定函數到可學習參數，從複雜的嵌入到簡單的偏置項。RoPE 和 ALiBi 的流行表明，簡單而優雅的設計往往經得起時間的考驗。

---

**延伸閱讀**
- [Shaw 2018: Self-Attention with Relative Position Representations](https://www.google.com/search?q=relative+position+encoding+shaw+2018)
- [Transformer XL: Segment-Level Recurrence](https://www.google.com/search?q=transformer+xl+relative+position)
- [RoPE: Rotary Position Embedding](https://www.google.com/search?q=RoPE+rotary+position+embedding+2021)
