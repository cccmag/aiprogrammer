# Attention is All You Need

## 2017 年：深度學習的轉折點

### 歷史背景

2017 年 6 月，Google 發表了「Attention is All You Need」論文，提出了 Transformer 架構。這篇論文徹底改變了序列建類任務的處理方式。

### 論文核心

```python
# Attention(Q, K, V) = softmax(QK^T / √d_k) V
```

這一行公式，開啟了深度學習的新時代。

---

## 為何 Attention 如此重要？

### 傳統 RNN 的問題

| 問題 | 說明 |
|------|------|
| 梯度消失 | 長序列難以訓練 |
| 平行計算受限 | 必須順序處理 |
| 長距離依賴 | 難以捕捉遠距離關係 |

### Attention 的優勢

1. **直接連接**：任意位置可以直接互動
2. **平行計算**：矩陣運算可並行
3. **可解釋性**：可視化注意力權重

---

## Transformer 架構

### 整體結構

```
輸入
  -> 詞嵌入 + 位置編碼
  -> N × Encoder（自注意力 + 前饋網路）
  -> N × Decoder
      ├─ 自注意力（Masked）
      ├─ 編碼器-解碼器注意力
      └─ 前饋網路
  -> 輸出
```

### 核心元件

#### 1. 位置編碼（Positional Encoding）

```python
PE(pos, 2i) = sin(pos / 10000^(2i/d))
PE(pos, 2i+1) = cos(pos / 10000^(2i/d))
```

#### 2. 多頭注意力（Multi-Head Attention）

```python
MultiHead(Q, K, V) = Concat(head_1, ..., head_h) W^O
where head_i = Attention(QW_i^Q, KW_i^K, VW_i^V)
```

#### 3. 前饋網路

```python
FFN(x) = max(0, xW_1 + b_1) W_2 + b_2
```

---

## 訓練技巧

### 1. 殘差連接

每個子層都有：
```python
output = LayerNorm(x + Sublayer(x))
```

### 2. Label Smoothing

使用標籤平滑（soft targets）提高泛化能力。

### 3. Dropout

在每個子層輸出和嵌入層應用 dropout。

---

## 歷史意義

### 影響範圍

| 領域 | 應用 |
|------|------|
| NLP | 翻譯、生成、分類 |
| 視覺 | ViT、DETR |
| 音訊 | 語音辨識、合成 |
| 多模態 | CLIP、DALL-E |

### 開啟大型預訓練時代

Transformer 的可擴展性使其成為大型預訓練模型的基礎：
- BERT、GPT、T5 及其衍生
- 催生了數十億參數的模型

---

**下一步**：[BERT：雙向 Transformer 的崛起](focus2.md)

## 延伸閱讀

- [Attention is All You Need 原文](https://www.google.com/search?q=Attention+is+All+You+Need+paper+2017)
- [Transformer+architecture+tutorial](https://www.google.com/search?q=Transformer+architecture+tutorial+attention+2017)