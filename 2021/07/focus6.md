# 主題六：自然語言處理的應用

## 翻譯、摘要、問答系統

### 1. 神經機器翻譯

神經機器翻譯（NMT）自 2014 年 Seq2Seq 模型提出以來，經歷了快速發展：

**經典架構演進**：
- Seq2Seq + Attention（2014）
- GNMT（2016）- Google 的 production NMT 系統
- Transformer（2017）- 現已成為主流

```python
class NeuralMachineTranslator(nn.Module):
    def __init__(self, src_vocab_size, tgt_vocab_size, d_model, num_heads, num_layers):
        super().__init__()
        self.encoder = Encoder(src_vocab_size, d_model, num_heads, num_layers)
        self.decoder = Decoder(tgt_vocab_size, d_model, num_heads, num_layers)
        self.output_projection = nn.Linear(d_model, tgt_vocab_size)

    def forward(self, src, tgt, src_mask=None, tgt_mask=None):
        encoder_output = self.encoder(src, src_mask)
        decoder_output = self.decoder(tgt, encoder_output, src_mask, tgt_mask)
        return self.output_projection(decoder_output)

    def translate(self, src, max_len=100):
        encoder_output = self.encoder(src)

        outputs = [SOS_TOKEN]
        for _ in range(max_len):
            tgt = torch.tensor(outputs).unsqueeze(0)
            decoder_output = self.decoder(tgt, encoder_output)
            next_token = self.output_projection(decoder_output[:, -1]).argmax()

            if next_token == EOS_TOKEN:
                break
            outputs.append(next_token.item())

        return outputs
```

**Transformer 翻譯的優勢**：
- 完全并行計算
- 更好地處理長距離依賴
- 翻譯品質顯著提升

### 2. 文字摘要

文字摘要分為兩種主要方法：

**抽取式摘要**：
- 從原文中挑選重要句子
- 簡單但受原文限制

**生成式摘要**：
- 生成全新的文字
- 更靈活但難度更高

```python
class TextSummarizer(nn.Module):
    def __init__(self, vocab_size, d_model, num_heads, num_layers):
        super().__init__()
        self.encoder = TransformerEncoder(vocab_size, d_model, num_heads, num_layers)
        self.decoder = TransformerDecoder(vocab_size, d_model, num_heads, num_layers)

    def forward(self, src, tgt, src_mask=None, tgt_mask=None):
        encoder_output = self.encoder(src, src_mask)
        decoder_output = self.decoder(tgt, encoder_output, src_mask, tgt_mask)
        return decoder_output

    def generate_summary(self, src, max_len=150, beam_size=5):
        """使用 Beam Search 生成摘要"""
        encoder_output = self.encoder(src)

        beams = [(0, [SOS_TOKEN])]
        completed = []

        for _ in range(max_len):
            all_candidates = []

            for score, sequence in beams:
                if sequence[-1] == EOS_TOKEN:
                    completed.append((score, sequence))
                    continue

                tgt = torch.tensor(sequence).unsqueeze(0)
                tgt_mask = self.make tgt_mask(tgt.size(1))

                decoder_output = self.decoder(tgt, encoder_output, tgt_mask=tgt_mask)
                log_probs = F.log_softmax(self.output_projection(decoder_output[:, -1]), dim=-1)

                topk = log_probs.topk(beam_size)
                for k in range(beam_size):
                    candidate_score = score + topk.values[0, k].item()
                    candidate_sequence = sequence + [topk.indices[0, k].item()]
                    all_candidates.append((candidate_score, candidate_sequence))

            beams = heapq.nlargest(beam_size, all_candidates, key=lambda x: x[0])

        return max(completed + beams, key=lambda x: x[0]/len(x[1]))[1]
```

### 3. 問答系統

問答系統是 NLP 的重要應用，可以分為幾種類型：

**抽取式問答**：
- 從給定文本中找出答案
- 通常預測答案的開始和結束位置

```python
class QuestionAnswering(nn.Module):
    def __init__(self, bert_model):
        super().__init__()
        self.bert = bert_model
        self.qa_outputs = nn.Linear(bert_model.config.hidden_size, 2)

    def forward(self, input_ids, attention_mask, start_positions=None, end_positions=None):
        outputs = self.bert(input_ids=input_ids, attention_mask=attention_mask)
        sequence_output = outputs.last_hidden_state

        logits = self.qa_outputs(sequence_output)
        start_logits, end_logits = logits.split(1, dim=-1)
        start_logits = start_logits.squeeze(-1)
        end_logits = end_logits.squeeze(-1)

        if start_positions is not None and end_positions is not None:
            loss_fct = nn.CrossEntropyLoss()
            start_loss = loss_fct(start_logits, start_positions)
            end_loss = loss_fct(end_logits, end_positions)
            loss = (start_loss + end_loss) / 2
            return {'loss': loss, 'start_logits': start_logits, 'end_logits': end_logits}

        return {'start_logits': start_logits, 'end_logits': end_logits}
```

**生成式問答**：
- 根据问题和上下文生成答案
- 可以處理更複雜的問題

### 4. 情感分析

情感分析是另一個重要的 NLP 應用：

```python
class SentimentClassifier(nn.Module):
    def __init__(self, bert_model, num_classes):
        super().__init__()
        self.bert = bert_model
        self.classifier = nn.Linear(bert_model.config.hidden_size, num_classes)

    def forward(self, input_ids, attention_mask):
        outputs = self.bert(input_ids=input_ids, attention_mask=attention_mask)
        pooled_output = outputs.pooler_output
        logits = self.classifier(pooled_output)
        return logits
```

### 5. 對話系統

對話系統是 NLP 技術的综合應用：

**任務導向對話**：
- 預訂、查詢等特定任務
- 需要對話狀態追蹤

**開放域對話**：
- 自由聊天
- 挑戰：保持一致性、主題相關性

### 6. 應用的核心技術

這些應用共享一些核心技術：

**預訓練語言模型**：
- 語言理解的基礎
- 決定了模型的基本能力

**序列到序列生成**：
- 翻譯、摘要的核心
- 需要處理曝光偏差問題

**注意力機制**：
- 對齊源序列和目標序列
- 提供可解釋性

### 7. 產業應用案例

**搜尋引擎**：
- Google 採用 BERT 理解搜尋意圖
- 顯著改善搜尋結果品質

**客服系統**：
- 自動化回答常見問題
- 提高效率和用戶體驗

**內容審核**：
- 識別有害內容
- 需要及時性和準確性

---

## 延伸閱讀

- [神經機器翻譯教程](https://www.google.com/search?q=neural+machine+translation+transformer+tutorial)
- [文字摘要方法](https://www.google.com/search?q=text+summarization+neural+networks)
- [問答系統綜述](https://www.google.com/search?q=question+answering+systems+review)