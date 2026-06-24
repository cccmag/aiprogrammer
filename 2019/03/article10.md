# 訓練監控與 Early Stopping

## 訓練監控的重要性

即時監控訓練過程可以發現問題並及時調整。

## Keras Callbacks

```python
from tensorflow.keras.callbacks import (
    EarlyStopping,
    ModelCheckpoint,
    ReduceLROnPlateau,
    TensorBoard,
    CSVLogger
)
```

## Early Stopping

當驗證損失不再改善時停止訓練：

```python
early_stopping = EarlyStopping(
    monitor='val_loss',
    patience=10,
    restore_best_weights=True,
    verbose=1
)

model.fit(
    x_train, y_train,
    epochs=100,
    validation_split=0.2,
    callbacks=[early_stopping]
)
```

## Model Checkpoint

保存最佳模型：

```python
checkpoint = ModelCheckpoint(
    'best_model.h5',
    monitor='val_accuracy',
    save_best_only=True,
    mode='max',
    verbose=1
)

model.fit(
    x_train, y_train,
    epochs=100,
    validation_split=0.2,
    callbacks=[checkpoint]
)
```

## Reduce Learning Rate on Plateau

當指標停止改善時降低學習率：

```python
reduce_lr = ReduceLROnPlateau(
    monitor='val_loss',
    factor=0.5,
    patience=5,
    min_lr=1e-7,
    verbose=1
)

model.fit(
    x_train, y_train,
    epochs=100,
    validation_split=0.2,
    callbacks=[reduce_lr]
)
```

## TensorBoard

```python
tensorboard = TensorBoard(
    log_dir='./logs',
    histogram_freq=1,
    write_graph=True,
    write_images=True
)

model.fit(
    x_train, y_train,
    epochs=10,
    callbacks=[tensorboard]
)

%load_ext tensorboard
%tensorboard --logdir=./logs
```

## CSVLogger

記錄訓練過程到 CSV：

```python
csv_logger = CSVLogger(
    'training.log',
    separator=',',
    append=False
)

model.fit(
    x_train, y_train,
    epochs=10,
    callbacks=[csv_logger]
)

import pandas as pd
history = pd.read_csv('training.log')
print(history.head())
```

## 完整 Callback 設定

```python
callbacks = [
    EarlyStopping(
        monitor='val_loss',
        patience=10,
        restore_best_weights=True
    ),
    ModelCheckpoint(
        'best_model.h5',
        monitor='val_accuracy',
        save_best_only=True
    ),
    ReduceLROnPlateau(
        monitor='val_loss',
        factor=0.5,
        patience=5,
        min_lr=1e-7
    ),
    TensorBoard('./logs'),
    CSVLogger('training.log')
]

model.fit(
    x_train, y_train,
    epochs=100,
    validation_split=0.2,
    callbacks=callbacks
)
```

## 自訂 Callback

```python
class PrintLossCallback(keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs=None):
        print(f"Epoch {epoch}: loss={logs['loss']:.4f}, val_loss={logs['val_loss']:.4f}")

model.fit(
    x_train, y_train,
    epochs=10,
    callbacks=[PrintLossCallback()]
)
```

## LearningRateScheduler

```python
def lr_schedule(epoch):
    if epoch < 10:
        return 0.001
    elif epoch < 30:
        return 0.0005
    else:
        return 0.0001

lr_scheduler = keras.callbacks.LearningRateScheduler(lr_schedule)

model.fit(
    x_train, y_train,
    epochs=50,
    callbacks=[lr_scheduler]
)
```

## 監控訓練歷史

```python
history = model.fit(
    x_train, y_train,
    epochs=20,
    validation_split=0.2
)

print(f"訓練歷史鍵: {history.history.keys()}")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

ax1.plot(history.history['loss'], label='Training Loss')
ax1.plot(history.history['val_loss'], label='Validation Loss')
ax1.set_xlabel('Epoch')
ax1.set_ylabel('Loss')
ax1.set_title('Loss over Epochs')
ax1.legend()

ax2.plot(history.history['accuracy'], label='Training Accuracy')
ax2.plot(history.history['val_accuracy'], label='Validation Accuracy')
ax2.set_xlabel('Epoch')
ax2.set_ylabel('Accuracy')
ax2.set_title('Accuracy over Epochs')
ax2.legend()

plt.tight_layout()
plt.show()
```

## 診斷問題

### 欠擬合
- 訓練與驗證損失都很高
- 解決方案：增加模型容量、延長訓練

### 過擬合
- 訓練損失低，驗證損失高
- 解決方案：加入正則化、Dropout

### 不穩定
- 訓練損失震盪
- 解決方案：降低學習率

## 參考資源

- https://www.google.com/search?q=Keras+callbacks+EarlyStopping+ModelCheckpoint+2019
- https://www.google.com/search?q=TensorBoard+training+monitoring+deep+learning+2019
- https://www.google.com/search?q=training+neural+network+overfitting+underfitting+diagnosis+2019