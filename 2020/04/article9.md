# 知識蒸餾與模型壓縮

## 為什麼要壓縮？

大型語言模型如 GPT-2（15億參數）難以部署在資源受限的設備上。知識蒸餾可以將大模型的知識轉移到小模型。

## 知識蒸餾原理

```python
import torch
import torch.nn as nn

class DistillationLoss(nn.Module):
    def __init__(self, temperature=2.0, alpha=0.5):
        super().__init__()
        self.temperature = temperature
        self.alpha = alpha
        self.ce_loss = nn.CrossEntropyLoss()
        self.kl_loss = nn.KLDivLoss(reduction="batchmean")
    
    def forward(self, student_logits, teacher_logits, labels):
        # 軟目標 loss（蒸餾）
        soft_teacher = torch.softmax(teacher_logits / self.temperature, dim=-1)
        soft_student = torch.log_softmax(student_logits / self.temperature, dim=-1)
        distill_loss = self.kl_loss(soft_student, soft_teacher) * (self.temperature ** 2)
        
        # 硬目標 loss
        hard_loss = self.ce_loss(student_logits, labels)
        
        # 混合 loss
        return self.alpha * distill_loss + (1 - self.alpha) * hard_loss
```

## 量化 (Quantization)

將 FP32 權重轉換為 INT8：

```python
import torch.quantization

model = GPT2LMHeadModel.from_pretrained("gpt2")

# 動態量化
quantized_model = torch.quantization.quantize_dynamic(
    model, {nn.Linear}, dtype=torch.qint8
)
```

## 權重剪枝 (Pruning)

```python
import torch.nn.utils.prune as prune

def prune_model(model, amount=0.3):
    for name, module in model.named_modules():
        if isinstance(module, nn.Linear):
            prune.l1_unstructured(module, name='weight', amount=amount)
    return model

pruned_model = prune_model(model, amount=0.3)
```

## 蒸餾實作流程

```python
def distill(teacher_model, student_model, train_loader, epochs=3):
    optimizer = torch.optim.Adam(student_model.parameters(), lr=1e-4)
    criterion = DistillationLoss(temperature=2.0, alpha=0.5)
    
    for epoch in range(epochs):
        for batch in train_loader:
            teacher_outputs = teacher_model(batch["input_ids"])
            student_outputs = student_model(batch["input_ids"])
            
            loss = criterion(
                student_outputs.logits,
                teacher_outputs.logits,
                batch["labels"]
            )
            
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
    
    return student_model
```

## 模型大小比較

| 方法 | 原始大小 | 壓縮後 | 效能保留 |
|------|---------|--------|---------|
| FP32 | 1.5GB | 1.5GB | 100% |
| INT8 量化 | 1.5GB | ~400MB | ~95% |
| 蒸餾小模型 | 1.5GB | ~300MB | ~90% |
| 剪枝 30% | 1.5GB | ~1GB | ~93% |

## 參考資源

- https://www.google.com/search?q=knowledge+distillation+model+compression+deep+learning+tutorial+2020
- https://www.google.com/search?q=GPT-2+quantization+INT8+pruning+model+size+reduction
- https://www.google.com/search?q=model+compression+distillation+quantization+pruning+efficiency+comparison