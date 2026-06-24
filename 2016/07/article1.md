# 向量化與 SIMD 加速

## 什麼是 SIMD？

SIMD（Single Instruction, Multiple Data）是一種並行計算技術，允許一條指令同時處理多筆資料。

## 传统方式 vs SIMD

```cpp
// 传统方式：處理 4 個浮點數需要 4 次迴圈
for (int i = 0; i < 4; i++) {
    c[i] = a[i] + b[i];
}

// SIMD 方式：一次處理 4 個浮點數
__m128 va = _mm_loadu_ps(a);
__m128 vb = _mm_loadu_ps(b);
__m128 vc = _mm_add_ps(va, vb);
_mm_storeu_ps(c, vc);
```

## x86 SIMD 指令集

### SSE（Streaming SIMD Extensions）

SSE 提供 128 位元寄存器，可容納 4 個 32 位元浮點數：

```cpp
#include <xmmintrin.h>

void vectorAdd(float* a, float* b, float* c, int n) {
    for (int i = 0; i < n; i += 4) {
        __m128 va = _mm_loadu_ps(&a[i]);
        __m128 vb = _mm_loadu_ps(&b[i]);
        __m128 vc = _mm_add_ps(va, vb);
        _mm_storeu_ps(&c[i], vc);
    }
}
```

### AVX（Advanced Vector Extensions）

AVX 提供 256 位元寄存器，可容納 8 個 32 位元浮點數：

```cpp
#include <immintrin.h>

void vectorAdd256(float* a, float* b, float* c, int n) {
    for (int i = 0; i < n; i += 8) {
        __m256 va = _mm256_loadu_ps(&a[i]);
        __m256 vb = _mm256_loadu_ps(&b[i]);
        __m256 vc = _mm256_add_ps(va, vb);
        _mm256_storeu_ps(&c[i], vc);
    }
}
```

## ARM NEON

行動裝置上的 SIMD 技術：

```cpp
#include <arm_neon.h>

void vectorAddNeon(float* a, float* b, float* c, int n) {
    for (int i = 0; i < n; i += 4) {
        float32x4_t va = vld1q_f32(&a[i]);
        float32x4_t vb = vld1q_f32(&b[i]);
        float32x4_t vc = vaddq_f32(va, vb);
        vst1q_f32(&c[i], vc);
    }
}
```

## 矩陣乘法優化

```cpp
void matMulOptimized(float* a, float* b, float* c, int n) {
    for (int i = 0; i < n; i += 4) {
        for (int k = 0; k < n; k++) {
            __m128 ak = _mm_set1_ps(a[i * n + k]);
            for (int j = 0; j < n; j += 4) {
                __m128 bkj = _mm_loadu_ps(&b[k * n + j]);
                __m128 ci = _mm_loadu_ps(&c[i * n + j]);
                __m128 r = _mm_mul_ps(ak, bkj);
                ci = _mm_add_ps(ci, r);
                _mm_storeu_ps(&c[i * n + j], ci);
            }
        }
    }
}
```

## 參考資料

- [SIMD 程式設計](https://www.google.com/search?q=SIMD+programming+tutorial)
- [SSE/AVX 優化](https://www.google.com/search?q=SSE+AVX+optimization+C++)