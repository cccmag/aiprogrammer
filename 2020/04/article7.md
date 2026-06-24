# 語言模型評估方法

## 困惑度 (Perplexity)

困惑度是最常用的語言模型評估指標：

```python
import math
from transformers import GPT2LMHeadModel, GPT2Tokenizer

tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2")

def calculate_perplexity(text):
    inputs = tokenizer(text, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs, labels=inputs["input_ids"])
    loss = outputs.loss
    perplexity = math.exp(loss.item())
    return perplexity

text = "The quick brown fox jumps over the lazy dog"
print(f"Perplexity: {calculate_perplexity(text):.2f}")
```

## BLEU 分數

用於評估生成文字與參考文字的相似度：

```python
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction

reference = [["The", "quick", "brown", "fox", "jumps"]]
candidate = ["The", "quick", "brown", "dog"]

score = sentence_bleu(reference, candidate, smoothing_function=SmoothingFunction().method1)
print(f"BLEU score: {score:.4f}")
```

## ROUGE 分數

常用於摘要任務評估：

```python
from rouge import Rouge

rouge = Rouge()
scores = rouge.get_scores(
    "The quick brown fox jumps over the lazy dog",
    "The quick brown fox jumped over the lazy dog"
)
print(scores)
```

## 下游任務評估

```python
from sklearn.metrics import accuracy_score, f1_score

# 文字分類
y_true = [0, 1, 1, 0, 1]
y_pred = [0, 1, 0, 0, 1]

accuracy = accuracy_score(y_true, y_pred)
f1 = f1_score(y_true, y_pred, average='weighted')
print(f"Accuracy: {accuracy:.4f}")
print(f"F1 Score: {f1:.4f}")
```

## 人類評估

自動化指標有其限制，有時需要人類評估：

1. 流暢度（Fluency）：文字是否通順
2. 相關性（Relevance）：輸出是否與輸入相關
3. 準確性（Accuracy）：資訊是否正確
4. 連貫性（Coherence）：整體是否連貫

## 評估陷阱

- **過度依賴自動化指標**：BLEU 分數與人類判斷可能不符
- **測試集洩漏**：確保測試資料不在訓練資料中
- **任務特化**：不同任務需要不同的評估方法

## 參考資源

- https://www.google.com/search?q=language+model+evaluation+perplexity+BLEU+ROUGE+metrics+2020
- https://www.google.com/search?q=perplexity+GPT-2+language+model+how+to+calculate+formula
- https://www.google.com/search?q=NLP+evaluation+metrics+text+generation+summarization+translation