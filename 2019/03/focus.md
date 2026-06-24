# 主題總覽：類神經網路基礎

類神經網路（Neural Network）是受人腦神經元結構啟發的計算模型，是深度學習與現代人工智慧的核心技術。

## 為什麼要學習類神經網路？

類神經網路能自動學習資料的複雜模式，在影像辨識、自然語言處理、語音識別等領域取得突破性成果。2019 年初，類神經網路已成為 AI 從業者的必備知識。

## 核心概念地圖

### 1. 感知器（Perceptron）

感知器是最簡單的類神經網路單元，透過加權求和與激活函數產生輸出。是理解更複雜網路的基礎。

### 2. 多層感知器（MLP）

MLP 由多個感知器組成，包含輸入層、隱藏層與輸出層。能夠學習非線性問題。

### 3. 激活函數

激活函數引入非線性，使網路能夠學習複雜模式。常用包括 Sigmoid、Tanh、ReLU 等。

### 4. 反向傳播（Backpropagation）

反向傳播是訓練神經網路的核心演算法，透過梯度下降最小化損失函數。

### 5. 梯度下降優化

各種梯度下降變體（SGD、Adam、RMSProp）用於加速網路訓練。

## 學習路徑

建議依序閱讀 focus1 到 focus7，先理解感知器原理，再學習 MLP 架構與訓練方法，最後動手實作。article1 到 article10 提供了實用的技術細節。

## 本期結構

- focus1–7：類神經網路核心概念
- article1–5：NumPy 實作與訓練技術
- article6–10：實務應用與最佳實踐
- _code/neural_network.py：神經網路展示腳本

## 參考資源

- https://www.google.com/search?q=neural+network+perceptron+MLP+tutorial+2019
- https://www.google.com/search?q=deep+learning+backpropagation+gradient+descent+2019
- https://www.google.com/search?q=neural+network+activation+function+ReLU+sigmoid+2019