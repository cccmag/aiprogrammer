# BERT 微調實驗

## 環境準備

微調 BERT 需要以下環境：
- Python 3.6+
- PyTorch 1.0+ 或 TensorFlow 2.0+
- transformers 套件（ Hugging Face）

```bash
pip install torch transformers
```

## 使用 Hugging Face Transformers

Hugging Face 提供了易用的 BERT API：

```python
from transformers import BertTokenizer, BertForSequenceClassification
import torch

# 載入預訓練模型與 tokenizer
model_name = 'bert-base-uncased'
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertForSequenceClassification.from_pretrained(model_name, num_labels=2)
```

## 文本分類微調

### 資料準備

```python
# 文本分詞
texts = ["This is a positive example", "This is a negative example"]
labels = [1, 0]

# 編碼
encoded = tokenizer(texts, padding=True, truncation=True, return_tensors='pt')
input_ids = encoded['input_ids']
attention_mask = encoded['attention_mask']
```

### 訓練流程

```python
from torch.optim import AdamW

optimizer = AdamW(model.parameters(), lr=2e-5)

for epoch in range(3):
    optimizer.zero_grad()
    
    # 前向傳播
    outputs = model(input_ids, attention_mask=attention_mask, labels=torch.tensor(labels))
    loss = outputs.loss
    
    # 反向傳播
    loss.backward()
    optimizer.step()
    
    print(f"Epoch {epoch+1}, Loss: {loss.item()}")
```

## 問答任務微調

問答任務使用 BertForQuestionAnswering：

```python
from transformers import BertForQuestionAnswering

model = BertForQuestionAnswering.from_pretrained('bert-base-uncased')

# 輸入問題與上下文
question = "What is BERT?"
context = "BERT is a language representation model introduced by Google."

# 編碼
encoded = tokenizer(question, context, return_tensors='pt')
outputs = model(**encoded)

# 取得答案跨度
start_logits = outputs.start_logits
end_logits = outputs.end_logits
start_idx = torch.argmax(start_logits)
end_idx = torch.argmax(end_logits)
answer = tokenizer.decode(encoded['input_ids'][0][start_idx:end_idx+1])
```

## 常見問題與解決

### GPU 記憶體不足
- 減少批次大小
- 使用梯度累積
- 使用較小的模型（如 bert-small）

### 訓練不收斂
- 檢查學習率（建議 2e-5 ~ 5e-5）
- 增加 warmup 步數
- 確認標籤正確

## 預訓練模型下載

Hugging Face Model Hub 提供多種預訓練模型：
- `bert-base-uncased`：Base 版本，英文，無大小寫
- `bert-base-chinese`：中文預訓練模型
- `bert-large-uncased`：Large 版本

## 參考資源

- https://www.google.com/search?q=BERT+微调+PyTorch+Hugging+Face+文本分类+实战+2018
- https://www.google.com/search?q=BERT+fine-tuning+question+answering+SQuAD+PyTorch+example
- https://www.google.com/search?q=transformers+library+BERT+usage+tutorial+tokenizer+model+download