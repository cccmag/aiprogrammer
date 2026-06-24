# 注意力機制的興起

## 2015 年的革命性創新

2015 年，Bahdanau、Cho 和 Bengio 發表了論文《Neural Machine Translation by Jointly Learning to Align and Translate》，提出了注意力機制（Attention Mechanism）。這是深度學習領域最重要的突破之一，不僅解決了 Seq2Seq 的瓶頸問題，還為後來 Transformer 的誕生奠定了基礎。

注意力機制的核心思想：**在解碼的每個時間步，讓模型能夠「關注」輸入序列的不同部分，而不是僅依賴單一的語義向量**。

---

## 為什麼需要注意力？

### Seq2Seq 的瓶頸

傳統 Seq2Seq 模型將整個輸入序列編碼為單個向量：

```
問題：所有資訊必須壓縮到固定維度的向量中

輸入序列越長，需要壓縮的資訊越多
→ 早期資訊被稀釋
→ 長期依賴難以捕捉
→ 翻譯品質下降
```

```
BLEU 分數 vs 句子長度關係：

長度  | 傳統 Seq2Seq | + Attention
-----|-------------|------------
< 10 |    32.5     |   33.1
10-20|    28.3     |   31.8
20-30|    24.1     |   30.2
30-40|    20.5     |   29.1
> 40 |    17.2     |   28.4
```

注意力機制在長序列上效果顯著。

### 人類翻譯的啟示

人類譯者在翻譯時：
1. 不會記憶整個句子
2. 會來回查看原文的各個部分
3. 根據當前翻譯位置動態調整關注點

注意力機制正是模擬了這個過程。

---

## 注意力機制的原理

### 架構圖

```
┌─────────────────────────────────────────────────────┐
│                 Attention 機制                       │
├─────────────────────────────────────────────────────┤
│                                                     │
│   Encoder 隱藏狀態:  h1   h2   h3   h4   h5         │
│                           │                         │
│                    ┌──────┴──────┐                  │
│                    │   Attention │                  │
│                    │   計算      │                  │
│                    └──────┬──────┘                  │
│                           │                         │
│              ┌────────────┼────────────┐            │
│              │            │            │            │
│              ▼            ▼            ▼            │
│           α1           α2           α3             │
│           (0.1)        (0.6)        (0.3)          │
│              │            │            │            │
│              └────────────┼────────────┘            │
│                           │                         │
│                           ▼                         │
│                   上下文向量 c                       │
│                   = Σ α_i * h_i                     │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### 計算步驟

**1. 計算注意力分數**

對於解碼器的每個時間步 t，計算與每個編碼器隱藏狀態的相關性：

```python
score(h_t, h_s) = v^T * tanh(W * [h_t; h_s])

# 其中：
# h_t: 解碼器當前隱藏狀態
# h_s: 編碼器第 s 個隱藏狀態
# v, W: 可學習參數
```

**2. 計算注意力權重**

使用 Softmax 將分數轉換為機率分佈：

```python
alpha_t = softmax(score_t)
# alpha_t[s] = exp(score[h_t, h_s]) / Σ exp(score[h_t, h_s'])
```

**3. 計算上下文向量**

用注意力權重加權平均編碼器隱藏狀態：

```python
c_t = Σ_s alpha_t[s] * h_s
```

**4. 組合上下文向量**

將上下文向量與解碼器隱藏狀態結合：

```python
# 方法 1：拼接
h_t_combined = tanh(W * [c_t; h_t])

# 方法 2：殘差連接
h_t_combined = h_t + c_t
```

---

## 注意力機制的變體

### 加性注意力（Additive Attention）

原始論文使用的方式：

```python
score(h_t, h_s) = v^T * tanh(W * [h_t; h_s])
```

適用場景：小型模型，輸入維度較低。

### 點積注意力（Multiplicative Attention）

使用點積計算相似度：

```python
score(h_t, h_s) = h_t^T * h_s
# 或縮放版本
score(h_t, h_s) = (h_t^T * h_s) / √d
```

優點：可以利用矩陣乘法高效計算。

### 雙線性注意力（Bilinear Attention）

使用雙線性變換：

```python
score(h_t, h_s) = h_t^T * W * h_s
```

適用場景：需要學習特定的對齊關係。

---

## 注意力視覺化

注意力機制的一個重要優勢是**可解釋性**：我們可以直觀看到模型在生成每個輸出時「關注」了輸入的哪些部分。

### 機器翻譯例子

```
英文: The   cat   sat   on   the   mat   .
德文: Die   Katze saß  auf  dem  Teppich .

注意力視覺化：
     Die    Katze    saß    auf    dem    Teppich
     ─────────────────────────────────────────────
The  ███░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
cat  ░░░░████████████░░░░░░░░░░░░░░░░░░░░
sat  ░░░░░░░░░████████████░░░░░░░░░░░░░░░
on   ░░░░░░░░░░░░░░████████████░░░░░░░░░░
the  ░░░░░░░░░░░░░░░░░░████████████░░░░░░
mat  ░░░░░░░░░░░░░░░░░░░░░░░██████████████
.    ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░

每個單詞的翻譯主要「關注」對應的源單詞
```

### 自注意力（Self-Attention）

自注意力是注意力機制的一個重要推廣：

```
自注意力：輸入序列關注自身

每個位置可以關注序列中的所有其他位置：
- 捕捉長距離依賴
- 發現詞與詞之間的語法/語義關係
```

### 多頭注意力（Multi-Head Attention）

並行使用多個注意力機制：

```python
# 多頭注意力
heads = []
for i in range(num_heads):
    head_i = attention(Q * W_i^Q, K * W_i^K, V * W_i^V)
    heads.append(head_i)

# 拼接所有頭的輸出
multi_head = concat(heads) * W^O
```

每個頭可以學習不同的注意力模式：
- 頭 1：語法關係
- 頭 2：語義關係
- 頭 3：共參照關係

---

## 注意力機制的影響

### 解決長序列問題

注意力機制使得模型能夠：
- 直接訪問序列中任意位置的資訊
- 不依賴於壓縮的語義向量
- 更好地處理長距離依賴

### 開啟 Transformer 時代

注意力機制最終導致了 Transformer 的誕生（2017）：

```
Transformer 架構：
- 完全基於注意力機制
- 拋棄 RNN 的循環結構
- 實現真正的平行計算
- 奠定現代 NLP 的基礎
```

### 跨領域應用

注意力機制被廣泛應用於：
- **影像處理**：CNN 特徵的注意力
- **語音辨識**：音頻 frames 的對齊
- **推薦系統**：用戶-物品交互
- **圖形神經網路**：節點之間的消息傳遞

---

## 延伸閱讀

- [注意力機制原始論文 2015](https://www.google.com/search?q=Bahdanau+attention+mechanism+2015)
- [Neural Machine Translation by Jointly Learning to Align and Translate](https://www.google.com/search?q=Neural+Machine+Translation+by+Jointly+Learning+to+Align+and+Translate)
- [注意力機制視覺化](https://www.google.com/search?q=attention+visualization+neural+machine+translation)

---

*本篇文章為「AI 程式人雜誌 2019 年 7 月號」循環神經網路系列之五。*