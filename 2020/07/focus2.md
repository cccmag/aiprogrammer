# Few-shot Learning：從頭訓練到提示學習

## 傳統監督學習的局限

### 傳統方法的問題

在深度學習的早期階段，訓練一個模型需要：

1. **大量標記資料**：通常需要數萬到數百萬筆標記範例
2. **漫長的訓練過程**：每個新任務都需要從頭訓練
3. **任務特定的架構**：不同任務需要不同的模型設計

這對於许多實際應用來說是不可行的。

### Transfer Learning 的興起

2010 年代中期，Transfer Learning 成為主流：

1. **預訓練階段**：在大規模無標記資料上預訓練語言模型
2. **微調階段**：在特定任務的少量標記資料上進行調整

這大幅減少了任務所需的標記資料數量。

### GPT-1 的貢獻

GPT-1（2018）展示了：
- 使用 BooksCorpus 資料集（7000 本書）
- 預訓練語言模型
- 在下游任務上進行微調

但 GPT-1 仍需要任務特定的微調。

---

## Few-shot、One-shot、Zero-shot

### GPT-3 的創新

GPT-3 採用了完全不同的方法：**完全不進行微調**

模型只需要在輸入中看到少量範例，就能完成任務：

```
輸入格式：
[範例1]
[範例2]
[範例3]
[測試輸入]

模型輸出：預測結果
```

### 三種學習方式的比較

| 方式 | 說明 | 需要的資料量 |
|------|------|------------|
| Few-shot | 提供少量範例（通常 10-100） | K 個範例 |
| One-shot | 提供一個範例 | 1 個範例 |
| Zero-shot | 不提供範例，只提供任務描述 | 0 個範例 |

### GPT-3 的實驗結果

在 LAMBADA 資料集上：

| 方式 | 準確率 |
|------|--------|
| SOTA（微調） | 86.4% |
| GPT-3 Few-shot | 86.4% |
| GPT-3 One-shot | 76.2% |
| GPT-3 Zero-shot | 72.5% |

GPT-3 的 Few-shot 結果與最好的微調方法相當！

### 為何有效？

理論上猜測：

1. **大量知識儲存**：模型在預訓練中學習了語言模式和世界知識
2. **情境理解**：模型學會從範例中推斷任務意圖
3. **通用表示**：Transformer 架構提供了靈活的金鑰-值記憶

---

## In-context Learning 原理

### 機制解釋

「情境學習」（In-context Learning）是 GPT-3 的核心能力：

1. **注意範例**：模型會關注輸入中的所有範例
2. **Pattern Matching**：學習輸入與輸出之間的模式
3. **任務推理**：從少量範例中推斷出任務規則

### 與傳統 ML 的比較

```
傳統 ML：
  模型引數 <- 學習（梯度下降）
  輸入 -> 模型 -> 輸出

GPT-3 In-context Learning：
  範例 + 輸入 -> 語言模型 -> 輸出
```

---

**下一步**：[Prompt Engineering：引導語言模型的新方法](focus3.md)

## 延伸閱讀

- [Few-shot+Learning+GPT-3](https://www.google.com/search?q=few-shot+learning+GPT-3+in-context+learning)
- [Prompt+Engineering+guide+2020](https://www.google.com/search?q=prompt+engineering+language+models+2020)
- [One-shot+Zero-shot+learning+NLP](https://www.google.com/search?q=one-shot+zero-shot+learning+NLP+transformer)