# Learning Rate Finder：找到最佳學習率

## 前言

Leslie Smith 於 2017 年提出的 Learning Rate Finder 是一種自動找到合適學習率的方法。

## 方法原理

```python
def find_learning_rate(model, train_loader, optimizer_class,
                      start_lr=1e-7, end_lr=10, num_iterations=100):
    """
    Learning Rate Finder 實現

    從很小的學習率開始，逐漸增加
    觀察 loss 的變化，找到 loss 下降最快的點
    """

    model.train()
    optimizer = optimizer_class(model.parameters(), lr=start_lr)

    lrs = []
    losses = []

    # 線性增加學習率
    lr_multiplier = (end_lr / start_lr) ** (1 / num_iterations)

    for iteration, (data, target) in enumerate(train_loader):
        if iteration >= num_iterations:
            break

        # 更新學習率
        current_lr = start_lr * (lr_multiplier ** iteration)
        optimizer.param_groups[0]['lr'] = current_lr

        # 訓練一步
        output = model(data)
        loss = F.cross_entropy(output, target)
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()

        lrs.append(current_lr)
        losses.append(loss.item())

    return lrs, losses
```

## 分析結果

```python
def find_optimal_lr(lrs, losses):
    """
    找到 loss 下降最快的學習率
    """
    # 去掉前面的燒入期和後面的爆炸期
    start_idx = int(len(lrs) * 0.1)
    end_idx = int(len(lrs) * 0.9)

    relevant_lrs = lrs[start_idx:end_idx]
    relevant_losses = losses[start_idx:end_idx]

    # 找到 loss 最小的點
    min_loss_idx = relevant_losses.index(min(relevant_losses))
    optimal_lr = relevant_lrs[min_loss_idx]

    return optimal_lr

# 可視化
def plot_lr_finder(lrs, losses, optimal_lr):
    import matplotlib.pyplot as plt

    plt.figure(figsize=(10, 6))
    plt.plot(lrs, losses)
    plt.axvline(x=optimal_lr, color='r', linestyle='--',
               label=f'Optimal LR: {optimal_lr:.6f}')
    plt.xscale('log')
    plt.xlabel('Learning Rate')
    plt.ylabel('Loss')
    plt.legend()
    plt.grid(True)
    plt.savefig('lr_finder.png')
```

## 實際應用

```python
# 完整的使用流程
def train_with_lr_finder():
    # 1. 建立模型
    model = SimpleModel()

    # 2. 找到最佳學習率
    lrs, losses = find_learning_rate(
        model,
        train_loader,
        optimizer_class=torch.optim.Adam
    )

    # 3. 分析結果
    optimal_lr = find_optimal_lr(lrs, losses)
    print(f"Optimal learning rate: {optimal_lr}")

    # 4. 使用找到的學習率訓練
    optimizer = torch.optim.Adam(model.parameters(), lr=optimal_lr)

    # 或者使用較小的值作為起點
    optimizer = torch.optim.Adam(model.parameters(), lr=optimal_lr * 0.1)

    # 配合 One Cycle LR 使用
    scheduler = torch.optim.lr_scheduler.OneCycleLR(
        optimizer,
        max_lr=optimal_lr,
        epochs=num_epochs,
        steps_per_epoch=len(train_loader)
    )
```

## LR Finder 的價值

```
┌─────────────────────────────────────────────────────────┐
│              Learning Rate Finder 價值                  │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  優點:                                                 │
│  - 自動化，不需要反覆試驗                                │
│  - 直觀，透過圖形可以看到學習率影響                      │
│  - 節省時間                                            │
│                                                         │
│  適用的場景:                                           │
│  - 新資料集                                            │
│  - 新模型架構                                          │
│  - 轉移學習後的微調                                    │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## One Cycle LR

找到最佳學習率後，可以配合 One Cycle 使用：

```python
scheduler = torch.optim.lr_scheduler.OneCycleLR(
    optimizer,
    max_lr=optimal_lr,
    epochs=num_epochs,
    steps_per_epoch=len(train_loader),
    pct_start=0.3,  # 前 30% 的 epoch 用於 warmup
    div_factor=25,   # 初始學習率 = max_lr / 25
    final_div_factor=10000  # 最終學習率 = max_lr / 10000
)
```

---

**延伸閱讀**

- [Cyclical Learning Rates (Smith, 2017)](https://www.google.com/search?q=cyclical+learning+rates+smith+2017)
- [Super-Convergence](https://www.google.com/search?q=super+convergence+smith)
- [LR Finder Implementation](https://www.google.com/search?q=pytorch+lrfinder)

---

*本篇文章為「AI 程式人雜誌 2017 年 11 月號」AI 相關文章之一。*