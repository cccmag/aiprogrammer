# TensorFlow Lite：行動端深度學習

## 前言

隨著行動裝置的普及，將深度學習模型部署到邊緣裝置變得越來越重要。TensorFlow Lite 提供了將 TensorFlow 模型轉換為輕量級版本的工具，專為行動和嵌入式裝置設計。

## TensorFlow Lite 架構

```
TensorFlow 模型 → TensorFlow Lite 轉換器 → .tflite 模型
                                               ↓
                                        行動/嵌入式裝置
                                               ↓
                                         TensorFlow Lite 解釋器
```

## 模型轉換

### 轉換流程

```python
# 1. 儲存 TensorFlow 模型
import tensorflow as tf
model = tf.keras.models.load_model('my_model.h5')
model.save('my_model.pb')

# 2. 使用 TOCO 轉換
# tflite_convert --graph_def_file=my_model.pb \
#                 --output_file=my_model.tflite \
#                 --input_format=TENSORFLOW_GRAPHDEF \
#                 --output_format=TFLITE \
#                 --input_shape=1,784 \
#                 --input_array=input \
#                 --output_array=output
```

### 量化優化

```python
# 量化可以大幅減少模型大小
# float32 → int8
# 記憶體使用減少 4x
```

## 應用場景

### 行動 App

- 影像分類
- 物體偵測
- 語音辨識
- 文字分類

### 嵌入式系統

- Raspberry Pi
- Arduino
- 物聯網裝置

## 結語

TensorFlow Lite 使得在行動裝置上執行深度學習模型成為可能，這對於需要低延遲、高隱私或離線運作的應用場景特別重要。

---

## 延伸閱讀

- [TensorFlow+Lite+官方](https://www.google.com/search?q=TensorFlow+Lite+official)
- [TensorFlow+Lite+教程](https://www.google.com/search?q=TensorFlow+Lite+tutorial+mobile)
- [行動端+深度學習](https://www.google.com/search?q=mobile+deep+learning+deployment)

---

*本篇文章為「AI 程式人雜誌 2017 年 2 月號」文章系列之一。*