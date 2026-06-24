# 多模態模型評估

## 多模態評估的獨特挑戰

多模態模型（如 GPT-4V、Gemini Pro Vision）需要同時理解文字、圖像、音訊等多種模態。評估這類模型需要全新的基準與方法論。

## 主要多模態基準

```python
# 多模態評估流程範例
import json
from PIL import Image
import requests

class MultimodalEvaluator:
    def __init__(self, model):
        self.model = model

    def evaluate_vqa(self, image_path, question, answer):
        image = Image.open(image_path)
        response = self.model.generate(
            image=image,
            text=question
        )
        return {
            "question": question,
            "predicted": response,
            "expected": answer,
            "correct": self.check_answer(response, answer)
        }

    def check_answer(self, predicted, expected):
        return predicted.strip().lower() == expected.strip().lower()

    def evaluate_image_caption(self, image_path, reference):
        image = Image.open(image_path)
        caption = self.model.generate(image=image, text="描述這張圖片")
        bleu = self.compute_bleu(caption, reference)
        return {"caption": caption, "bleu_score": bleu}

    def compute_bleu(self, candidate, reference):
        # 簡化版 BLEU 計算
        c_tokens = candidate.split()
        r_tokens = reference.split()
        matches = sum(1 for t in c_tokens if t in r_tokens)
        return matches / max(len(c_tokens), 1)
```

## MMMU 基準

MMMU 是目前最具挑戰性的多模態基準，包含大學程度的跨學科問答：

```python
mmmu_categories = [
    "藝術與設計", "商業", "科學", "健康與醫學",
    "人文與社會科學", "技術與工程"
]

def evaluate_mmmu(model, mmmu_data):
    scores = {cat: [] for cat in mmmu_categories}
    for item in mmmu_data:
        cat = item["category"]
        result = model.evaluate_vqa(
            item["image"], item["question"], item["answer"]
        )
        scores[cat].append(result["correct"])

    for cat, results in scores.items():
        acc = sum(results) / len(results) * 100
        print(f"{cat}: {acc:.1f}%")
```

## 視覺推理評估

```python
# 評估模型是否能理解圖表中的數據關係
def evaluate_chart_understanding(model, chart_image, questions):
    results = []
    for q in questions:
        resp = model.generate(image=chart_image, text=q["question"])
        numeric_ans = extract_number(resp)
        is_correct = abs(numeric_ans - q["expected_value"]) < 0.1
        results.append(is_correct)
    return sum(results) / len(results)

def extract_number(text):
    import re
    numbers = re.findall(r"\d+\.?\d*", text)
    return float(numbers[0]) if numbers else 0
```

## 結語

Google 搜尋「MMMU Benchmark」「Multi-modal LLM Evaluation」可找到最新資料集與排行榜。多模態評估仍在快速發展，標準化是未來的重要方向。
