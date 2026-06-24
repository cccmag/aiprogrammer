# GPT-3 的架構與訓練

## Transformer 架構回顧

### Attention 機制

GPT-3 基於 Transformer 的解碼器（Decoder-only）架構：

```
Attention(Q, K, V) = softmax(QK^T / √d) V
```

- Q（Query）：當前詞的查詢向量
- K（Key）：所有詞的鍵向量
- V（Value）：所有詞的值向量

### GPT-3 的具體架構

| 參數 | 數值 |
|------|------|
| 層數 | 96 |
| 隱藏維度 | 12288 |
| 注意力頭數 | 96 |
| 每頭維度 | 128 |
| 總參數 | 1750 億 |

### 與 GPT-2 的比較

| 參數 | GPT-2 | GPT-3 |
|------|-------|-------|
| 層數 | 48 | 96 |
| 隱藏維度 | 1600 | 12288 |
| 注意力頭 | 25 | 96 |
| 上下文長度 | 1024 | 2048 |

---

## 訓練方法

### 自回歸語言建模

GPT-3 使用標準的自回歸目標：

```
L = -Σ log P(w_t | w_{<t})
```

預測下一個詞，最大化似然。

### 訓練資料

| 資料來源 | 佔比 |
|---------|------|
| Common Crawl | 60% |
| WebText2 | 22% |
| Books1 | 8% |
| Books2 | 8% |
| Wikipedia | 3% |

### 訓練成本

- 預計需要 **3.14 × 10^23 FLOPs**
- 在 A100 GPU 上約需 355 年
- 實際使用了數千個 GPU 進行訓練

---

## 稀疏注意力

### 為何需要稀疏注意力？

全注意力機制的複雜度是 O(n²)，對於長輸入來說不可行。

### GPT-3 的策略

採用 **稀疏注意力**（Sparse Attention）：

- 每個 token 只關注局部窗口內的 token
- 減少計算複雜度
- 保持大部分注意力能力

### 改進方向

2020 年的研究開始探索更高效的注意力機制：

- **Linformer**：線性複雜度注意力
- **Reformer**：局部敏感哈希
- **Longformer**：Longformer 的滑動窗口注意力

---

## 模型評估

### Benchmark 結果

GPT-3 在多個 benchmark 上達到或超過 SOTA：

| 任務 | 微調 SOTA | GPT-3 Few-shot |
|------|----------|---------------|
| SuperGLUE | 89.0 | 87.5 |
| LAMBADA | 86.4 | 86.4 |
| TriviaQA | 68.9 | 71.2 |

### GPT-3 的優勢

1. **無需微調**：直接在各任務上評估
2. **通用性**：同一模型處理多種任務
3. **持續學習**：可透過 prompt 持續適應

---

**下一步**：[GPT-3 的應用場景](focus5.md)

## 延伸閱讀

- [GPT-3+architecture+details](https://www.google.com/search?q=GPT-3+architecture+Transformer+175B+parameters)
- [sparse+attention+transformer](https://www.google.com/search?q=sparse+attention+transformer+efficiency+2020)
- [Transformer+training+compute](https://www.google.com/search?q=Transformer+training+compute+requirements+175B)