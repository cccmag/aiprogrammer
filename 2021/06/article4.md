# Article 4：記憶體優化 — ZeRO-Offload

## ZeRO-Offload 的設計思想

ZeRO-Offload 是 ZeRO-3 與 CPU offload 的結合。其核心思想是：將優化器狀態和/或梯度 offload 到 CPU 記憶體，在 CPU 上進行部分計算（如 Adam 的第一階動量計算），然後將更新後的引數拷貝回 GPU。這使得可以在同樣的 GPU 數量下訓練更大的模型。

## 記憶體節省效果

以 ZeRO-3 Offload 為例：優化器狀態、梯度和參數都可以 offload 到 CPU。此時每個 GPU 只需保存約 1/4 的參數（用於 current mini-batch 的計算），其餘由 CPU 管理。理論上，可以使用比 GPU 記憶體大得多的模型。

## 通訊模式

ZeRO-Offload 的通訊模式是：計算完梯度後，進行 AllReduce 交換梯度，然後將梯度 offload 到 CPU。下一個 iteration，從 CPU 載入參數並傳輸到 GPU。這種模式增加了 CPU-GPU 通訊，但减少了 GPU 間通訊。

## 何時使用 Offload

ZeRO-Offload 適合以下場景：
1. 模型大到單節點多卡仍無法容納
2. 有足夠的 CPU 記憶體
3. 願意犧牲部分訓練速度以換取更大模型

對於可以放入記憶體的模型，Offload 反而會拖慢訓練。

## 實務考量

1. 確保 CPU-GPU 頻寬足够（PCIe 4.0 或更好）
2. 監控 CPU 記憶體使用，避免 swap
3. 考慮使用 NVMe offload（ZeRO-Infinity）進一步擴展

## 參考資源

- ZeRO-Offload Paper：https://www.google.com/search?q=ZeRO+offload+Microsoft+paper
- ZeRO-Infinity：https://www.google.com/search?q=ZeRO+infinity+deep+speed