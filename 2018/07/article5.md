# 正則化技術：Dropout、Batch Normalization

## 1. 為什麼需要正則化？

深度神經網路容易過擬合——訓練誤差持續下降，但驗證誤差開始上升。

```python
# 過擬合的典型現象
train_losses = [0.5, 0.3, 0.2, 0.1, 0.05, 0.02, 0.01]
val_losses =   [0.6, 0.5, 0.5, 0.6, 0.8, 1.0, 1.2]
# 訓練持續改進，但驗證集表現變差
```

## 2. Dropout

### 隨機關閉神經元

```python
def dropout(x, rate=0.5):
    mask = np.random.binomial(1, 1-rate, x.shape) / (1-rate)
    return x * mask
```

### Keras Dropout 層

```python
from keras.layers import Dense, Dropout

model = Sequential([
    Dense(256, activation='relu', input_shape=(784,)),
    Dropout(0.5),  # 50% 神經元被隨機關閉
    Dense(128, activation='relu'),
    Dropout(0.5),
    Dense(10, activation='softmax')
])
```

### Dropout 的作用

1. **減少神經元依賴**：強迫每個神經元獨立學習有用特徵
2. **模型集成**：每次訓練相當於訓練一個小子網路
3. **稀疏表示**：促進稀疏表示的學習

## 3. L1/L2 正則化

### 損失函數加上懲罰項

```python
# L2 正則化（Weight Decay）
loss = original_loss + lambda * sum(W ** 2)

# Keras L2 正則化
from keras.regularizers import l2
Dense(128, kernel_regularizer=l2(0.01))
```

### Dropout vs L2

| 方法 | 機制 | 適用場景 |
|------|------|----------|
| Dropout | 隨機關閉神經元 | 大型網路、影像任務 |
| L2 | 懲罰大權重 | 小型網路、文字任務 |
| L1 | 促進稀疏權重 | 特徵選擇、壓縮模型 |

## 4. Batch Normalization

### 穩定層間輸入分佈

```python
def batch_norm(x, gamma, beta, moving_mean, moving_var, epsilon=1e-5):
    # 標準化
    x_norm = (x - moving_mean) / np.sqrt(moving_var + epsilon)
    # 縮放和平移
    return gamma * x_norm + beta
```

### Keras BatchNormalization 層

```python
from keras.layers import Dense, BatchNormalization

model = Sequential([
    Dense(256, use_bias=False),
    BatchNormalization(),
    Activation('relu'),
    Dense(128, use_bias=False),
    BatchNormalization(),
    Activation('relu'),
    Dense(10, activation='softmax')
])
```

### BatchNorm 的優點

1. **加速收斂**：減少 internal covariate shift
2. **替代 Dropout**：有時不需要額外正則化
3. **允許更高學習率**：梯度更穩定
4. **模型初始化不敏感**：對初始權重要求降低

## 5. 資料增強

```python
from keras.preprocessing.image import ImageDataGenerator

datagen = ImageDataGenerator(
    rotation_range=15,
    width_shift_range=0.1,
    height_shift_range=0.1,
    horizontal_flip=True,
    zoom_range=0.1
)

# 訓練時使用增強資料
model.fit(datagen.flow(x_train, y_train, batch_size=32), epochs=50)
```

## 6. Early Stopping

```python
from keras.callbacks import EarlyStopping

early_stop = EarlyStopping(
    monitor='val_loss',
    patience=10,
    restore_best_weights=True
)

model.fit(x_train, y_train, callbacks=[early_stop])
```

## 7. 小結

正則化技術是防止過擬合的關鍵。實務上常組合使用：Dropout + BatchNorm + Early Stopping + 資料增強，能有效提升模型泛化能力。

---

**參考資料**
- [Dropout Paper](https://www.google.com/search?q=dropout+regularization+paper)
- [Batch Normalization Paper](https://www.google.com/search?q=batch+normalization+paper)