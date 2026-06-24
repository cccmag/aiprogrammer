# 矩陣運算與平行化

## Tiled 演算法與加速比

### 為什麼矩陣運算如此重要

矩陣乘法是深度學習的核心操作。全連接層是矩陣乘，卷積層可以轉換為矩陣乘，注意力機制也是矩陣乘。事實上，DL 訓練的絕大多數 FLOPs 都花費在矩陣乘法上。因此，優化矩陣乘法就等同於優化整個深度學習工作流程。

### 樸素矩陣乘法的問題

樸素的矩陣乘法 C = A × B 具有 O(n³) 的時間複雜度。對於 n=1000 的矩陣，需要執行 10 億次乘加運算。但更重要的是記憶體訪問模式：

```python
# 樸素實現
for i in range(N):
    for j in range(N):
        for k in range(N):
            C[i][j] += A[i][k] * B[k][j]
```

這個三層迴圈中，內層迴圈對 B 的訪問是「列主序」的——每次迭代 B[k][j] 都會跳到不同的列。如果矩陣以行主序儲存（如 C 語言和 PyTorch 的預設方式），這會導致大量的快取未命中，浪費記憶體頻寬。

### Tiled 矩陣乘法

解決方案是 Tiled 矩陣乘法（也稱為 Blocked 或 Tiling），將矩陣劃分為較小的 tile，每個 tile 適合放入共享記憶體或 L1 快取：

```
Matrix A          Matrix B          Matrix C
┌───┬───┐        ┌───┬───┐        ┌───┬───┐
│ A₁₁│ A₁₂│        │ B₁₁│ B₁₂│        │ C₁₁│ C₁₂│
├───┼───┤ ×      ├───┼───┤ =      ├───┼───┤
│ A₂₁│ A₂₂│        │ B₂₁│ B₂₂│        │ C₂₁│ C₂₂│
└───┴───┘        └───┴───┘        └───┴───┘

C₁₁ = A₁₁×B₁₁ + A₁₂×B₂₁
C₁₂ = A₁₁×B₁₂ + A₁₂×B₂₂
C₂₁ = A₂₁×B₁₁ + A₂₂×B₂₁
C₂₂ = A₂₁×B₁₂ + A₂₂×B₂₂
```

每個 tile 的計算可以完全在 shared memory 中完成，大幅減少對 global memory 的訪問。

### CUDA Tiled 矩陣乘法的實作策略

在 CUDA 中，Tiled 矩陣乘法的典型實作：

1. **Block 分配**：每個 block 計算 C 的一個 tile（如 16×16）
2. **協作載入**：block 內所有 thread 協作將 A 和 B 的對應 tile 載入 shared memory
3. **計算**：從 shared memory 讀取資料進行乘加運算
4. **累加**：對多個 k-tile 的結果進行累加

```cpp
__global__ void tiledMatMul(float *A, float *B, float *C, int N) {
    __shared__ float As[TILE][TILE], Bs[TILE][TILE];
    int row = blockIdx.y * TILE + threadIdx.y;
    int col = blockIdx.x * TILE + threadIdx.x;
    float sum = 0;
    for (int t = 0; t < N / TILE; t++) {
        As[threadIdx.y][threadIdx.x] = A[row * N + t * TILE + threadIdx.x];
        Bs[threadIdx.y][threadIdx.x] = B[(t * TILE + threadIdx.y) * N + col];
        __syncthreads();
        for (int k = 0; k < TILE; k++)
            sum += As[threadIdx.y][k] * Bs[k][threadIdx.x];
        __syncthreads();
    }
    C[row * N + col] = sum;
}
```

### cuBLAS：不要自己寫

實務上，除非是研究或學習目的，不要自己寫矩陣乘法。NVIDIA 的 cuBLAS 庫經過了極致的最佳化，考慮了所有 GPU 微架構特性。cuBLAS 使用以下技術：

- **自動調優**：根據矩陣大小和 GPU 型號選擇最佳演算法
- **Tensor Core 利用**：在支援的 GPU 上自動使用 Tensor Core 進行混合精度運算
- **資料布局最佳化**：自動處理矩陣轉置和記憶體布局
- **非同步執行**：支援 stream 和 CUDA graph 實現並行運算

### 計算與記憶體的平衡

矩陣運算的效能瓶頸通常在於記憶體頻寬而非計算能力。對於每個浮點運算，需要從記憶體讀取 2 個輸入並寫回 1 個結果（運算強度約 0.5 FLOP/byte）。透過 Tiling 技術，可以有效提高資料重用率，讓運算強度提升到 10+ FLOP/byte。

### 延伸閱讀

- [cuBLAS Documentation](https://www.google.com/search?q=cuBLAS+documentation)
- [Optimizing Matrix Multiplication](https://www.google.com/search?q=optimizing+matrix+multiplication+CUDA)
- [Tiled Matrix Multiplication CUDA](https://www.google.com/search?q=CUDA+tiled+matrix+multiplication)
