# OpenCV 入門：影像處理基礎

## 前言

OpenCV 是電腦視覺領域最重要的開源庫之一，提供了豐富的影像處理功能。

## 基本操作

```python
import cv2

# 讀取影像
img = cv2.imread('image.jpg')

# 轉換顏色空間
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 調整大小
resized = cv2.resize(img, (224, 224))

# 儲存影像
cv2.imwrite('output.jpg', resized)
```

## 幾何變換

```python
# 翻轉
flipped = cv2.flip(img, 1)  # 1=水平, 0=垂直, -1=兩者

# 旋轉
h, w = img.shape[:2]
center = (w // 2, h // 2)
M = cv2.getRotationMatrix2D(center, 45, 1.0)
rotated = cv2.warpAffine(img, M, (w, h))

# 平移
M = np.float32([[1, 0, 50], [0, 1, 30]])
translated = cv2.warpAffine(img, M, (w, h))
```

## 濾波器

```python
# 模糊
blurred = cv2.GaussianBlur(img, (5, 5), 0)

# 銳化
kernel = np.array([[-1, -1, -1],
                   [-1,  9, -1],
                   [-1, -1, -1]])
sharpened = cv2.filter2D(img, -1, kernel)

# 邊緣檢測
edges = cv2.Canny(img, 100, 200)
```

## 輪廓檢測

```python
# 找輪廓
contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# 繪製輪廓
cv2.drawContours(img, contours, -1, (0, 255, 0), 2)
```

## 延伸閱讀

- [OpenCV 官方文檔](https://www.google.com/search?q=OpenCV+python+tutorial)
- [OpenCV 官網](https://www.google.com/search?q=opencv+official+documentation)