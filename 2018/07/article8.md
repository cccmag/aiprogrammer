# 損失函數選擇與設計

## 1. 任務類型與損失函數

不同任務需要不同的損失函數：

```python
# 分類任務：Cross-Entropy
loss = -sum(y_true * log(y_pred))

# 回歸任務：MSE
loss = sum((y_pred - y_true) ** 2)

# 排序任務：Margin Ranking Loss
loss = max(0, 1 - score_pos + score_neg)
```

## 2. Keras 內建損失函數

```python
from keras import losses

# 類別交叉熵（二分類）
losses.binary_crossentropy(y_true, y_pred)

# 類別交叉熵（多分類）
losses.categorical_crossentropy(y_true, y_pred)

# 稀疏類別交叉熵（標籤為整數）
losses.sparse_categorical_crossentropy(y_true, y_pred)

# 均方誤差
losses.mse(y_true, y_pred)
losses.mean_squared_error(y_true, y_pred)

# 平均絕對誤差
losses.mae(y_true, y_pred)

# Huber 損失（對異常值更魯棒）
losses.huber(y_true, y_pred)
```

## 3. 客製化損失函數

### Focal Loss（處理類別不平衡）

```python
def focal_loss(gamma=2.0, alpha=0.25):
    def focal_loss_fixed(y_true, y_pred):
        epsilon = tf.keras.backend.epsilon()
        y_pred = tf.clip_by_value(y_pred, epsilon, 1.0 - epsilon)
        pt = tf.where(tf.equal(y_true, 1), y_pred, 1 - y_pred)
        alpha_t = tf.where(tf.equal(y_true, 1), alpha, 1 - alpha)
        return -alpha_t * (1 - pt) ** gamma * tf.log(pt)
    return focal_loss_fixed
```

### 邊界損失（度量學習）

```python
def triplet_loss(margin=0.3):
    def triplet_loss_fixed(y_true, y_pred):
        anchor, positive, negative = tf.unstack(
            tf.reshape(y_pred, [-1, 3, embedding_size]), axis=1
        )
        pos_dist = tf.reduce_sum(tf.square(anchor - positive), axis=1)
        neg_dist = tf.reduce_sum(tf.square(anchor - negative), axis=1)
        loss = tf.maximum(pos_dist - neg_dist + margin, 0)
        return tf.reduce_mean(loss)
    return triplet_loss_fixed
```

## 4. 多任務學習的損失組合

```python
# 多任務模型
input_img = Input(shape=(28, 28, 1))
x = Conv2D(32, (3, 3), activation='relu')(input_img)
# ... 特徵萃取 ...

# 任務 1：分類
class_output = Dense(num_classes, activation='softmax', name='class')(x)
# 任務 2：重建
recon_output = Dense(np.prod(input_shape), activation='sigmoid', name='recon')(x)

model = Model(inputs=input_img, outputs=[class_output, recon_output])

model.compile(
    optimizer='adam',
    loss={
        'class': 'categorical_crossentropy',
        'recon': 'binary_crossentropy'
    },
    loss_weights={
        'class': 1.0,
        'recon': 0.5
    }
)
```

## 5. 損失函數的數值穩定性

```python
# 不穩定版本
loss = -y_true * np.log(y_pred)  # y_pred 接近 0 時會 overflow

# 穩定版本
epsilon = 1e-15
y_pred = np.clip(y_pred, epsilon, 1 - epsilon)
loss = -y_true * np.log(y_pred)  # 不會 overflow

# Keras 的 categorical_crossentropy 已經做了這個保護
```

## 6. 小結

選擇適當的損失函數對模型訓練至關重要。類別不平衡時考慮 Focal Loss，多任務學習時需要平衡不同任務的損失權重。

---

**參考資料**
- [Loss Functions in Keras](https://www.google.com/search?q=Keras+loss+functions+tutorial)
- [Focal Loss for Dense Object Detection](https://www.google.com/search?q=focal+loss+paper)