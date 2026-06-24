# SIMD 向量化

## SIMD 簡介

SIMD（Single Instruction, Multiple Data）允許一條指令同時處理多筆資料。

## SSE / AVX 指令集

### 向量暫存器大小

| 指令集 | 暫存器 | 向量大小 |
|-------|--------|---------|
| SSE | XMM0-15 | 128 位元（16 位元組） |
| AVX | XMM0-15 / YMM0-15 | 256 位元（32 位元組） |
| AVX-512 | ZMM0-31 | 512 位元（64 位元組） |

### 可處理的資料量

以 float 為例（32 位元）：

| 指令集 | float 數量 |
|-------|-----------|
| SSE | 4 |
| AVX | 8 |
| AVX-512 | 16 |

## Intrinsics 程式設計

### 標頭檔

```c
#include <xmmintrin.h>    // SSE
#include <emmintrin.h>    // SSE2
#include <pmmintrin.h>    // SSE3
#include <tmmintrin.h>    // SSSE3
#include <smmintrin.h>    // SSE4.1
#include <nmmintrin.h>    // SSE4.2
#include <immintrin.h>    // AVX/AVX2/AVX-512
```

### 資料類型

```c
__m128  v1;    // 4 個 float 或 2 個 double
__m128d v2;
__m128i v3;    // 整數向量

__m256  v4;    // 8 個 float（AVX）
__m256d v5;
__m256i v6;
```

### 基本運算

```c
#include <immintrin.h>

// 載入與儲存
__m256 a = _mm256_loadu_ps(arr);          // 未對齊載入
__m256 b = _mm256_set1_ps(1.0f);          // 所有元素設為 1.0
__m256 c = _mm256_add_ps(a, b);           // 加法
__m256 d = _mm256_mul_ps(a, b);           // 乘法

_mm256_storeu_ps(result, d);              // 未對齊儲存
```

## 向量化範例

### 陣列相加

```c
void vector_add(float* a, float* b, float* c, int n) {
    int i;
    for (i = 0; i + 8 <= n; i += 8) {
        __m256 va = _mm256_loadu_ps(&a[i]);
        __m256 vb = _mm256_loadu_ps(&b[i]);
        __m256 vc = _mm256_add_ps(va, vb);
        _mm256_storeu_ps(&c[i], vc);
    }
    // 處理剩餘元素
    for (; i < n; i++)
        c[i] = a[i] + b[i];
}
```

### 矩陣乘法（簡化版）

```c
void mat_mul(float* A, float* B, float* C, int n) {
    for (int i = 0; i < n; i++) {
        for (int k = 0; k < n; k++) {
            __m256 ak = _mm256_set1_ps(A[i * n + k]);
            int j;
            for (j = 0; j + 8 <= n; j += 8) {
                __m256 bk = _mm256_loadu_ps(&B[k * n + j]);
                __m256 c = _mm256_loadu_ps(&C[i * n + j]);
                c = _mm256_fmadd_ps(ak, bk, c);  // a*b+c（融合乘加）
                _mm256_storeu_ps(&C[i * n + j], c);
            }
            for (; j < n; j++)
                C[i * n + j] += A[i * n + k] * B[k * n + j];
        }
    }
}
```

## 自動向量化

### 範例：簡單循環

```c
void sum_array(float* a, float* b, float* c, int n) {
    for (int i = 0; i < n; i++)
        c[i] = a[i] + b[i];
}
```

編譯器可能自動向量化：
```bash
gcc -O3 -ftree-vectorize -S program.c
```

### 幫助編譯器向量化

```c
// 1. 確保記憶體對齊
__attribute__((aligned(32))) float arr[1024];

// 2. 使用 restrict 避免指標別名
void process(float* __restrict a, float* __restrict b, int n) {
    for (int i = 0; i < n; i++)
        a[i] += b[i];
}

// 3. 使用 #pragma simd
#pragma omp simd
for (int i = 0; i < n; i++)
    c[i] = a[i] + b[i];
```

## AVX-512 特性

### 語法

```c
#include <immintrin.h>

// 512 位元暫存器
__m512 a = _mm512_set1_ps(1.0f);
__m512 b = _mm512_add_ps(a, a);  // 16 個 float

// 遮罩操作
__mmask16 mask = 0xFF55;  // 選擇性操作
__m512 result = _mm512_mask_add_ps(c, mask, a, b);
```

### 融合乘加（FMA）

```c
// 單一指令：a * b + c
__m512 result = _mm512_fmadd_ps(a, b, c);
__m512 result = _mm512_fmsub_ps(a, b, c);  // a * b - c
__m512 result = _mm512_fnmsub_ps(a, b, c); // -(a * b) + c
```

## 效能考量

### 記憶體對齊

```c
// 對齊的載入（更快）
__m256 a = _mm256_load_ps(aligned_ptr);

// 未對齊的載入（較慢，但功能正確）
__m256 a = _mm256_loadu_ps(unaligned_ptr);
```

### 避免資料相關

```c
// 不好：每次迭代依賴前一次結果
for (int i = 1; i < n; i++)
    a[i] = a[i-1] * b[i];

// 好：獨立的操作，可以向量化
for (int i = 0; i < n; i++)
    a[i] = b[i] + c[i];
```

### 混合使用

```c
// 熱路徑使用 SIMD，其他使用一般程式碼
void process() {
    // SIMD 處理大部分資料
    for (i = 0; i + 8 <= n; i += 8) { /* SIMD */ }

    // 處理剩餘元素
    for (; i < n; i++) { /* scalar */ }
}
```

## ARM NEON

行動裝置的 SIMD：

```c
#include <arm_neon.h>

// 128 位元 NEON（與 SSE 類似）
float32x4_t a = vld1q_f32(arr);
float32x4_t b = vaddq_f32(a, a);
vst1q_f32(result, b);
```

## 參考資料

- [SIMD Intrinsics 指南](https://www.google.com/search?q=SIMD+intrinsics+guide)
- [AVX 程式設計](https://www.google.com/search?q=AVX+programming+tutorial)
- [自動向量化](https://www.google.com/search?q=auto+vectorization+C++)