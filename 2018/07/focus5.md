# Estimator API 分散式訓練

## 企業級分散式深度學習

### Estimator API 簡介

Estimator 是 TensorFlow 的高階 API，封裝了模型訓練、評估、預測和導出等常見任務，並原生支援分散式訓練。

```python
import tensorflow as tf

# 定義模型函數
def model_fn(features, labels, mode):
    # 建立模型
    net = tf.layers.dense(features, 128, activation=tf.nn.relu)
    net = tf.layers.dense(net, 64, activation=tf.nn.relu)
    logits = tf.layers.dense(net, 10)

    # 預測模式
    predictions = tf.argmax(logits, axis=1)
    
    # 訓練模式
    loss = tf.losses.sparse_softmax_cross_entropy(labels, logits)
    
    # 評估模式
    eval_metric_ops = {
        'accuracy': tf.metrics.accuracy(labels, predictions)
    }
    
    return tf.estimator.EstimatorSpec(
        mode=mode,
        loss=loss,
        eval_metric_ops=eval_metric_ops
    )

# 建立 Estimator
estimator = tf.estimator.Estimator(model_fn=model_fn, model_dir='./model')
```

### 分散式訓練設定

```python
# 分散式設定
cluster = {
    'chief': ['worker0:2222'],
    'ps': ['ps0:2222'],
    'worker': ['worker1:2222', 'worker2:2222']
}

# 任務類型與索引
task_type = 'chief'
task_index = 0

# 建立 RunConfig
config = tf.estimator.RunConfig(
    session_config=tf.ConfigProto(
        gpu_options=tf.GPUOptions(per_process_gpu_memory_fraction=0.5)
    )
)
```

### MirroredStrategy：單機多卡

```python
# 單機多卡同步訓練
strategy = tf.contrib.distribute.MirroredStrategy()
config = tf.estimator.RunConfig(train_distribute=strategy)

estimator = tf.estimator.Estimator(
    model_fn=model_fn,
    config=config
)
```

### ParameterServerStrategy：多機多卡

```python
# 多機訓練
strategy = tf.contrib.distribute.ParameterServerStrategy()
config = tf.estimator.RunConfig(train_distribute=strategy)

estimator = tf.estimator.Estimator(
    model_fn=model_fn,
    config=config
)
```

### 輸入函數

```python
# 訓練輸入
def train_input_fn():
    dataset = tf.data.Dataset.from_tensor_slices((x_train, y_train))
    dataset = dataset.shuffle(buffer_size=10000)
    dataset = dataset.batch(32)
    dataset = dataset.repeat(10)
    return dataset

# 評估輸入
def eval_input_fn():
    dataset = tf.data.Dataset.from_tensor_slices((x_test, y_test))
    dataset = dataset.batch(32)
    return dataset
```

### 訓練與評估

```python
# 訓練
estimator.train(input_fn=train_input_fn, steps=1000)

# 評估
eval_result = estimator.evaluate(input_fn=eval_input_fn)
print(f"Test accuracy: {eval_result['accuracy']:.4f}")
```

### Keras 到 Estimator

```python
# 將 Keras 模型轉換為 Estimator
keras_model = tf.keras.Sequential([
    tf.keras.layers.Dense(128, activation='relu', input_shape=(784,)),
    tf.keras.layers.Dense(10, activation='softmax')
])

estimator = tf.keras.estimator.model_to_estimator(
    keras_model=keras_model,
    model_dir='./estimator_model'
)
```

### 小結

Estimator API 簡化了分散式訓練的複雜性，無需手動管理 Session 和變量同步，是企業級應用的重要工具。

---

**下一步**：[深度學習框架比較（2018）](focus6.md)