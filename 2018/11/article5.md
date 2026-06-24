# Transformer 架構解析

## 總覽

Transformer 由 Google 在 2017 年提出，完全基於注意力機制，拋棄了 RNN 的循環結構。它在機器翻譯任務上刷新了紀錄，後來成為幾乎所有大型語言模型的基礎架構。

## 架構組成

### Encoder 部分
- N 個相同的 Transformer Encoder 層堆疊
- 每層包含：Multi-Head Self-Attention + Position-wise Feed-Forward
- 每個子層都有残差連接與 Layer Normalization

### Decoder 部分
- N 個相同的 Transformer Decoder 層堆疊
- 每層包含：Masked Self-Attention + Encoder-Decoder Attention + Feed-Forward
- 確保訓練時只看見當前位置之前的輸出

## Self-Attention 詳解

Transformer 的 Self-Attention 將輸入序列的每個位置映射為 Q、K、V 三個向量：

```python
Q = X @ W_Q
K = X @ W_K
V = X @ W_V
```

注意力計算：
```python
Attention(Q, K, V) = softmax(Q @ K.T / sqrt(d_k)) @ V
```

## Multi-Head Attention

將 Q、K、V 投影到多個子空間，每個頭獨立計算注意力：
```
MultiHead(Q, K, V) = Concat(head_1, ..., head_h) @ W_O

head_i = Attention(Q @ W_i_Q, K @ W_i_K, V @ W_i_V)
```

這樣每個頭可以關注不同類型的資訊。

## 位置編碼

Transformer 本身不處理序列順序，需要額外加入位置編碼：
```python
PE(pos, 2i) = sin(pos / 10000^(2i/d_model))
PE(pos, 2i+1) = cos(pos / 10000^(2i/d_model))
```

位置編碼與輸入嵌入相加，讓模型能夠區分不同位置的詞。

## Feed-Forward 網路

每層還包含一個前饋網路：
```
FFN(x) = max(0, x @ W_1 + b_1) @ W_2 + b_2
```
這是一個兩層的全連接網路，使用 ReLU 激活。

## Layer Normalization 與残差連接

每個子層的輸出：
```
Output = LayerNorm(x + Sublayer(x))
```
残差連接幫助梯度流動，Layer Normalization 穩定訓練。

## 與 RNN 的比較

| 特性 | Transformer | RNN |
|------|-------------|-----|
| 計算順序 | 完全平行 | 順序依賴 |
| 路徑長度 | O(1) | O(n) |
| 長距離依賴 | 直接建模 | 需要門控 |
| 記憶體需求 | O(n²) 注意力 | O(n) |

## 參考資源

- https://www.google.com/search?q=Transformer+架構+詳解+Encoder+Decoder+Self-Attention+原理
- https://www.google.com/search?q=positional+encoding+位置編碼+Transformer+為何需要+方法
- https://www.google.com/search?q=Transformer+vs+RNN+比較+優勢+劣勢+何時使用