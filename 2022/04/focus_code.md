# 焦點程式碼：PyTorch 完整範例

## 程式碼說明

本月的焦點程式碼 `_code/pytorch_demo.py` 以一個完整的神經網路訓練範例，演示了 PyTorch 的核心功能。本範例使用合成的正弦波資料，訓練一個小型全連接網路進行迴歸預測。

## 執行方式

```bash
cd _code
python3 pytorch_demo.py
```

或執行測試腳本：

```bash
cd _code
bash test.sh
```

## 功能演示清單

### 1. Tensor 基礎與裝置管理
建立張量、矩陣乘法、形狀變換。展示了 PyTorch 的 Tensor API 與 NumPy 的相似性。

### 2. 自動微分（Autograd）
示範 `requires_grad`、`backward()` 和計算圖的梯度計算。同時展示了 `torch.no_grad()` 如何停止梯度追蹤。

### 3. nn.Module 與自訂模型
定義了 `SineNet` 類別——一個使用 `nn.Sequential` 的三層全連接網路。並示範了自訂 `CustomLinear` 層的方式。

### 4. DataLoader 與批次訓練
使用 `TensorDataset` 和 `DataLoader` 建立資料管線，設定 batch size 為 16 並啟用隨機打亂。

### 5. 最佳化器與學習率排程
使用 Adam 最佳化器搭配餘弦退火學習率排程（CosineAnnealingLR），示範排程器的初始化和步進操作。

### 6. 完整訓練迴圈
執行 200 個 epoch 的訓練，每個 epoch 中迭代 DataLoader 的 batch，計算 MSE loss，進行反向傳播和參數更新。

### 7. 模型儲存與載入
使用 `torch.save` 和 `load_state_dict` 儲存與載入模型權重，並在測試資料上進行推理。

## 輸出範例

執行後會依序輸出 Tensor 形狀資訊、Autograd 計算結果、模型結構、訓練過程的 loss 值、以及測試預測結果。

## 參考資源

- 完整原始碼：`_code/pytorch_demo.py`
- PyTorch 官方教學：https://pytorch.org/tutorials/
