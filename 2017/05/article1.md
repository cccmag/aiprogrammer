# 文章 1：Python 影像處理基礎

## 前言

影像處理是電腦視覺與機器學習的重要基礎。本章節介紹 Python 中處理影像的基本方法。

## 讀取與顯示影像

```python
from PIL import Image
import matplotlib.pyplot as plt

img = Image.open('image.jpg')
img.show()

img_array = np.array(img)
print(img_array.shape)  # (height, width, channels)
```

## 常用影像處理操作

### 調整大小

```python
resized = img.resize((width, height))
```

### 裁剪

```python
cropped = img.crop((left, top, right, bottom))
```

### 旋轉與翻轉

```python
rotated = img.rotate(45)
flipped = img.transpose(Image.FLIP_LEFT_RIGHT)
```

## 色彩空間轉換

```python
from PIL import Image

img = Image.open('image.jpg')
gray = img.convert('L')  # 轉灰階
rgb = img.convert('RGB')
```

## NumPy 陣列操作

```python
import numpy as np
from PIL import Image

img = Image.open('image.jpg')
arr = np.array(img)

print(f"Shape: {arr.shape}")  # (H, W, C)
print(f"Dtype: {arr.dtype}")  # uint8

# 取得特定像素
pixel = arr[100, 100]
print(f"Pixel at (100,100): {pixel}")

# 設定像素值
arr[100, 100] = [255, 0, 0]
```

## 影像通道操作

```python
img = Image.open('image.jpg')
r, g, b = img.split()

# 合併通道
merged = Image.merge('RGB', (r, g, b))

# 單通道處理
red_channel = np.array(img)[:, :, 0]
```

## 影像統計

```python
import numpy as np
from PIL import Image

arr = np.array(img)

print(f"Mean: {np.mean(arr)}")
print(f"Std: {np.std(arr)}")
print(f"Min: {np.min(arr)}, Max: {np.max(arr)}")
```

## 總結

Python 的 PIL 和 NumPy 提供了強大的影像處理能力。這些基礎知識對後續學習影像辨識與 CNN 非常重要。

## 延伸閱讀

- https://www.google.com/search?q=Python+PIL+image+processing+tutorial
- https://www.google.com/search?q=numpy+image+array+manipulation