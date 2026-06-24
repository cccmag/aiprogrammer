# OpenCV 實務應用

## OpenCV 簡介

OpenCV（Open Source Computer Vision Library）是開放原始碼的電腦視覺庫，提供豐富的影像處理與視覺辨識功能。

## 基本操作

### 讀取、顯示、儲存

```python
import cv2

# 讀取圖像
img = cv2.imread('image.jpg')

# 讀取灰階
gray = cv2.imread('image.jpg', cv2.IMREAD_GRAYSCALE)

# 顯示圖像
cv2.imshow('Window Name', img)
cv2.waitKey(0)  # 等待按鍵
cv2.destroyAllWindows()

# 儲存
cv2.imwrite('output.jpg', img)
```

### 圖像屬性

```python
print(f"Shape: {img.shape}")  # (height, width, channels)
print(f"Size: {img.size}")    # 總像素數
print(f"Dtype: {img.dtype}")  # 資料類型
```

## 色彩空間

```python
# BGR to RGB
rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# BGR to Gray
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# BGR to HSV
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
```

## 圖像運算

```python
# 調整亮度
brighter = cv2.convertScaleAbs(img, alpha=1.5, beta=0)

# 調整對比度
# alpha > 1: 增加對比度
# beta: 調整亮度

# 混合圖像
added = cv2.addWeighted(img1, 0.7, img2, 0.3, 0)
```

## 幾何變換

```python
# 調整大小
resized = cv2.resize(img, (new_width, new_height))
resized = cv2.resize(img, None, fx=0.5, fy=0.5)  # 比例

# 旋轉
(h, w) = img.shape[:2]
center = (w // 2, h // 2)
M = cv2.getRotationMatrix2D(center, 45, 1.0)
rotated = cv2.warpAffine(img, M, (w, h))

# 翻轉
flipped_h = cv2.flip(img, 1)  # 水平
flipped_v = cv2.flip(img, 0)  # 垂直
```

## 繪圖

```python
import numpy as np

canvas = np.zeros((500, 500, 3), dtype=np.uint8) + 255

# 線條
cv2.line(canvas, (0, 0), (500, 500), (0, 0, 255), 2)

# 矩形
cv2.rectangle(canvas, (50, 50), (200, 200), (0, 255, 0), 3)

# 圓形
cv2.circle(canvas, (250, 250), 100, (255, 0, 0), -1)  # -1 為填充

# 文字
cv2.putText(canvas, 'OpenCV', (50, 450), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 2)
```

## 邊緣偵測

```python
# 灰階
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 高斯模糊去噪
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# Canny 邊緣偵測
edges = cv2.Canny(blurred, 50, 150)

# 輪廓偵測
contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
```

## 人臉偵測

### 使用 Haar Cascade

```python
# 載入預訓練模型
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
)

# 偵測
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
faces = face_cascade.detectMultiScale(
    gray,
    scaleFactor=1.1,
    minNeighbors=5,
    minSize=(30, 30)
)

# 繪製結果
for (x, y, w, h) in faces:
    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
```

### 使用 DNN 模組

```python
# OpenCV 3.3+ DNN 人臉偵測
net = cv2.dnn.readNetFromCaffe(
    'deploy.prototxt',
    'res10_300x300_ssd_iter_140000.caffemodel'
)

blob = cv2.dnn.blobFromImage(
    cv2.resize(img, (300, 300)),
    1.0, (300, 300), (104.0, 177.0, 123.0)
)

net.setInput(blob)
detections = net.forward()

for i in range(detections.shape[2]):
    confidence = detections[0, 0, i, 2]
    if confidence > 0.5:
        box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
        (x1, y1, x2, y2) = box.astype("int")
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
```

## 影片處理

```python
# 讀取影片
cap = cv2.VideoCapture('video.mp4')

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # 處理 frame
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    cv2.imshow('Frame', gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```

## 攝影機處理

```python
# 連接攝影機
cap = cv2.VideoCapture(0)  # 0 為預設攝影機

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    cv2.imshow('Camera', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```

## 即時人臉偵測

```python
import cv2

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
)

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

    cv2.imshow('Face Detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```

## 總結

OpenCV 是電腦視覺開發的利器：
- 基本操作：讀取、處理、儲存
- 影像變換：縮放、旋轉、幾何調整
- 高級功能：邊緣偵測、人臉偵測
- 影片處理：支援攝影機與影片檔案

結合深度學習模型，OpenCV 可實現更複雜的視覺任務。