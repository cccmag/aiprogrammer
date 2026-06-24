# 模型蒸餾策略比較

## 蒸餾的基本框架

知識蒸餾（Knowledge Distillation）讓一個小型學生模型模仿大型教師模型的輸出行為。核心損失函數為：

$$L = \alpha \cdot L_{hard} + (1-\alpha) \cdot L_{soft}$$

其中 $L_{soft}$ 比較教師與學生的 softmax 輸出（使用溫度參數 $T$ 控制機率分布的平滑度）。

## 蒸餾策略實作

```python
import math
import random

def softmax_with_temperature(logits, temperature=1.0):
    max_v = max(logits)
    exps = [math.e ** ((l - max_v) / temperature) for l in logits]
    total = sum(exps)
    return [e / total for e in exps]

def distillation_loss(student_logits, teacher_logits, labels, T=4.0, alpha=0.7):
    soft_teacher = softmax_with_temperature(teacher_logits, T)
    soft_student = softmax_with_temperature(student_logits, T)

    # KL divergence (soft loss)
    kl = -sum(st * math.log(ss / st + 1e-10)
              for st, ss in zip(soft_teacher, soft_student))

    # Cross entropy (hard loss)
    ce = -math.log(softmax_with_temperature(student_logits)[labels] + 1e-10)

    return alpha * T * T * kl + (1 - alpha) * ce
```

## 三種主要策略

### 1. 黑盒蒸餾（Black-box KD）

僅使用教師模型的輸出機率分布。最簡單，但資訊量有限：

```python
class BlackBoxDistiller:
    def train_step(self, student, teacher, data):
        for x, label in data:
            teacher_logits = teacher.predict(x)
            student_logits = student.predict(x)
            loss = distillation_loss(student_logits, teacher_logits, label)
            student.update(loss)
```

### 2. 白盒蒸餾（White-box KD）

存取教師模型的**中間層特徵圖**。學生不僅模仿最終輸出，也模仿內部表示：

```python
class WhiteBoxDistiller:
    def layerwise_loss(self, student_feats, teacher_feats):
        total = 0.0
        for sf, tf in zip(student_feats, teacher_feats):
            total += sum((a - b)**2 for a, b in zip(sf, tf))
        return total / len(student_feats)
```

### 3. 自我蒸餾（Self-Distillation）

同一個模型在不同訓練階段之間相互學習，不需要獨立教師：

```python
class SelfDistillation:
    def train(self, model, data, epochs=10):
        for epoch in range(epochs):
            teacher_snapshot = model.copy_params()
            for x, label in data:
                current_logits = model.predict(x)
                teacher_logits = teacher_snapshot.predict(x)
                loss = distillation_loss(current_logits, teacher_logits, label)
                model.update(loss)
```

## 策略比較

| 策略 | 壓縮比 | 所需存取 | 實作難度 |
|------|-------|---------|---------|
| 黑盒 KD | 3-10x | 教師輸出 | 低 |
| 白盒 KD | 5-20x | 中間層 | 中 |
| 自我蒸餾 | 2-5x | 自身參數 | 低 |

## 延伸閱讀

- [知識蒸餾綜述](https://www.google.com/search?q=knowledge+distillation+survey+deep+learning)
- [Hinton 原始蒸餾論文](https://www.google.com/search?q=Hinton+distilling+knowledge+neural+networks)
- [TinyBERT 與蒸餾](https://www.google.com/search?q=TinyBERT+knowledge+distillation)

選擇蒸餾策略需要權衡壓縮比與實作成本。白盒蒸餾效果最好但需修改模型架構；黑盒蒸餾最通用。自我蒸餾則是零成本的輕量方案。
