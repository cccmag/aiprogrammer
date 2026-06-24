# 神經網路剪枝與蒸餾技術

## 前言

深度學習模型越來越大，但部署環境往往資源有限。神經網路剪枝（Pruning）和蒸餾（Distillation）是兩種主要的模型壓縮技術，讓大型模型可以在邊緣設備上運行。

## 為什麼需要模型壓縮？

### 模型規模 vs 部署環境

```
模型規模增長趨勢：
────────────────────────────────

2012 AlexNet:     60M 參數
2014 VGG:        138M 參數
2017 BERT:       340M 參數
2020 GPT-3:    175,000M 參數  ◄───── 1750 億

部署環境限制：
├── 行動裝置：記憶體有限、計算能力弱
├── IoT 設備：嵌入式晶片、低功耗需求
├── 邊緣運算：延遲敏感、即時反應
└── 使用者裝置：沒有 GPU
```

### 壓縮的價值

```
壓縮效果：
────────────────────────────────

原始模型  ──►  剪枝蒸餾  ──►  輕量模型

大小：   500MB     →     50MB      (10x 小)
速度：   100ms    →     10ms      (10x 快)
精度：   95%      →     94%       (幾乎不變)
功耗：   高       →     低        (適合行動裝置)
```

## 神經網路剪枝

### 剪枝的類型

```
剪枝分類：
────────────────────────────────

1. 非結構化剪枝（Unstructured）
   └── 移除個別權重
   └── 精度高，但硬體加速困難

2. 結構化剪枝（Structured）
   ├── 移除整個神經元
   ├── 移除整個卷積核
   └── 硬體友好，容易加速
```

### Magnitude-based Pruning

最簡單有效的剪枝方法：

```python
import torch
import torch.nn as nn

def magnitude_pruning(model, sparsity=0.5):
    """
    幅度剪枝：移除絕對值最小的權重
    
    參數：
    - model: 要剪枝的模型
    - sparsity: 剪枝比例（0.5 = 移除 50% 的權重）
    """
    for name, param in model.named_parameters():
        if 'weight' in name:
            # 計算閾值
            threshold = torch.quantile(
                torch.abs(param.data.flatten()),
                sparsity
            )
            # 建立 mask：小於閾值的設為 0
            mask = torch.abs(param.data) > threshold
            param.data *= mask.float()
    
    return model
```

### Lottery Ticket Hypothesis

彩票假說：網路中總是存在一組「幸運」的初始權重，可以單獨訓練達到原始網路的精度：

```python
# 彩票假說訓練流程

def lottery_ticket_training(model, train_loader, test_loader):
    # 1. 訓練原始網路到收斂
    model = train(model, train_loader)
    
    # 2. 剪枝：保留重要連接
    pruned_model = magnitude_pruning(model, sparsity=0.5)
    
    # 3. 重置剩餘權重到初始值
    pruned_model.reset_to_original_weights()
    
    # 4. 只訓練剪枝後的結構
    pruned_model = train(pruned_model, train_loader)
    
    return pruned_model
```

### 迭代剪枝

避免一次性大量剪枝導致精度崩潰：

```python
def iterative_pruning(model, train_loader, target_sparsity=0.9, steps=10):
    """
    迭代剪枝：分多次逐步增加剪枝比例
    """
    current_sparsity = 0.0
    sparsity_step = target_sparsity / steps
    
    for step in range(steps):
        # 訓練
        model = train(model, train_loader)
        
        # 增加剪枝比例
        current_sparsity += sparsity_step
        model = magnitude_pruning(model, current_sparsity)
        
        print(f"Step {step+1}: Sparsity={current_sparsity:.2%}")
    
    return model
```

## 模型蒸餾

### 蒸餾原理

蒸餾（Knowledge Distillation）利用大型教師模型的「暗知識」來訓練小型學生模型：

```
蒸餾過程：
────────────────────────────────

教師模型（大型）：
  輸入：「這是什麼？」
  輸出：dog: 0.92, cat: 0.05, car: 0.03
                    │
                    ▼ 軟標籤（暗知識）
  學生模型學習：
  - 不只學習正確答案
  - 還學習錯誤答案的相對概率
                    │
                    ▼
學生模型（小型）：
  輸入：「這是什麼？」
  輸出：dog: 0.91, cat: 0.06, car: 0.03
  （用更少的參數達到接近的精度）
```

### 蒸餾實現

```python
import torch
import torch.nn.functional as F

class DistillationLoss(nn.Module):
    def __init__(self, temperature=4.0, alpha=0.5):
        super().__init__()
        self.temperature = temperature  # 蒸餾溫度
        self.alpha = alpha              # 軟標籤權重
    
    def forward(self, student_logits, teacher_logits, labels):
        # 硬目標（真實標籤）
        hard_loss = F.cross_entropy(student_logits, labels)
        
        # 軟目標（教師輸出）
        soft_loss = F.kl_div(
            F.log_softmax(student_logits / self.temperature, dim=1),
            F.softmax(teacher_logits / self.temperature, dim=1),
            reduction='batchmean'
        ) * (self.temperature ** 2)
        
        # 組合損失
        return self.alpha * hard_loss + (1 - self.alpha) * soft_loss
```

### 實際應用

```python
def distill(teacher, student, train_loader, epochs=50):
    teacher.eval()
    student.train()
    
    criterion = DistillationLoss(temperature=4.0, alpha=0.5)
    optimizer = torch.optim.Adam(student.parameters(), lr=0.001)
    
    for epoch in range(epochs):
        for inputs, labels in train_loader:
            # 教師前向傳播（不計算梯度）
            with torch.no_grad():
                teacher_logits = teacher(inputs)
            
            # 學生前向傳播
            student_logits = student(inputs)
            
            # 計算蒸餾損失
            loss = criterion(student_logits, teacher_logits, labels)
            
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
        
        print(f"Epoch {epoch+1}, Loss: {loss.item():.4f}")
```

## 量化

### 量化原理

將浮點數權重轉換為低位整數：

```
量化位元數 vs 精度：
────────────────────────────────

FP32 (32-bit):  完整精度        - 記憶體：4 bytes
FP16 (16-bit):  半精度          - 記憶體：2 bytes (50% 節省)
INT8 (8-bit):   整數量化        - 記憶體：1 byte  (75% 節省)
INT4 (4-bit):   進一步壓縮      - 記憶體：0.5 byte (87.5% 節省)
```

### 量化實作

```python
def quantize_to_int8(tensor):
    """
    對稱量化到 INT8
    """
    # 計算scale
    max_val = torch.max(torch.abs(tensor))
    scale = max_val / 127.0
    
    # 量化
    quantized = torch.round(tensor / scale)
    quantized = torch.clamp(quantized, -127, 127)
    
    return quantized.to(torch.int8), scale

def dequantize(quantized, scale):
    """
    反量化回浮點數
    """
    return quantized.float() * scale
```

## 延伸閱讀

- [模型剪枝技術綜述](https://www.google.com/search?q=neural+network+pruning+survey+2020)
- [Knowledge Distillation](https://www.google.com/search?q=knowledge+distillation+Hinton)
- [Lottery Ticket Hypothesis](https://www.google.com/search?q=lottery+ticket+hypothesis+Frankle)
- [模型量化技術](https://www.google.com/search?q=neural+network+quantization+INT8)

---

*本篇文章為「AI 程式人雜誌 2020 年 10 月號」文章集錦之一。*