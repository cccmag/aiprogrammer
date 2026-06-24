# 正規化技術

## 為什麼需要正規化？

正規化（Regularization）用於防止模型過擬合，提高模型的泛化能力。

## L1 正規化（Lasso）

$$L1_{loss} = MSE + \lambda \sum_{i}|w_i|$$

```python
def l1_regularization(weights, lambda_reg):
    return lambda_reg * np.sum(np.abs(weights))

def l1_gradient(weights, lambda_reg):
    return lambda_reg * np.sign(weights)
```

## L2 正規化（Ridge）

$$L2_{loss} = MSE + \lambda \sum_{i}w_i^2$$

```python
def l2_regularization(weights, lambda_reg):
    return lambda_reg * np.sum(weights ** 2)

def l2_gradient(weights, lambda_reg):
    return 2 * lambda_reg * weights
```

## Elastic Net

結合 L1 與 L2：

```python
def elastic_net(weights, lambda_l1, lambda_l2):
    return lambda_l1 * np.sum(np.abs(weights)) + lambda_l2 * np.sum(weights ** 2)
```

## 在梯度更新中加入正規化

```python
def gradient_descent_with_l2(X, y, weights, learning_rate, lambda_reg, epochs):
    for epoch in range(epochs):
        prediction = X.dot(weights)
        error = prediction - y
        gradient = X.T.dot(error) / len(y)

        gradient += lambda_reg * weights
        weights -= learning_rate * gradient

    return weights
```

## Dropout

Dropout 在訓練時隨機關閉部分神經元，增強網路的魯棒性。

```python
class Dropout:
    def __init__(self, dropout_rate):
        self.dropout_rate = dropout_rate
        self.mask = None

    def forward(self, x, training=True):
        if training:
            self.mask = np.random.binomial(1, 1 - self.dropout_rate, x.shape) / (1 - self.dropout_rate)
            return x * self.mask
        return x

    def backward(self, gradient):
        return gradient * self.mask
```

## Keras 中的 Dropout

```python
from tensorflow import keras
from tensorflow.keras import layers

model = keras.Sequential([
    layers.Dense(256, activation='relu', input_shape=(784,)),
    layers.Dropout(0.3),
    layers.Dense(128, activation='relu'),
    layers.Dropout(0.3),
    layers.Dense(10, activation='softmax')
])
```

## L1/L2 正規化 in Keras

```python
from tensorflow.keras.regularizers import l1, l2, l1_l2

model = keras.Sequential([
    layers.Dense(256, activation='relu',
                 kernel_regularizer=l2(0.01),
                 input_shape=(784,)),
    layers.Dense(128, activation='relu',
                 kernel_regularizer=l1_l2(l1=0.01, l2=0.01)),
    layers.Dense(10, activation='softmax')
])
```

## 比較正規化效果

```python
from sklearn.datasets import make_moons
from sklearn.model_selection import train_test_split

X, y = make_moons(n_samples=1000, noise=0.3, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

def create_network(with_dropout=False, dropout_rate=0.5):
    model = keras.Sequential([
        layers.Dense(64, activation='relu', input_shape=(2,)),
        layers.Dense(64, activation='relu'),
    ])

    if with_dropout:
        model.add(layers.Dropout(dropout_rate))

    model.add(layers.Dense(1, activation='sigmoid'))
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model

model_no_dropout = create_network(with_dropout=False)
model_with_dropout = create_network(with_dropout=True, dropout_rate=0.5)

model_no_dropout.fit(X_train, y_train, epochs=50, verbose=0)
model_with_dropout.fit(X_train, y_train, epochs=50, verbose=0)

print(f"無 Dropout 測試分數: {model_no_dropout.evaluate(X_test, y_test)[1]:.2%}")
print(f"有 Dropout 測試分數: {model_with_dropout.evaluate(X_test, y_test)[1]:.2%}")
```

## Early Stopping

當驗證損失不再改善時停止訓練。

```python
from tensorflow.keras.callbacks import EarlyStopping

early_stopping = EarlyStopping(
    monitor='val_loss',
    patience=5,
    restore_best_weights=True
)

history = model.fit(
    x_train, y_train,
    epochs=100,
    validation_split=0.2,
    callbacks=[early_stopping]
)
```

## 資料增強（Data Augmentation）

對訓練資料進行變換，增加資料多樣性。

```python
from tensorflow.keras.preprocessing.image import ImageDataGenerator

datagen = ImageDataGenerator(
    rotation_range=10,
    width_shift_range=0.1,
    height_shift_range=0.1,
    horizontal_flip=True,
    zoom_range=0.1
)

datagen.fit(x_train)
model.fit(datagen.flow(x_train, y_train, batch_size=32),
          epochs=50,
          validation_data=(x_val, y_val))
```

## 參考資源

- https://www.google.com/search?q=regularization+L1+L2+dropout+neural+network+2019
- https://www.google.com/search?q=early+stopping+Keras+callback+overfitting+2019
- https://www.google.com/search?q=data+augmentation+neural+network+training+2019