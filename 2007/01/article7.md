# GPU 運算普及：CUDA 與平行計算

## 前言

2007 年，NVIDIA 正式發布了 CUDA（Compute Unified Device Architecture）平台，將 GPU 從單純的遊戲顯示核心轉變為通用的平行運算設備。

## CUDA 的發布背景

### GPU 的運算潛力

傳統上，GPU 被用於圖形渲染。但 GPU 的架構特性使其非常適合平行運算：

```
┌────────────────────────────────────────────────────────┐
│            CPU vs GPU 架構差異                         │
├────────────────────────────────────────────────────────┤
│                                                        │
│  CPU：                                                 │
│  - 少量強大的核心 (2-8 個)                             │
│  - 擅長序列處理                                        │
│  - 低延遲                                              │
│  - 通用用途                                            │
│                                                        │
│  GPU：                                                 │
│  - 大量弱小的核心 (數百到數千個)                       │
│  - 擅長平行處理                                        │
│  - 高吞吐量                                            │
│  - 針對圖形優化                                        │
│                                                        │
└────────────────────────────────────────────────────────┘
```

### CUDA 的意義

```python
# CUDA 之前，要用 GPU 計算必須：
PRE_CUDA = {
    "問題": "必須透過圖形 API (OpenGL/DirectX) 存取",
    "限制": "無法直接寫運算代碼",
    "效率": "大量开销用於格式轉換"
}

# CUDA 出現後：
WITH_CUDA = {
    "可能": "用 C 語言直接寫 GPU 程式",
    "優勢": "簡單的記憶體模型和執行模型",
    "效率": "直接存取 GPU 運算能力"
}
```

## CUDA 架構

### 基本概念

```c
// CUDA 程式的基本結構
// 這個範例展示向量加法

#include <cuda_runtime.h>

// Kernel 函式：在 GPU 上執行
__global__ void vectorAdd(float *A, float *B, float *C, int N)
{
    // 每個執行緒處理一個元素
    int i = blockDim.x * blockIdx.x + threadIdx.x;
    if (i < N) {
        C[i] = A[i] + B[i];
    }
}

int main()
{
    // 主機端記憶體配置
    float *h_A, *h_B, *h_C;
    float *d_A, *d_B, *d_C;

    // 配置 GPU 記憶體
    cudaMalloc(&d_A, N * sizeof(float));
    cudaMalloc(&d_B, N * sizeof(float));
    cudaMalloc(&d_C, N * sizeof(float));

    // 複製資料到 GPU
    cudaMemcpy(d_A, h_A, N * sizeof(float), cudaMemcpyHostToDevice);
    cudaMemcpy(d_B, h_B, N * sizeof(float), cudaMemcpyHostToDevice);

    // 啟動 Kernel
    int threadsPerBlock = 256;
    int blocksPerGrid = (N + threadsPerBlock - 1) / threadsPerBlock;
    vectorAdd<<<blocksPerGrid, threadsPerBlock>>>(d_A, d_B, d_C, N);

    // 複製結果回主機
    cudaMemcpy(h_C, d_C, N * sizeof(float), cudaMemcpyDeviceToHost);

    // 釋放記憶體
    cudaFree(d_A);
    cudaFree(d_B);
    cudaFree(d_C);

    return 0;
}
```

### CUDA 執行模型

```
┌────────────────────────────────────────────────────────┐
│            CUDA 執行模型                               │
├────────────────────────────────────────────────────────┤
│                                                        │
│  執行層級：                                            │
│  Grid → Block → Thread                               │
│                                                        │
│  ┌─────────────────────────────────────────┐          │
│  │              Grid                        │          │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐ │          │
│  │  │  Block  │  │  Block  │  │  Block  │ │          │
│  │  │ ┌─┬─┬─┐ │  │ ┌─┬─┬─┐ │  │ ┌─┬─┬─┐ │ │          │
│  │  │ │T│T│T│ │  │ │T│T│T│ │  │ │T│T│T│ │ │          │
│  │  │ └─┴─┴─┘ │  │ └─┴─┴─┘ │  │ └─┴─┴─┘ │ │          │
│  │  └─────────┘  └─────────┘  └─────────┘ │          │
│  └─────────────────────────────────────────┘          │
│                                                        │
│  每個執行緒有唯一 ID，可存取自己的資料                  │
│                                                        │
└────────────────────────────────────────────────────────┘
```

