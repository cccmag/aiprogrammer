# AI 簡介與發展歷史

## 簡介

人工智慧（Artificial Intelligence，簡稱 AI）是電腦科學的一個分支，致力於創造能夠模擬人類智慧的機器。本篇介紹 AI 的發展歷程和主要應用領域。

## AI 發展歷程

### 1950 年代：AI 的誕生

- 1950 年：Alan Turing 發表《Computing Machinery and Intelligence》，提出「圖靈測試」
- 1956 年：Dartmouth 會議，首次提出「人工智慧」一詞
- 早期研究：.logic Theorist、通用問題解決器（GPS）

### 1960-1970 年代：專家系統

- 專家系統興起
- ELIZA（第一個聊天機器人）
- 1974-1980 年：第一次 AI 冬天（資金減少、研究停滯）

### 1980 年代：專家系統繁榮

- 專家系統商業化
- 日本第五代電腦計畫
- 1987-1993 年：第二次 AI 冬天

### 1990 年代：機器學習興起

- 統計學習方法興起
- 深藍擊敗西洋棋冠軍（1997）
- 機器學習取代規則系統

### 2010 年代：深度學習突破

- 2012 年：AlexNet 在 ImageNet 比賽中突破性勝出
- 2014 年：GAN（生成對抗網路）提出
- 2015 年：AlphaGo 擊敗圍棋冠軍
- 2016 年：TensorFlow 開源

## AI 的分支

### 機器學習

機器學習是 AI 的一個分支，讓電腦從資料中學習：

```python
# 監督式學習
# 輸入資料有標籤
# 例如：分類、迴歸

from sklearn.linear_model import LinearRegression

X = [[1], [2], [3], [4], [5]]
y = [2, 4, 6, 8, 10]

model = LinearRegression()
model.fit(X, y)
print(model.predict([[6]]))  # 輸出: [12.]
```

### 深度學習

使用神經網路進行學習：

```python
# 使用 Keras 建構簡單神經網路
from keras.models import Sequential
from keras.layers import Dense

model = Sequential([
    Dense(10, activation='relu', input_shape=(784,)),
    Dense(10, activation='softmax')
])
```

### 自然語言處理

讓電腦理解和使用人類語言：

- 機器翻譯
- 情緒分析
- 文字分類
- 問答系統

### 電腦視覺

讓電腦「看見」和理解圖像：

- 影像分類
- 物件偵測
- 人臉辨識
- 語意分割

## AI 應用領域

### 醫療

- 疾病診斷
- 藥物發現
- 醫學影像分析

### 金融

- 風險評估
- 詐欺偵測
- 演算法交易

### 交通

- 自動駕駛
- 交通流量預測
- 路徑優化

### 娛樂

- 推薦系統
- 遊戲 AI
- 內容生成

## AI 與人類的關係

### AI 能做的

- 大量資料分析
- 重複性任務
- 模式識別
- 優化問題

### AI 做不到的

- 真正的理解
- 創意思考
- 情感理解
- 跨領域推理

## 未來展望

- 更強大的通用人工智慧（AGI）
- AI 倫理與安全
- 人機協作
- AI 在各領域的深入應用

## 學習路徑建議

1. Python 程式設計
2. 資料結構與演算法
3. 機器學習基礎
4. 深度學習框架
5. 專案實踐