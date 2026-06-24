# 交叉注意力 Cross-Attention

## 什麼是 Cross-Attention？

Cross-Attention（交叉注意力）與 Self-Attention 的核心區別在於 Query 和 Key-Value 的來源：

- **Self-Attention**：Q、K、V 都來自同一個序列
- **Cross-Attention**：Q 來自一個序列，K 和 V 來自另一個序列

這種設計使得模型能夠在兩個不同的序列（或模態）之間建立對應關係。

```
Self-Attention:     Q ← X,  K ← X,  V ← X
Cross-Attention:    Q ← X,  K ← Y,  V ← Y
```

## 編碼器-解碼器注意力

### 在 Transformer 中的角色

在 Transformer 架構中，Cross-Attention 出現在解碼器的第二個子層。解碼器在每個解碼步驟使用 Cross-Attention 來關注編碼器的輸出：

```
Transformer 解碼器結構：

輸出序列 ──► Masked Self-Attention ──► 輸入嵌入
                     │
                     ▼
          Cross-Attention ◄──── 編碼器輸出
                     │
                     ▼
              Feed-Forward
                     │
                     ▼
                 預測結果
```

這個結構與傳統的 Bahdanau Attention 扮演著類似的角色——讓解碼器能夠動態地關注輸入序列的不同部分。

### 語音辨識中的應用

在語音辨識系統中，Cross-Attention 將聲學特徵序列（來自編碼器）與文字序列（來自解碼器）對齊：

- Q 來自解碼器對應的文字嵌入
- K、V 來自編碼器對應的聲學特徵

注意力權重矩陣顯示出明顯的對角線模式，對應著語音與文字之間的時間對齊關係。

## 多模態注意力

Cross-Attention 的真正威力體現在多模態學習中，它允許不同模態的資料在抽象層面進行交互。

### 文字到圖像生成（Stable Diffusion）

Stable Diffusion 使用 Cross-Attention 將文字提示與圖像特徵結合：

```
文字編碼器 ──► K, V
                  │
                  ▼
圖像特徵 ◄── Cross-Attention ◄── Q (來自圖像)
```

每個文字 token 的注意力權重決定了它在圖像生成過程中的影響力。當提示為「一隻坐在草地上的貓」時，「貓」和「草地」的注意力權重分別影響圖像中對應區域的生成。

### 視覺語言模型（CLIP）

CLIP 使用 Cross-Attention 在圖像特徵和文字特徵之間建立聯繫：

- 圖像編碼器輸出圖像 patch 的特徵序列
- 文字編碼器輸出文字 token 的特徵序列
- Cross-Attention 讓兩種特徵互相「關注」對方

這種雙向的注意力使得 CLIP 能夠學習到圖像-文字的聯合表示空間。

## Cross-Attention 的實現

```
def cross_attention(query, key, value, mask=None):
    """
    query: (batch, q_len, d_model)
    key:   (batch, k_len, d_model)
    value: (batch, k_len, d_model)
    """
    d_k = key.shape[-1]
    scores = query @ key.transpose(-2, -1) / sqrt(d_k)
    if mask is not None:
        scores = scores.masked_fill(mask == 0, -1e9)
    weights = softmax(scores, dim=-1)
    output = weights @ value
    return output, weights
```

### 注意力權重的形狀

在 Cross-Attention 中，注意力權重的形狀為 (q_len, k_len)：

```
      鍵序列位置
      k₁  k₂  k₃  k₄  k₅
q₁  [ 0.1 0.2 0.5 0.1 0.1 ]
q₂  [ 0.3 0.4 0.1 0.1 0.1 ]
q₃  [ 0.1 0.1 0.1 0.3 0.4 ]
```

每行對應一個查詢位置在所有鍵位置上的注意力分佈。對於機器翻譯，這通常形成一個近似對角線的模式。

## Cross-Attention 與 Self-Attention 的比較

| 特性 | Self-Attention | Cross-Attention |
|------|---------------|-----------------|
| Q、K、V 來源 | 同一個序列 | Q 和 K/V 來自不同序列 |
| 作用 | 捕捉序列內部關係 | 捕捉序列間關係 |
| 應用 | Transformer 編碼器 | Transformer 解碼器、多模態模型 |
| 權重特徵 | 對角線模式 | 跨域對應關係 |
| 序列長度 | 通常相等 | 可以不同 |

## 在擴散模型中的應用

現代擴散模型（如 Stable Diffusion、DALL-E）廣泛使用 Cross-Attention 來實現文字引導的圖像生成：

1. 文字提示通過 CLIP 文字編碼器轉換為 token 序列
2. 這些 token 序列作為 Cross-Attention 的 Key 和 Value
3. 圖像的 U-Net 特徵圖作為 Query
4. 模型在每個去噪步驟中，根據文字提示調整圖像生成方向

Cross-Attention 的權重還可以用來生成「注意力熱力圖」，顯示文字中每個詞對應的圖像區域，實現了零樣本的語義分割能力。

---

**延伸閱讀**
- [Stable Diffusion Cross-Attention](https://www.google.com/search?q=stable+diffusion+cross+attention)
- [CLIP 視覺語言模型](https://www.google.com/search?q=CLIP+contrastive+language+image+pretraining)
- [Transformer 解碼器 Cross-Attention](https://www.google.com/search?q=transformer+decoder+cross+attention)
