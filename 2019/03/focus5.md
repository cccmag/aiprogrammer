# 5. 梯度下降優化

## 梯度下降原理

梯度下降透過沿著損失函數梯度的反方向更新參數，逐步最小化損失。

```
w = w - α * ∂L/∂w
```

其中 α 是學習率（learning rate）。

## 批量梯度下降（Batch GD）

每次使用全部訓練資料計算梯度。

```python
def batch_gradient_descent(X, y, weights, learning_rate, epochs):
    m = len(y)

    for epoch in range(epochs):
        prediction = X.dot(weights)
        error = prediction - y
        gradient = X.T.dot(error) / m
        weights -= learning_rate * gradient

        if epoch % 100 == 0:
            loss = (error ** 2).mean()
            print(f"Epoch {epoch}: Loss = {loss:.6f}")

    return weights
```

## 隨機梯度下降（SGD）

每次使用一個樣本計算梯度。

```python
def sgd(X, y, weights, learning_rate, epochs):
    m = len(y)

    for epoch in range(epochs):
        for i in range(m):
            xi = X[i:i+1]
            yi = y[i:i+1]

            prediction = xi.dot(weights)
            error = prediction - yi
            gradient = xi.T.dot(error)
            weights -= learning_rate * gradient

    return weights
```

## Mini-batch 梯度下降

每次使用一批樣本（通常 32/64/128）計算梯度，結合了效率與穩定性。

```python
def mini_batch_gd(X, y, weights, learning_rate, epochs, batch_size=32):
    m = len(y)

    for epoch in range(epochs):
        indices = np.random.permutation(m)

        for start in range(0, m, batch_size):
            end = min(start + batch_size, m)
            batch_idx = indices[start:end]

            xi = X[batch_idx]
            yi = y[batch_idx]

            prediction = xi.dot(weights)
            error = prediction - yi
            gradient = xi.T.dot(error) / batch_size
            weights -= learning_rate * gradient

    return weights
```

## Momentum

Momentum 累積之前的梯度方向，加速收斂並減少震盪。

```python
def gradient_descent_with_momentum(X, y, weights, learning_rate, momentum, epochs):
    m = len(y)
    velocity = np.zeros_like(weights)

    for epoch in range(epochs):
        prediction = X.dot(weights)
        error = prediction - y
        gradient = X.T.dot(error) / m

        velocity = momentum * velocity - learning_rate * gradient
        weights += velocity

    return weights
```

## RMSProp

RMSProp 自適應調整每個參數的學習率。

```python
def rmsprop(X, y, weights, learning_rate, rho, epsilon, epochs):
    m = len(y)
    cache = np.zeros_like(weights)

    for epoch in range(epochs):
        prediction = X.dot(weights)
        error = prediction - y
        gradient = X.T.dot(error) / m

        cache = rho * cache + (1 - rho) * gradient ** 2
        weights -= learning_rate * gradient / (np.sqrt(cache) + epsilon)

    return weights
```

## Adam（Adaptive Moment Estimation）

Adam 結合 Momentum 與 RMSProp，是目前最常用的優化器。

```python
def adam(X, y, weights, learning_rate, beta1, beta2, epsilon, epochs):
    m = len(y)
    m_t = np.zeros_like(weights)
    v_t = np.zeros_like(weights)

    for epoch in range(epochs):
        prediction = X.dot(weights)
        error = prediction - y
        gradient = X.T.dot(error) / m

        m_t = beta1 * m_t + (1 - beta1) * gradient
        v_t = beta2 * v_t + (1 - beta2) * gradient ** 2

        m_hat = m_t / (1 - beta1 ** (epoch + 1))
        v_hat = v_t / (1 - beta2 ** (epoch + 1))

        weights -= learning_rate * m_hat / (np.sqrt(v_hat) + epsilon)

    return weights
```

## 學習率衰減

隨著訓練進行，逐漸降低學習率。

```python
def lr_decay(initial_lr, epoch, decay_rate):
    return initial_lr / (1 + decay_rate * epoch)

for epoch in range(epochs):
    lr = lr_decay(0.1, epoch, 0.01)
    # 使用 lr 更新梯度
```

常見衰減方式：
- Step decay：每 N 個 epoch 衰減一次
- Exponential decay：指數衰減
- Cosine annealing：餘弦降溫

## 學習率選擇

- 過大：震盪，不收斂
- 過小：收斂太慢
- 建議起始值：0.001 ~ 0.1

## 參考資源

- https://www.google.com/search?q=gradient+descent+optimization+SGD+momentum+Adam+2019
- https://www.google.com/search?q=learning+rate+decay+neural+network+training+2019
- https://www.google.com/search?q=Adam+optimizer+vs+SGD+deep+learning+2019