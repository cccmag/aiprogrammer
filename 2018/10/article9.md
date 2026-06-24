# 問答系統應用

## 問答任務類型

問答系統（Question Answering）是 NLP 的重要應用，任務類型包括：

### 1. 抽取式問答（Extractive QA）
從給定文件中抽取答案片段。答案通常是文件中的一個連續span。
- SQuAD：給定段落與問題，抽出答案span
- Natural Questions：Google 搜尋結果中找答案

### 2. 選擇式問答（Multiple Choice QA）
從多個候選答案中選擇正確選項。
- RACE：英語考試閱讀理解
- ARC：AI2 Reasoning Challenge

### 3. 生成式問答（Abstractive QA）
答案並非直接來自文件，而是需要理解和生成。
- MS MARCO：微軟機器閱讀理解
- CoQA：對話式問答

## BERT 在問答任務的突破

BERT 在 SQuAD 1.1 上刷新紀錄：
- Human performance: 91.2% EM, 96.4% F1
- BERT-base: 84.3% EM, 90.9% F1
- BERT-large: 86.9% EM, 92.2% F1

BERT 的雙向理解能力使其能夠準確定位答案位置。

## SQuAD 格式說明

SQuAD 的輸入輸出格式：
- **輸入**：問題 + 文章段落
- **輸出**：答案在段落中的起始位置與結束位置

## BERT 問答模型實作

```python
from transformers import BertForQuestionAnswering, BertTokenizer
import torch

model_name = 'bert-large-uncased-whole-word-masking-finetuned-squad'
model = BertForQuestionAnswering.from_pretrained(model_name)
tokenizer = BertTokenizer.from_pretrained(model_name)

def answer_question(question, context):
    encoded = tokenizer.encode_plus(
        question, context,
        add_special_tokens=True,
        return_tensors='pt'
    )
    
    outputs = model(**encoded)
    start_logits = outputs.start_logits
    end_logits = outputs.end_logits
    
    start_idx = torch.argmax(start_logits)
    end_idx = torch.argmax(end_logits)
    
    tokens = tokenizer.convert_ids_to_tokens(encoded['input_ids'][0])
    answer = ''.join(tokens[start_idx:end_idx+1]).replace('##', '')
    
    return answer

# 測試
context = """
BERT is a language representation model introduced by Google in 2018.
It uses a transformer architecture and pre-training techniques.
"""
question = "When was BERT introduced?"
print(answer_question(question, context))  # 輸出: 2018
```

## 預訓練問答模型

Hugging Face 提供多個在 SQuAD 上微調的模型：
- `bert-large-uncased-whole-word-masking-finetuned-squad`
- `deepset/bert-base-squad2`（SQuAD 2.0）
- `distilbert-base-cased-distilled-squad`（輕量版）

## 多語言問答

多語言 BERT（mBERT）可用於跨語言問答：
- 在英語資料微調
- 直接應用於其他語言
- 無需目標語言的標注資料

## 實務建議

1. **長文本處理**：BERT 有 512 token 限制，需採用滑動窗口策略
2. **答案類型**：先判斷問題類型（誰、什麼時候、為什麼）再抽取
3. **置信度**：使用 start/end logits 的差異評估答案品質

## 參考資源

- https://www.google.com/search?q=BERT+问答系统+SQuAD+抽取式+问答+實作+2018
- https://www.google.com/search?q=BERT+question+answering+PyTorch+Hugging+Face+squad+example
- https://www.google.com/search?q=SQuAD+dataset+question+answering+format+BERT+performance