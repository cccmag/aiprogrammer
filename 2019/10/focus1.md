# BERT 的誕生與原理

## 前言

2018 年 10 月，Google AI Language 團隊發布了 BERT（Bidirectional Encoder Representations from Transformers），這款模型在自然語言處理領域掀起了革命。本篇文章將深入探討 BERT 的誕生背景、架構原理和訓練方式。

## BERT 的誕生背景

### NLP 的困境

在 BERT 出現之前，NLP 領域面臨著諸多挑戰：

1. **任務導向的模型設計**：每個 NLP 任務通常需要設計特定的模型架構
2. **資料不足**：大多數任務缺乏大規模的標註資料
3. **单向語言模型限制**：傳統的語言模型只能利用單一方向的上下文

### Transformer 的奠基

2017 年，Google 發表了《Attention Is All You Need》論文，提出了 Transformer 架構。Transformer 完全基於注意力機制，摒棄了傳統的 RNN 和 CNN。

Transformer 的關鍵創新是自注意力機制（Self-Attention），它允許模型同時關注序列中的所有位置：

```
輸入序列：The cat sat on the mat
                ↓
Self-Attention：每個 token 都可以關注所有其他 token
                ↓
輸出：融合了全局資訊的表示
```

## BERT 的核心架構

### 雙向 Transformer 編碼器

BERT 使用雙向 Transformer 編碼器，這是其與 GPT（單向）和 ELMo（淺層雙向）的根本區別：

```
GPT：← Transformer 解碼器（单向）
ELMo：→ 淺層雙向 LSTM
BERT：← Transformer 編碼器（雙向）→
```

### BERT 的輸入表示

BERT 的輸入採用獨特的表示方式：

```
[CLS] + 句子 A + [SEP] + 句子 B + [SEP]
```

每個 token 的表示是三個嵌入的組合：
- **Token Embedding**：詞嵌入
- **Segment Embedding**：句子嵌入（區分句子 A 和 B）
- **Position Embedding**：位置嵌入

### Masked Language Model（MLM）

BERT 的預訓練使用了一種創新的 Masked Language Model 目標：

```
輸入：The [MASK] is a pet animal
標籤：[MASK] → cat
```

訓練時隨機遮蔽約 15% 的 token，模型需要根據上下文預測被遮蔽的詞。這種方法允許模型學習雙向上下文表示。

### Next Sentence Prediction（NSP）

BERT 還使用了 Next Sentence Prediction 目標：

```
句子 A：The cat sat on the mat
句子 B：It looks comfortable
標籤：IsNext

句子 A：The cat sat on the mat
句子 B：Many people like pizza
標籤：NotNext
```

NSP 任務幫助 BERT 學習句子間的關係，對問答和自然語言推理等任務至關重要。

## BERT 的配置

Google 發布了多個 BERT 配置：

| 配置 | 層數 | 隱藏維度 | 注意力頭數 | 參數量 |
|------|------|----------|------------|--------|
| BERT BASE | 12 | 768 | 12 | 110M |
| BERT LARGE | 24 | 1024 | 16 | 340M |

## BERT 的預訓練過程

### 訓練資料

BERT 使用了兩個大型語料庫：
- **BooksCorpus**：8 億詞
- **English Wikipedia**：25 億詞

### 訓練細節

- **批次大小**：256 序列（256 × 512 tokens）
- **訓練步數**：1,000,000 步
- **學習率**：1e-4
- **遮蔽策略**：80% 替换為 [MASK]，10% 保持不變，10% 替换為隨機詞

## BERT 的突破

### 效能提升

BERT 在多個 NLP 基準測試中刷新紀錄：

- **GLUE**：從 72.8 提升至 80.2
- **SQuAD 1.1**：從 91.2 提升至 93.2
- **SQuAD 2.0**：從 86.5 提升至 89.5

### 通用性

BERT 的另一大貢獻是展示了預訓練模型的可遷移性。同一個預訓練模型可以透過微調來解決各種不同的 NLP 任務。

## 結論

BERT 的誕生標誌著 NLP 進入了預訓練時代。透過雙向 Transformer 編碼器、Masked Language Model 和 Next Sentence Prediction，BERT 學習了強大的語言表示，為後續的研究和應用奠定了基礎。

---

**延伸閱讀**

- [BERT: Pre-training of Deep Bidirectional Transformers](https://www.google.com/search?q=BERT+pre+training+deep+bidirectional+transformers+paper)
- [Google AI BERT](https://www.google.com/search?q=Google+AI+BERT+model)
- [Transformer 原始論文](https://www.google.com/search?q=Attention+is+All+You+Need+paper)