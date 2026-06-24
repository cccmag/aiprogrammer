# 注意力機制詳解

## Scaled Dot-Product Attention

### 機制原理

注意力機制允許模型在處理每個位置時，關注輸入序列的所有其他位置：

```
步驟：
1. 將輸入投影為 Q、K、V 三個矩陣
2. 計算 Q 和 K 的相似度
3. 通過 softmax 獲得權重
4. 將權重應用於 V
```

### 數學表達

```
Attention(Q, K, V) = softmax(QK^T / √d_k) × V
```

### 為何要縮放（Scaling）？

當維度較大時，點積的值可能會很大，導致 softmax 進入飽和區域。透過除以 √d_k 來控制。

## Multi-Head Attention

### 設計理念

將 Q、K、V 分別投影到多個子空間，並行計算注意力：

```
MultiHead(Q, K, V) = Concat(head₁, ..., headₕ) × W^O

其中 headᵢ = Attention(QW^Q_i, KW^K_i, VW^V_i)
```

### 優勢

1. **多視角**：每個頭可以關注不同的語義關係
2. **穩定性**：減少單一注意力機制的偏差
3. **表達力**：增加模型容量

## 自注意力（Self-Attention）

### 與傳統注意力的區別

- **傳統注意力**：兩種不同序列之間
- **自注意力**：同一序列內部

```python
# 自注意力的 Q、K、V 都來自同一輸入
Q = X × W_Q
K = X × W_K
V = X × W_V
```

---

## 延伸閱讀

- [注意力機制視覺化](https://www.google.com/search?q=attention+mechanism+visualization)
- [Multi-Head+Attention詳解](https://www.google.com/search?q=multi-head+attention+explained)
- [BERT+Attention+機制](https://www.google.com/search?q=BERT+self-attention)

*本篇文章為「AI 程式人雜誌 2021 年 1 月號」精選文章。*