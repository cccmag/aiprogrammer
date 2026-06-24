# Focus 5：PyTorch 分散式訓練實踐

## PyTorch 分散式生態

PyTorch 提供完整的分散式訓練支持：torch.distributed 是底層通訊介面；DistributedDataParallel (DDP)是高層資料平行封裝；FSDP 是更先進的引數分片訓練。2021 年，這些工具更加成熟，生態更加豐富。

## DistributedDataParallel

DDP 是最廣泛使用的資料平行訓練工具。它自動處理：
- 梯度 AllReduce（通過 Ring-AllReduce）
- 梯度同步
- 模型副本的一致性

使用 DDP 很簡單：只需要將模型用 DDP 包裝，框架自動處理其餘部分。相比於早期的手動資料平行，DDP 更高效且更易用。

## 啟動方式

PyTorch 支援多種啟動方式。最常用的是 torch.distributed.launch，指定每節點的 GPU 數量和總进程數。對於叢集環境，需要配置 init_method（如 NCCL 的 TCP 初始化）。PyTorch 1.10+ 引入了更好的 elastic 訓練，支援節點故障恢復。

## 多節點訓練

多節點訓練需要正確配置網路和環境。關鍵環境變數包括：
- WORLD_SIZE：總进程數
- RANK：當前进程的全局排名
- LOCAL_RANK：當前節點内的本地排名

確保網路頻寬足够（使用 InfiniBand 或高速乙太網路）對效能至關重要。

## 效能調優

1. 使用 bucketing 減少通訊次數
2. 將通訊與計算重疊
3. 選擇合適的後端（NCCL for GPU, Gloo for CPU）
4. 避免不必要的同步點

## 參考資源

- PyTorch DDP Tutorial：https://www.google.com/search?q=DistributedDataParallel+pytorch+tutorial
- PyTorch Distributed：https://www.google.com/search?q=pytorch+distributed+training+best+practices