# 對抗性樣本生成與防禦

## 前言

對抗性樣本（Adversarial Examples）是 AI 安全領域最經典的攻擊手段之一。攻擊者在原始輸入上加入人眼難以察覺的擾動，就能讓模型做出完全錯誤的預測。隨著深度學習模型廣泛部署於人臉辨識、自動駕駛、醫療診斷等場景，對抗性攻擊的威脅已從學術研究走進現實世界。

## 對抗性樣本生成方法

最常見的生成演算法是 **FGSM（Fast Gradient Sign Method）**，利用梯度資訊產生擾動：

```python
import torch
import torch.nn.functional as F

def fgsm_attack(model, images, labels, epsilon=0.03):
    images.requires_grad = True
    outputs = model(images)
    loss = F.cross_entropy(outputs, labels)
    model.zero_grad()
    loss.backward()
    sign = images.grad.sign()
    perturbed = images + epsilon * sign
    return torch.clamp(perturbed, 0, 1)
```

更強大的攻擊包括 **PGD（Projected Gradient Descent）** 與 **C&W（Carlini-Wagner）**，前者疊代多步 FGSM，後者將攻擊轉化為最佳化問題。

## 防禦策略

對抗性訓練（Adversarial Training）是目前最有效的防禦方法，在訓練過程中即時加入對抗性樣本：

```python
def adversarial_training(model, loader, optimizer, epochs, epsilon=0.03):
    for epoch in range(epochs):
        for images, labels in loader:
            adv_images = fgsm_attack(model, images, labels, epsilon)
            optimizer.zero_grad()
            loss = F.cross_entropy(model(adv_images), labels)
            loss.backward()
            optimizer.step()
```

其他防禦手段包括輸入預處理（JPEG 壓縮、隨機縮放）、特徵去噪、以及基於隨機化的模型整合。

## 實戰建議

在生產環境中部署對抗性防禦時，建議採用**多層防禦**策略：輸入層進行異常檢測，模型層使用對抗性訓練，輸出層加入信心值過濾。定期使用多種攻擊演算法（FGSM、PGD、C&W）對模型進行紅隊測試，確保防禦的有效性。更多資訊可參考 [https://www.google.com/search?q=adversarial+examples+defense+2026](https://www.google.com/search?q=adversarial+examples+defense+2026)。
