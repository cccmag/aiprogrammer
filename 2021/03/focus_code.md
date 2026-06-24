# CUDA 程式設計範例

## 前言

本篇文章展示 CUDA 程式設計的核心概念，包括記憶體管理、核函數設計和效能優化。

完整的 CUDA 實作請參考：[_code/cuda_demo.cu](_code/cuda_demo.cu)

## 核心程式碼

### 簡單核心函數

```cpp
__global__ void vectorAdd(float *a, float *b, float *c, int n) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx < n) {
        c[idx] = a[idx] + b[idx];
    }
}
```

### 呼叫核函數

```cpp
int main() {
    int n = 1000000;
    size_t bytes = n * sizeof(float);

    // 配置記憶體
    float *h_a, *h_b, *h_c;
    float *d_a, *d_b, *d_c;

    cudaMalloc(&d_a, bytes);
    cudaMalloc(&d_b, bytes);
    cudaMalloc(&d_c, bytes);

    // 拷貝資料
    cudaMemcpy(d_a, h_a, bytes, cudaMemcpyHostToDevice);
    cudaMemcpy(d_b, h_b, bytes, cudaMemcpyHostToDevice);

    // 啟動核函數
    int blockSize = 256;
    int gridSize = (n + blockSize - 1) / blockSize;
    vectorAdd<<<gridSize, blockSize>>>(d_a, d_b, d_c, n);

    // 拷貝結果
    cudaMemcpy(h_c, d_c, bytes, cudaMemcpyDeviceToHost);

    // 釋放記憶體
    cudaFree(d_a);
    cudaFree(d_b);
    cudaFree(d_c);

    return 0;
}
```

## 矩陣乘法優化

### 基本版本

```cpp
__global__ void matrixMul(float *a, float *b, float *c, int n) {
    int row = blockIdx.y * blockDim.y + threadIdx.y;
    int col = blockIdx.x * blockDim.x + threadIdx.x;

    float sum = 0.0f;
    if (row < n && col < n) {
        for (int k = 0; k < n; k++) {
            sum += a[row * n + k] * b[k * n + col];
        }
        c[row * n + col] = sum;
    }
}
```

### 共享記憶體優化

```cpp
__global__ void matrixMulShared(float *a, float *b, float *c, int n) {
    __shared__ float s_a[16][16];
    __shared__ float s_b[16][16];

    int tx = threadIdx.x;
    int ty = threadIdx.y;
    int row = blockIdx.y * 16 + ty;
    int col = blockIdx.x * 16 + tx;

    float sum = 0.0f;

    for (int m = 0; m < n/16; m++) {
        s_a[ty][tx] = a[row * n + m * 16 + tx];
        s_b[ty][tx] = b[(m * 16 + ty) * n + col];
        __syncthreads();

        for (int k = 0; k < 16; k++) {
            sum += s_a[ty][k] * s_b[k][tx];
        }
        __syncthreads();
    }

    if (row < n && col < n) {
        c[row * n + col] = sum;
    }
}
```

## 效能測量

```cpp
cudaEvent_t start, stop;
cudaEventCreate(&start);
cudaEventCreate(&stop);

cudaEventRecord(start);
kernel<<<gridSize, blockSize>>>(args);
cudaEventRecord(stop);

cudaEventSynchronize(stop);
float milliseconds = 0;
cudaEventElapsedTime(&milliseconds, start, stop);
```

---

## 延伸閱讀

- [CUDA C++ 程式設計指南](https://www.google.com/search?q=CUDA+C++Programming+Guide)
- [GPU+記憶體優化](https://www.google.com/search?q=GPU+memory+optimization+CUDA)
- [CUDA+效能分析工具](https://www.google.com/search?q=Nsight+CUDA+profiling)

*本篇文章為「AI 程式人雜誌 2021 年 3 月號」補充文章。*