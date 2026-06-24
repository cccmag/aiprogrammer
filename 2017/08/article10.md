# 物體偵測實作

## 基於傳統方法的偵測

### Haar Cascade

```python
import cv2

# 載入預訓練分類器
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
)
eye_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_eye.xml'
)

img = cv2.imread('people.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 偵測人臉
faces = face_cascade.detectMultiScale(gray, 1.3, 5)

for (x, y, w, h) in faces:
    cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

    roi_gray = gray[y:y+h, x:x+w]
    roi_color = img[y:y+h, x:x+w]

    # 在人臉區域偵測眼睛
    eyes = eye_cascade.detectMultiScale(roi_gray)
    for (ex, ey, ew, eh) in eyes:
        cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)

cv2.imwrite('result.jpg', img)
```

## HOG + SVM

```python
import cv2
from sklearn import svm
import numpy as np

def extract_hog(img):
    """提取 HOG 特徵"""
    win_size = (64, 64)
    block_size = (16, 16)
    block_stride = (8, 8)
    cell_size = (8, 8)
    nbins = 9

    hog = cv2.HOGDescriptor(win_size, block_size, block_stride,
                            cell_size, nbins)
    return hog.compute(img)

# 準備訓練資料
# X_train, y_train = load_training_data()

# 訓練 SVM
# clf = svm.SVC()
# clf.fit(X_train, y_train)
```

## 基於深度學習的偵測

### 使用 Darknet/YOLO

```bash
# 安裝
git clone https://github.com/pjreddie/darknet.git
cd darknet
make

# 下載權重
wget https://pjreddie.com/media/files/yolo.weights
```

```bash
# 使用 Darknet 偵測
./darknet detect cfg/yolo.cfg yolo.weights data/dog.jpg
```

### 使用 OpenCV DNN 模組

```python
import cv2
import numpy as np

# 載入模型
net = cv2.dnn.readNetFromDarknet('yolov3.cfg', 'yolov3.weights')
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)

# 讀取類別
classes = []
with open('coco.names', 'r') as f:
    classes = [line.strip() for line in f.readlines()]

# 讀取圖像
img = cv2.imread('input.jpg')
blob = cv2.dnn.blobFromImage(img, 1/255, (416, 416), swapRB=True, crop=False)

net.setInput(blob)
outputs = net.forward(get_output_layers(net))

# 處理輸出
conf_threshold = 0.5
nms_threshold = 0.4

for out in outputs:
    for detection in out:
        scores = detection[5:]
        class_id = np.argmax(scores)
        confidence = scores[class_id]

        if confidence > conf_threshold:
            # 繪製邊界框
            pass

# NMS
# indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)
```

### Keras YOLO3

```bash
pip install keras-yolo3
```

```python
from yolo import YOLO

yolo = YOLO()
image = cv2.imread('input.jpg')
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

result = yolo.detect_image(image)

result = cv2.cvtColor(result, cv2.COLOR_RGB2BGR)
cv2.imwrite('output.jpg', result)
```

## 評估偵測結果

```python
def compute_iou(box1, box2):
    """計算 IoU"""
    x1 = max(box1[0], box2[0])
    y1 = max(box1[1], box2[1])
    x2 = min(box1[2], box2[2])
    y2 = min(box1[3], box2[3])

    intersection = max(0, x2 - x1) * max(0, y2 - y1)

    area1 = (box1[2] - box1[0]) * (1[3] - box1[1])
    area2 = (box2[2] - box2[0]) * (box2[3] - box2[1])
    union = area1 + area2 - intersection

    return intersection / (union + 1e-6)

def evaluate_detections(predictions, ground_truth, iou_threshold=0.5):
    """計算 mAP"""
    # 對每個類別計算 AP
    # 然後平均
    pass
```

## 資料增強

```python
import albumentations as A

transform = A.Compose([
    A.HorizontalFlip(p=0.5),
    A.RandomBrightnessContrast(p=0.5),
    A.RandomGamma(p=0.5),
    A.HueSaturationValue(p=0.5),
], bbox_params=A.BboxParams(format='pascal_voc'))

# 應用於訓練
transformed = transform(image=image, bboxes=bboxes, labels=labels)
```

## 總結

物體偵測有多種實現方式：
- **傳統方法**：Haar Cascade、HOG+SVM，簡單快速但精度有限
- **深度學習**：YOLO、Faster R-CNN，精度高但需較多計算資源
- **OpenCV DNN**：可在 CPU 上執行預訓練的深度學習模型

選擇合適的方法要根據應用場景的需求。