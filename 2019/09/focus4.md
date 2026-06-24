# Eager Execution

## 動態計算圖的威力

TensorFlow 2.0 的最重要變化之一是將 Eager Execution（急切執行）設為默認模式。這種「每次操作立即執行」的模式讓 TensorFlow 變得更加直觀和易於調試。

---

## 什麼是 Eager Execution？

### 對比：Graph Execution vs Eager Execution

```
Graph Execution (TF 1.x):
1. 定義計算圖（不執行）
2. 在 session 中執行
3. 難以調試

Eager Execution (TF 2.0):
1. 定義操作（立即執行）
2. 直接獲得結果
3. 像 Python 一樣調試
```

### 簡單示例

```python
import tensorflow as tf

# TF 1.x
a = tf.constant([[1, 2], [3, 4]])
b = tf.constant([[5, 6], [7, 8]])
c = tf.matmul(a, b)
# 需要 session.run(c) 才能獲得結果

# TF 2.0 (Eager)
a = tf.constant([[1, 2], [3, 4]])
b = tf.constant([[5, 6], [7, 8]])
c = tf.matmul(a, b)
print(c)  # 立即獲得結果
# tf.Tensor([[19, 22], [43, 50]], shape=(2, 2), dtype=int32)
```

---

## Eager Execution 的優勢

### 1. 直觀的調試

```python
# 就像普通 Python 代碼一樣調試
x = tf.constant([[1.0, 2.0], [3.0, 4.0]])

# 逐步檢查
print("x 的形狀:", x.shape)
print("x 的設備:", x.device)
print("x 的值:", x.numpy())

# 使用 pdb 調試
import pdb
pdb.set_trace()
```

### 2. 即時的錯誤報告

```python
# 錯誤立即報告
try:
    # 形狀不匹配
    a = tf.constant([1, 2, 3])
    b = tf.constant([4, 5])
    c = a + b  # 立即報錯！
except tf.errors.InvalidArgumentError as e:
    print(f"錯誤: {e}")
```

### 3. 更自然的 Python 流程控制

```python
# Eager 模式下可以使用 Python 控制流
x = tf.constant([[1.0, 2.0], [3.0, 4.0]])

if tf.reduce_sum(x) > 10:
    y = x * 2
else:
    y = x / 2

# Python for 迴圈
for i in range(3):
    print(f"Step {i}: {x * i}")
```

---

## 與 Eager 配合的函式

### tf.function

使用 `@tf.function` 裝飾器將 eager 代碼轉換為高效的 TensorFlow 圖：

```python
import tensorflow as tf

# 裝飾器將函數編譯為圖
@tf.function
def compute_sum(x):
    return tf.reduce_sum(x)

# 調用時更高效
result = compute_sum(tf.constant([1, 2, 3, 4, 5]))
print(result.numpy())  # 15
```

### 何時使用 @tf.function

```
適合 @tf.function：
- 計算密集的模型
- 需要高效能的推論
- 部署場景

不適合 @tf.function：
- 調試階段
- 動態控制流
- 涉及外部 I/O
```

---

## GradientTape

用於自動微分：

```python
# Eager 模式下的梯度計算
x = tf.Variable([[1.0, 2.0], [3.0, 4.0]])

with tf.GradientTape() as tape:
    y = x ** 2
    loss = tf.reduce_sum(y)

# 計算梯度
gradients = tape.gradient(loss, x)
print(gradients)
# tf.Tensor([[2., 4.], [6., 8.]], shape=(2, 2), dtype=float32)
```

### 多次微分

```python
x = tf.Variable(3.0)

with tf.GradientTape() as tape1:
    with tf.GradientTape() as tape2:
        y = x ** 4
    dy_dx = tape2.gradient(y, x)
d2y_dx2 = tape1.gradient(dy_dx, x)

print(f"一階導數: {dy_dx.numpy()}")   # 27.0
print(f"二階導數: {d2y_dx2.numpy()}")  # 18.0
```

### 自定義訓練循環

```python
# 使用 GradientTape 的完整訓練循環
model = tf.keras.Sequential([
    tf.keras.layers.Dense(10, activation='relu', input_shape=(784,)),
    tf.keras.layers.Dense(10, activation='softmax')
])

optimizer = tf.keras.optimizers.Adam()
loss_fn = tf.keras.losses.SparseCategoricalCrossentropy()

@tf.function
def train_step(x, y):
    with tf.GradientTape() as tape:
        predictions = model(x)
        loss = loss_fn(y, predictions)

    gradients = tape.gradient(loss, model.trainable_variables)
    optimizer.apply_gradients(zip(gradients, model.trainable_variables))
    return loss

for epoch in range(5):
    for x_batch, y_batch in train_dataset:
        loss = train_step(x_batch, y_batch)
    print(f"Epoch {epoch}: Loss = {loss.numpy():.4f}")
```

---

## 效能優化

### 圖編譯的好處

```python
# @tf.function 自動優化
@tf.function
def complex_operation(x):
    for i in tf.range(1000):
        x = x * 2 - 1
    return x

# 比純 eager 快 10-100 倍
```

### Autograph

`@tf.function` 自動將 Python 控制流轉換為 TensorFlow 操作：

```python
@tf.function
def sum_even(n):
    total = tf.constant(0)
    for i in tf.range(n + 1):
        if i % 2 == 0:
            total += i
    return total

print(sum_even(100).numpy())  # 2550
```

---

## 混合策略

### 調試用 Eager，生產用 @tf.function

```python
# 開發階段：保持 eager
model = build_model()

# 訓練階段：使用 @tf.function
@tf.function
def train_epoch(dataset):
    for x, y in dataset:
        # 訓練邏輯
        ...

# 推論階段：使用 @tf.function
@tf.function
def predict(x):
    return model(x)
```

---

## 結語

Eager Execution 是 TensorFlow 2.0 最受歡迎的改變之一。它讓 TensorFlow 變得更加 Pythonic，降低了學習曲線，讓調試更加直觀。

結合 `@tf.function`，我們可以在保持易用性的同時獲得高效能。

---

**延伸閱讀**

- [TensorFlow Eager Execution](https://www.google.com/search?q=TensorFlow+eager+execution)
- [tf.function documentation](https://www.google.com/search?q=tf.function+tutorial)
- [GradientTape+tutorial](https://www.google.com/search?q=GradientTape+tutorial)

---

*本篇文章為「AI 程式人雜誌 2019 年 9 月號」TensorFlow 2.0 系列之四。*