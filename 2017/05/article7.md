# 文章 7：傳統影像辨識方法

## 前言

在深度學習出現之前，傳統機器學習方法主導了電腦視覺領域。本章節介紹這些經典方法與特徵。

## 特徵工程

手工設計的特徵需要領域知識與精心調參：

```python
import cv2

# Harris 角點檢測
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
corners = cv2.cornerHarris(gray, blockSize=2, ksize=3, k=0.04)
```

## SIFT（尺度不變特徵轉換）

1999 年 David Lowe 提出，用於影像匹配：

```python
import cv2

sift = cv2.SIFT_create()
keypoints, descriptors = sift.detectAndCompute(gray_image, None)
```

特點：
- 尺度不變性
- 旋轉不變性
- 對光照變化魯棒

## HOG（方向梯度直方圖）

常用於人物偵測：

```python
from skimage.feature import hog

features, hog_image = hog(
    image,
    orientations=9,
    pixels_per_cell=(8, 8),
    cells_per_block=(2, 2),
    visualize=True,
    feature_vector=True
)
```

## Haar 特徵

用於人臉偵測：

```python
import cv2

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
)
faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5)
```

## LBP（局部二值模式）

用於紋理分析與人臉辨識：

```python
from skimage.feature import local_binary_pattern

radius = 3
n_points = 8 * radius
lbp = local_binary_pattern(image, n_points, radius, method='uniform')
```

## 傳統分類器

### SVM（支持向量機）

```python
from sklearn.svm import SVC

model = SVC(kernel='rbf', C=1.0)
model.fit(train_features, train_labels)
predictions = model.predict(test_features)
```

### 隨機森林

```python
from sklearn.ensemble import RandomForestClassifier

model = RandomForestClassifier(n_estimators=100)
model.fit(train_features, train_labels)
```

## 深度學習的優勢

| 傳統方法 | 深度學習 |
|----------|----------|
| 手工特徵 | 自動學習特徵 |
| 需要領域知識 | 端到端學習 |
| 淺層結構 | 深層結構 |
| 準確率有限 | 準確率更高 |

## 總結

傳統影像辨識方法依赖手工特徵工程，在深度學習出現後被大幅超越。然而，這些方法仍是理解電腦視覺基礎的重要知識。

## 延伸閱讀

- https://www.google.com/search?q=SIFT+HOG+Haar+features+computer+vision
- https://www.google.com/search?q=traditional+vs+deep+learning+image+recognition