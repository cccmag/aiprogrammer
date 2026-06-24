# 梯度消失與解決方案

## 問題描述

梯度消失（Vanishing Gradient）是訓練深層神經網路時最常見的難題。當網路層數增加時，靠近輸入層的權重梯度會變得極小，導致這些層幾乎無法學習。

### 為什麼會發生？

以 Sigmoid 為啟用函數的深層網路為例：

```
δ^(l) = ((w^(l+1))^T · δ^(l+1)) ⊙ σ'(z^(l))
```

Sigmoid 的導數最大為 0.25：

```
σ'(x) = σ(x)·(1-σ(x))
最大值：σ'(0) = 0.5·0.5 = 0.25
```

每經過一層，梯度至少縮小 0.25 倍。經過 10 層後：

```
梯度 ≈ (0.25)^10 ≈ 9.5 × 10^(-7)
```

這樣的梯度幾乎無法推動權重更新。

### 視覺化

```
梯度大小
│
│   輸出層 ████████████
│   層 9  █████████
│   層 8  ███████
│   層 7  █████
│   層 6  ███
│   層 5  ██
│   層 4  █
│   層 3  ▄
│   層 2  ▂
│   層 1  ▁
└─────────────────── 深度
```

## 梯度爆炸

與梯度消失相對的是梯度爆炸（Exploding Gradient）——梯度變得非常大，導致權重更新過大，網路無法收斂。這在 RNN 中尤為常見。

梯度爆炸的解決方案包括梯度裁剪：

```python
def clip_gradient(grads, max_norm=1.0):
    total_norm = sum(np.sum(g**2) for g in grads) ** 0.5
    if total_norm > max_norm:
        scale = max_norm / (total_norm + 1e-6)
        grads = [g * scale for g in grads]
    return grads
```

## 解決方案一：更好的初始化

### Xavier 初始化

Glorot 和 Bengio 在 2010 年提出 Xavier 初始化，考慮前向和反向傳播的方差：

```python
# Xavier 初始化
limit = math.sqrt(6.0 / (n_in + n_out))
W = np.random.uniform(-limit, limit, (n_out, n_in))
```

適用於 Sigmoid 和 Tanh。

### He 初始化

He 等人在 2015 年針對 ReLU 提出：

```python
# He 初始化
std = math.sqrt(2.0 / n_in)
W = np.random.randn(n_out, n_in) * std
```

## 解決方案二：ReLU 系列啟用函數

ReLU 在正半軸梯度為 1，不會縮小梯度。針對 Dead ReLU，後續提出了：

```python
# Leaky ReLU
def leaky_relu(x, alpha=0.01):
    return x if x > 0 else alpha * x

# ELU
def elu(x, alpha=1.0):
    return x if x > 0 else alpha * (math.exp(x) - 1)
```

## 解決方案三：殘差連接（Residual Connection）

ResNet 在 2015 年提出了殘差連接，讓梯度可以直接流過：

```
傳統網路：y = F(x)
殘差網路：y = F(x) + x
```

```
傳統網路：
x → [Conv] → [ReLU] → [Conv] → ReLU → y
   梯度衰減             梯度更小

殘差網路：
x ──→ [Conv] → [ReLU] → [Conv] → ──→ ReLU → y
    │                               ↑
    └─────────── 捷徑連接 ──────────┘
   梯度可以直接流回
```

這使得訓練 100+ 層的網路成為可能。

## 解決方案四：Batch Normalization

如 focus5 所述，BN 通過歸一化每層輸入，使梯度保持在有效範圍內。

## 解決方案五：LSTM/GRU

對於 RNN 的梯度問題，LSTM（長短期記憶）和 GRU（門控循環單元）引入了門控機制：

```
f_t = σ(W_f · [h_(t-1), x_t] + b_f)   # 遺忘門
i_t = σ(W_i · [h_(t-1), x_t] + b_i)   # 輸入門
o_t = σ(W_o · [h_(t-1), x_t] + b_o)   # 輸出門
C_t = f_t ⊙ C_(t-1) + i_t ⊙ tanh(W_c · [h_(t-1), x_t] + b_c)
h_t = o_t ⊙ tanh(C_t)
```

## 歷史影響

梯度消失問題是 2000 年代深層網路難以訓練的主要原因。直到 2010-2015 年間上述解決方案陸續提出後，深度學習才真正起飛。

| 時間 | 突破 | 影響 |
|------|------|------|
| 2010 | Xavier 初始化 | 改善梯度流 |
| 2011 | ReLU | 消除正域梯度消失 |
| 2015 | BatchNorm | 穩定訓練 |
| 2015 | ResNet | 殘差連接 |
| 2015 | 梯度裁剪 | 防止梯度爆炸 |

---

## 延伸閱讀

- [Vanishing Gradient Problem](https://www.google.com/search?q=vanishing+gradient+problem+deep+learning)
- [ResNet 論文 2015](https://www.google.com/search?q=Deep+Residual+Learning+for+Image+Recognition)
- [LSTM 論文 1997](https://www.google.com/search?q=Long+Short-Term+Memory+Hochreiter)

*本篇文章為「AI 程式人雜誌 2022 年 1 月號」歷史回顧系列之一。*
