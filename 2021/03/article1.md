# CUDA C++ 基礎

## 記憶體配置

### 設備記憶體配置

```cpp
// 配置設備記憶體
float *d_array;
size_t bytes = N * sizeof(float);
cudaMalloc(&d_array, bytes);

// 釋放設備記憶體
cudaFree(d_array);
```

### 主機與設備間傳輸

```cpp
// 主機到設備
cudaMemcpy(d_array, h_array, bytes, cudaMemcpyHostToDevice);

// 設備到主機
cudaMemcpy(h_array, d_array, bytes, cudaMemcpyDeviceToHost);

// 設備到設備
cudaMemcpy(d_dst, d_src, bytes, cudaMemcpyDeviceToDevice);
```

## 核函數（Kernel）

### 基本語法

```cpp
__global__ void kernelName(float *data, int n) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx < n) {
        data[idx] = data[idx] * 2.0f;
    }
}
```

### 啟動配置

```cpp
// 一維執行緒組織
int blockSize = 256;
int gridSize = (n + blockSize - 1) / blockSize;
kernelName<<<gridSize, blockSize>>>(data, n);
```

### 執行緒層級

```
gridDim：區塊數量
blockDim：每區塊執行緒數
blockIdx：區塊索引
threadIdx：執行緒索引
```

## 錯誤處理

```cpp
cudaError_t err = cudaMalloc(&d_array, bytes);
if (err != cudaSuccess) {
    fprintf(stderr, "CUDA Error: %s\n", cudaGetErrorString(err));
}
```

---

## 延伸閱讀

- [CUDA C++ 官方教程](https://www.google.com/search?q=CUDA+C++tutorial)
- [記憶體管理詳解](https://www.google.com/search?q=CUDA+memory+management)
- [核函數設計模式](https://www.google.com/search?q=CUDA+kernel+design+patterns)

*本篇文章為「AI 程式人雜誌 2021 年 3 月號」精選文章。*