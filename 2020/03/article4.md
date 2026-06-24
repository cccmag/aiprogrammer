# tf.keras 高階 API

## Model 訓練與驗證

```python
model = tf.keras.Sequential([
    tf.keras.layers.Dense(128, activation='relu', input_shape=(784,)),
    tf.keras.layers.Dropout(0.3),
    tf.keras.layers.Dense(10)
])

model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
    loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
    metrics=['accuracy']
)

history = model.fit(
    x_train, y_train,
    validation_data=(x_val, y_val),
    epochs=20,
    batch_size=32,
    callbacks=[
        tf.keras.callbacks.EarlyStopping(patience=5),
        tf.keras.callbacks.ModelCheckpoint('best.h5', save_best_only=True)
    ]
)
```

## 自訂層

```python
class CustomDense(tf.keras.layers.Layer):
    def __init__(self, units):
        super().__init__()
        self.units = units

    def build(self, input_shape):
        self.w = self.add_weight(
            shape=(input_shape[-1], self.units),
            initializer='glorot_uniform',
            trainable=True
        )
        self.b = self.add_weight(
            shape=(self.units,),
            initializer='zeros',
            trainable=True
        )

    def call(self, inputs):
        return tf.matmul(inputs, self.w) + self.b
```

## 自訂模型

```python
class MyModel(tf.keras.Model):
    def __init__(self):
        super().__init__()
        self.dense1 = tf.keras.layers.Dense(64, activation='relu')
        self.dense2 = tf.keras.layers.Dense(64, activation='relu')
        self.output_layer = tf.keras.layers.Dense(10)

    def call(self, x):
        x = self.dense1(x)
        x = self.dense2(x)
        return self.output_layer(x)
```

## 回調函數

```python
callbacks = [
    tf.keras.callbacks.EarlyStopping(
        monitor='val_loss',
        patience=10,
        restore_best_weights=True
    ),
    tf.keras.callbacks.ReduceLROnPlateau(
        monitor='val_loss',
        factor=0.1,
        patience=5
    ),
    tf.keras.callbacks.TensorBoard('./logs')
]
```

## 模型評估與預測

```python
# 評估
loss, accuracy = model.evaluate(x_test, y_test)

# 預測
predictions = model.predict(x_test)
predicted_classes = tf.argmax(predictions, axis=1)
```

## 模型視覺化

```python
# 顯示結構
model.summary()

# 繪製架構圖
tf.keras.utils.plot_model(
    model,
    to_file='model.png',
    show_shapes=True,
    show_layer_names=True,
    expand_nested=True
)
```

## 參考資源

- https://www.google.com/search?q=tf.keras+Sequential+Functional+API+tutorial+2020
- https://www.google.com/search?q=tf.keras+custom+layer+model+callbacks+2020
- https://www.google.com/search?q=Keras+TensorFlow+training+evaluation+2020