# OpenCV 基本操作

## OpenCV 入門

```python
import cv2
import numpy as np

# 讀取圖像
img = cv2.imread('image.jpg')

# 讀取灰階
gray = cv2.imread('image.jpg', cv2.IMREAD_GRAYSCALE)

# 顯示
cv2.imshow('Image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()

# 儲存
cv2.imwrite('output.jpg', img)
```

## 色彩空間

```python
# BGR to RGB
rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# BGR to Gray
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# BGR to HSV
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# 某顏色的 mask
lower_blue = np.array([100, 50, 50])
upper_blue = np.array([130, 255, 255])
mask = cv2.inRange(hsv, lower_blue, upper_blue)
```

## 基本繪圖

```python
import numpy as np

# 建立白色畫布
canvas = np.zeros((500, 500, 3), dtype=np.uint8) + 255

# 線條
cv2.line(canvas, (0, 0), (500, 500), (0, 0, 255), 3)

# 矩形
cv2.rectangle(canvas, (50, 50), (200, 200), (0, 255, 0), 3)

# 圓形
cv2.circle(canvas, (250, 250), 50, (255, 0, 0), -1)

# 文字
cv2.putText(canvas, 'Hello', (100, 450), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 3)
```

## 幾何變換

```python
# 調整大小
resized = cv2.resize(img, (new_width, new_height))
resized = cv2.resize(img, None, fx=0.5, fy=0.5)

# 旋轉
h, w = img.shape[:2]
center = (w // 2, h // 2)
M = cv2.getRotationMatrix2D(center, 45, 1.0)
rotated = cv2.warpAffine(img, M, (w, h))

# 翻轉
flipped_h = cv2.flip(img, 1)  # 水平
flipped_v = cv2.flip(img, 0)  # 垂直
```

## 濾波器

```python
# 高斯模糊
blurred = cv2.GaussianBlur(img, (5, 5), 0)

# 中值滤波
median = cv2.medianBlur(img, 5)

# 雙邊滤波（保邊緣）
bilateral = cv2.bilateralFilter(img, 9, 75, 75)

# 銳化
kernel = np.array([[-1, -1, -1],
                   [-1,  9, -1],
                   [-1, -1, -1]])
sharpened = cv2.filter2D(img, -1, kernel)
```

## 邊緣偵測

```python
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Canny 邊緣偵測
edges = cv2.Canny(gray, 50, 150)

# Sobel
sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)

# Laplacian
laplacian = cv2.Laplacian(gray, cv2.CV_64F)
```

## 輪廓

```python
# 找輪廓
contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# 繪製輪廓
cv2.drawContours(img, contours, -1, (0, 255, 0), 2)

# 輪廓特徵
for cnt in contours:
    area = cv2.contourArea(cnt)
    perimeter = cv2.arcLength(cnt, True)
    x, y, w, h = cv2.boundingRect(cnt)
```

## 人臉偵測

```python
# Haar Cascade
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
faces = face_cascade.detectMultiScale(gray, 1.3, 5)

for (x, y, w, h) in faces:
    cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
```

## 影片處理

```python
cap = cv2.VideoCapture('video.mp4')

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow('Frame', gray)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```

## 總結

OpenCV 提供了完整的電腦視覺工具集：
- 圖像讀寫與基本操作
- 色彩空間轉換
- 濾波器與邊緣偵測
- 輪廓與人臉偵測
- 影片處理

結合 NumPy 可實現各種視覺應用。