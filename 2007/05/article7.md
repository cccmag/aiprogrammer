# 支援向量機的黃金年代

## 前言

2007 年，支援向量機（SVM）仍是機器學習的主流方法。

## SVM 核心概念

```python
# libSVM 的使用
from svm import *

# 訓練
problem = svm_problem(labels, training_vectors)
param = svm_parameter('C', 10, 'kernel', 'rbf')
model = svm_train(problem, param)

# 預測
prediction = svm_predict(labels, test_vectors, model)
```

## 結語

SVM 在影像分類、文字分類等任務中表現優異。

---

## 延伸閱讀

- [SVM+support+vector+machine+2007](https://www.google.com/search?q=SVM+support+vector+machine+2007)

---