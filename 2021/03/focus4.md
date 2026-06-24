# cuBLAS 與 cuFFT

## cuBLAS 簡介

cuBLAS 是 NVIDIA 提供的 BLAS（Basic Linear Algebra Subprograms）GPU 實現：

```cpp
#include <cublas_v2.h>

cublasStatus_t status;
cublasHandle_t handle;
cublasCreate(&handle);

// 矩陣乘法：C = alpha * A * B + beta * C
float *d_A, *d_B, *d_C;
float alpha = 1.0f, beta = 0.0f;

cublasSgemm(handle,
    CUBLAS_OP_N, CUBLAS_OP_N,
    m, n, k,
    &alpha,
    d_A, lda,
    d_B, ldb,
    &beta,
    d_C, ldc
);
```

## 常用函數

| 函數 | 說明 |
|------|------|
| cublasSgemm | 單精度矩陣乘法 |
| cublasDgemm | 雙精度矩陣乘法 |
| cublasGemmEx | 混合精度矩陣乘法 |
| cublasAxpy | 向量更新 |

## cuFFT 簡介

cuFFT 用於離散傅立葉變換：

```cpp
#include <cufft.h>

cufftHandle plan;
cufftPlan1d(&plan, N, CUFFT_C2C, 1);

// 執行 FFT
cufftExecC2C(plan, (cufftComplex *)d_data,
                       (cufftComplex *)d_data,
                       CUFFT_FORWARD);

// 銷毀計劃
cufftDestroy(plan);
```

## FFT 應用

- 訊號處理
- 影像處理
- 卷積加速

## 效能優化

```cpp
// 選擇最佳 plansize
cufftPlanMany(&plan, rank, n,
              inembed, istride, idist,
              onembed, ostride, odist,
              type, batch);
```

---

## 延伸閱讀

- [cuBLAS+官方文檔](https://www.google.com/search?q=cuBLAS+documentation+NVIDIA)
- [cuFFT+使用教學](https://www.google.com/search?q=cuFFT+tutorial+examples)
- [GPU+線性代數庫](https://www.google.com/search?q=GPGPU+linear+algebra+library)

*本篇文章為「AI 程式人雜誌 2021 年 3 月號」精選文章。*