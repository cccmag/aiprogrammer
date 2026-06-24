# NCCL 與 GPU 通訊

## NCCL 簡介

NCCL（NVIDIA Collective Communications Library）是 NVIDIA 提供的 GPU 間集體通訊函式庫。它針對 NVIDIA GPU 的記憶體架構進行深度最佳化，支援多種 GPU 互連方式。

## 支援的通訊模式

NCCL 實作了 All-Reduce、Broadcast、Reduce、All-Gather、Reduce-Scatter 等所有常見的集體通訊操作。每個操作針對不同通訊拓撲進行了最佳化。

## 通訊拓撲

**NVLink**：GPU 間直接高速互連，H100 提供 900 GB/s 雙向頻寬。適合張量平行和資料平行。

**PCIe**：透過 PCIe 交換器互連，頻寬約 64 GB/s（PCIe 5.0 x16）。適合機內 GPU 通訊。

**InfiniBand**：跨機器通訊標準，HDR 200Gbps。適合多機資料平行訓練。

**RoCE**（RDMA over Converged Ethernet）：乙太網路上的 RDMA 方案，成本低於 InfiniBand。

## 效能調校

使用 `ncclComm` 的參數調整與 CUDA graph 配合，可達到接近硬體極限的通訊效率。`NCCL_ALGO` 和 `NCCL_PROTO` 環境變數可控制演算法選擇。

## NCCL 與 PyTorch

PyTorch DDP 的預設後端就是 NCCL，使用方式非常簡單：`torch.distributed.init_process_group(backend='nccl')`。NCCL 會自動偵測可用 GPU 並建立通訊群組。

## 故障排除

常見問題包括版本不匹配、網路防火牆阻擋、以及超過 `NCCL_SOCKET_NTHREADS` 限制等。使用 `NCCL_DEBUG=INFO` 可輸出詳細通訊日誌。

[搜尋 NCCL 集體通訊](https://www.google.com/search?q=NCCL+collective+communication+library)
[搜尋 NCCL 效能調校](https://www.google.com/search?q=NCCL+performance+tuning+NVLink)
