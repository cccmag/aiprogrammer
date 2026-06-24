# Eager Execution 動態圖模式

## 告別 tf.Session()

### 什麼是 Eager Execution？

Eager Execution 是 TensorFlow 1.5 引入的特性，實現「即時執行」——運算會立即返回結果，不需要先建立計算圖再執行。

```python
import tensorflow as tf

# 啟用 eager execution（TensorFlow 2.0 預設開啟）
tf.enable_eager_execution()

# 立即可以看到結果
x = tf.constant([[1.0, 2.0], [3.0, 4.0]])
y = tf.constant([[5.0, 6.0], [7.0, 8.0]])
z = tf.matmul(x, y)
print(z)  # 立即輸出結果
```

### 傳統 Graph 模式 vs Eager 模式

```python
# Graph 模式（需要 session）
a = tf.placeholder(tf.float32)
b = tf.placeholder(tf.float32)
c = a + b

with tf.Session() as sess:
    result = sess.run(c, feed_dict={a: 1.0, b: 2.0})

# Eager 模式（即時執行）
a = tf.constant(1.0)
b = tf.constant(2.0)
c = a + b
print(c.numpy())  # 3.0
```

### 自動微分

```python
def gradient_test(x):
    # 使用 GradientTape 追蹤運算
    with tf.GradientTape() as tape:
        tape.watch(x)
        y = x ** 2 + 2 * x + 1
    # 計算 dy/dx = 2x + 2
    dy_dx = tape.gradient(y, x)
    return dy_dx

x = tf.constant(3.0)
print(gradient_test(x))  # 8.0，正確！
```

### 訓練範例

```python
# 模型定義
model = tf.keras.Sequential([
    tf.keras.layers.Dense(10, activation='relu', input_shape=(784,)),
    tf.keras.layers.Dense(10, activation='softmax')
])

# 損失函數
loss_fn = tf.keras.losses MeanSquaredError()

# 訓練迴圈
optimizer = tf.keras.optimizers.Adam()

for epoch in range(100):
    with tf.GradientTape() as tape:
        predictions = model(x_train)
        loss = loss_fn(y_train, predictions)
    
    gradients = tape.gradient(loss, model.trainable_variables)
    optimizer.apply_gradients(zip(gradients, model.trainable_variables))
```

### 優點

1. **除錯容易** — 立即看到每個運算的輸出
2. **直觉编程** — 接近一般 Python 程式碼
3. **動態輸入** — 可以使用 Python 迴圈和條件判斷
4. **更好的錯誤訊息** — 錯誤發生時立即拋出

### 小結

Eager Execution 代表 TensorFlow 從「先建圖後執行」轉向「Python 優先」的設計理念，為日後 TensorFlow 2.0 的到來奠定基礎。

---

**下一步**：[TensorFlow Serving 部署模型](focus4.md)