# ZeRO 最佳化與記憶體節省

## ZeRO 的核心思想

ZeRO（Zero Redundancy Optimizer）由微軟 DeepSpeed 團隊提出，核心洞察是：在傳統資料平行中，每個 GPU 都儲存了完整的模型參數、梯度和最佳化器狀態，存在大量冗餘。ZeRO 透過分割這些狀態來消除冗餘。

## ZeRO 三階段

**Stage 1 — 分割最佳化器狀態**：將 Adam 的 momentum 和 variance 平均分配到各 GPU。每個 GPU 只儲存和更新自己負責的參數部分。記憶體節省約4倍。

**Stage 2 — 分割梯度**：在 Stage 1 的基礎上，再將梯度也分割儲存。反向傳播完成後，梯度被分散到各 GPU，不再全部複製。記憶體節省約8倍。

**Stage 3 — 分割參數**：最徹底的階段，將模型參數也分割儲存。每個 GPU 只在需要時從其他 GPU 獲取參數（透過 all-gather）。記憶體節省與 GPU 數量成正比。

## 通訊開銷

ZeRO 用通訊換取記憶體。Stage 3 需要在每個訓練步驟中進行多次 all-gather 和 reduce-scatter 操作，網路頻寬成為關鍵瓶頸。

## ZeRO-Offload

ZeRO-Offload 將最佳化器狀態和梯度卸載到 CPU 記憶體，利用 CPU RAM 的低成本擴展 GPU 有效記憶體容量。適合 GPU 記憶體有限但 CPU RAM 充足的場景。

## 與 FSDP 的關係

PyTorch 的 FSDP（Fully Sharded Data Parallel）實作了 ZeRO Stage 3 的概念，已成為 PyTorch 官方的標準分散式訓練方案。

[搜尋 ZeRO DeepSpeed 最佳化](https://www.google.com/search?q=ZeRO+DeepSpeed+optimizer)
[搜尋 FSDP PyTorch 分散式訓練](https://www.google.com/search?q=FSDP+Fully+Sharded+Data+Parallel+PyTorch)
