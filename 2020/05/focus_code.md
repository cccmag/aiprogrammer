# 主題程式碼說明

## 程式碼範例結構

本期提供了 GPU 訓練優化的完整範例，展示如何使用混合精度、梯度累積等技術。

## 檔案列表

- `gpu_train.py`：GPU 訓練範例，包含 AMP 與梯度累積

## 依賴套件

```bash
pip install torch torchvision
```

## 使用方式

```bash
python3 gpu_train.py
```

## 重點函數

### `train_with_amp(model, train_loader)`

展示完整的 AMP 訓練流程，包括 GradScaler 的使用。

### `train_with_accumulation(model, train_loader, accum_steps)`

展示梯度累積的實作方式。

### `benchmark_gpu()`

基準測試，比較不同設定下的效能。

## 練習題

1. 調整 `batch_size` 與 `accumulation_steps`，觀察記憶體使用變化
2. 啟用/停用 AMP，比較訓練速度
3. 使用 `nvidia-smi` 監控 GPU 使用率

## 參考資源

- https://www.google.com/search?q=PyTorch+GPU+training+AMP+example+code+tutorial+2020
- https://www.google.com/search?q=gradient+accumulation+PyTorch+implementation+code+guide