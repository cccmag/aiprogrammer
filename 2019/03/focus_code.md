# 程式碼說明 — 神經網路展示

## 功能概述

`_code/neural_network.py` 是一個展示類神經網路基礎的腳本。包含感知器、MLP、梯度下降等範例。

## demo() 函數說明

### 1. 感知器展示

展示感知器學習 AND 邏輯閘，印出權重與預測結果。

### 2. MLP 展示

展示多層感知器解決 XOR 問題，說明隱藏層的重要性。

### 3. 激活函數展示

展示 Sigmoid、Tanh、ReLU 等激活函數的圖形。

### 4. 梯度下降展示

展示不同學習率下的收斂行為。

## 執行方式

```bash
cd _code
python3 neural_network.py
```

或使用測試腳本：

```bash
bash test.sh
```

## 輸出範例

```
============================================================
類神經網路基礎展示
============================================================

[1] 感知器 - AND 邏輯閘學習
最終權重: [0.3, 0.2], 偏差: -0.4
預測結果: [0 0 0 1]
實際結果: [0 0 0 1]

[2] MLP - XOR 問題
MLP 預測結果: [0 1 1 0]
MLP 實際結果: [0 1 1 0]

[3] 激活函數展示
Sigmoid: [0.5000, 0.7311, ...]
Tanh: [0.0000, 0.7616, ...]
ReLU: [0.0000, 0.7616, ...]

[4] 梯度下降收斂
Epoch 0: Loss = 0.2500
Epoch 100: Loss = 0.1250
Epoch 200: Loss = 0.0625
收斂完成: True

============================================================
展示完成
============================================================
```

## 依賴

本腳本使用 Python 3 標準函式庫與 NumPy，無需額外安裝（展示用的腳本）。

如需完整功能：
```bash
pip install numpy matplotlib tensorflow
```

## 練習題

1. 修改感知器學習 OR 邏輯閘
2. 嘗試不同的 MLP 架構，觀察對 XOR 問題的影響
3. 調整學習率，觀察收斂速度的變化
4. 實現 Leaky ReLU 激活函數

## 參考資源

- https://www.google.com/search?q=neural+network+perceptron+MLP+Python+tutorial+2019
- https://www.google.com/search?q=neural+network+backpropagation+gradient+descent+2019