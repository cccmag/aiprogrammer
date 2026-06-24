# BERT：雙向 Transformer 的崛起

## 2018 年：Google 的突破

### 歷史背景

2018 年 10 月，Google 發表了 BERT（Bidirectional Encoder Representations from Transformers），這是第一個真正意義上的雙向預訓練語言模型。

### 論文資訊

- **標題**：BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding
- **作者**：Jacob Devlin, Ming-Wei Chang, Kenton Lee, Kristina Toutanova
- **發布**：NAACL 2019

---

## BERT 的核心創新

### 雙向 Transformer

之前的 GPT 只使用左到右的上下文，而 BERT 同時利用左右兩側的上下文：

```
GPT:   [The, cat, sat, on, the, mat]
              ↓
         只看左側

BERT:  [The, cat, sat, on, the, mat]
              ↓
         雙向同時看
```

### Masked Language Model (MLM)

BERT 透過遮罩語言模型進行預訓練：

```python
# 輸入：[CLS] The [MASK] sat on the [MASK] [SEP]
# 目標：預測被遮罩的詞
```

隨機遮罩約 15% 的單詞，讓模型從兩側上下文學習。

### Next Sentence Prediction (NSP)

訓練理解句子間關係：

```python
Sentence A: The cat sat on the mat.
Sentence B: It was comfortable.
Label: IsNext

Sentence A: The cat sat on the mat.
Sentence B: Tomorrow will be sunny.
Label: NotNext
```

---

## BERT 的規模

| 配置 | 層數 | 隱藏維度 | 參數數量 |
|------|------|---------|---------|
| BERT-base | 12 | 768 | 1.1 億 |
| BERT-large | 24 | 1024 | 3.4 億 |

---

## 下游任務微調

### 句子分類

```python
# CLS token 的表示用於分類
output = model(input_ids)
class_logits = classifier(output[0][:, 0])  # 取 [CLS] token
```

### 問答任務

```python
# 預測答案的起始和結束位置
start_logits, end_logits = model(input_ids)
start_position = argmax(start_logits)
end_position = argmax(end_logits)
```

### 命名實體識別

```python
# 每個 token 的表示用於分類
output = model(input_ids)
token_logits = classifier(output[0])  # 每個 token
```

---

## BERT 的成功

### Benchmark 結果

| 任務 | 之前 SOTA | BERT |
|------|----------|------|
| GLUE | 72.8 | 80.5 |
| SQuAD 1.1 | 91.1 | 93.2 |
| SQuAD 2.0 | 83.0 | 86.3 |

### 開源貢獻

Google 開源了：
- 預訓練模型（BERT-base, BERT-large）
- 原始碼
- TensorFlow 實現

這極大推動了 NLP 研究的發展。

---

## BERT 的影響

### 衍生模型

| 模型 | 改進 |
|------|------|
| RoBERTa | 去除 NSP，動態遮罩 |
| ALBERT | 引數共享，詞典分解 |
| ELECTRA | 替換 token 檢測 |
| DistilBERT | 蒸餾壓縮 |

### 任務特定微調

BERT 開啟了「預訓練 + 微調」範式的普及。

---

**下一步**：[GPT 系列：從 GPT 到 GPT-3](focus3.md)

## 延伸閱讀

- [BERT+paper+2018](https://www.google.com/search?q=BERT+pre-training+deep+bidirectional+transformers+paper)
- [Google+BERT+NAACL+2019](https://www.google.com/search?q=BERT+Google+NAACL+2019)