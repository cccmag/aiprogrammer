# CUDA 程式設計模型

## SIMT 與 Kernel 執行

### CUDA 簡介

CUDA（Compute Unified Device Architecture）是 NVIDIA 於 2007 年提出的通用 GPU 程式設計平台。它允許開發者使用 C/C++、Python 等語言編寫在 GPU 上執行的函式——稱為 Kernel。CUDA 的成功之處在於將 GPU 的程式設計模型抽象化，讓開發者無需直接操作底層圖形 API。

### SIMT 執行模型

CUDA 的核心執行模型是 SIMT（Single Instruction, Multiple Threads）。與傳統 SIMD（如 SSE、AVX）不同，SIMT 允許每個執行緒有獨立的程式計數器，這意味著執行緒可以獨立地分支和返回。但為了效率，warp 內的執行緒通常執行相同的指令序列。

當 warp 內的執行緒遇到分支時，GPU 會執行所謂的「warp divergence」：先執行一條分支路徑，停用另一條分支的執行緒，然後再反過來執行。這導致某些執行緒的運算單元被浪費。

### Thread / Block / Grid 層次

CUDA 的執行緒組織為三層結構：

```
Grid （對應整個 Kernel 啟動）
 └── Block 0  （對應一個 SM 上的執行）
     └── Thread 0  （對應一個 CUDA Core 的執行）
     └── Thread 1
     └── ...
 └── Block 1
 └── ...
```

- **Thread**：最小的執行單位，每個 thread 有獨立的暫存器
- **Block**：一組 thread 的集合，共享 shared memory，可以在同一個 SM 上執行
- **Grid**：一組 block 的集合，對應一次 Kernel 啟動

### Kernel 啟動與配置

在 CUDA 中，Kernel 的啟動需要指定 Grid 和 Block 的維度：

```cpp
// CUDA C++ Kernel
__global__ void vecAdd(float *A, float *B, float *C, int N) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i < N) C[i] = A[i] + B[i];
}

// 啟動 Kernel
int threadsPerBlock = 256;
int blocksPerGrid = (N + threadsPerBlock - 1) / threadsPerBlock;
vecAdd<<<blocksPerGrid, threadsPerBlock>>>(d_A, d_B, d_C, N);
```

這個看似簡單的配置背後包含豐富的硬體考量：Block 大小應是 warp 大小（32）的倍數；Block 數量應該足夠多以隱藏記憶體延遲；每個 Block 的資源（暫存器、共享記憶體）使用量應在 SM 限制之內。

### CUDA 程式開發流程

典型的 CUDA 程式設計周期包含以下步驟：

1. **記憶體分配**：在 GPU 上分配記憶體（cudaMalloc）
2. **資料傳輸**：將資料從 CPU 複製到 GPU（cudaMemcpy HostToDevice）
3. **Kernel 執行**：啟動 GPU Kernel
4. **結果回傳**：將結果從 GPU 複製回 CPU（cudaMemcpy DeviceToHost）
5. **資源釋放**：釋放 GPU 記憶體（cudaFree）

### 記憶體層次

CUDA 提供了多層次的記憶體空間：

- **Global Memory**：所有 thread 可存取，容量大但延遲高（數百 cycle）
- **Shared Memory**：同一 Block 內 thread 共享，低延遲（~5 cycle），容量有限（典型 48K-164KB 每 SM）
- **Registers**：每個 thread 私有，零延遲，但數量有限
- **Constant Memory**：唯讀快取，適合儲存常數
- **Texture Memory**：針對特定訪問模式最佳化

### 從 Python 看 CUDA

在 Python 中，通常透過 PyTorch 或 Numba 操控 GPU，無需直接撰寫 CUDA C++：

```python
import torch
A = torch.randn(1000, 1000).cuda()
B = torch.randn(1000, 1000).cuda()
C = A @ B  # PyTorch 自動產生最佳化 CUDA Kernel
```

### 延伸閱讀

- [CUDA Programming Guide](https://www.google.com/search?q=CUDA+Programming+Guide)
- [An Even Easier Introduction to CUDA](https://www.google.com/search?q=An+Even+Easier+Introduction+to+CUDA)
- [NVIDIA CUDA Python](https://www.google.com/search?q=NVIDIA+CUDA+Python)
