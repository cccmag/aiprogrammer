# 深度學習應用領域：電腦視覺、語音辨識、自然語言處理

## 前言

深度學習在多個領域取得了突破性進展。本篇文章介紹深度學習在電腦視覺、語音辨識和自然語言處理三大核心領域的應用。

## 電腦視覺

### ImageNet 競賽的回顧

```
2012 年：AlexNet - 深度學習時代的開始
2014 年：VGG、GoogLeNet - 網路深度持續增加
2015 年：ResNet - 殘差連接解決深度網路訓練問題
2016-2017 年：更複雜的架構和遷移學習普及
```

### 經典模型架構

```python
# LeNet-5：最早的成功 CNN
# 7層網路，手寫數字辨識

# AlexNet：深度學習突破口
# 5層卷積 + 3層全連接，ImageNet 錯誤率 16%

# VGGNet：更小的 3x3 卷積核
# 16-19層，簡化但加深

# GoogLeNet：Inception 模組
# 多尺度特徵融合

# ResNet：殘差連接
# 152層，解決梯度消失問題
```

### 典型應用

```python
# 影像分類
from keras.applications import ResNet50

model = ResNet50(weights='imagenet')
predictions = model.predict(image)

# 物件偵測
# Faster R-CNN, YOLO, SSD

# 語義分割
# FCN, U-Net, DeepLab

# 風格遷移
# Neural Style Transfer
```

### 預訓練模型與遷移學習

```python
from keras.applications import VGG16
from keras.layers import Dense, Flatten
from keras.models import Model

# 載入預訓練模型（不包含頂層）
base_model = VGG16(weights='imagenet', include_top=False, input_shape=(224, 224, 3))

# 新增自訂分類器
x = base_model.output
x = Flatten()(x)
x = Dense(256, activation='relu')(x)
predictions = Dense(10, activation='softmax')(x)

model = Model(inputs=base_model.input, outputs=predictions)

# 凍結預訓練層
for layer in base_model.layers:
    layer.trainable = False

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
```

## 語音辨識

### 深度學習在語音的突破

```
2012 年：深度神經網路用於語音辨識
    - Microsoft, Google 開始使用 DNN
    - 錯誤率大幅下降

CTC (Connectionist Temporal Classification)
    - 解決輸入輸出長度不對齊問題
    - 無需強制對齊的標籤
```

### CTC 網路原理

```python
# CTC loss 的關鍵：
# 1. 處理變長序列
# 2. 自動對齊輸入輸出
# 3. 支援重複輸出

# 典型語音辨識網路
# 輸入：MFCC 特徵或原始波形
# 編碼：多層 RNN/LSTM
# 解碼：CTC 層 +貪心解碼或束搜索
```

### 端到端語音辨識

```python
# Deep Speech (Mozilla)
# 使用雙向 LSTM + CTC

# WaveNet
# 自迴歸生成模型
# 1D 卷積 + Dilated convolution

# QuartzNet
# 改進的 CTC 模型
# 更好的效能和效率
```

### 應用場景

- **語音助理**：Siri、Google Assistant、Alexa
- **語音轉文字**：會議記錄、字幕生成
- **聲紋辨識**：身份驗證
- **語音合成**：Text-to-Speech

## 自然語言處理

### 深度學習在 NLP 的應用

```
2013 年：Word2Vec - 詞向量表示
2014 年：Seq2Seq - 序列到序列模型
2015 年：Attention - 注意力機制
2016-2017 年：記憶網路、Transformer 興起
```

### 詞向量（Word Embeddings）

```python
from gensim.models import Word2Vec

# 訓練詞向量
sentences = [['I', 'love', 'machine', 'learning'], ['AI', 'is', 'the', 'future']]
model = Word2Vec(sentences, vector_size=100, window=5, min_count=1)

# 使用詞向量
vector = model.wv['machine']
similar = model.wv.most_similar('AI')
```

### Sequence-to-Sequence 模型

```python
# Encoder-Decoder 架構
# Encoder: 輸入序列 → 上下文向量
# Decoder: 上下文向量 → 輸出序列

# 機器翻譯
# 輸入：「Hello」 → 輸出：「你好」

# 文字摘要
# 輸入：長文章 → 輸出：簡短摘要
```

### Attention 機制

```python
# Attention 讓模型能夠關注輸入的相關部分
# 解決了長序列的資訊衰減問題

# 應用：
# - 機器翻譯
# - 文字摘要
# - 影像標題生成
# - 問答系統
```

### 典型的 NLP 任務

| 任務 | 輸入 | 輸出 | 典型模型 |
|------|------|------|---------|
| 文字分類 | 文件 | 類別 | CNN, LSTM |
| 情感分析 | 句子 | 正/負 | Bi-LSTM |
| 機器翻譯 | 源語言語句 | 目標語言語句 | Seq2Seq + Attention |
| 問答系統 | 問題 + 上下文 | 答案 | Memory Networks |
| 文字生成 | 條件 | 文字 | LSTM, GPT |

## 多領域融合

### 跨模態學習

深度學習開始融合多種感知模態：

- **影像標題**：CNN + RNN + Attention
- **語音辨識**：WaveNet + CTC
- **視覺問答**：影像處理 + NLP

### 深度學習平台的統一趨勢

```python
# 同一個框架處理多種任務
# TensorFlow, PyTorch, etc.

# 遷移學習
# 在一個領域學習的知識遷移到另一個領域
```

## 結論

深度學習在電腦視覺、語音辨識和自然語言處理三大領域都取得了突破：

- **電腦視覺**：影像分類、物件偵測、語義分割已接近或超越人類水準
- **語音辨識**：深度學習大幅提升了語音辨識的準確率
- **NLP**：從詞向量到注意力機制，文字理解和生成能力顯著增強

這些進展為 AI 技術的實際應用奠定了堅實基礎，也預示著更多創新應用的到來。

---

## 延伸閱讀

- [深度學習+電腦視覺](https://www.google.com/search?q=deep+learning+computer+vision+applications)
- [深度學習+語音辨識](https://www.google.com/search?q=deep+learning+speech+recognition+CTC)
- [深度學習+NLP+應用](https://www.google.com/search?q=deep+learning+NLP+applications+2017)
- [CNN+RNN+LSTM+比較](https://www.google.com/search?q=CNN+RNN+LSTM+deep+learning+comparison)

---

*本篇文章為「AI 程式人雜誌 2017 年 2 月號」焦點系列之一。*