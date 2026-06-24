# 影像增強技巧

## 前言

資料增強是提升模型泛化能力的重要技術。本文介紹常用的影像增強方法。

---

## 一、資料增強的原理

### 為何有效？

- 增加訓練樣本多樣性
- 減少過擬合
- 提高模型魯棒性

### 常見策略

| 策略 | 說明 |
|------|------|
| 幾何變換 | 翻轉、旋轉、裁剪 |
| 色彩變換 | 亮度、對比度、色調 |
| 雜訊注入 | 添加高斯噪聲 |
| 混合增強 | CutMix, MixUp |

---

## 二、torchvision.transforms

### 常用變換

```python
import torchvision.transforms as transforms

train_transform = transforms.Compose([
    transforms.RandomHorizontalFlip(p=0.5),      # 隨機水平翻轉
    transforms.RandomVerticalFlip(p=0.1),        # 隨機垂直翻轉
    transforms.RandomRotation(15),               # 隨機旋轉 ±15 度
    transforms.ColorJitter(brightness=0.2),      # 亮度調整
    transforms.ColorJitter(contrast=0.2),        # 對比度調整
    transforms.RandomCrop(32, padding=4),        # 隨機裁剪
    transforms.ToTensor(),                        # 轉換為張量
    transforms.Normalize((0.5,), (0.5,))          # 正規化
])

test_transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.5,), (0.5,))
])
```

### 彈性變換

```python
transforms.ElasticTransform(alpha=50.0, sigma=5.0)
```

### 隨機仿射

```python
transforms.RandomAffine(
    degrees=15,
    translate=(0.1, 0.1),
    scale=(0.9, 1.1),
    shear=5
)
```

---

## 三、Albumentations 庫

更強大的增強庫：

```python
import albumentations as A

transform = A.Compose([
    A.RandomBrightnessContrast(p=0.5),
    A.HueSaturationValue(p=0.3),
    A.GaussNoise(p=0.2),
    A.CLAHE(p=0.2),
    A.Blur(blur_limit=3, p=0.1),
    A.GridDistortion(p=0.2),
    A.ElasticTransform(alpha=50, sigma=5, p=0.2),
])

# 使用
image = cv2.imread('image.jpg')
augmented = transform(image=image)
```

---

## 四、CutMix 和 MixUp

### CutMix

將一張圖像的一部分裁剪下來貼到另一張：

```python
def cutmix(images, labels, alpha=1.0):
    batch_size = images.size(0)
    indices = torch.randperm(batch_size)

    # 採樣 lambda
    lam = np.random.beta(alpha, alpha)

    # 邊界框
    bbx1, bby1, bbx2, bby2 = rand_bbox(images.size(), lam)

    images[:, :, bbx1:bbx2, bby1:bby2] = images[indices, :, bbx1:bbx2, bby1:bby2]

    # 調整 lambda 為實際面積比例
    lam = 1 - ((bbx2 - bbx1) * (bby2 - bby1) / (images.size()[-1] * images.size()[-2]))

    return images, labels, labels[indices], lam

def rand_bbox(size, lam):
    W = size[2]
    H = size[3]
    cut_rat = np.sqrt(1. - lam)
    cut_w = int(W * cut_rat)
    cut_h = int(H * cut_rat)

    cx = np.random.randint(W)
    cy = np.random.randint(H)

    bbx1 = np.clip(cx - cut_w // 2, 0, W)
    bby1 = np.clip(cy - cut_h // 2, 0, H)
    bbx2 = np.clip(cx + cut_w // 2, 0, W)
    bby2 = np.clip(cy + cut_h // 2, 0, H)

    return bbx1, bby1, bbx2, bby2
```

### MixUp

混合兩張圖像：

```python
def mixup_data(x, y, alpha=1.0):
    if alpha > 0:
        lam = np.random.beta(alpha, alpha)
    else:
        lam = 1

    batch_size = x.size(0)
    index = torch.randperm(batch_size)

    mixed_x = lam * x + (1 - lam) * x[index, :]
    y_a, y_b = y, y[index]

    return mixed_x, y_a, y_b, lam
```

---

## 五、自訂增強

```python
class CustomTransform:
    def __call__(self, image):
        # 隨機銳化
        if random.random() > 0.5:
            kernel = np.array([[-1,-1,-1],
                              [-1, 9,-1],
                              [-1,-1,-1]])
            image = cv2.filter2D(image, -1, kernel)

        # 隨機霧化
        if random.random() > 0.5:
            h, w = image.shape[:2]
            sigma = random.uniform(0.1, 0.2)
            image = cv2.GaussianBlur(image, (0,0), sigma)

        return image
```

---

## 六、實驗技巧

### 訓練時增強

```python
# 建議
train_transform = transforms.Compose([
    transforms.RandomResizedCrop(224),
    transforms.RandomHorizontalFlip(),
    transforms.ColorJitter(0.3, 0.3, 0.3),
    transforms.ToTensor(),
    transforms.Normalize(mean, std)
])
```

### 測試時增強 (TTA)

```python
def tta_predict(model, image, num_aug=5):
    predictions = []

    for _ in range(num_aug):
        augmented = test_transform(image)
        pred = model(augmented.unsqueeze(0))
        predictions.append(pred)

    # 平均預測
    return torch.stack(predictions).mean(0)
```

---

## 結語

適當的資料增強可以顯著提升模型效能。建議根據任務特性選擇合適的增強策略，並通過實驗驗證效果。

---

*延伸閱讀：[data+augmentation+image+deep+learning+2020](https://www.google.com/search?q=data+augmentation+image+deep+learning+2020)*