# 對抗性攻擊與防禦

## 從圖像分類到 LLM 的攻防演進（2017-2029）

### 對抗性樣本的起源

2017 年，Goodfellow 等人提出了 Fast Gradient Sign Method（FGSM），開啟了對抗性攻擊的研究領域。其核心思想非常簡單：在輸入上添加人類無法察覺的微小擾動，使模型做出錯誤預測。

```python
def fgsm_attack(model, images, labels, epsilon=0.03):
    """Fast Gradient Sign Method — 最經典的對抗性攻擊"""
    images.requires_grad = True
    outputs = model(images)
    loss = torch.nn.functional.cross_entropy(outputs, labels)
    model.zero_grad()
    loss.backward()
    # 沿著梯度方向添加擾動
    perturbed = images + epsilon * images.grad.sign()
    return torch.clamp(perturbed, 0, 1)
```

### 2020-2024：攻防競賽的白熱化

這段期間攻擊方法快速迭代：

| 年份 | 攻擊方法 | 核心思想 |
|------|---------|---------|
| 2017 | FGSM | 單步梯度攻擊 |
| 2018 | PGD | 多步投影梯度 |
| 2020 | AutoAttack | 集成多種攻擊 |
| 2022 | Patch Attack | 實體世界攻擊 |
| 2024 | Universal LLM Jailbreak | 跨模型通用越獄 |

### PGD 攻擊實現

Projected Gradient Descent 是 FGSM 的多步版本，攻擊效果更強：

```python
def pgd_attack(model, images, labels, epsilon=0.03, alpha=0.01, steps=40):
    """Projected Gradient Descent — 最強的 white-box 攻擊之一"""
    perturbed = images.clone().detach().requires_grad_(True)

    for _ in range(steps):
        outputs = model(perturbed)
        loss = torch.nn.functional.cross_entropy(outputs, labels)
        model.zero_grad()
        loss.backward()

        with torch.no_grad():
            # 梯度上升（最大化 loss）
            perturbed += alpha * perturbed.grad.sign()
            # 投影回 epsilon 球面
            delta = torch.clamp(perturbed - images, -epsilon, epsilon)
            perturbed = torch.clamp(images + delta, 0, 1).requires_grad_(True)

    return perturbed.detach()
```

### 2025-2029：LLM 對抗性攻擊

LLM 的對抗性攻擊與傳統圖像模型完全不同。攻擊者不是修改像素，而是操縱文字提示：

```python
def generate_jailbreak_prompt(target_query: str, iterations: int = 50) -> str:
    """自動化越獄提示生成（使用梯度引導的 token 搜尋）"""
    import torch

    def loss_fn(model, input_ids, target_ids):
        outputs = model(input_ids)
        logits = outputs.logits[:, -target_ids.shape[1]:, :]
        return torch.nn.functional.cross_entropy(
            logits.reshape(-1, logits.size(-1)),
            target_ids.reshape(-1)
        )

    # 初始化對抗性 suffix
    suffix = "!" * 20
    best_suffix = suffix
    best_loss = float("inf")

    for step in range(iterations):
        input_text = f"{suffix}\n{target_query}"
        tokens = tokenizer(input_text, return_tensors="pt")
        target = tokenizer("I will comply", return_tensors="pt").input_ids

        loss = loss_fn(model, tokens.input_ids, target)
        if loss < best_loss:
            best_loss = loss
            best_suffix = suffix

        # Greedy Coordinate Gradient (GCG) 搜尋
        # 逐一替換 suffix 中的 token，選擇使 loss 最小的 token
        for pos in range(len(suffix)):
            candidates = top_k_alternative_tokens(model, tokens, pos, k=256)
            suffix = replace_and_evaluate(suffix, pos, candidates, loss_fn)

    return best_suffix
```

### 防禦策略的演進

對抗性防禦大致可分為四代：

1. **對抗性訓練（2017-2020）**：加入對抗性樣本進行訓練
2. **認證防禦（2020-2023）**：提供數學證明的 robust 保證
3. **輸入淨化（2023-2026）**：使用 diffusion model 重建輸入
4. **行為防禦（2026-2029）**：監控模型行為模式，偵測異常輸出

```python
def adversarial_training(model, dataloader, epsilon=0.03, epochs=10):
    """對抗性訓練 — 第一代防禦"""
    optimizer = torch.optim.Adam(model.parameters())

    for epoch in range(epochs):
        for images, labels in dataloader:
            # 生成對抗性樣本
            adv_images = pgd_attack(model, images, labels, epsilon)
            # 同時在原始和對抗性樣本上訓練
            combined = torch.cat([images, adv_images])
            combined_labels = torch.cat([labels, labels])

            optimizer.zero_grad()
            outputs = model(combined)
            loss = torch.nn.functional.cross_entropy(outputs, combined_labels)
            loss.backward()
            optimizer.step()
```

### 關鍵洞察

對抗性攻擊的本質是模型在高維空間中的線性行為——即使在非線性模型中，局部線性區域仍然存在。這解釋了為什麼對抗性樣本如此容易產生，又如此難以徹底防禦。

---

**下一步**：[模型竊取與反向工程](focus3.md)

## 延伸閱讀

- [Explaining and Harnessing Adversarial Examples](https://www.google.com/search?q=Goodfellow+adversarial+examples+FGSM)
- [Towards Deep Learning Models Resistant to Adversarial Attacks](https://www.google.com/search?q=PGD+adversarial+training+Madry)
- [Universal and Transferable Adversarial Attacks](https://www.google.com/search?q=universal+adversarial+perturbations)
