# 即時物件偵測應用

## 1. 即時偵測的需求

自動駕駛、機器人視覺、監控系統都需要即時（>30 FPS）的物件偵測。

## 2. YOLO 在即時應用中的優勢

```python
# YOLO 的單次前向傳播特性適合即時處理
# 對比 Faster R-CNN 的區域提議方法

# YOLO: ~45 FPS on Pascal VOC
# SSD: ~46 FPS on Pascal VOC
# Faster R-CNN: ~7 FPS on Pascal VOC
```

## 3. 邊緣部署

```python
# NVIDIA Jetson TX2 部署
import torch

model = torch.load('yolov3.pt')
model.eval()

# TensorRT 加速
torch_to_trt = torch2trt(
    model,
    [torch.randn(1, 3, 416, 416).cuda()],
    fp16_mode=True
)

# 推論
result = torch_to_trt(detect(input_image))
```

## 4. 影片處理流程

```python
import cv2

cap = cv2.VideoCapture(0)  #  webcam
while True:
    ret, frame = cap.read()
    detections = model.detect(frame)
    for det in detections:
        x, y, w, h, conf, cls = det
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
    cv2.imshow('Detection', frame)
    if cv2.waitKey(1) == ord('q'):
        break
```

## 5. 預測加速技巧

```python
# 降低輸入解析度
# 減少 Anchor 數量
# 模型蒸餾壓縮
# TensorRT / ONNX 優化
# 半精度（FP16）推論
```

## 6. 小結

YOLO 是 2018 年即時物件偵測的首選方案，結合模型壓縮和硬體優化可以達到更高幀率。

---

**參考資料**
- [YOLO Real-time Detection](https://www.google.com/search?q=YOLO+real+time+object+detection+2018)
- [Object Detection on Edge Devices](https://www.google.com/search?q=object+detection+edge+device+2018)