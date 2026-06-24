# Transformer 效能優化

## 前言

大型 Transformer 模型計算代價高昂。本文介紹各種優化技術來提升效能。

---

## 一、模型量化

### INT8 量化

```python
import torch
from transformers import AutoModelForSequenceClassification

# 載入並量化
model = AutoModelForSequenceClassification.from_pretrained(
    "bert-base-uncased",
    load_in_8bit=True
)
```

### 動態量化

```python
model = AutoModelForSequenceClassification.from_pretrained("bert-base-uncased")

# 動態量化（訓練後）
quantized_model = torch.quantization.quantize_dynamic(
    model,
    {torch.nn.Linear},
    dtype=torch.qint8
)
```

### 量化效果

| 格式 | 記憶體 | 速度 | 精度損失 |
|------|--------|------|---------|
| FP32 | 1x | 1x | - |
| FP16 | 0.5x | ~1.5x | 輕微 |
| INT8 | 0.25x | ~2-4x | 中等 |
| INT4 | 0.125x | ~4-8x | 較大 |

---

## 二、知識蒸餾

### 基本蒸餾

```python
class DistillationTrainer:
    def __init__(self, teacher, student, temperature=2.0, alpha=0.5):
        self.teacher = teacher
        self.student = student
        self.temperature = temperature
        self.alpha = alpha
    
    def distillation_loss(self, student_logits, teacher_logits, labels):
        # KL 散度損失
        soft_teacher = torch.softmax(teacher_logits / self.temperature, dim=-1)
        soft_student = torch.log_softmax(student_logits / self.temperature, dim=-1)
        kl_loss = torch.nn.functional.kl_div(soft_student, soft_teacher, reduction='batchmean')
        
        # 硬目標損失
        ce_loss = torch.nn.functional.cross_entropy(student_logits, labels)
        
        return self.alpha * (self.temperature ** 2) * kl_loss + (1 - self.alpha) * ce_loss
```

### DistilBERT 蒸餾

```python
# DistilBERT：6 層蒸餾自 12 層 BERT
# 參數減少 40%，速度提升 60%，保留 97% 效能
```

---

## 三、模型剪枝

### 結構化剪枝

```python
def prune_heads(model, heads_to_prune):
    """
    heads_to_prune: dict of {layer_num: [head_indices]}
    """
    for layer, heads in heads_to_prune.items():
        model.bert.encoder.layer[layer].attention.self.prune_heads(heads)
```

### 重要性評估

```python
def compute_head_importance(model, dataloader):
    importance = {}
    # 計算每個頭對損失的梯度
    # ...
    return importance
```

---

## 四、知識蒸餾變體

### TinyBERT

| 層數 | 隱藏維度 | 參數 |
|------|---------|------|
| BERT-base | 12 | 1.1 億 |
| TinyBERT | 4 | 1400 萬 |

### MiniLM

- 蒸餾最後一層 Transformer
- 保留主要語義能力

---

## 五、推論加速

### ONNX Runtime

```python
import torch
from transformers import AutoModel
from onnxruntime import InferenceSession

# 匯出為 ONNX
model = AutoModel.from_pretrained("bert-base-uncased")
model.eval()

input_ids = torch.randint(0, 1000, (1, 128))
torch.onnx.export(
    model,
    input_ids,
    "bert.onnx",
    input_names=["input_ids"],
    output_names=["output"]
)

# 使用 ONNX Runtime 推論
session = InferenceSession("bert.onnx")
result = session.run(None, {"input_ids": input_ids.numpy()})
```

### TorchScript

```python
model = AutoModel.from_pretrained("bert-base-uncased")
model.eval()

# TorchScript 追蹤
traced_model = torch.jit.trace(model, input_ids)
traced_model.save("bert_traced.pt")
```

---

## 六、硬體加速

### GPU 優化

```python
# 混合精度訓練
from torch.cuda.amp import autocast, GradScaler

scaler = GradScaler()

for batch in dataloader:
    with autocast():
        outputs = model(**batch)
        loss = outputs.loss
    
    scaler.scale(loss).backward()
    scaler.step(optimizer)
    scaler.update()
```

### Batch 優化

```python
# 動態 batch
def dynamic_batch_inference(examples, model, max_batch_size=32):
    results = []
    for i in range(0, len(examples), max_batch_size):
        batch = examples[i:i+max_batch_size]
        batch_results = model(batch)
        results.extend(batch_results)
    return results
```

---

## 七、緩存優化

### KV Cache (解碼時)

```python
# GPT-2 解碼時使用 KV Cache
# 避免重複計算已生成的 token
```

### 模型快取

```python
from transformers import AutoModelForCausalLM

# 使用快取
model = AutoModelForCausalLM.from_pretrained("gpt2", use_cache=True)
```

---

## 結語

Transformer 效能優化是部署大型模型的關鍵。量化、蒸餾、剪枝等技術可以顯著減少計算和記憶體需求，同時保持可接受的精度。

---

*延伸閱讀：[transformer+model+optimization+techniques+2020](https://www.google.com/search?q=transformer+model+optimization+quantization+distillation+2020)*