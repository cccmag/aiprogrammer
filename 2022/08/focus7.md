# 分散式訓練基礎設施

## 通訊架構

### NCCL（NVIDIA Collective Communications Library）
NCCL 是 NVIDIA 提供的多 GPU 通訊函式庫，實作了 All-Reduce、Broadcast、Reduce-Scatter、All-Gather 等集體通訊原語。針對 GPU 間互連進行最佳化，支援 PCIe、NVLink、InfiniBand 等通訊協定。

### GLOO（Facebook）
GLOO 是 Facebook 開源的通訊函式庫，提供 CPU 和 GPU 的集體通訊實作。CPU 模式下使用 TCP 或共享記憶體，GPU 模式下可選用 NCCL 後端。

### MPI（Message Passing Interface）
傳統 HPC 領域的標準通訊介面。雖然在深度學習領域逐漸被 NCCL 取代，但在某些特定場景（如大規模 CPU 訓練）仍有使用。

## 叢集管理

### SLURM
HPC 領域最廣泛使用的資源管理系統。支援作業排程、資源分配、任務啟動。在深度學習領域，SLURM 負責分配 GPU 節點並啟動分散式訓練腳本。

### Kubernetes
雲原生時代的容器編排系統。K8s 配合 Volcano 或 Kubeflow 可實現 GPU 資源的動態排程與彈性擴縮。適合需要動態調整資源的訓練任務。

## 儲存系統

分散式訓練需要高效能的儲存系統來處理大量訓練資料。建議使用：
- 平行檔案系統（Lustre、GPFS）
- 物件儲存（S3、MinIO）
- 快取層（Alluxio、JuiceFS）

[搜尋 NCCL 多 GPU 通訊](https://www.google.com/search?q=NCCL+multi+GPU+communication)
[搜尋 SLURM GPU 叢集](https://www.google.com/search?q=SLURM+GPU+cluster+deep+learning)
