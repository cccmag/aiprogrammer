# RLHF 實戰

## 從語言模型到人類偏好

RLHF（Reinforcement Learning from Human Feedback）是 ChatGPT 背後的關鍵技術。它解決了純語言模型只學到「文字接龍」而非「有用回覆」的問題。RLHF 分為三個階段：SFT、Reward Model、PPO 微調。

## 第一階段：監督式微調（SFT）

收集高品質的人類示範資料，對預訓練語言模型進行監督式微調：

```python
from transformers import AutoModelForCausalLM, AutoTokenizer, Trainer

model = AutoModelForCausalLM.from_pretrained("gpt2")
tokenizer = AutoTokenizer.from_pretrained("gpt2")

def tokenize_function(examples):
    return tokenizer(
        ["<prompt>" + p + "<response>" + r for p, r
         in zip(examples["prompt"], examples["response"])],
        truncation=True, padding="max_length", max_length=512)

trainer = Trainer(
    model=model,
    train_dataset=dataset.map(tokenize_function, batched=True),
    args=TrainingArguments(output_dir="./sft_model", num_train_epochs=3))
trainer.train()
```

## 第二階段：獎勵模型訓練

人類對多個模型輸出進行偏好排序，訓練 Reward Model 來預測人類偏好：

```python
import torch
import torch.nn as nn

class RewardModel(nn.Module):
    def __init__(self, base_model):
        super().__init__()
        self.base_model = base_model
        self.reward_head = nn.Linear(
            base_model.config.hidden_size, 1)

    def forward(self, input_ids, attention_mask):
        outputs = self.base_model(
            input_ids, attention_mask=attention_mask,
            output_hidden_states=True)
        hidden = outputs.hidden_states[-1][:, -1, :]
        return self.reward_head(hidden).squeeze(-1)

# Bradley-Terry preference loss
def preference_loss(chosen_reward, rejected_reward):
    return -torch.log(torch.sigmoid(chosen_reward - rejected_reward)).mean()
```

## 第三階段：PPO 微調

用 PPO 演算法以 Reward Model 為回饋，微調語言模型：

```python
from transformers import AutoModelForCausalLM
from trl import PPOConfig, PPOTrainer, AutoModelForSeq2SeqLMWithValueHead

model = AutoModelForCausalLM.from_pretrained("./sft_model")
model = AutoModelForSeq2SeqLMWithValueHead.from_pretrained(model)
ref_model = AutoModelForCausalLM.from_pretrained("./sft_model")
reward_model = RewardModel.load_from_checkpoint("./reward_model")

config = PPOConfig(
    model_name="./sft_model", learning_rate=1.41e-5,
    batch_size=16, ppo_epochs=4)

ppo_trainer = PPOTrainer(
    config, model, ref_model, tokenizer)

for prompt in dataset["prompt"]:
    # Generate response
    response = ppo_trainer.generate(prompt)
    # Get reward
    reward = reward_model(prompt, response)
    # PPO step
    train_stats = ppo_trainer.step([prompt], [response], [reward])
```

## KL 懲罰的重要性

RLHF 的 PPO 階段必須加入 KL 散度懲罰，防止模型偏離 SFT 模型太遠而產生亂碼：

```python
# PPO objective with KL penalty
kl_penalty = -beta * kl_divergence(
    policy_log_probs, ref_log_probs)
ppo_loss = -advantage * ratio + kl_penalty
```

## 結語

RLHF 讓語言模型從「模仿人類文字」進化為「滿足人類偏好」。2024 年後的 DPO（Direct Preference Optimization）更簡化了這個流程，但理解經典 RLHF 仍是掌握對齊技術的基礎。


**延伸閱讀**
- [Training language models to follow instructions](https://www.google.com/search?q=InstructGPT+RLHF+OpenAI+2022)
- [Learning to summarize from human feedback](https://www.google.com/search?q=RLHF+summarization+OpenAI)
- [Direct Preference Optimization](https://www.google.com/search?q=DPO+preference+optimization+Rafailov+2023)
