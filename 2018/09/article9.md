# OpenCV 與深度學習整合

## 1. OpenCV 基礎

```python
import cv2

# 讀取影像
img = cv2.imread('image.jpg')

# 轉換色彩空間
rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# 調整大小
resized = cv2.resize(img, (224, 224))
```

## 2. OpenCV DNN 模組

```python
# OpenCV 4.0 支援 DNN 模組，可執行深度學習模型
import cv2

net = cv2.dnn.readNetFromTensorflow('model.pb')

blob = cv2.dnn.blobFromImage(
    image, 1.0/255, (224, 224), (0, 0, 0), swapRB=True
)
net.setInput(blob)
predictions = net.forward()
```

## 3. 預處理影像

```python
# 常用於深度學習的 OpenCV 預處理
def preprocess_for_dnn(image, target_size=(224, 224)):
    # 調整大小
    image = cv2.resize(image, target_size)

    # 正規化
    image = image.astype(np.float32) / 255.0

    # 標準化（如 ImageNet）
    mean = np.array([0.485, 0.456, 0.406])
    std = np.array([0.229, 0.224, 0.225])
    image = (image - mean) / std

    # 轉換為 Blob（CHW 格式）
    blob = cv2.dnn.blobFromImage(image)
    return blob
```

## 4. 物件偵測整合

```python
# 使用 OpenCV DNN 執行 YOLO
net = cv2.dnn.readNetFromDarknet('yolov3.cfg', 'yolov3.weights')

# 執行偵測
layer_names = net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

blob = cv2.dnn.blobFromImage(img, 1/255, (416, 416), swapRB=True)
net.setInput(blob)
outs = net.forward(output_layers)

# 解析結果
for out in outs:
    for detection in out:
        scores = detection[5:]
        classId = np.argmax(scores)
        confidence = scores[classId]
        if confidence > 0.5:
            # 繪製邊界框
            center, w, h = detection[:4]
            x, y = int(center[0] - w/2), int(center[1] - h/2)
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
```

## 5. 攝影機即時推論

```python
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 前處理
    blob = cv2.dnn.blobFromImage(frame, 1/255, (416, 416))
    net.setInput(blob)

    # 推論
    detections = net.forward()

    # 繪製結果
    for det in detections[0]:
        if det[4] > 0.5:  # 信心度閾值
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    cv2.imshow('Real-time Detection', frame)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```

## 6. 小結

OpenCV 的 DNN 模組提供了輕鬆部署深度學習模型的能力，結合 OpenCV 的影像處理功能，可以快速建構視覺應用。

---

**參考資料**
- [OpenCV DNN Module](https://www.google.com/search?q=OpenCV+DNN+module+deep+learning+2018)
- [OpenCV with YOLO](https://www.google.com/search?q=OpenCV+YOLO+Python+tutorial)