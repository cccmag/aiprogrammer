# 對抗性樣本生成與防禦

## 概述

對抗性樣本（Adversarial Examples）是透過在輸入資料中加入人眼難以察覺的擾動，導致 AI 模型產生錯誤輸出。本文介紹常見的生成方法與防禦策略。

## 對抗性樣本生成方法

### Fast Gradient Sign Method (FGSM)

FGSM 透過損失函數對輸入的梯度方向加入擾動：

```python
import torch
import torch.nn as nn

def fgsm_attack(model, x, y, eps=0.03):
    x.requires_grad = True
    output = model(x)
    loss = nn.CrossEntropyLoss()(output, y)
    model.zero_grad()
    loss.backward()
    perturbation = eps * x.grad.sign()
    x_adv = x + perturbation
    return torch.clamp(x_adv, 0, 1)
```

### Projected Gradient Descent (PGD)

PGD 是更強大的迭代式攻擊方法：

```python
def pgd_attack(model, x, y, eps=0.03, alpha=0.01, steps=40):
    x_adv = x.clone().detach() + torch.randn_like(x) * 0.001
    for _ in range(steps):
        x_adv.requires_grad = True
        output = model(x_adv)
        loss = nn.CrossEntropyLoss()(output, y)
        model.zero_grad()
        loss.backward()
        grad = x_adv.grad.sign()
        x_adv = x_adv + alpha * grad
        delta = torch.clamp(x_adv - x, -eps, eps)
        x_adv = torch.clamp(x + delta, 0, 1).detach()
    return x_adv
```

## 防禦策略

### 對抗性訓練（Adversarial Training）

將對抗性樣本加入訓練資料中：

```python
def adversarial_training(model, loader, optimizer, epochs=10):
    for epoch in range(epochs):
        for x, y in loader:
            x_adv = pgd_attack(model, x, y)
            optimizer.zero_grad()
            loss = nn.CrossEntropyLoss()(model(x_adv), y)
            loss += nn.CrossEntropyLoss()(model(x), y)
            loss.backward()
            optimizer.step()
```

### 輸入預處理防禦

透過縮放、壓縮等方式過濾擾動：

```python
import torch.nn.functional as F

def median_smoothing(x, kernel_size=3):
    return F.median_pool2d(x, kernel_size, stride=1,
                           padding=kernel_size // 2)
```

## 實戰建議

1. 使用 PGD 訓練作為 baseline
2. 結合多種防禦策略（ensemble defense）
3. 定期使用外部紅隊測試驗證模型魯棒性

參考資料：https://www.google.com/search?q=adversarial+examples+generation+defense+2026
