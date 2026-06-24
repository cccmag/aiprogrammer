# GPU 記憶體管理與最佳化

## Unified Memory 與記憶體池

### GPU 記憶體階層

GPU 的記憶體層次直接決定了程式設計模型和效能特徵：

```
速度（快 → 慢）              容量（小 → 大）
Registers  (0 cycle, ~256KB/SM)
  └→ Shared Memory  (~5 cycle, 48-228KB/SM)
     └→ L1/L2 Cache  (~30/200 cycle)
        └→ Global Memory  (~400 cycle, up to 80GB)
           └→ CPU Host Memory  (~10000 cycle, up to TB)
```

每一層都有其存在的理由：暫存器和共享記憶體提供了低延遲、高頻寬的資料存取，但容量有限；Global Memory 提供大容量但高延遲；Host Memory 則在容量上無限，但延遲極高。

### Global Memory 最佳化

Global Memory 的存取模式對效能影響巨大。GPU 記憶體控制器偏好合併連續的存取：

```cpp
// 合併存取（Coalesced Access）—— 高效
float val = data[threadIdx.x];  // 相鄰 thread 存取相鄰位址

// 非合併存取（Non-coalesced Access）—— 低效
float val = data[threadIdx.x * stride];  // 跨步訪問
```

合併存取的關鍵是讓 warp 內 32 個 thread 的記憶體請求落在同一個連續記憶體區塊中。這通常需要將資料布局從「陣列的結構」（AoS）改為「結構的陣列」（SoA）。

### Shared Memory 與同步

Shared Memory 是 GPU 程式中最重要的效能優化工具。它位於晶片上，延遲極低（約 5 cycle），但每個 SM 只有數十 KB。

使用 Shared Memory 的典型模式：

```cpp
__global__ void kernel() {
    __shared__ float cache[256];
    cache[threadIdx.x] = global_data[threadIdx.x];
    __syncthreads();  // 確保所有 thread 載入完成
    // 從 shared memory 讀取進行計算
}
```

Shared Memory 的主要挑戰是 Bank Conflict：shared memory 被劃分為 32 個 banks，如果 warp 內多個 thread 訪問同一 bank 的不同位址，會發生序列化。解決方案包括 padding 和重排訪問模式。

### Unified Memory

CUDA 6.0 引入的 Unified Memory（UM）讓 CPU 和 GPU 共享統一的虛擬位址空間：

```cpp
int *data;
cudaMallocManaged(&data, N * sizeof(int));
// CPU 和 GPU 都可以訪問 data
```

UM 的優勢是程式碼簡潔——無需手動管理資料傳輸。系統會根據訪問模式自動在 CPU 和 GPU 之間遷移資料頁面。

但 UM 並不是萬靈丹。自動遷移存在效能開銷（頁面錯誤處理），且無法充分利用雙向頻寬。在效能敏感的場景，手動管理仍然優於 UM。CUDA 6.0 到 11.x 的演進中，UM 的效能逐步改善，但仍然不是 HPC 應用的首選。

### 記憶體池化技術

記憶體分配和釋放是高成本操作。cudaMalloc 和 cudaFree 涉及驅動程式層的系統呼叫。記憶體池化（Memory Pooling）技術可以解決這個問題：

```cpp
cudaMemPool_t pool;
cudaDeviceGetDefaultMemPool(&pool, device);
// 或建立自訂 pool
// 使用記憶體池時，重複使用已釋放的記憶體區塊
```

記憶體池減少了 cudaMalloc/cudaFree 的調用次數，對於頻繁分配和釋放記憶體的場景（如動態 batch 訓練）特別有用。

### Memory Oversubscription

當模型需要的記憶體超過 GPU 可用的記憶體時，有幾種處理策略：

- **梯度檢查點**（Gradient Checkpointing）：在 forward 過程只保存部分激活值，backward 時重新計算。以時間換空間。
- **CPU Offloading**：將優化器狀態或較少使用的資料遷移到 CPU 記憶體
- **記憶體壓縮**：使用 ZeRO 優化器（來自 DeepSpeed）將模型狀態分散到多個 GPU

### 實戰記憶體分析

使用 nvidia-smi 監控記憶體使用量：

```bash
nvidia-smi --query-gpu=index,memory.total,memory.used,memory.free --format=csv
```

在 PyTorch 中追蹤記憶體分配：

```python
print(torch.cuda.memory_summary())
```

### 延伸閱讀

- [CUDA Memory Optimization](https://www.google.com/search?q=CUDA+memory+optimization+guide)
- [Unified Memory CUDA](https://www.google.com/search?q=CUDA+unified+memory)
- [PyTorch Memory Management](https://www.google.com/search?q=PyTorch+GPU+memory+management)
