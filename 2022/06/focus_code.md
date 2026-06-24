# 程式碼說明 — focus_code.md

## 概述

本期的範例程式碼位於 `_code/transformer.py`，使用純 Python 與 NumPy 從頭實作 Transformer 的核心元件。無需任何深度學習框架即可執行，適合教學與學習目的。程式碼以可讀性為導向，每一行都對應到論文中的數學公式。

## 元件說明

### `scaled_dot_product_attention(Q, K, V, mask)`

實作縮放點積注意力。計算步驟為：Q 與 K 的點積得到相似度分數，除以 sqrt(d_k) 進行縮放，應用 softmax 得到注意力權重，最後用權重加權求和 V。可選參數 mask 支援 causal mask 和 padding mask，遮罩位置設為 -inf 使其 softmax 後權重歸零。

### `PositionalEncoding`

使用 sin/cos 三角函數產生固定頻率的位置編碼。偶數維度使用 sin 函數，奇數維度使用 cos 函數。不同維度對應不同頻率。此類別預先計算好位置編碼矩陣，forward 時直接與輸入相加，支援任意序列長度。

### `MultiHeadAttention`

實作多頭注意力機制。先將 Q、K、V 分別透過線性變換投影到 h 個子空間，然後每個頭獨立計算縮放點積注意力，最後將 h 個頭的輸出拼接並透過輸出投影矩陣融合。實際運算中透過 reshape 和 transpose 將所有頭的計算批次化，提高效率。

### `FeedForward`

兩層線性變換的位置式前饋網路。公式為 FFN(x) = x W_1 W_2 + b_2（省略了激活函數的實作以保持簡潔）。

### `layer_norm`

實現標準的 Layer Normalization。對每個樣本的特徵維度計算均值和變異數，進行歸一化後再使用可學習的縮放參數。

### `TransformerBlock`

單一 Transformer 編碼器區塊。先計算多頭自注意力並進行殘差連接與 Layer Norm，然後計算前饋網路並再次殘差連接與 Layer Norm。這是 Transformer 編碼器的基本單元。

## 執行程式

```bash
cd _code
bash test.sh
```

`test.sh` 使用 `set -x` 顯示執行過程並呼叫 `python3 transformer.py`。`demo()` 函式展示完整資料流：隨機輸入經位置編碼、Transformer 區塊處理、最後輸出，展示各元件的正確運作。

## 參考資源

- NumPy 官方文件：https://www.google.com/search?q=numpy+python+library
- Transformer 從零實作：https://www.google.com/search?q=transformer+numpy+implementation
