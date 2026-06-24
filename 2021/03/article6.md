# 深度學習加速原理

## GPU 與深度學習

GPU 的平行運算架構非常適合深度學習：

- **矩陣乘法**：高度並行
- **卷積運算**：滑動窗口
- **自動微分**：梯度計算

## 運算加速原理

### 矩陣運算

```
傳統方式（CPU）：
for i in range(n):
    for j in range(m):
        C[i][j] += A[i][k] * B[k][j]

GPU 方式：
每個執行緒計算 C[i][j] 的單一元素
```

### 卷積加速

GPU 使用「展開 - 矩陣乘法 - reshape」策略：
1. 將卷積核和輸入展開
2. 轉換為矩陣乘法
3. 受益於高度優化的矩陣運算庫

## cuDNN 庫

NVIDIA 提供的深度學習原語庫：

```cpp
#include <cudnn.h>

cudnnHandle_t cudnn;
cudnnCreate(&cudnn);

cudnnConvolutionForward(cudnn,
    &alpha, input_desc, input_data,
    filter_desc, filter_data,
    conv_desc, algo, workSpace, workSpaceSize,
    &beta, output_desc, output_data);
```

## 混合精度加速

```cpp
// 使用 TensorCore 加速
__half *d_input, *d_output;
// 矩陣乘法使用 TensorCore
cublasGemmEx(handle,
    CUBLAS_OP_N, CUBLAS_OP_N,
    m, n, k,
    &alpha, d_A, CUDA_R_16F, lda,
           d_B, CUDA_R_16F, ldb,
    &beta,  d_C, CUDA_R_16F, ldc,
    CUDA_R_16F, CUBLAS_GEMM_DEFAULT_TENSOR_OP);
```

---

## 延伸閱讀

- [GPU+深度學習加速原理](https://www.google.com/search?q=GPU+deep+learning+acceleration)
- [cuDNN+使用說明](https://www.google.com/search?q=cuDNN+documentation)
- [混合精度訓練](https://www.google.com/search?q=mixed+precision+training+TensorCore)

*本篇文章為「AI 程式人雜誌 2021 年 3 月號」精選文章。*