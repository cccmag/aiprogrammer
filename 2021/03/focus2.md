# CUDA 程式模型

## 執行模型

### 主機與設備

```cpp
// 主機端（CPU）
int main() {
    // 配置記憶體
    float *d_data;
    cudaMalloc(&d_data, size);

    // 拷貝資料到設備
    cudaMemcpy(d_data, h_data, size, cudaMemcpyHostToDevice);

    // 啟動核心
    myKernel<<<blocks, threads>>>(d_data);

    // 拷貝結果回主機
    cudaMemcpy(h_result, d_data, size, cudaMemcpyDeviceToHost);

    cudaFree(d_data);
}
```

### 核心函數

```cpp
__global__ void myKernel(float *data) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    data[idx] = data[idx] * 2.0f;
}
```

## 執行配置

```cpp
// 二維區塊
dim3 blocks(16, 16);
// 三維執行緒
dim3 threads(32, 32, 1);

myKernel<<<blocks, threads>>>(data);
```

## 記憶體層級

```
全域記憶體（Device Memory）
    ↓
共享記憶體（Shared Memory）
    ↓
暫存器（Registers）
    ↓
本地記憶體（Local Memory）
```

| 記憶體類型 | 延遲 | 作用域 |
|-----------|------|--------|
| 暫存器 | 1 cycle | 執行緒 |
| 本地 | ~100 cycles | 執行緒 |
| 共享 | ~10 cycles | 區塊 |
| 全域 | ~400 cycles | 全域 |

## Warp 執行

- 每個 Warp 包含 32 個執行緒
- 同一 Warp 執行相同指令
- 分支分歧導致效能下降

---

## 延伸閱讀

- [CUDA+C++程式設計指南](https://www.google.com/search?q=CUDA+C+Programming+Guide)
- [執行模型詳解](https://www.google.com/search?q=CUDA+execution+model)
- [記憶體層級介紹](https://www.google.com/search?q=CUDA+memory+hierarchy)

*本篇文章為「AI 程式人雜誌 2021 年 3 月號」精選文章。*