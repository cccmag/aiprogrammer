# T5：Text-to-Text Transfer Transformer

## Google 的統一框架

### 論文資訊

- **標題**：Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer
- **作者**：Colin Raffel et al.
- **發布**：JMLR 2020

---

## T5 的核心思想

### Text-to-Text 框架

T5 將所有 NLP 任務統一為文字到文字的轉換：

```
輸入: "translate English to German: Hello, how are you?"
輸出: "Hallo, wie geht es dir?"

輸入: "sentiment: This movie is amazing!"
輸出: "positive"

輸入: "summarize: [長文章]"
輸出: "[摘要]"
```

### 統一的損失函數

```python
# 所有任務使用相同的交叉熵損失
loss = cross_entropy(model_output, target_sequence)
```

---

## T5 的架構

### 基礎架構

T5 使用標準的 Transformer Encoder-Decoder 架構：

| 元件 | 說明 |
|------|------|
| Encoder | 12-24 層，雙向注意力 |
| Decoder | 12-24 層，自回歸生成 |
| 位置編碼 | 相對位置編碼 |

### 模型規模

| 配置 | 層數 | d_model | 參數 |
|------|------|---------|------|
| T5-small | 6 | 512 | 6,000 萬 |
| T5-base | 12 | 768 | 2.2 億 |
| T5-large | 24 | 1024 | 7.7 億 |
| T5-11B | 24 | 1024 | 110 億 |

---

## 預訓練目標

### 降遮罩語言建模（Denoising Objective）

T5 採用了一種獨特的預訓練目標：

```python
# 輸入: "Thank you <extra_id_0> me to your party <extra_id_1> week"
# 目標: "<extra_id_0> for inviting <extra_id_1> last"
```

隨機選擇 15% 的片段進行遮罩，然後讓模型預測被遮罩的內容。

### 與 BERT 的比較

| 方面 | BERT | T5 |
|------|------|-----|
| 遮罩比例 | 15% token | 15% tokens |
| 遮罩長度 | 單一 token | 可變長度片段 |
| 預測目標 | 被遮罩 token | 被遮罩片段 |

---

## Benchmark 結果

| 任務 | SOTA | T5 |
|------|------|-----|
| GLUE | 89.0 | 88.9 |
| SuperGLUE | 71.5 | 71.8 |
| SQuAD 1.1 | 93.2 | 93.7 |
| SQuAD 2.0 | 86.3 | 86.5 |

---

## T5 的影響

### 開源貢獻

Google 開源了：
- T5 預訓練模型
- C4 資料集（Common Crawl 的清洗版本）
- 完整的訓練程式碼

### 實際應用

- Google 搜尋的 NLP 功能
- Gmail 的智慧回复
- 翻譯服務

---

## T5 vs BERT vs GPT

| 方面 | T5 | BERT | GPT-3 |
|------|-----|------|-------|
| 架構 | Encoder-Decoder | Encoder | Decoder |
| 注意力 | 雙向 | 雙向 | 單向 |
| 生成方式 | 編碼-解碼 | N/A | 自回歸 |
| 微調 | 需微調 | 需微調 | Few-shot |

---

**下一步**：[RoBERTa 與模型最佳化](focus5.md)

## 延伸閱讀

- [T5+Text-to-Text+Transformer+paper](https://www.google.com/search?q=T5+Text-to-Text+Transfer+Transformer+paper+2020)
- [Google+T5+explore+limits+transfer+learning](https://www.google.com/search?q=Google+T5+explore+limits+transfer+learning)