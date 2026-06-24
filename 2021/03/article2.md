# 共享記憶體最佳化

## 共享記憶體基礎

```cpp
__global__ void kernel(float *data) {
    __shared__ float s_data[256];

    int idx = threadIdx.x;
    s_data[idx] = data[idx];
    __syncthreads();

    // 使用共享記憶體
    float sum = s_data[0] + s_data[1];
}
```

## 同步機制

### `__syncthreads()`

同一區塊內所有執行緒同步：

```cpp
__shared__ float temp[256];

temp[threadIdx.x] = compute();
__syncthreads();  // 所有執行緒到達此點後才繼續

if (threadIdx.x == 0) {
    float sum = 0;
    for (int i = 0; i < 256; i++) sum += temp[i];
}
```

### 記憶體fence

```cpp
__threadfence();  // 記憶體可見性屏障
```

##  банняк  Usage

### 矩陣轉置

```cpp
__global__ void transpose(float *odata, float *idata, int width) {
    __shared__ float tile[16][16];

    int x = blockIdx.x * 16 + threadIdx.x;
    int y = blockIdx.y * 16 + threadIdx.y;

    tile[threadIdx.y][threadIdx.x] = idata[y * width + x];
    __syncthreads();

    int outX = blockIdx.y * 16 + threadIdx.x;
    int outY = blockIdx.x * 16 + threadIdx.y;
    odata[outY * width + outX] = tile[threadIdx.x][threadIdx.y];
}
```

## 效能考量

- bank 大小：通常 32 或 64 位元組
- 避免 bank 衝突
- 合理規劃 tile 大小

---

## 延伸閱讀

- [共享記憶體詳解](https://www.google.com/search?q=CUDA+shared+memory+tutorial)
- [銀行衝突優化](https://www.google.com/search?q=shared+memory+bank+conflict)
- [同步原語](https://www.google.com/search?q=__syncthreads+usage)

*本篇文章為「AI 程式人雜誌 2021 年 3 月號」精選文章。*