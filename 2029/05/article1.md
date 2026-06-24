# EleutherAI LM Eval Harness 實戰

## 什麼是 LM Eval Harness？

EleutherAI 推出的 LM Eval Harness 是目前最廣泛使用的語言模型評估框架之一。它提供統一的評估介面，支援數百個標準基準（Benchmark），讓研究人員能公平比較不同模型。

## 快速安裝與使用

```python
# 安裝 LM Eval Harness
# pip install lm-eval

import lm_eval
from lm_eval import evaluate
from lm_eval.models.huggingface import HFLM

# 載入模型（以 GPT-2 為例）
model = HFLM(pretrained="gpt2")

# 執行 MMLU 評估
results = lm_eval.simple_evaluate(
    model=model,
    tasks=["mmlu"],
    num_fewshot=5,
    batch_size=1
)

print(results["results"]["mmlu"]["acc"])
```

## 自訂任務

```python
import lm_eval.tasks as tasks

# 建立自訂評估任務
custom_task = tasks.TaskConfig(
    task_name="my_custom_task",
    dataset_path="json",
    dataset_kwargs={"data_files": "my_data.json"},
    doc_to_text="問題：{{question}}\n答案：",
    doc_to_target="{{answer}}",
    metric_list=[{"metric": "exact_match"}]
)

tasks.TASK_REGISTRY.register(custom_task)
```

## 支援的主要基準

LM Eval Harness 支援數十種基準，涵蓋：

- **知識推理**：MMLU、ARC、HellaSwag
- **數學能力**：GSM8K、MATH
- **程式碼生成**：HumanEval、MBPP
- **多語言理解**：XNLI、PAWS-X

## 任務註冊機制

LM Eval Harness 採用任務註冊機制，所有基準都定義在 `lm_eval/tasks` 目錄下。每個任務包含資料集路徑、提示模板、評分指標等配置。使用者可以透過 YAML 檔案輕鬆新增自訂任務，無需修改框架程式碼。

## 批次評估與加速

```python
# 多 GPU 批次評估
results = lm_eval.simple_evaluate(
    model=model,
    tasks=["hellaswag", "arc_easy", "arc_challenge"],
    num_fewshot=0,
    batch_size=auto,  # 自動選擇最佳批次大小
    device="cuda:0"
)
```

## 結果輸出與比較

```python
# 比較多個模型的結果
def compare_models(models, task):
    results = {}
    for name, model in models.items():
        result = lm_eval.simple_evaluate(
            model=model, tasks=[task]
        )
        results[name] = result["results"][task]["acc"]
    return results

models = {
    "gpt2": HFLM(pretrained="gpt2"),
    "gpt2-medium": HFLM(pretrained="gpt2-medium")
}
comparison = compare_models(models, "hellaswag")
print(comparison)
```

## 產出報告

評估完成後可產生 JSON 格式結果，便於後續分析與視覺化。Google 搜尋「LM Eval Harness」可找到官方文件與最新支援的任務清單。

## 結語

LM Eval Harness 讓模型評估變得標準化、可重現。無論是訓練新模型或比較現有模型，這套工具都是必備利器。
