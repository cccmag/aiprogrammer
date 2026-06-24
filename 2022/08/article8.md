# 壓縮通訊與量化梯度

## 為何需要壓縮

在大規模分散式訓練中，梯度通訊時間佔總訓練時間的相當比例。每個訓練步驟需要傳輸的資料量約為模型參數量的兩倍（每個參數對應一個梯度值）。對於 GPT-3（1750億參數），每次通訊需要傳輸約 350GB 的 FP16 梯度資料。

## 梯度壓縮技術

### 量化（Quantization）
將 FP32 梯度量化為 FP16、INT8 甚至二進制格式。FP16 量化幾乎無精度損失，INT8 量化通常可接受。

### 稀疏化（Sparsification）
只傳輸梯度中絕對值最大的 top-k% 元素，其餘設為零。典型壓縮比為 1% 到 10%。

### 誤差回饋（Error Feedback）
壓縮技術會引入誤差，誤差回饋機制將每次壓縮的誤差累積並在下一次補償，確保模型收斂不受影響。

## 梯度累積作為通訊最佳化

梯度累積不直接壓縮資料，但透過減少通訊頻率來降低總通訊量。累積 K 步後才進行一次 All-Reduce，通訊量變為原來的 1/K。

## PowerSGD

PowerSGD 是一種低秩分解的梯度壓縮演算法。透過奇異值分解將梯度矩陣分解為兩個低秩矩陣，大幅減少傳輸量，同時保持較高的精度。

## 實戰建議

- 先試 FP16 通訊（幾乎無成本）
- 若網路為瓶頸，試 INT8 量化 + 誤差回饋
- 極大規模訓練時考慮 top-k 稀疏化
- 將梯度累積作為基礎最佳化手段

[搜尋梯度壓縮分散式訓練](https://www.google.com/search?q=gradient+compression+distributed+training)
[搜尋 PowerSGD 梯度壓縮](https://www.google.com/search?q=PowerSGD+gradient+compression)
