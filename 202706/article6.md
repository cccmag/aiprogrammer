# LLM 評估：從 Perplexity 到 Chatbot Arena

## 前言

隨著 LLM 能力不斷提升，如何公正且全面地評估模型表現成為關鍵挑戰。你可能會注意到，同一個模型在不同的排行榜上排名可能截然不同，這是因為評估方法與資料集的選擇會深刻影響結果。從早期的 Perplexity 到當前的 Chatbot Arena 競技場，評估方法經歷了巨大的演變。本文將系統介紹 LLM 評估的各個面向，從最基礎的內在指標到最先進的 AI 評判機制，並提供 Python 實作，讓讀者能建立自己的評估管線。

## 內在評估指標

內在指標直接衡量模型對語言的建模能力，不需要特定的任務資料集。這類指標的優點是計算快速、可重現性高，但它們與人類真實感受的相關性有限。因此，實務上我們通常同時使用內在指標與外在任務導向的評估，才能全面了解模型的真實能力。

### Perplexity

Perplexity（困惑度）衡量模型對文字的預測能力，值越低表示模型越有把握。從資訊理論的角度來看，Perplexity 可以理解為模型在預測下一個 token 時的平均「選擇數」：如果 Perplexity 是 10，代表模型在每次預測時，平均需要從 10 個可能性中選擇，這說明模型對語言的掌握還不夠精確。

```python
import torch
import math

def calculate_perplexity(model, tokenizer, text):
    inputs = tokenizer(text, return_tensors="pt").to("cuda")
    with torch.no_grad():
        outputs = model(**inputs, labels=inputs["input_ids"])
        loss = outputs.loss
    return math.exp(loss.item())

# 範例：比較兩個模型
text = "深度學習是機器學習的一個分支領域。"
ppl_a = calculate_perplexity(model_a, tokenizer, text)
ppl_b = calculate_perplexity(model_b, tokenizer, text)
print(f"Model A: {ppl_a:.2f}, Model B: {ppl_b:.2f}")
```

Perplexity 的局限：與人類評價相關性有限，且容易被訓練資料污染。

### BLEU 與 ROUGE

BLEU（機器翻譯）和 ROUGE（摘要生成）是最早用於評估生成品質的指標：

```python
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from rouge_score import rouge_scorer

reference = "Transformer 是一種基於注意力機制的神經網路架構"
candidate = "Transformer 是一種注意力機制的神經網路"

# BLEU
smoothie = SmoothingFunction().method4
bleu = sentence_bleu([reference.split()], candidate.split(),
                     smoothing_function=smoothie)
print(f"BLEU: {bleu:.4f}")

# ROUGE
scorer = rouge_scorer.RougeScorer(["rouge1", "rouge2", "rougeL"], use_stemmer=True)
scores = scorer.score(reference, candidate)
print(f"ROUGE-1: {scores['rouge1'].fmeasure:.4f}")
print(f"ROUGE-L: {scores['rougeL'].fmeasure:.4f}")
```

## 綜合性 Benchmark

### MMLU（Massive Multitask Language Understanding）

MMLU 測試模型在 57 個學科上的知識，包含人文、科學、法律等領域：

```python
def evaluate_mmlu(model, tokenizer, mmlu_dataset):
    correct = 0
    total = 0
    for item in mmlu_dataset:
        prompt = f"""問題：{item['question']}
選項：
A. {item['choices'][0]}
B. {item['choices'][1]}
C. {item['choices'][2]}
D. {item['choices'][3]}

請回答正確選項（A/B/C/D）："""

        inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
        outputs = model.generate(**inputs, max_new_tokens=1)
        answer = tokenizer.decode(outputs[0][-1:])
        if answer.strip().upper() == item["answer"]:
            correct += 1
        total += 1
    return correct / total
```

### HumanEval（程式碼生成）

HumanEval 測試模型生成 Python 函式的能力：

```python
def evaluate_humaneval(model, tokenizer, humaneval_tasks):
    pass_rate = 0
    for task in humaneval_tasks:
        prompt = task["prompt"]  # 函式簽名與 docstring
        inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
        outputs = model.generate(**inputs, max_new_tokens=256)
        generated_code = tokenizer.decode(outputs[0])

        # 執行測試
        test_code = task["test"]  # 包含 assert 的測試程式碼
        try:
            exec(generated_code + "\n" + test_code)
            pass_rate += 1
        except Exception:
            pass
    return pass_rate / len(humaneval_tasks)
```

## 人類評價與 Chatbot Arena

LMSYS 的 Chatbot Arena 採用群眾外包的 ELO 評分系統，讓使用者直接比較兩個匿名模型的輸出：

```python
class ELO:
    def __init__(self, k=32):
        self.k = k
        self.ratings = {}

    def expected_score(self, rating_a, rating_b):
        return 1.0 / (1.0 + 10.0 ** ((rating_b - rating_a) / 400.0))

    def update(self, model_a, model_b, winner):
        if model_a not in self.ratings:
            self.ratings[model_a] = 1500
        if model_b not in self.ratings:
            self.ratings[model_b] = 1500

        ea = self.expected_score(self.ratings[model_a], self.ratings[model_b])
        eb = 1.0 - ea

        if winner == "a":
            sa, sb = 1.0, 0.0
        elif winner == "b":
            sa, sb = 0.0, 1.0
        else:  # 平手
            sa, sb = 0.5, 0.5

        self.ratings[model_a] += self.k * (sa - ea)
        self.ratings[model_b] += self.k * (sb - eb)
```

## 自動化評估管線

結合多種指標的評估腳本：

```python
class LLMEvaluator:
    def __init__(self, model, tokenizer):
        self.model = model
        self.tokenizer = tokenizer

    def evaluate_all(self, test_cases):
        results = {
            "perplexity": [],
            "rouge_l": [],
            "bert_score": [],
            "llm_judge": []
        }
        for case in test_cases:
            # 計算 perplexity
            ppl = calculate_perplexity(self.model, self.tokenizer, case["reference"])
            results["perplexity"].append(ppl)

            # 生成與比較
            generated = self.generate(case["prompt"])
            results["rouge_l"].append(
                self.compute_rouge(case["reference"], generated)
            )

            # LLM-as-judge
            judge_score = self.llm_judge(case["prompt"], generated, case["reference"])
            results["llm_judge"].append(judge_score)

        return {k: torch.mean(torch.tensor(v)) for k, v in results.items()}
```

## 常見陷阱與注意事項

- **資料污染**：Benchmark 資料可能出現在訓練集中
- **Metric 偏差**：BLEU 對 n-gram 重疊敏感，不適合創意生成
- **語境敏感**：提示詞的措辭會顯著影響結果
- **統計顯著性**：單次評估可能不穩定，應重複多次

## 參考資源

- [LMSYS Chatbot Arena](https://www.google.com/search?q=lmsys+chatbot+arena+leaderboard)
- [MMLU Benchmark](https://www.google.com/search?q=MMLU+massive+multitask+language+understanding)
- [HuggingFace Open LLM Leaderboard](https://www.google.com/search?q=huggingface+open+llm+leaderboard)
