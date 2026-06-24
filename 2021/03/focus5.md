# ROCm 與 AMD GPU

## ROCm 簡介

ROCm（Radeon Open Compute Platform）是 AMD 的開放運算平台：

```bash
# 安裝 ROCm
sudo apt install rocm-dkms
```

## HIP 程式設計

HIP 提供與 CUDA 相容的程式設計介面：

```cpp
#define HIP_RUNTIME_COMPILE 1

#include <hip/hip_runtime.h>

__global__ void kernel(float *data) {
    int idx = hipThreadIdx_x;
    data[idx] = data[idx] * 2.0f;
}

void launchKernel(float *d_data, int size) {
    hipLaunchKernelGGL(kernel,
        dim3(1), dim3(size), 0, 0,
        d_data);
}
```

## 與 CUDA 的比較

| 特性 | CUDA | ROCm |
|------|------|------|
| 開發者 | NVIDIA | AMD |
| 語言 | CUDA C++ | HIP / CUDA |
| 效能 | 極高 | 接近 CUDA |
| 生態 | 成熟 | 持續發展 |

## 支援的 GPU

```
CDNA 架構：
- AMD Instinct MI100
- AMD Instinct MI200

RDNA 架構：
- RX 6000 系列
```

## 深度學習支援

```bash
# 安裝 MIOpen（AMD 的深度學習庫）
sudo apt install rocm-miopennn
```

---

## 延伸閱讀

- [ROCm+官方網站](https://www.google.com/search?q=AMD+ROCm+official)
- [HIP+程式設計指南](https://www.google.com/search?q=HIP+programming+guide)
- [ROCm+vs+CUDA](https://www.google.com/search?q=ROCm+vs+CUDA+comparison)

*本篇文章為「AI 程式人雜誌 2021 年 3 月號」精選文章。*