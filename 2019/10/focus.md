# 本期焦點

## BERT 與預訓練語言模型的發展歷程

### 引言

2018 年 10 月，Google 發布了 BERT（Bidirectional Encoder Representations from Transformers），這是一款革命性的語言模型。2019 年 10 月，正當 BERT 迎來一週年之際，我們有必要回顧這項技術的發展歷程，以及它如何改變了自然語言處理（NLP）領域的格局。

從 Word2Vec 到 ELMo，從 BERT 到 GPT-2，語言模型的發展經歷了漫長的演進。預訓練技術的出現，讓我們能夠使用大量無標注文本資料來學習語言表示，然後針對特定任務進行微調。這種方法的出現徹底改變了 NLP 的研究和應用方式。

---

## 大綱

* [程式：Transformer 與注意力機制實作](focus_code.md)
   - Self-Attention 機制
   - 多頭注意力
   - Transformer 架構

1. [BERT 的誕生與原理](focus1.md)
   - Transformer 架構基礎
   - 雙向預訓練
   - Masked Language Model

2. [預訓練革命](focus2.md)
   - Word2Vec 與詞嵌入
   - ELMo 與上下文表示
   - OpenAI GPT

3. [GPT 與 GPT-2 的發展](focus3.md)
   - GPT 的架構
   - GPT-2 的爭議
   - 生成式預訓練

4. [XLNet 與 RoBERTa](focus4.md)
   - 排列語言模型
   - 更多資料與更長時間訓練
   - 超越 BERT

5. [ALBERT 與模型優化](focus5.md)
   - 引數共享
   - 句子順序預測
   - 模型蒸餾

6. [預訓練模型的應用](focus6.md)
   - 文字分類
   - 問答系統
   - 文字生成

7. [NLP 任務的全新時代](focus7.md)
   - GLUE 基準
   - BERT 在各任務的突破
   - 未來展望

---

## 濃縮回顧

### BERT 的誕生

2018 年 10 月，Google 發布了 BERT，這是 NLP 領域的重大突破。BERT 的核心創新包括：

**雙向 Transformer 編碼器**：不同於過往只能從左到右或獨立處理每個 token 的模型，BERT 能夠同時利用左右上下文資訊。

**Masked Language Model（MLM）**：訓練時隨機遮蔽 15% 的 token，模型需要根據上下文預測被遮蔽的詞。

**Next Sentence Prediction（NSP）**：學習句子間關係，幫助理解文件層級的語義。

### 預訓練的革命

預訓練的概念並非 BERT 首創，但 BERT 將其發揚光大：

```
預訓練階段：使用大量無標注文本學習語言表示
    ↓
微調階段：使用特定任務的標註資料進行調整
```

這種方法大幅降低了任務特定資料的需求，並顯著提升了各類 NLP 任務的效能。

### 主要預訓練模型時間線

| 時間 | 模型 | 機構 |
|------|------|------|
| 2018年6月 | GPT | OpenAI |
| 2018年10月 | BERT | Google |
| 2019年2月 | GPT-2 (小型) | OpenAI |
| 2019年6月 | XLNet | Google/CMU |
| 2019年7月 | RoBERTa | Facebook |
| 2019年9月 | ALBERT | Google |

### 注意力機制

Transformer 的核心是自注意力（Self-Attention）機制：

```python
def attention(query, keys, values):
    scores = dot_product(query, keys)
    weights = softmax(scores / sqrt(d_k))
    return weighted_sum(weights, values)
```

這種機制允許模型權衡不同位置的重要性，是 BERT 強大能力的關鍵。

---

## 結論與展望

BERT 不僅是一個模型，更開創了一個時代。從 2018 年 10 月到 2019 年 10 月短短一年間，我們見證了 NLP 領域的翻天覆地變化。預訓練+微調的模式已成為標準，各種 BERT 變體層出不窮。

展望未來，我們可以期待：
- 更大規模的預訓練模型
- 更高效的壓縮和蒸餾技術
- 更多多模態預訓練模型
- 預訓練在更多領域的應用

---

## 延伸閱讀

- [BERT 原始論文](https://www.google.com/search?q=BERT+pre+training+natural+language+understanding)
- [Transformer 架構](https://www.google.com/search?q=Attention+is+All+You+Need+Transformer)
- [預訓練模型發展](https://www.google.com/search?q=pretrained+language+models+2019)

---

*本期焦點到此結束。下期我們將繼續關注 AI 技術的最新進展，敬請期待。*