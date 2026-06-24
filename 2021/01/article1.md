# Transformer 架構回顧

## 從 RNN 到 Transformer

### RNN 的局限性

傳統的循環神經網路（RNN）存在以下問題：
- **順序處理**：無法平行計算
- **梯度消失**：長序列訓練困難
- **長期依賴**：難以捕捉遠距離關係

```
RNN 處理序列：
h₀ → h₁ → h₂ → h₃ → ...
  ↑    ↑    ↑    ↑
 x₀   x₁   x₂   x₃
```

### Transformer 的誕生

2017 年，Google 在論文《Attention is All You Need》中提出了 Transformer 架構，完全基於注意力機制，放棄了 RNN 的順序結構。

```
Transformer 核心：
輸入 → 編碼器堆疊 → 解碼器堆疊 → 輸出
          ↑              ↑
      自注意力        交叉注意力
```

## Transformer 的核心組件

### 編碼器（Encoder）

每個編碼器層包含：
1. **Multi-Head Self-Attention**
2. **前饋神經網路**
3. **殘差連接與層歸一化**

### 解碼器（Decoder）

每個解碼器層包含：
1. **Masked Self-Attention**（防止看到未來）
2. **Cross Attention**（關注編碼器輸出）
3. **前饋神經網路**

### 注意力機制的數學形式

```
Attention(Q, K, V) = softmax(QK^T / √d) × V

其中：
Q = 查詢矩陣（Query）
K = 鍵矩陣（Key）
V = 值矩陣（Value）
d = 維度（用於縮放）
```

## 為何 Transformer 有效？

1. **平行計算**：擺脫順序依賴
2. **長距離依賴**：直接計算任意位置的關聯
3. **可擴展性**：易於擴展到更大規模

---

## 延伸閱讀

- [Attention is All You Need 論文](https://www.google.com/search?q=Attention+is+All+You+Need+paper)
- [Transformer+架構圖解](https://www.google.com/search?q=transformer+architecture+visualized)
- [BERT+vs+GPT+比較](https://www.google.com/search?q=BERT+vs+GPT+architecture)

*本篇文章為「AI 程式人雜誌 2021 年 1 月號」精選文章。*