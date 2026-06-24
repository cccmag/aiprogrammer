# 電腦視覺的商業應用：臉部偵測普及

## 前言

2009 年，電腦視覺技術開始在商業領域广泛应用。OpenCV 的成熟和臉部偵測技術的普及，為許多新應用打開了大門。

## OpenCV 的成熟

### OpenCV 2.0

OpenCV 2.0 於 2009 年發布，带來了重要的 C++ API 更新。

```python
# OpenCV 2.0 Python 介面

import cv2

# 載入圖片
img = cv2.imread('photo.jpg')

# 轉換為灰階
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 臉部偵測
face_cascade = cv2.CascadeClassifier(
    'haarcascade_frontalface_default.xml'
)
faces = face_cascade.detectMultiScale(gray, 1.3, 5)

# 繪製邊界框
for (x, y, w, h) in faces:
    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

# 顯示
cv2.imshow('Faces', img)
cv2.waitKey(0)
```

### 預訓練分類器

```python
# OpenCV 提供的 Haar 分類器

# 臉部偵測
face_cascade = cv2.CascadeClassifier(
    'haarcascade_frontalface_default.xml'
)

# 眼睛偵測
eye_cascade = cv2.CascadeClassifier(
    'haarcascade_eye.xml'
)

# 微笑偵測
smile_cascade = cv2.CascadeClassifier(
    'haarcascade_smile.xml'
)
```

## 商業應用場景

### 身份驗證

```python
# 簡化的臉部登入系統

def authenticate(username):
    # 拍攝照片
    img = capture_webcam()

    # 臉部偵測
    faces = detect_faces(img)

    if len(faces) == 1:
        # 取出臉部
        face = extract_face(img, faces[0])

        # 與註冊的臉部比對
        stored = load_face_embeddings(username)
        similarity = compare_faces(face, stored)

        return similarity > 0.8

    return False
```

### 數位相機功能

```markdown
2009 年數位相機的臉部偵測功能：

1. 臉部對焦
   - 自動對焦在臉部
   - 優先測光

2. 臉部追蹤
   - 持續追蹤移動的臉部
   - 保持對焦清晰

3. 眨眼偵測
   - 提醒用戶閉眼
   - 自動重拍

4. 微笑偵測
   - 自動拍攝笑臉
   - 設定靈敏度
```

### 影像標記

```python
# Facebook 的自動標記

def suggest_tags(photo):
    # 偵測臉部
    faces = detect_faces(photo)

    # 對每個臉部
    for i, face in enumerate(faces):
        # 提取特徵
        embedding = extract_face_embedding(face)

        # 與用戶比對
        match = find_matching_user(embedding)

        if match:
            yield (i, match.name, match.confidence)
```

## 技術挑戰

### 光照變化

```python
# 對抗光照變化

# 標準化
normalized = cv2.equalizeHist(gray)

# 直方圖均衡化
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
equalized = clahe.apply(gray)
```

### 角度變化

```python
# 多角度訓練

# 訓練多個分類器
front_faces = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
profile_faces = cv2.CascadeClassifier('haarcascade_profileface.xml')

# 嘗試多個角度
def detect_all_faces(img):
    faces = []
    faces.extend(front_faces.detectMultiScale(img))
    faces.extend(profile_faces.detectMultiScale(cv2.flip(img, 1)))
    return merge_overlapping(faces)
```

## 結語

2009 年是電腦視覺商業應用的起點。從相機到手機，臉部偵測開始普及。

## 延伸閱讀

- [OpenCV 官方網站](https://www.google.com/search?q=OpenCV+official+website)
- [臉部偵測技術](https://www.google.com/search?q=face+detection+2009)
- [OpenCV Python 教程](https://www.google.com/search?q=OpenCV+Python+tutorial+2009)

---

*本篇文章為「AI 程式人雜誌 2009 年 8 月號」文章系列之一。*