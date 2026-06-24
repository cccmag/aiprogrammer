# 資料增強：提升模型泛化能力

## 1. 為什麼需要資料增強？

深度學習模型需要大量資料，而獲取標註資料成本高。資料增強透過人工生成更多訓練樣本，提升模型泛化能力。

```python
# 原始資料有限
train_images.shape  # (5000, 32, 32, 3)

# 增強後
augmented_images.shape  # (50000, 32, 32, 3) — 10 倍！
```

## 2. 幾何變換

```python
from keras.preprocessing.image import ImageDataGenerator

datagen = ImageDataGenerator(
    rotation_range=15,      # 旋轉 ±15 度
    width_shift_range=0.1,  # 水平平移
    height_shift_range=0.1, # 垂直平移
    shear_range=0.1,        # 剪切變換
    zoom_range=0.1,         # 縮放
    horizontal_flip=True,   # 水平翻轉
    fill_mode='nearest'     # 填充方式
)

# 產生增強影像
for X_batch, y_batch in datagen.flow(X_train, y_train, batch_size=32):
    # 訓練模型
    model.train(X_batch, y_batch)
    break
```

## 3. 色彩變換

```python
# 亮度調整
def adjust_brightness(image, delta):
    return np.clip(image + delta, 0, 1)

# 對比度調整
def adjust_contrast(image, factor):
    mean = np.mean(image)
    return np.clip((image - mean) * factor + mean, 0, 1)

# 色彩空間變換
import cv2
hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
hsv[:,:,0] = (hsv[:,:,0] + 10) % 180  # 調整色相
image = cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)
```

## 4. Keras 內建增強

```python
# CIFAR-10 範例
datagen = ImageDataGenerator(
    rotation_range=15,
    width_shift_range=0.1,
    height_shift_range=0.1,
    horizontal_flip=True,
    zoom_range=0.1,
    zca_whitening=True,  # ZCA 白化
    featurewise_center=True,
    featurewise_std_normalization=True
)
datagen.fit(X_train)

model.fit(datagen.flow(X_train, y_train, batch_size=32), epochs=50)
```

## 5. Cutout 與 Random Erasing

```python
def cutout(image, mask_size=8):
    h, w = image.shape[:2]
    y = np.random.randint(h)
    x = np.random.randint(w)

    y1 = np.clip(y - mask_size // 2, 0, h)
    y2 = np.clip(y + mask_size // 2, 0, h)
    x1 = np.clip(x - mask_size // 2, 0, w)
    x2 = np.clip(x + mask_size // 2, 0, w)

    image[y1:y2, x1:x2] = 0
    return image
```

## 6. Mixup

```python
def mixup(x1, y1, x2, y2, alpha=0.2):
    lam = np.random.beta(alpha, alpha)
    x = lam * x1 + (1 - lam) * x2
    y = lam * y1 + (1 - lam) * y2
    return x, y
```

## 7. 小結

資料增強是提升模型泛化能力的关键技術。幾何變換最常用，色彩變換可模擬不同光照條件。2018 年提出的 Cutout、Mixup 等技術進一步提升了增強效果。

---

**參考資料**
- [Data Augmentation techniques](https://www.google.com/search?q=data+augmentation+deep+learning+techniques)
- [Cutout Regularization](https://www.google.com/search?q=cutout+data+augmentation+2018)