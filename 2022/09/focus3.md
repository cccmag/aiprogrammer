# Luong Attention（乘法注意力）

## 回顧 Bahdanau 的侷限

Bahdanau 的加法注意力雖然效果顯著，但它有一個實際問題：計算效率不高。每個對齊分數的計算都需要一個非線性變換（tanh）和兩次矩陣乘法。這在解碼器需要對長序列中每個位置進行計算時，會導致顯著的計算開銷。

```
score(h_t, h_s) = v^T tanh(W_q h_t + W_k h_s)
                             ↑      ↑
                        兩個矩陣乘法 + 非線性激活
```

2015 年，Luong、Pham 與 Manning 在論文《Effective Approaches to Attention-based Neural Machine Translation》中提出了更簡潔、更高效的注意力變體——Luong Attention（也稱為「乘法注意力」或 Multiplicative Attention）。

## 全域與區域注意力

Luong 等人提出了兩種注意力模式：

### 全域注意力（Global Attention）

全域注意力計算時考慮編碼器的所有隱藏狀態，與 Bahdanau 類似。但 Luong 提出了更簡單的評分函數。

### 區域注意力（Local Attention）

區域注意力只在編碼器輸出的一個子集上計算注意力。這是在計算效率和注意力品質之間的權衡：

- **Local-m**：以當前解碼位置為中心，預測一個固定的對齊窗口
- **Local-p**：預測一個對齊位置和窗口寬度，使用高斯分佈給窗口內的位置加權

區域注意力解決了全域注意力的 O(T) 計算問題（其中 T 是輸入序列長度），將複雜度降低到 O(2W)，其中 W 是窗口大小。

## 三種評分函數

Luong 提出了三種計算注意力分數的方法：

### 1. Dot（點積）

```
score(h_t, h_s) = h_t^T · h_s
```

最簡單的評分方式。不需要任何參數，直接計算兩個隱藏狀態的點積。點積的幾何意義是測量兩個向量在方向上的相似程度。

### 2. General（通用）

```
score(h_t, h_s) = h_t^T · W · h_s
```

在點積的基礎上加入一個可學習的權重矩陣 W，增加模型的表達能力。W 的作用是將查詢向量投影到與鍵向量相容的空間。

### 3. Concat（拼接）

```
score(h_t, h_s) = v^T tanh(W [h_t; h_s])
```

類似於 Bahdanau 的方法，但簡化了計算過程。這個方法在概念上與 Bahdanau Attention 最接近。

## 與 Bahdanau 的對比

### 計算效率

Luong 的 Dot 方法具有明顯的計算優勢：

| 方法 | 參數量 | 計算開銷 | 表現 |
|------|-------|---------|------|
| Bahdanau | 3 個權重矩陣 | 高 (tanh) | 好 |
| Luong Dot | 0 個參數 | 極低 | 中等 |
| Luong General | 1 個權重矩陣 | 低 | 好 |
| Luong Concat | 2 個權重矩陣 | 中等 | 好 |

### 架構差異

Luong Attention 與 Bahdanau 的另一個重要區別在於上下文向量的使用方式：

- **Bahdanau**：上下文向量直接影響解碼器的隱藏狀態計算（與 RNN 隱藏狀態拼接）
- **Luong**：上下文向量在計算出解碼器隱藏狀態之後才被合併（通過一個輸出層）

```
Bahdanau: [h_{t-1}, c_t] → GRU → h_t
Luong:    h_t → [h_t, c_t] → tanh(W_c [h_t; c_t]) → 預測
```

這使得 Luong 的架構更簡潔，且易於與不同的 RNN 單元組合使用。

## 實驗結果與分析

Luong 在論文中報告的實驗結果顯示：

1. Dot 方法在品質上與 Bahdanau 相當，但計算速度快得多
2. General 方法在大部分語言對上略微優於 Dot
3. 區域注意力在計算效率上遠超全域注意力，而品質下降極小（甚至在某些語料上更好）
4. Luong Attention 的一個實用優勢是它對解碼器的設計限制更少

## 歷史意義

Luong Attention 的重要貢獻不僅是提供了一種更高效的注意力計算方法，更重要的是它系統地比較了不同注意力機制的變體。這種系統化的實驗方法幫助研究社區更好地理解注意力機制的設計空間。

Dot 注意力的簡潔性尤其重要——它直接啟發了後來 Transformer 中的「縮放點積注意力」（Scaled Dot-Product Attention）。如果說 Bahdanau 是注意力機制的「發現者」，那麼 Luong 就是注意力機制的「系統化者」，而 Transformer 則是注意力機制的「革命者」。

---

**延伸閱讀**
- [Luong 2015: Effective Approaches to Attention-based NMT](https://www.google.com/search?q=Luong+attention+2015)
- [區域注意力機制](https://www.google.com/search?q=local+attention+mechanism)
- [點積注意力與縮放因子](https://www.google.com/search?q=scaled+dot+product+attention+transformer)
