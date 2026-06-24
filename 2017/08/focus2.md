# 圖像處理基礎

## 圖像的基本概念

數位圖像是由像素組成的網格。每個像素包含顏色資訊，常用 RGB（紅綠藍）三通道表示。

```python
import numpy as np

# 建立簡單的 4x4 灰階圖像
img = np.array([
    [[100], [120], [130], [110]],
    [[90], [80], [95], [105]],
    [[70], [60], [75], [85]],
    [[50], [40], [55], [65]],
])

print(f"Shape: {img.shape}")  # (4, 4, 1)
```

## OpenCV 基本操作

```python
import cv2
import numpy as np

# 讀取圖像
img = cv2.imread('image.jpg')
print(f"Shape: {img.shape}")  # (height, width, channels)

# 轉灰階
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 儲存
cv2.imwrite('output.jpg', gray)
```

## 幾何變換

### 調整大小

```python
# 調整為特定尺寸
resized = cv2.resize(img, (width, height))

# 按比例縮放
scale = 0.5
resized = cv2.resize(img, None, fx=scale, fy=scale, interpolation=cv2.INTER_LINEAR)

# 不同插值方法
cv2.INTER_NEAREST  # 最近鄰插值，速度快但品質差
cv2.INTER_LINEAR   # 雙線性插值（預設）
cv2.INTER_CUBIC    # 雙三次插值，品質好但慢
```

### 旋轉

```python
# 取得旋轉矩陣
(h, w) = img.shape[:2]
center = (w // 2, h // 2)
angle = 45
scale = 1.0

M = cv2.getRotationMatrix2D(center, angle, scale)
rotated = cv2.warpAffine(img, M, (w, h))
```

### 平移

```python
# 平移矩陣
M = np.float32([[1, 0, tx], [0, 1, ty]])
translated = cv2.warpAffine(img, M, (w, h))
```

## 濾波器

### 高斯模糊

```python
# 5x5 高斯核
blurred = cv2.GaussianBlur(img, (5, 5), 0)
```

### 中值滤波

```python
# 去除椒鹽噪聲
median = cv2.medianBlur(img, 5)
```

### 雙邊滤波

```python
# 保邊緣平滑
bilateral = cv2.bilateralFilter(img, 9, 75, 75)
```

## 邊緣偵測

### Sobel 算子

```python
# 計算梯度
sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
```

### Laplacian

```python
# 二階導數
laplacian = cv2.Laplacian(gray, cv2.CV_64F)
```

### Canny 邊緣偵測

```python
# 標準邊緣偵測方法
edges = cv2.Canny(gray, threshold1, threshold2)
```

## 形態學操作

```python
# 建立結構元素
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))

# 侵蝕
eroded = cv2.erode(img, kernel)

# 膨脹
dilated = cv2.dilate(img, kernel)

# 開運算（侵蝕後膨脹，去除小物件）
opened = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)

# 閉運算（膨脹後侵蝕，填補小孔洞）
closed = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
```

## 色彩空間

```python
# BGR 到 HSV
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# BGR 到 Gray
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 取得特定顏色範圍
lower_blue = np.array([100, 50, 50])
upper_blue = np.array([130, 255, 255])
mask = cv2.inRange(hsv, lower_blue, upper_blue)
```

## 直方圖

```python
import matplotlib.pyplot as plt

# 計算灰階直方圖
hist = cv2.calcHist([gray], [0], None, [256], [0, 256])

# 繪製
plt.figure()
plt.title("Grayscale Histogram")
plt.xlabel("Bins")
plt.ylabel("# of Pixels")
plt.plot(hist)
plt.xlim([0, 256])
plt.show()
```

## 圖像閾值

```python
# 全域閾值
_, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

# 自適應閾值
adaptive_thresh = cv2.adaptiveThreshold(
    gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
)
```

## 輪廓偵測

```python
# 找輪廓
contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# 繪製輪廓
cv2.drawContours(img, contours, -1, (0, 255, 0), 2)

# 取得邊界框
x, y, w, h = cv2.boundingRect(contour)
cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
```

## 總結

傳統圖像處理是電腦視覺的基礎。掌握濾波、邊緣偵測、形態學操作等技巧，有助於理解深度學習視覺方法的原理。