## 科學計算的應用

### 2007 年的應用領域

CUDA 最初在科學計算領域獲得青睞：

```python
# 2007 年 CUDA 的主要應用
CUDA_APPLICATIONS_2007 = {
    "分子動力學": "NAMD、VMD 模擬",
    "流體力學": "CFD 計算",
    "天氣預測": "氣候模型",
    "生物資訊": "序列比對",
    "物理模擬": "粒子系統",
    "電腦視覺": "影像處理"
}
```

### 效能提升

```
┌────────────────────────────────────────────────────────┐
│          GPU vs CPU 效能比較 (2007 年)                 │
├────────────────────────────────────────────────────────┤
│                                                        │
│  測試項目：矩陣乘法                                    │
│                                                        │
│  CPU (Core 2 Duo 3.0GHz)：                           │
│  - 時間：~2000 ms                                    │
│                                                        │
│  GPU (NVIDIA 8800 GTX)：                              │
│  - 時間：~100 ms                                     │
│  - 加速：~20x                                        │
│                                                        │
│  注意：並非所有問題都適合 GPU                          │
│                                                        │
└────────────────────────────────────────────────────────┘
```

## CUDA 對 AI 的影響

### 深度學習的硬體基礎

CUDA 的出現對深度學習有深遠影響：

```python
# GPU 加速深度學習訓練
DEEP_LEARNING_SPEEDUP = {
    "訓練時間": "可能縮短 10-100 倍",
    "模型大小": "可用更大的模型",
    "資料規模": "可處理更大的資料集"
}

# 這為日後 AlexNet (2012) 的成功奠定基礎
```

### 時間線對照

```
┌────────────────────────────────────────────────────────┐
│          GPU 運算與深度學習的時間線                     │
├────────────────────────────────────────────────────────┤
│                                                        │
│  2006：NVIDIA 發布 CUDA beta                          │
│  2007：NVIDIA 正式發布 CUDA 1.0                       │
│       └─ GeForce 8800 系列                            │
│                                                        │
│  2008：CUDA 2.0，更多最佳化                          │
│                                                        │
│  2009：深度學習論文開始使用 GPU                       │
│                                                        │
│  2012：AlexNet 使用 GPU 訓練，                        │
│       ImageNet 突破，深度學習時代來臨                  │
│                                                        │
└────────────────────────────────────────────────────────┘
```

## OpenCL 與其他選項

### OpenCL 的競爭

2007 年，Khronos Group 也發布了 OpenCL 標準：

```python
# CUDA vs OpenCL
COMPARISON = {
    "CUDA": {
        "優點": "更好的效能、完整工具鏈",
        "缺點": "僅支援 NVIDIA GPU",
        "生態": "更成熟"
    },
    "OpenCL": {
        "優點": "跨平台、多廠商支援",
        "缺點": "效能通常較差",
        "生態": "逐漸成長"
    }
}
```

## 結論

2007 年 CUDA 的發布，開啟了 GPU 通用運算的時代。這項技術不僅改變了科學計算的版圖，更為日後深度學習的爆發提供了硬體基礎。

我們今天所見的 AI 革命，某種程度上可以追溯到 2007 年 NVIDIA 的這個決定。

---

## 延伸閱讀

- [CUDA 發布歷史](https://www.google.com/search?q=NVIDIA+CUDA+2007+launch)
- [GPU 運算簡介](https://www.google.com/search?q=GPGPU+history+CUDA)
- [CUDA 程式設計](https://www.google.com/search?q=CUDA+programming+tutorial)

---

*本篇文章為「AI 程式人雜誌 2007 年 1 月號」文章集錦系列。*