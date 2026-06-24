# 語言模型微調技巧

## 微調流程

微調是將預訓練模型適應特定任務的關鍵步驟。

```python
from transformers import GPT2LMHeadModel, GPT2Tokenizer, Trainer, TrainingArguments

tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2")

# 準備資料
train_encodings = tokenizer(train_texts, truncation=True, padding=True, max_length=512)
```

## Trainer API

```python
training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=3,
    per_device_train_batch_size=4,
    per_device_eval_batch_size=4,
    warmup_steps=500,
    weight_decay=0.01,
    logging_dir="./logs",
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
)

trainer.train()
```

## 學習率排程

```python
from transformers import get_linear_schedule_with_warmup

optimizer = torch.optim.AdamW(model.parameters(), lr=5e-5)
total_steps = len(train_loader) * num_epochs
scheduler = get_linear_schedule_with_warmup(
    optimizer, num_warmup_steps=500, num_training_steps=total_steps
)
```

## 梯度累積

當 GPU 記憶體不足時，使用梯度累積：

```python
gradient_accumulation_steps = 4
effective_batch_size = batch_size * gradient_accumulation_steps

for step, batch in enumerate(train_loader):
    outputs = model(**batch)
    loss = outputs.loss / gradient_accumulation_steps
    loss.backward()
    
    if (step + 1) % gradient_accumulation_steps == 0:
        optimizer.step()
        scheduler.step()
        optimizer.zero_grad()
```

## 混合精度訓練

使用 FP16 加速訓練（需要 AMP）：

```python
from torch.cuda.amp import autocast, GradScaler

scaler = GradScaler()

for batch in train_loader:
    with autocast():
        outputs = model(**batch)
        loss = outputs.loss
    
    scaler.scale(loss).backward()
    scaler.step(optimizer)
    scaler.update()
```

## 早停策略

```python
from transformers import EarlyStoppingCallback

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    callbacks=[EarlyStoppingCallback(early_stopping_patience=3)]
)
```

## 參考資源

- https://www.google.com/search?q= GPT-2+BERT+fine-tuning+tutorial+PyTorch+2020
- https://www.google.com/search?q=transformers+Trainer+API+training+arguments+best+practices
- https://www.google.com/search?q=mixed+precision+FP16+training+deep+learning+gradient+accumulation