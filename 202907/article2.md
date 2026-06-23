# 模型萃取攻擊防護

## 前言

模型萃取攻擊（Model Extraction Attack）又稱模型竊取，攻擊者透過反覆查詢目標模型的 API，利用模型的預測輸出訓練一個功能相近的替代模型。這類攻擊不僅侵犯模型擁有者的智慧財產權，更可能暴露模型內部的敏感資訊。

## 攻擊原理

常見的模型萃取方法使用 **Knockoff Nets** 策略：攻擊者收集大量查詢樣本，對目標模型進行黑箱查詢，再用收集到的「輸入-輸出」配對訓練自己的模型：

```python
import numpy as np
from sklearn.neural_network import MLPClassifier

def extract_model(target_api, query_size=10000):
    queries = np.random.randn(query_size, 784)
    predictions = [target_api.predict(q) for q in queries]
    stolen = MLPClassifier(hidden_layer_sizes=(256, 128))
    stolen.fit(queries, np.array(predictions))
    return stolen
```

## 防護策略

### 輸出擾動

對模型輸出加入精心設計的噪聲，使攻擊者無法獲得精確的梯度或機率分佈：

```python
def protected_predict(model, x, epsilon=0.1):
    probs = model.predict_proba(x)
    noise = np.random.laplace(0, epsilon, probs.shape)
    return probs + noise
```

### 查詢限制

實施查詢頻率限制、異常模式檢測，以及針對高相似度查詢序列的阻斷機制。使用 **PRADA** 演算法可以有效識別萃取攻擊的查詢模式。

## 水印技術

在模型權重或訓練資料中嵌入難以移除的浮水印，一旦發現可疑的替代模型，可以透過浮水印驗證所有權。詳細技術可參考 [https://www.google.com/search?q=model+extraction+attack+defense+2026](https://www.google.com/search?q=model+extraction+attack+defense+2026)。
