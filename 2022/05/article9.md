# 語言模型評估：困惑度

## 為什麼需要評估

不同語言模型的性能差異巨大，從簡單的 n-gram 到 GPT-3 都需要一致的評估標準。

## 困惑度（Perplexity）

困惑度是語言模型最常用的評估指標，衡量模型對測試資料的「驚訝程度」：

```
PPL(W) = P(w_1, w_2, ..., w_N)^{-1/N}
       = exp(-1/N * sum_{i=1}^N log P(w_i|w_<i))
```

```python
import math

def compute_perplexity(model, corpus, stride=512):
    """計算語言模型的困惑度"""
    total_loss = 0.0
    total_tokens = 0

    for i in range(0, len(corpus), stride):
        chunk = corpus[i:i+stride+1]
        inputs = chunk[:-1]
        targets = chunk[1:]

        with torch.no_grad():
            outputs = model(torch.tensor([inputs]))
            loss = criterion(outputs.view(-1, vocab_size),
                           torch.tensor(targets).view(-1))
            total_loss += loss.item() * len(inputs)
            total_tokens += len(inputs)

    avg_loss = total_loss / total_tokens
    return math.exp(avg_loss)
```

## 困惑度的直覺理解

| 困惑度值 | 模型能力 | 類比 |
|---------|---------|------|
| 詞彙量大小 (V) | 隨機猜測 | 擲骰子 |
| 1000 | 弱 | 勉強猜對 |
| 100 | 中等 | n-gram 模型 |
| 30-50 | 強 | RNN/LSTM |
| 20-30 | 很強 | BERT/GPT |
| <20 | 前沿 | GPT-3 級別 |

## BLEU 分數

## 生成任務的難題

困惑度主要評估模型對資料的擬合程度，但不一定能反映生成品質。例如，重複生成「the the the」的模型可能困惑度很低。

## BLEU 分數

BLEU（Bilingual Evaluation Understudy）用於評估生成文本與參考文本的相似度：

```python
from nltk.translate.bleu_score import sentence_bleu

def compute_bleu(reference, candidate):
    """計算 BLEU 分數"""
    # reference: ["the cat is on the mat"]
    # candidate: "the cat sat on the mat"
    return sentence_bleu([reference.split()], candidate.split())

# BLEU 基於 n-gram 精確率
# 懲罰過短的生成（brevity penalty）
```

## ROUGE 分數

ROUGE（Recall-Oriented Understudy for Gisting Evaluation）用於評估摘要任務：

- **ROUGE-N**：n-gram 召回率
- **ROUGE-L**：最長公共子序列
- **ROUGE-S**：跳躍 bigram

## 人類評估

自動化指標有其局限，人類評估仍然不可或缺：

| 維度 | 說明 | 分數範圍 |
|------|------|---------|
| 流暢度 | 語法是否正確 | 1-5 |
| 相關性 | 內容是否切題 | 1-5 |
| 連貫性 | 邏輯是否一致 | 1-5 |
| 資訊性 | 是否包含有用資訊 | 1-5 |

## 綜合評估框架

```python
def evaluate_language_model(model, test_data, reference=None):
    results = {}

    # 困惑度
    results["perplexity"] = compute_perplexity(model, test_data)

    # BLEU（如果有參考）
    if reference:
        results["bleu"] = compute_bleu(reference, model.generate())

    # 多樣性
    generated = model.generate(n_samples=100)
    results["distinct-1"] = distinct_ngrams(generated, 1)
    results["distinct-2"] = distinct_ngrams(generated, 2)

    return results
```

## 延伸閱讀

- [Perplexity 解釋](https://www.google.com/search?q=perplexity+in+language+models+explained)
- [BLEU 論文](https://www.google.com/search?q=BLEU+a+method+for+automatic+evaluation+of+machine+translation)
- [ROUGE 論文](https://www.google.com/search?q=ROUGE+automatic+evaluation+summarization)
