# 微調 LLM 的完整指南：資料準備到評估

## 前言

大型語言模型雖然能力強大，但通用模型往往無法滿足特定領域的需求。舉例來說，Llama 3.1 雖然能流暢回答一般性問題，但如果要它在醫學診斷、法律文件分析或公司內部客服等專業場景中表現良好，就需要透過微調讓模型學習特定領域的知識與表達方式。微調（Fine-tuning）正是讓 LLM 適應特定任務的核心技術。本文將從資料準備、LoRA 微調、超參數設定到評估，提供完整的實作指南，幫助讀者將通用模型轉變為領域專家。

## 資料準備與格式

微調的第一步是準備高品質的資料。業界有句名言：「垃圾進，垃圾出。」即使在 LoRA 等參數高效微調方法下，資料品質仍然是決定最終模型表現的最關鍵因素。優質的微調資料應該具備多樣性、正確性與一致性。多樣性確保模型能應對各種輸入變化；正確性避免模型學到錯誤知識；一致性則讓模型的輸出風格與格式可預測。常見的資料格式包括：

### 對話格式（Chat Template）

HuggingFace Transformers 使用 `apply_chat_template` 來格式化對話資料：

```python
from datasets import load_dataset

dataset = load_dataset("json", data_files="training_data.json")
# 範例資料格式
# {"messages": [
#     {"role": "system", "content": "你是一個 AI 助手"},
#     {"role": "user", "content": "什麼是 Transformer？"},
#     {"role": "assistant", "content": "Transformer 是一種..."}
# ]}

def format_chat(example, tokenizer):
    return {
        "text": tokenizer.apply_chat_template(
            example["messages"], tokenize=False
        )
    }

formatted_dataset = dataset.map(
    lambda x: format_chat(x, tokenizer)
)
```

### 指令微調格式

```python
# Alpaca 格式
{
    "instruction": "解釋什麼是梯度下降",
    "input": "",
    "output": "梯度下降是一種最佳化演算法..."
}

def format_instruction(example):
    if example["input"]:
        prompt = f"### 指令：{example['instruction']}\n### 輸入：{example['input']}\n### 回應："
    else:
        prompt = f"### 指令：{example['instruction']}\n### 回應："
    return {"text": prompt + example["output"]}
```

## 選擇基礎模型

選擇基座模型是關鍵決策：

- **Llama 3.1 (8B/70B/405B)**：通用能力強，生態系完整
- **Mistral / Mixtral**：高效能，適合邊緣部署
- **Qwen 2.5**：中英文雙語表現優異
- **Gemma 2**：Google 出品，小而美

## LoRA vs 全參數微調

LoRA（Low-Rank Adaptation）是目前最主流的參數高效微調方法，僅更新原始權重的低秩分解矩陣：

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import LoraConfig, get_peft_model, TaskType

model_name = "meta-llama/Llama-3.1-8B-Instruct"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.bfloat16,
    device_map="auto"
)

lora_config = LoraConfig(
    task_type=TaskType.CAUSAL_LM,
    r=8,            # LoRA rank
    lora_alpha=32,  # 縮放參數
    lora_dropout=0.1,
    target_modules=["q_proj", "v_proj", "k_proj", "o_proj"],
)

model = get_peft_model(model, lora_config)
model.print_trainable_parameters()
# 輸出：trainable params: 4,194,304 / total params: 8,000,000,000 = 0.05%
```

LoRA 僅訓練約 0.1-1% 的參數，在單張 GPU 上即可微調 8B 模型。

## 訓練循環

使用 HuggingFace Trainer 進行微調：

```python
from transformers import TrainingArguments, Trainer

training_args = TrainingArguments(
    output_dir="./lora-llm-output",
    per_device_train_batch_size=4,
    gradient_accumulation_steps=8,
    num_train_epochs=3,
    learning_rate=2e-4,
    fp16=True,
    logging_steps=10,
    save_strategy="epoch",
    evaluation_strategy="epoch",
    report_to="wandb",  # 使用 Weights & Biases 監控
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    tokenizer=tokenizer,
    data_collator=lambda data: {
        'input_ids': torch.stack([d['input_ids'] for d in data]),
        'attention_mask': torch.stack([d['attention_mask'] for d in data]),
        'labels': torch.stack([d['input_ids'] for d in data]),
    }
)

trainer.train()
trainer.save_model("./final-lora-model")
```

## 超參數調校

關鍵超參數建議：

| 參數 | 全參數微調 | LoRA |
|------|-----------|------|
| Learning Rate | 1e-5 ~ 5e-5 | 1e-4 ~ 5e-4 |
| Batch Size | 取決於 GPU 記憶體 | 可較大 |
| LoRA Rank (r) | — | 8 ~ 64 |
| LoRA Alpha | — | 16 ~ 64 |
| Epochs | 2 ~ 5 | 1 ~ 5 |

## 評估方法

微調後的模型需要從多個面向評估：

```python
from datasets import load_metric

def evaluate_model(model, tokenizer, test_dataset):
    model.eval()
    predictions = []
    references = []

    for example in test_dataset:
        prompt = example["prompt"]
        inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=512,
                temperature=0.7
            )
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        predictions.append(response)
        references.append(example["expected"])

    # 計算 ROUGE 分數
    rouge = load_metric("rouge")
    results = rouge.compute(
        predictions=predictions, references=references
    )
    return results
```

## 常見問題與解決方案

- **災難性遺忘**：在微調資料中混合 10-20% 的通用資料
- **過度擬合**：使用 LoRA dropout、early stopping、資料擴增
- **GPU 記憶體不足**：使用 gradient checkpointing、quantization、LoRA

## 參考資源

- [HuggingFace PEFT 官方文件](https://www.google.com/search?q=huggingface+peft+lora+documentation)
- [LoRA 原始論文](https://www.google.com/search?q=LoRA+Low-Rank+Adaptation+paper)
- [微調最佳實務](https://www.google.com/search?q=LLM+fine-tuning+best+practices+guide)
