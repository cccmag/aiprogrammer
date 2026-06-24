# 自我注意力 Self-Attention

## 從 RNN 到 Transformer

在 Transformer 出現之前，序列建模的主流方法是 RNN（LSTM/GRU）及其雙向變體。RNN 雖然能夠捕捉序列依賴關係，但有兩個根本限制：

1. **順序計算**：RNN 必須按時間步依次計算，無法並行化
2. **長距離衰減**：隨著序列增長，梯度容易消失或爆炸

2017 年，Vaswani 等人發表的《Attention Is All You Need》徹底改變了這一切。他們提出的 Transformer 架構完全拋棄了 RNN，僅依靠 Self-Attention 和位置編碼來建模序列。論文的標題本身就是一個宣言——「只需要注意力就夠了」。

## Query-Key-Value 機制

Self-Attention 的核心是 Query-Key-Value（QKV）機制，這個概念來自資訊檢索系統。

### 類比：圖書館檢索

想像你去圖書館找書：
- **Query（查詢）**：你的問題或需求
- **Key（鍵）**：每本書的標籤或索引
- **Value（值）**：書本身的內容

圖書館管理員的工作是：將你的查詢與所有書的索引進行比對，找到最相關的書，然後返回這些書的內容。

Self-Attention 的工作原理完全相同：
- 每個位置的 Query 與所有位置的 Key 進行比對
- 根據比對分數（注意力權重）加權聚合所有位置的 Value

### 數學公式

對於輸入序列 X = [x₁, x₂, ..., xₙ]，Self-Attention 的計算過程如下：

```
Q = X W_q          # 查詢矩陣
K = X W_k          # 鍵矩陣
V = X W_v          # 值矩陣

Attention(Q, K, V) = softmax(Q K^T / √d_k) V
```

其中 W_q、W_k、W_v 是可學習的參數矩陣，d_k 是 Key 的維度。

## 縮放點積注意力

### 為什麼需要縮放？

標準點積注意力的計算為 `softmax(Q K^T) V`。這裡有一個數值穩定性問題：當 d_k 很大時，點積 Q K^T 的元素會變得非常大，導致 softmax 進入梯度極小的區域（softmax 的尾部）。

舉例來說，如果 d_k = 512，Q 和 K 的每個元素是均值 0 方差 1 的隨機變量，那麼點積的方差約為 d_k = 512，標準差約為 22.6。這意味著很多點積值會落在 [-50, 50] 範圍內，softmax 會產生極接近 one-hot 的權重分佈，梯度幾乎為零。

**解決方案**：將點積除以 √d_k，使方差恢復到 1。

```
Attention(Q, K, V) = softmax(Q K^T / √d_k) V
```

### 並行計算優勢

與 RNN 不同，Self-Attention 可以一次性計算所有位置之間的關係：

```
Softmax(Q K^T / √d_k)       ┌─── value_1 ──┐
┌────────────────────┐      │               │
│ w₁₁ w₁₂ ... w₁ₙ   │      │ value_2       │
│ w₂₁ w₂₂ ... w₂ₙ   │  @   │  ...          │
│  ...  ...         │      │ value_n       │
│ wₙ₁ wₙ₂ ... wₙₙ   │      └───────────────┘
└────────────────────┘
```

這意味著所有的注意力權重和加權求和都可以用高效的矩陣乘法一次性完成。

## Multi-Head Attention

單純的 Self-Attention 只能在一種表示空間中捕捉關係。為了讓模型能夠學習不同類型的關係，Transformer 引入了 Multi-Head Attention：

```
MultiHead(Q, K, V) = Concat(head₁, ..., headₕ) W_o
headᵢ = Attention(Q W_qⁱ, K W_kⁱ, V W_vⁱ)
```

每個頭（Head）在不同的投影空間中學習注意力模式。例如，在語言模型中：
- 一個頭可能關注語法關係
- 另一個頭可能關注語義相似性
- 又一個頭可能關注位置資訊

### 視覺化 Multi-Head 注意力

```
輸入 ──┬──► Head 1: 語法關係
       ├──► Head 2: 語義相似性
       ├──► Head 3: 位置資訊
       └──► Head 4: 共指解析
            │
            ▼
         Concat + 線性投影
            │
            ▼
         輸出
```

## Self-Attention 的特性總結

### 優點

- **並行計算**：不依賴時間步，適合 GPU 加速
- **長距離依賴**：任意兩個位置之間的關係只需要一次計算
- **多模式學習**：Multi-Head 可在不同子空間學習不同模式
- **可解釋性**：注意力權重直觀反映了模型關注的位置

### 缺點

- **計算複雜度 O(n²)**：對長序列不友好
- **無位置感知**：需要額外的位置編碼
- **記憶體消耗大**：需要儲存 n×n 的注意力矩陣

---

**延伸閱讀**
- [Vaswani 2017: Attention Is All You Need](https://www.google.com/search?q=Attention+Is+All+You+Need+2017)
- [Transformer 架構詳解](https://www.google.com/search?q=transformer+architecture+explained)
- [Multi-Head Attention 可視化](https://www.google.com/search?q=multi+head+attention+visualization+bert)
