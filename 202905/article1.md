# EleutherAI LM Eval Harness 實戰

## 1. 什麼是 LM Eval Harness

LM Evaluation Harness 是 EleutherAI 開發的開源評估框架，支援數百個基準測試的標準化執行，讓研究者在統一的環境中比較不同模型的表現。

## 2. 基本用法

安裝後透過 YAML 定義任務，框架會自動處理提示模板與評分邏輯。

```python
# examples/lm_eval_demo.py
import lm_eval
from lm_eval.models.huggingface import HFLM

model = HFLM(pretrained="gpt2")
results = lm_eval.simple_evaluate(
    model=model,
    tasks=["hellaswag", "arc_easy", "mmlu"],
    num_fewshot=5,
    batch_size=auto
)
print(results["results"]["hellaswag"]["acc"])
```

## 3. 任務組態深入

每個任務定義為 YAML 檔案，包含資料集、提示模板與評分邏輯。

```yaml
# custom_task.yaml
task: custom_qa
dataset_path: json
dataset_name: null
training_split: train
validation_split: test
doc_to_text: "問題: {{question}}\n答案:"
doc_to_target: "{{answer}}"
metric_list:
  - metric: exact_match
    aggregation: mean
```

## 4. 自訂評估任務

建立自訂任務需要定義 `doc_to_text`（提示）、`doc_to_target`（正確答案）以及評分指標。框架支援 few-shot 範例自動提取與標準化輸出解析。

```python
def process_results(doc, results):
    pred = results[0].strip()
    gold = doc["answer"].strip()
    return {"em": int(pred == gold), "f1": compute_f1(pred, gold)}
```

## 5. 實戰注意事項

批次大小會影響評估速度，也需要確保記憶體足夠。隨機種子應固定以確保可重現性。LM Eval Harness 支援 vLLM 等推理加速引擎，可大幅提升評估效率。

## 6. 結語

LM Eval Harness 已成為 AI 評估的事實標準。熟悉其架構後，不僅能使用現有基準，更能快速為自訂場景建立專屬評估任務。

- https://www.google.com/search?q=EleutherAI+LM+evaluation+harness+tutorial
- https://www.google.com/search?q=lm+eval+harness+custom+task+yaml
