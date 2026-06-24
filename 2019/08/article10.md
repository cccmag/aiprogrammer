# 神經網路搜尋（NAS）自動化模型設計

## 前言

神經網路搜尋（Neural Architecture Search, NAS）是一種自動設計神經網路架構的技術。2019 年，這個領域取得了顯著進展。

## NAS 的基本流程

### 搜索空間

```python
search_space = {
    'num_layers': [4, 8, 12, 16],
    'kernel_size': [3, 5, 7],
    'num_filters': [32, 64, 128, 256],
    'activation': ['relu', 'swish']
}
```

### 搜索策略

```python
# 常見的搜索策略

# 1. 隨機搜索
architecture = random_search(search_space)

# 2. 強化學習
architecture = rl_search(controller)

# 3. 梯度方法 (DARTS)
architecture = gradient_based_search()
```

---

## 主流方法

### DARTS

Differentiable Architecture Search (DARTS) 是 2019 年最重要的 NAS 方法之一：

```python
# DARTS 的核心思想
# 將離散的架構選擇放鬆為連續的機率

# 網路權重 w 和架構參數 α 交替優化
for epoch in range(num_epochs):
    # 更新網路權重
    w = w - lr_w * d_loss / dw

    # 更新架構參數
    α = α - lr_α * d_loss / dα
```

---

## 應用

### 影像分類

NAS 設計的模型在 ImageNet 上達到了 SOTA。

### 目標檢測

AutoML 目標檢測網路。

---

## 結語

NAS 展示了自動化模型設計的潛力，但也带来了計算成本高的問題。未來需要在效率和性能之間找到平衡。

---

**延伸閱讀**

- [NAS+Neural+Architecture+Search](https://www.google.com/search?q=neural+architecture+search+2019)
- [DARTS+paper](https://www.google.com/search?q=DARTS+differentiable+architecture+search)