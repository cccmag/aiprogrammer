# 臉部辨識技術：OpenCV 的興起

OpenCV (Open Computer Vision) 是 Intel 發起的開源電腦視覺庫，2007 年已經被廣泛應用於臉部辨識等領域。

## OpenCV 基礎

```python
"""
OpenCV 臉部偵測範例
"""
import cv

def detect_faces():
    # 載入分類器
    cascade = cv.LoadHaarCascadeClassifier('haarcascade_frontalface_default.xml')

    # 開啟 webcam
    capture = cv.CreateCameraCapture(0)

    while True:
        frame = cv.QueryFrame(capture)
        faces = cv.HaarDetectObjects(frame, cascade, cv.CreateMemStorage(), 1.2, 2, 0, (30, 30))

        for (x, y, w, h), _ in faces:
            cv.Rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        cv.ShowImage("Face Detection", frame)

        if cv.WaitKey(10) == 27:
            break
```

## 臉部辨識流程

```python
"""
臉部辨識步驟：
1. 人臉偵測 - 找到圖片中的人臉位置
2. 關鍵點偵測 - 找到眼睛、鼻子等特徵
3. 特徵比對 - 與資料庫比對
"""
```

## 結語

OpenCV 的開源特性使電腦視覺技術得以普及，推動了臉部辨識技術的發展。

---

*延伸閱讀：[OpenCV 官方網站](https://developers.google.com/search/?q=opencv+official)*