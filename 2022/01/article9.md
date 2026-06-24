# 遷移學習與預訓練

## 為什麼需要遷移學習？

訓練深度神經網路需要大量標註資料和計算資源。ImageNet 的 1400 萬張圖像需要數週在數百個 GPU 上訓練。對於大多數開發者來說，從零開始訓練是不現實的。

遷移學習（Transfer Learning）的核心理念是：利用在大型資料集上預訓練的模型，將其知識遷移到新任務上。

## 預訓練模型

### 什麼是預訓練？

預訓練是在大型通用資料集上訓練一個模型，使其學習通用的特徵表示。

```
預訓練階段：
  大規模資料（ImageNet、Wikipedia）
        ↓
  訓練通用模型（ResNet、BERT）
        ↓
  學到通用特徵（邊緣、形狀、語法、語義）

遷移階段：
  通用模型
    ↓
  小規模任務資料
    ↓
  微調（少量訓練）
    ↓
  任務專用模型
```

## 四種遷移策略

### 1. 特徵提取

凍結預訓練模型的所有層，只訓練新添加的分類層：

```python
model = models.resnet18(pretrained=True)

# 凍結所有層
for param in model.parameters():
    param.requires_grad = False

# 替換最後的分類層
model.fc = nn.Linear(512, num_classes)  # 新分類層

# 只訓練新層
optimizer = optim.Adam(model.fc.parameters(), lr=0.001)
```

適用場景：新資料集與預訓練資料集相似，資料量小（數百到數千張）。

### 2. 微調部分層

凍結底層（學習通用特徵），微調高層（學習任務特定特徵）：

```python
model = models.resnet18(pretrained=True)

# 凍結前幾層
for param in model.parameters():
    param.requires_grad = False

# 解凍最後兩個 block
for param in model.layer4.parameters():
    param.requires_grad = True
for param in model.fc.parameters():
    param.requires_grad = True
```

適用場景：新資料集與預訓練資料集有一定差異，資料量中等。

### 3. 完整微調

解凍所有層，使用較小的學習率進行訓練：

```python
model = models.resnet18(pretrained=True)
model.fc = nn.Linear(512, num_classes)

# 使用較小的學習率
optimizer = optim.Adam(model.parameters(), lr=1e-4)
```

適用場景：新資料集規模較大（數萬張以上），或與預訓練資料差異較大。

### 4. 知識蒸餾

使用大模型（教師）指導小模型（學生）學習：

```python
def distillation_loss(student_logits, teacher_logits, labels, T=3.0):
    soft_student = F.log_softmax(student_logits / T, dim=1)
    soft_teacher = F.softmax(teacher_logits / T, dim=1)
    distill_loss = F.kl_div(soft_student, soft_teacher, reduction='batchmean')
    ce_loss = F.cross_entropy(student_logits, labels)
    return 0.5 * distill_loss * T**2 + 0.5 * ce_loss
```

## 電腦視覺的預訓練模型

| 模型 | 預訓練資料集 | 參數量 | 應用 |
|------|-------------|-------|------|
| ResNet-50 | ImageNet | 25M | 通用分類 |
| EfficientNet | ImageNet | 5M-66M | 高效分類 |
| YOLOv5 | COCO | 7M-87M | 目標檢測 |
| Mask R-CNN | COCO | 44M | 實例分割 |

## NLP 的預訓練模型

| 模型 | 預訓練任務 | 參數量 | 特色 |
|------|-----------|-------|------|
| BERT | MLM + NSP | 110M-340M | 雙向上下文 |
| GPT-2 | 語言模型 | 117M-1.5B | 生成能力 |
| RoBERTa | MLM（改良） | 125M-355M | 優化訓練 |
| ALBERT | MLM + SOP | 12M-235M | 參數共享 |

## 微調 NLP 模型

```python
from transformers import BertForSequenceClassification, Trainer

model = BertForSequenceClassification.from_pretrained(
    'bert-base-uncased',
    num_labels=2  # 二分類
)

trainer = Trainer(
    model=model,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    training_args=TrainingArguments(
        output_dir='./results',
        learning_rate=2e-5,
        num_train_epochs=3,
    )
)
trainer.train()
```

## 成功因素

遷移學習成功的關鍵因素：

1. **通用特徵**：預訓練模型學到的底層特徵（邊緣、形狀）對大多數視覺任務通用
2. **資料效率**：微調只需要 1/10 到 1/100 的標註資料
3. **訓練速度**：微調時間通常是從零訓練的 1/10 到 1/100
4. **泛化能力**：預訓練模型提供了正則化效果，減少過擬合

## 注意事項

- **資料分布差異**：如果新任務的資料分布與預訓練資料差異過大，遷移效果可能不好
- **負遷移**：不當的遷移策略可能導致效能下降
- **領域特定模型**：某些領域（醫學影像、衛星圖像）需要領域特定的預訓練模型
- **凍結 vs 微調**：需要根據資料量選擇合適的策略

---

## 延伸閱讀

- [遷移學習綜述](https://www.google.com/search?q=transfer+learning+survey+deep+learning)
- [Hugging Face 預訓練模型庫](https://www.google.com/search?q=Hugging+Face+pretrained+models)
- [PyTorch 遷移學習教學](https://www.google.com/search?q=PyTorch+transfer+learning+tutorial)

*本篇文章為「AI 程式人雜誌 2022 年 1 月號」精選文章。*
