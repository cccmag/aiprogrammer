# SGD、Adam、AdamW 比較

## 隨機梯度下降（SGD）

SGD 是最基礎的最佳化演算法，其更新規則為：

```
θ = θ - lr * ∇L(θ)
```

加入動量（Momentum）後的更新方式：
```
v = β * v + (1-β) * ∇L(θ)
θ = θ - lr * v
```

優點：泛化能力強，在大量資料上表現穩定
缺點：收斂速度慢，需要仔細調整學習率

```python
optim.SGD(model.parameters(), lr=0.01, momentum=0.9)
```

## Adam

Adam（Adaptive Moment Estimation）結合了 Momentum 和 RMSProp 的優點：

- 維護梯度的一階動量（mean）和二階動量（variance）
- 對每個參數自適應調整學習率
- 超參數 $\beta_1$（預設 0.9）和 $\beta_2$（預設 0.999）

```
m = β1 * m + (1-β1) * g
v = β2 * v + (1-β2) * g^2
θ = θ - lr * m / (sqrt(v) + ε)
```

優點：收斂快速，對初始學習率較不敏感
缺點：可能導致泛化能力下降，權重衰減實作不正確

```python
optim.Adam(model.parameters(), lr=0.001)
```

## AdamW

AdamW 是 Adam 的改良版本，主要修正了 Adam 中權重衰減的實作方式。

在原始 Adam 中，權重衰減等同於 L2 正則化，但 Adam 的自適應學習率與 L2 正則化會產生不良互動。AdamW 將權重衰減與梯度更新分離：

```
θ = θ - lr * (adaptive_update + weight_decay * θ)
```

優點：更正確的權重衰減，在 Transformer 架構中表現優於 Adam

```python
optim.AdamW(model.parameters(), lr=0.001, weight_decay=0.01)
```

## 實戰建議

| 情境 | 推薦最佳化器 |
|------|-----------|
| 小型資料集、簡單模型 | SGD + Momentum |
| 大型模型、CV | Adam |
| Transformer、NLP | AdamW |
| 泛化優先 | SGD |
| 收斂速度優先 | Adam/AdamW |

## 參考資料

- SGD 論文：https://en.wikipedia.org/wiki/Stochastic_gradient_descent
- Adam 論文：https://arxiv.org/abs/1412.6980
- AdamW (Decoupled Weight Decay)：https://arxiv.org/abs/1711.05101
