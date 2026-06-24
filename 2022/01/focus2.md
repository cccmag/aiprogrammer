# 反向傳播演算法

## 從 XOR 困境到多層網路

XOR 困境的解決方案很直觀：使用多層網路。但在 1986 年之前，沒有人知道如何有效地訓練多層網路。反向傳播演算法的出現改變了這一切。

反向傳播（Backpropagation）的核心思想是：利用鏈式法則，從輸出層向輸入層逐層計算損失函數對每個權重的梯度。

## 鏈式法則

鏈式法則是微積分的基本法則，用於計算複合函數的導數：

```
若 z = f(y), y = g(x)
則 dz/dx = (dz/dy)·(dy/dx) = f'(y)·g'(x)
```

在多層網路中，損失函數 L 是輸出 a^(L) 的函數，而 a^(L) 又是權重 w^(L) 和前一層輸出 a^(L-1) 的函數。因此：

```
∂L/∂w^(L) = (∂L/∂a^(L)) · (∂a^(L)/∂z^(L)) · (∂z^(L)/∂w^(L))
```

其中 z^(L) = w^(L)·a^(L-1) + b^(L) 是加權和，a^(L) = σ(z^(L)) 是啟用值。

## 四條基本方程式

反向傳播可以用四條方程式概括。令 δ^(l)_j 為第 l 層第 j 個神經元的誤差：

**方程式 1：輸出層誤差**
```
δ^(L)_j = ∂L/∂a^(L)_j · σ'(z^(L)_j)
```

對於均方誤差 L = (1/2)·Σ(a_j - y_j)²：
```
δ^(L)_j = (a^(L)_j - y_j) · σ'(z^(L)_j)
```

**方程式 2：反向傳播誤差**
```
δ^(l) = ((w^(l+1))^T · δ^(l+1)) ⊙ σ'(z^(l))
```

其中 ⊙ 表示 Hadamard 乘積（逐元素相乘）。

**方程式 3：權重梯度**
```
∂L/∂w^(l)_jk = δ^(l)_j · a^(l-1)_k
```

**方程式 4：偏置梯度**
```
∂L/∂b^(l)_j = δ^(l)_j
```

## 演算法流程

```python
def train_one_step(X, y, model):
    # 1. 前向傳播
    activations = [X]
    for layer in model.layers:
        z = layer.W @ activations[-1] + layer.b
        a = activation(z)
        activations.append(a)
    
    # 2. 計算輸出層誤差
    delta = (activations[-1] - y) * activation_prime(z)
    
    # 3. 反向傳播
    for l in range(len(model.layers)-1, 0, -1):
        # 儲存權重梯度
        model.layers[l].W_grad = delta @ activations[l].T
        model.layers[l].b_grad = delta
        # 傳播到前一層
        delta = (model.layers[l].W.T @ delta) * activation_prime(z_prev)
    
    # 4. 梯度下降更新
    for layer in model.layers:
        layer.W -= learning_rate * layer.W_grad
        layer.b -= learning_rate * layer.b_grad
```

## 梯度下降更新

反向傳播計算出梯度後，使用梯度下降更新權重：

```
w ← w - η · ∂L/∂w
b ← b - η · ∂L/∂b
```

### 隨機梯度下降（SGD）

在大規模資料集上，每次使用所有樣本計算梯度不現實。隨機梯度下降每次只用一個樣本更新：

```python
for x, y in dataset:
    grads = backpropagation(model, x, y)
    update(model, grads, lr)
```

### 小批量梯度下降（Mini-batch SGD）

實際中最常用的折衷方案：

```python
for batch in dataloader(dataset, batch_size=32):
    grads = average_gradients(model, batch)
    update(model, grads, lr)
```

## 常見問題

1. **局部最小值**：非凸損失函數可能存在多個局部最小值，但在高維空間中，局部最小值通常不是大問題

2. **梯度消失**：使用 Sigmoid 時，深層網路的梯度會趨近於零（將在 focus6 詳細討論）

3. **學習率選擇**：學習率太小收斂慢，太大則可能震盪或不收斂

---

## 延伸閱讀

- [Rumelhart Hinton Williams 1986](https://www.google.com/search?q=Rumelhart+Hinton+Williams+backpropagation+1986)
- [反向傳播推導](https://www.google.com/search?q=backpropagation+derivation+step+by+step)
- [Neural Networks and Deep Learning](https://www.google.com/search?q=Neural+Networks+and+Deep+Learning+Michael+Nielsen)

*本篇文章為「AI 程式人雜誌 2022 年 1 月號」歷史回顧系列之一。*
