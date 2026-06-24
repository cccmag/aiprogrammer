# CUDA 執行緒層次結構

## Thread / Block / Grid 的設計哲學

### 三層抽象結構

CUDA 的執行緒層次結構是 GPU 程式設計最基礎也最重要的概念。它將執行緒組織為三個層次：Thread、Block 和 Grid。這個設計絕非隨意，而是與 GPU 的實體架構精準對應。

```
Thread（執行緒）
  └→ 對應 CUDA Core 的一次執行
  └→ 每個 thread 有獨立的暫存器
  └→ 可獨立定址和分支

Block（執行緒區塊）
  └→ 執行在同一個 SM 上的 thread 集合
  └→ 共享 shared memory
  └→ 可透過 __syncthreads() 同步

Grid（網格）
  └→ 對應一次 kernel 啟動
  └→ 由多個 block 組成
  └→ block 之間無通訊（除非使用 global memory）
```

### 為何需要三層結構

這個層次結構反映了 GPU 的記憶體和執行層次：

- **Thread** 層次對應於「資料平行」的基本單位。每個 thread 處理一個資料元素（如一個像素、一個矩陣元素、一個 token）。

- **Block** 層次對應於「協同平行」的單位。Block 內的 thread 需要協作時（如 tiled 矩陣乘法、歸約運算），可以透過 shared memory 和 synchronize 機制互動。

- **Grid** 層次對應於「獨立平行」的單位。不同的 block 完全獨立運行，無需通訊，因此可以任意分配到不同的 SM 上執行。

### Block 大小的選擇

Block 大小的選擇直接影響 GPU 的利用率。經驗法則：

- **必須是 warp 大小（32）的倍數**：否則會浪費執行緒
- **典型值為 128-256**：這個範圍可在多數場景達到良好平衡
- **過小（<64）**：SM 上並行的 warp 太少，無法隱藏延遲
- **過大（>1024）**：每個 thread 分配的資源（暫存器、shared memory）太少

```python
# PyTorch 中的等效概念
# 雖然 PyTorch 不直接暴露 thread/block/grid
# 但 tensor 的 shape 和分塊策略反映了相似的概念

# Grid → batch 維度
# Block → 特徵維度的分塊
x = torch.randn(64, 128, 256)  # batch=64, features=128x256
```

### Grid 大小的策略

Grid 大小（block 的數量）應該足夠多，以充分利用所有 SM：

- **至少是 SM 數量的 2-4 倍**：提供足夠的調度靈活性
- **更多 block 更好**：即使超過 SM 數量，多餘的 block 會在佇列中等待，自動填補管線

NVIDIA A100 有 108 個 SM，建議 block 數量至少 216-432 個（假設每個 block 256 thread）。

### 多維 index 與座標映射

CUDA 支援 1D、2D、3D 的 block/grid 組織，對應不同的資料維度：

```cpp
// 1D：處理向量
int i = blockIdx.x * blockDim.x + threadIdx.x;

// 2D：處理影像
int x = blockIdx.x * blockDim.x + threadIdx.x;
int y = blockIdx.y * blockDim.y + threadIdx.y;

// 3D：處理體積資料
int x = blockIdx.x * blockDim.x + threadIdx.x;
int y = blockIdx.y * blockDim.y + threadIdx.y;
int z = blockIdx.z * blockDim.z + threadIdx.z;
```

在 PyTorch 中，tensor 的維度自然對應到不同的 index 語意：

```python
# batch_size, channels, height, width
images = torch.randn(32, 3, 224, 224).cuda()
# GPU 內部會將這些維度映射到 grid/block/thread 層次
```

### 實際硬體的限制

每個 SM 能同時執行的 block 數量有限制：

- A100：每個 SM 最多 32 個 active blocks
- A100：每個 SM 最多 2048 個 active threads
- 每個 SM 的資源（暫存器、shared memory）在所有 active blocks 之間分配

這些限制意味著：一個 block 佔用的資源越多（暫存器多、shared memory 多），SM 上能並行的 block 就越少。在極端情況下，即使總執行緒數很多，實際並行度可能很低。

### 延伸閱讀

- [CUDA Thread Hierarchy](https://www.google.com/search?q=CUDA+thread+hierarchy+block+grid)
- [CUDA Occupancy Calculator](https://www.google.com/search?q=NVIDIA+CUDA+occupancy+calculator)
