# Focus 3：ZeRO — 零冗餘優化器

## ZeRO 的動機

傳統資料平行中，每個節點都完整保存模型參數、梯度和優化器狀態。對於大模型，這造成嚴重的記憶體冗餘——所有節點都在儲存同樣的資訊。ZeRO（Zero Redundancy Optimizer）通過分片（sharding）這些狀態來消除冗餘，理論上可以將記憶體需求減少 N 倍（N 為 GPU 數量）。

## 三個Stage

ZeRO 分為三個Stage。Stage 1：只分片優化器狀態，每個節點只保存 1/N 的優化器狀態。Stage 2：分片優化器狀態和梯度，進一步減少記憶體。Stage 3：分片所有狀態（參數、梯度、優化器狀態），記憶體需求與 GPU 數量成反比。

## 通訊開銷

ZeRO 的記憶體節省有代價：需要額外的通訊來獲取分片的狀態。Stage 1 增加少量通訊（AllReduce for gradients 變為 AllReduce + Gather）。Stage 2 和 Stage 3 通訊量進一步增加。但實務中，記憶體節省的好處通常超過通訊開銷。

## DeepSpeed 集成

ZeRO 是 Microsoft DeepSpeed 的核心技術。DeepSpeed 提供了優化的 ZeRO 實現，支援 Stage 1/2/3 以及 ZeRO-Offload（將部分狀態放到 CPU/NVMe）。使用 DeepSpeed 可以在單機多卡或多多卡環境中訓練數十億參數的模型。

## 與 FSDP 的關係

PyTorch 的 FSDP（Fully Sharded Data Parallel）借鑒了 ZeRO 的設計。兩者在核心思想上一致：分片模型狀態以節省記憶體。FSDP 的優勢是與 PyTorch 無縫整合；DeepSpeed 提供更豐富的功能（如 ZeRO-Infinity）。

## 參考資源

- ZeRO Paper：https://www.google.com/search?q=ZeRO+memory+optimizer+paper
- DeepSpeed ZeRO：https://www.google.com/search?q=DeepSpeed+ZeRO+stage+1+2+3