# 主題二：BERT 與預訓練語言模型

## 雙向編碼與微調策略

### 1. BERT 的誕生

2018 年，Google 在論文《BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding》中提出了 BERT，這是一種革命性的語言表示預訓練方法。

與之前的預訓練方法（如 ELMo、GPT）不同，BERT 是第一個真正「雙向」的深度預訓練語言模型。

### 2. 預訓練任務

BERT 採用兩個預訓練任務：

**Masked Language Model (MLM)**：
- 隨機遮罩 15% 的輸入 token
- 訓練模型預測被遮罩的詞
- 這個任務讓模型能夠同時利用左右上下文

```python
def mlm_loss(masked_tokens, logits, labels):
    """計算 MLM 損失"""
    loss_fn = nn.CrossEntropyLoss()
    masked_logits = logits[masked_tokens]
    masked_labels = labels[masked_tokens]
    return loss_fn(masked_logits, masked_labels)
```

**Next Sentence Prediction (NSP)**：
- 訓練模型判斷兩個句子是否連續
- 正樣本：實際相連的句子對
- 負樣本：隨機組合的句子對
- 幫助模型理解句子間關係

### 3. BERT 的輸入表示

BERT 的輸入是特殊設計的：

```python
[CLS] + 句子A + [SEP] + 句子B + [SEP]

其中 [CLS] 是分類符號，[SEP] 是分隔符號
每個 token 還會加上位置編碼和段落編碼
```

### 4. 微調策略

預訓練完成後，可以在特定任務上進行微調（Fine-tuning）：

```python
class BertForSequenceClassification(nn.Module):
    def __init__(self, bert_model, num_labels):
        super().__init__()
        self.bert = bert_model
        self.classifier = nn.Linear(bert_model.config.hidden_size, num_labels)

    def forward(self, input_ids, attention_mask, token_type_ids, labels=None):
        outputs = self.bert(
            input_ids=input_ids,
            attention_mask=attention_mask,
            token_type_ids=token_type_ids
        )

        pooled_output = outputs.pooler_output  # [CLS] 的輸出
        logits = self.classifier(pooled_output)

        loss = None
        if labels is not None:
            loss_fn = nn.CrossEntropyLoss()
            loss = loss_fn(logits, labels)

        return {'loss': loss, 'logits': logits}
```

### 5. BERT 的應用

BERT 及其變體幾乎適用於所有 NLP 任務：

**文字分類**：
- 情感分析、垃圾郵件檢測
- 使用 [CLS] token 的輸出進行分類

**命名實體識別**：
- 識別文字中的人名、地名、組織名等
- 每個 token 都會輸出一個標籤

**問答系統**：
- 從給定文本中找出問題的答案
- 預測答案的開始和結束位置

**自然語言推論**：
- 判斷兩個句子的邏輯關係（蘊含、反駁、中立）

### 6. BERT 的變體

BERT 之後，出現了大量基於其架構的改進模型：

**RoBERTa**：
- 移除 NSP 任務，使用更大批次和更多訓練資料
- 動態遮罩機制
- 更長時間訓練

**ALBERT**：
- 參數共享，大幅減少模型大小
- 句子順序預測取代 NSP
- 層間共享注意力

**ELECTRA**：
- 取代MLM，使用替換 token 檢測（Replaced Token Detection）
- 更高效的預訓練

**DistilBERT**：
- 知識蒸餾，保留 97% 效能但縮小 60% 體積
- 適合在邊緣設備部署

### 7. BERT 的影響

BERT 的成功開啟了 NLP 的「預訓練-微調」時代：

1. **降低任務特定資料需求**：預訓練學到的語言知識可以遷移到下游任務
2. **提升任務效能**：幾乎所有 NLP 任務都有顯著提升
3. **促進產業應用**：基於 BERT 的模型被廣泛應用於搜尋、客服、翻譯等場景

Google 將 BERT 應用於搜尋引擎，顯著改善了搜尋結果的相關性，這是 NLP 技術在業界最具影響力的應用之一。

---

## 延伸閱讀

- [BERT 論文](https://www.google.com/search?q=BERT+pre-training+deep+bidirectional+transformers)
- [RoBERTa 論文](https://www.google.com/search?q=RoBERTa+robustly+optimized+BERT)
- [Hugging Face BERT 教程](https://www.google.com/search?q=Hugging+Face+BERT+tutorial)