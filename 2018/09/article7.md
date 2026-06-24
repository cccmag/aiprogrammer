# 人臉偵測與識別技術

## 1. 人臉偵測 vs 人臉識別

```python
# 人臉偵測：在影像中找到人臉區域（邊界框）
# 人臉識別：確認是誰的臉（分類/比對）
```

## 2. MTCNN 人臉偵測

```python
# Multi-task Cascaded CNN
# 三階段級聯網路
# P-Net：候選框生成
# R-Net：候選框精修
# O-Net：最終偵測 + 關鍵點定位

from mtcnn import MTCNN

detector = MTCNN()
faces = detector.detect_faces(image)
# 輸出：邊界框、信心度、5個關鍵點
```

## 3. FaceNet 嵌入式學習

```python
# 將人臉映射到 128 維向量（嵌入式）
# 同一人的人臉向量距離近，不同人距離遠

def verify_face(embedding1, embedding2, threshold=0.5):
    distance = np.linalg.norm(embedding1 - embedding2)
    return distance < threshold
```

## 4. 人臉識別流程

```python
# 1. 人臉偵測
face = detect_face(image)

# 2. 人臉對齊
aligned_face = align_face(face, landmarks)

# 3. 特徵萃取
embedding = facenet(aligned_face)

# 4. 比對
identity = recognize(embedding, database)
```

## 5. 預訓練模型使用

```python
# dlib face_recognition
import face_recognition

# 載入已知人臉
known_image = face_recognition.load_image_file("person.jpg")
known_encoding = face_recognition.face_encodings(known_image)[0]

# 識別未知人臉
unknown_image = face_recognition.load_image_file("unknown.jpg")
unknown_encoding = face_recognition.face_encodings(unknown_image)[0]

# 比對
results = face_recognition.compare_faces([known_encoding], unknown_encoding)
```

## 6. 小結

人臉識別技術在 2018 年已相當成熟，FaceNet 開創的嵌入式方法成為主流，使得大規模人臉識別成為可能。

---

**參考資料**
- [FaceNet Paper](https://www.google.com/search?q=FaceNet+face+recognition+paper)
- [MTCNN Face Detection](https://www.google.com/search?q=MTCNN+face+detection+2018)