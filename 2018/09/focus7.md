# 影像生成：GAN 的濫觴

## 1. 生成對抗網路（GAN）

### 核心思想

```python
# GAN 由兩個網路組成：
# 1. Generator（生成器）：學習生成假影像
# 2. Discriminator（判別器）：區分真實影像和生成影像

# 兩者對抗訓練，Generator 試圖欺騙 Discriminator
# Discriminator 試圖不被欺騙

# 均衡點：Generator 生成的影像與真實影像無法區分
```

### 損失函數

```python
# min_G max_D E[log(D(x))] + E[log(1 - D(G(z)))]

# G 的目標：最小化這個 loss（讓 D(G(z)) 接近 1）
# D 的目標：最大化這個 loss（正確分類真假）
```

## 2. DCGAN（2015）

### 深度卷積 GAN

```python
# Generator
# 輸入：100 維隨機向量
# -> Reshape -> 4x4x1024
# -> Conv2DTranspose x 4（逐步放大，降低通道數）
# -> Tanh -> 64x64x3

# Discriminator
# 輸入：64x64x3 影像
# -> Conv2D x 4（逐步縮小，增加通道數）
# -> Sigmoid -> 0 到 1 的信心度
```

### Keras DCGAN 示例

```python
def build_generator():
    model = Sequential([
        Dense(4*4*1024, input_dim=100),
        Reshape((4, 4, 1024)),
        BatchNormalization(),
        Activation('relu'),

        Conv2DTranspose(512, (5,5), strides=(2,2), padding='same'),
        BatchNormalization(),
        Activation('relu'),

        Conv2DTranspose(256, (5,5), strides=(2,2), padding='same'),
        BatchNormalization(),
        Activation('relu'),

        Conv2DTranspose(128, (5,5), strides=(2,2), padding='same'),
        BatchNormalization(),
        Activation('relu'),

        Conv2DTranspose(3, (5,5), strides=(2,2), padding='same'),
        Activation('tanh')
    ])
    return model

def build_discriminator():
    model = Sequential([
        Conv2D(128, (5,5), strides=(2,2), padding='same', input_shape=(64,64,3)),
        LeakyReLU(0.2),

        Conv2D(256, (5,5), strides=(2,2), padding='same'),
        BatchNormalization(),
        LeakyReLU(0.2),

        Conv2D(512, (5,5), strides=(2,2), padding='same'),
        BatchNormalization(),
        LeakyReLU(0.2),

        Flatten(),
        Dense(1, activation='sigmoid')
    ])
    return model
```

## 3. 訓練穩定性的技巧

```python
# 1. Batch Normalization
# 穩定 GAN 訓練

# 2. Label Smoothing
# 真實標籤：0.9 而非 1.0
# 減少 Discriminator 過度自信

# 3. 學習率調整
# 較低的學習率（如 0.0002）
# Adam beta1 = 0.5（而非預設 0.9）

# 4. 避免 Mode Collapse
# 當 Generator 只生成少數多樣的樣本
# 解決：minibatch discrimination
```

## 4. 條件 GAN（cGAN）

```python
# 在生成和判別時加入條件資訊

def build_cgan_generator():
    # 輸入：隨機向量 + 類別標籤
    z = Input(shape=(100,))
    label = Input(shape=(10,))  # one-hot 編碼

    # 拼接
    combined = Concatenate()([z, label])

    # 生成影像
    img = Dense(4*4*512)(combined)
    img = Reshape((4,4,512))(img)
    # ... 卷積層 ...
    return Model([z, label], img)
```

## 5. Pix2Pix（2017）

### 影像對影像轉換

```python
# Pix2Pix = cGAN + L1 Loss
# 任務：將建築物線稿轉為賽柏全景
#       黑白圖轉彩色
#       白天轉夜晚

# Generator Loss = cGAN Loss + L1 Loss
# L1 Loss 確保輸出接近目標
```

## 6. 2018 年的 GAN 進展

```python
# ProGAN（Progressive Growing）
# 從低解析度開始，逐步增加解析度
# 穩定訓練高解析度 GAN

# BigGAN（2018）
# 大規模訓練的 GAN
# 512x512 解析度的高品質影像
# 使用更多的技巧：Spectral Normalization、Truncation Trick
```

## 7. 小結

GAN 是深度學習在生成模型領域的重大突破。從 DCGAN 到 BigGAN，影像生成的品質和解析度都在不斷提升。

---

**下一步**：[程式實作：CNN 模型訓練實務](focus_code.md)

## 延伸閱讀

- [GAN Tutorial](https://www.google.com/search?q=GAN+generative+adversarial+network+tutorial)
- [DCGAN Implementation](https://www.google.com/search?q=DCGAN+implementation+keras+2018)