# 電腦視覺的特征提取

## SIFT 特徵

Scale-Invariant Feature Transform：

```python
# 擷取 SIFT 特征
sift = cv2.SIFT()
keypoints, descriptors = sift.detectAndCompute(image, None)
```

## HOG 特徵

Histogram of Oriented Gradients：

```python
# 計算 HOG 特征
hog = cv2.HOGDescriptor()
features = hog.compute(image)
```

## 結論

這些特徵為後續物體辨識奠定基礎。

---

**延伸閱讀**

- [SIFT+HOG+features](https://www.google.com/search?q=SIFT+HOG+computer+vision)