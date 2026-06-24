# 單 GPU 到多 GPU

## 為何需要跨足多 GPU

當你發現單 GPU 訓練一個 epoch 需要數小時、batch size 無法加大導致收斂不穩、或模型太大無法放入單卡時，就是轉向多 GPU 的時候了。

## 第一步：資料載入的調整

單 GPU 使用 `DataLoader` 載入資料，轉換到多 GPU 後需要考慮：

**Sampler 的變更**：使用 `DistributedSampler` 確保每個進程拿到不同的資料子集。在每個 epoch 開始時呼叫 `sampler.set_epoch(epoch)` 以確保資料充分 shuffle。

**Batch size 的縮放**：若單 GPU batch size 為 64，使用 4 GPU 時 global batch size 變為 256。需要相應調整學習率，通常採用線性縮放規則：`lr_new = lr_base * n_gpus`。

## 模型包裝

將模型包裝進 `DistributedDataParallel` 模組中。需要注意的是，DDP 會在每個 forward 完成時自動進行 gradient synchronization，因此不需要手動處理梯度通訊。

## 初始化與啟動

使用 `torch.distributed.init_process_group` 初始化通訊後端。啟動方式有兩種：

**torchrun**：PyTorch 官方推薦的啟動器，自動設定環境變數。

**mp.spawn**：透過 `torch.multiprocessing.spawn` 手動啟動多進程。

## 常見陷阱

- Batch normalization 在分散式訓練中的行為不同，需考慮 SyncBN
- 隨機種子的設定需確保各進程初始參數相同
- 資料載入的路徑需在所有節點上可存取

[搜尋單GPU到多GPU遷移](https://www.google.com/search?q=single+GPU+to+multi+GPU+training+migration)
[搜尋PyTorch torchrun](https://www.google.com/search?q=PyTorch+torchrun+distributed+training)
