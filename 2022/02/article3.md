# 共享記憶體與同步

## GPU 上最快的資料共享機制

### Shared Memory 的本質

Shared Memory 是 GPU 上最昂貴也最強大的資源之一。它是晶片上（on-chip）的 SRAM，延遲約 5 cycle——比 Global Memory 的 400 cycle 快兩個數量級。但它的容量非常有限，在 A100 上每個 SM 只有 192 KB（可配置為 L1 + Shared Memory 的組合）。

Shared Memory 之所以「共享」，是因為它對同一個 Block 內的所有 Thread 可見。這使得 Block 內的 Thread 可以協作完成複雜的運算任務。

### 共享記憶體的典型使用模式

#### 模式一：資料快取

最常見的用法是將 Global Memory 中的資料載入 Shared Memory，然後反覆使用：

```python
# conceptual Python simulation
block_size = 16
shared_A = [[0.0] * block_size for _ in range(block_size)]

# 協作載入：每個 thread 載入一個元素
for tid in range(block_size * block_size):
    i, j = divmod(tid, block_size)
    shared_A[i][j] = global_A[row+i][col+j]

# __syncthreads() — 在此處同步

# 從 shared memory 讀取進行計算
for k in range(block_size):
    sum += shared_A[i][k] * shared_B[k][j]
```

這種模式在 Tiled 矩陣乘法中至關重要。透過共享記憶體，全域記憶體的訪問次數從 O(N³) 減少到 O(N²)，實現了數量級的頻寬節省。

#### 模式二：歸約運算（Reduction）

歸約運算（sum、max、min）需要將 Block 內所有 Thread 的結果合併：

```cpp
__global__ void reduce(float *input, float *output) {
    __shared__ float sdata[256];
    int tid = threadIdx.x;
    sdata[tid] = input[blockIdx.x * blockDim.x + tid];
    __syncthreads();

    for (int s = blockDim.x / 2; s > 0; s >>= 1) {
        if (tid < s) sdata[tid] += sdata[tid + s];
        __syncthreads();
    }

    if (tid == 0) output[blockIdx.x] = sdata[0];
}
```

#### 模式三：Stencil 運算

在影像處理和 PDE 求解中，Stencil 運算（如卷積、擴散）需要讀取鄰近元素。Shared Memory 可以快取 halo 區域，避免重複的 Global Memory 訪問。

### Bank Conflict 的陷阱

Shared Memory 被劃分為 32 個 Bank（記憶體通道），每個 Bank 寬度為 4 bytes。如果 warp 內多個 thread 訪問不同位址但同一個 Bank，訪問就會序列化：

```
Bank 0: threads {0, 32, 64, ...}
Bank 1: threads {1, 33, 65, ...}
...

# 無 conflict：連續訪問
data[threadIdx.x]  # thread 0 → bank 0, thread 1 → bank 1, ...

# 2-way conflict：跨步訪問 2
data[threadIdx.x * 2]  # thread 0, 16 都訪問 bank 0
```

解決方案：在宣告 shared memory 陣列時加上 padding（多一個元素寬度）：

```cpp
__shared__ float data[256][32 + 1];  // padding 避免 bank conflict
```

### 同步機制

CUDA 的同步原語非常有限，但這是刻意設計的：

- **__syncthreads()**：Block 內所有 thread 的 barrier。確保所有 thread 到達此點後才能繼續
- **threadfence()**：記憶體 fence，確保 thread 的寫入對其他 thread 可見
- **cooperative groups**：CUDA 9+ 引入的更靈活的同步機制

更重要的是理解「不需要同步」的情況：

- 不同 Block 之間不需要同步（硬體保證 global memory 的可見性）
- 不同 Grid 之間不需要同步（kernel 啟動是序列化的）

### 實戰建議

1. **Shared Memory 是稀缺資源**：每個 block 使用的 shared memory 越少，SM 上能運行的 block 越多
2. **預先載入，反覆使用**：將反覆使用的資料載入 shared memory
3. **避免 Bank Conflict**：考慮資料布局，必要時使用 padding
4. **減少同步次數**：__syncthreads 是昂貴的，只在必要時使用

### 延伸閱讀

- [CUDA Shared Memory](https://www.google.com/search?q=CUDA+shared+memory+tutorial)
- [Bank Conflict Avoidance](https://www.google.com/search?q=CUDA+bank+conflict+shared+memory)
