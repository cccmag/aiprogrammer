# 分散式訓練

## 多 GPU/TPU 訓練策略

TensorFlow 2.0 提供了強大的分散式訓練支持，使得在多個 GPU 或 TPU 上訓練模型變得前所未有的簡單。

---

## 分散式策略

### tf.distribute.Strategy

```python
import tensorflow as tf

# 查看可用的策略
print("可用策略:")
print(tf.distribute.list_strategies())
```

### MirroredStrategy

單機器多 GPU 訓練：

```python
# 自動在多個 GPU 上鏡像變量
strategy = tf.distribute.MirroredStrategy()

with strategy.scope():
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(10, activation='softmax')
    ])

    model.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )

model.fit(train_dataset, epochs=10)
```

### MultiWorkerMirroredStrategy

多機器訓練：

```python
# 定義集群配置
os.environ['TF_CONFIG'] = json.dumps({
    'cluster': {
        'worker': ['worker1:2222', 'worker2:2222', 'worker3:2222']
    },
    'task': {'type': 'worker', 'index': 0}
})

strategy = tf.distribute.experimental.MultiWorkerMirroredStrategy()

with strategy.scope():
    model = build_model()  # 與單 GPU 相同的代碼
```

---

## TPU 訓練

### TPUClusterResolver

```python
# TPU 訓練
resolver = tf.distribute.cluster_resolver.TPUClusterResolver()
tf.config.experimental_connect_to_cluster(resolver)
tf.tpu.experimental.initialize_tpu_system(resolver)
strategy = tf.distribute.experimental.TPUStrategy(resolver)

with strategy.scope():
    model = build_model()
```

### TPU 使用示例

```python
# 完整的 TPU 訓練流程
import os

# 設置 TPU
resolver = tf.distribute.cluster_resolver.TPUClusterResolver(
    'grpc://' + os.environ['COLAB_TPU_ADDR']
)
tf.config.experimental_connect_to_cluster(resolver)
tf.tpu.experimental.initialize_tpu_system(resolver)

# 策略
strategy = tf.distribute.experimental.TPUStrategy(resolver)

# 訓練
with strategy.scope():
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dense(10, activation='softmax')
    ])
    model.compile(optimizer='adam', loss='categorical_crossentropy')

model.fit(dataset, epochs=10)
```

---

## 自定義訓練循環

### 分散式策略下的自定義循環

```python
# 多 GPU 自定義訓練
strategy = tf.distribute.MirroredStrategy()

with strategy.scope():
    model = build_model()
    optimizer = tf.keras.optimizers.Adam()
    loss_fn = tf.keras.losses.SparseCategoricalCrossentropy()

@tf.function
def distributed_train_step(dataset_inputs):
    def train_step(inputs):
        x, y = inputs
        with tf.GradientTape() as tape:
            predictions = model(x, training=True)
            loss = loss_fn(y, predictions)

        gradients = tape.gradient(loss, model.trainable_variables)
        optimizer.apply_gradients(zip(gradients, model.trainable_variables))
        return loss

    per_replica_losses = strategy.run(train_step, args=(dataset_inputs,))
    return strategy.reduce(
        tf.distribute.ReduceOp.SUM,
        per_replica_losses,
        axis=None
    )
```

---

## 效能優化

### 梯度累積

```python
# 梯度累積以模擬更大的批次
accumulation_steps = 4
optimizer = tf.keras.optimizers.Adam()

@tf.function
def train_step(inputs, accumulator):
    x, y = inputs
    with tf.GradientTape() as tape:
        predictions = model(x)
        loss = loss_fn(y, predictions) / accumulation_steps

    gradients = tape.gradient(loss, model.trainable_variables)
    accumulator.apply_gradients(gradients)
```

### 混合精度

```python
# 使用 mixed_float16 提升效能
from tensorflow.keras import mixed_precision

mixed_precision.set_global_policy('mixed_float16')

# 自動在 TPU 上使用 float16/bfloat16
```

---

## 結語

分散式訓練讓我們能夠利用多個 GPU 或 TPU 加速模型訓練。TensorFlow 2.0 的策略 API 使得這些高級功能變得簡單易用。

---

**延伸閱讀**

- [TensorFlow+distributed+training](https://www.google.com/search?q=TensorFlow+distributed+training+tutorial)
- [Multi-GPU+TensorFlow](https://www.google.com/search?q=TensorFlow+multi-GPU+training)
- [TPU+TensorFlow](https://www.google.com/search?q=TensorFlow+TPU+training)