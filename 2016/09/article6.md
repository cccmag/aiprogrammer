# AVX-512 向量化

## AVX-512 簡介

AVX-512 是 Intel 的 512 位元 SIMD 指令集擴展。

### 與 AVX/AVX2 比較

| 特性 | AVX | AVX2 | AVX-512 |
|------|-----|------|---------|
| 暫存器大小 | 256 位元 | 256 位元 | 512 位元 |
| 暫存器數量 | 16 | 16 | 32 |
| float 操作數 | 8 | 8 | 16 |
| double 操作數 | 4 | 4 | 8 |

## 資料類型

```c
#include <immintrin.h>

__m512  v_float;    // 16 個 float
__m512d v_double;   // 8 個 double
__m512i v_int;      // 整數向量

// 遮罩類型
__mmask16 m16;      // 16 個 1 位元遮罩
__mmask8 m8;        // 8 個 1 位元遮罩
```

## 基本運算

### 載入與儲存

```c
// 對齊載入（要求 64 位元組對齊）
__m512 a = _mm512_load_ps(aligned_ptr);

// 未對齊載入
__m512 a = _mm512_loadu_ps(unaligned_ptr);

// 對齊儲存
_mm512_store_ps(aligned_ptr, a);

// 廣播：一個值填充整個暫存器
__m512 b = _mm512_set1_ps(1.0f);
```

### 算術運算

```c
// 加法
__m512 c = _mm512_add_ps(a, b);

// 乘法
__m512 d = _mm512_mul_ps(a, b);

// 融合乘加（FMA）
__m512 e = _mm512_fmadd_ps(a, b, c);  // a * b + c
__m512 f = _mm512_fnmadd_ps(a, b, c); // -a * b + c
```

## 遮罩操作

```c
__mmask16 mask = 0xFF55;  // 選擇性地操作

// 選擇性加法
__m512 result = _mm512_mask_add_ps(c, mask, a, b);
// 根據 mask 決定哪些元素被更新
```

## 對齊要求

```c
// 64 位元組對齊（AVX-512 要求）
__attribute__((aligned(64))) float array[64];

// 或使用 posix_memalign
void* ptr;
posix_memalign(&ptr, 64, size);
```

## 實際範例：陣列求和

```c
#include <immintrin.h>

float array_sum(float* arr, int n) {
    __m512 sum_vec = _mm512_setzero_ps();
    int i = 0;

    // 處理 16 個元素為一組
    for (; i + 16 <= n; i += 16) {
        __m512 v = _mm512_loadu_ps(&arr[i]);
        sum_vec = _mm512_add_ps(sum_vec, v);
    }

    // 水平相加所有元素
    float sum = _mm512_reduce_add_ps(sum_vec);

    // 處理剩餘元素
    for (; i < n; i++)
        sum += arr[i];

    return sum;
}
```

## 與 AVX-256 的混合使用

```c
// 某些處理器不支援 AVX-512 但支援 AVX2
// 可以動態檢測並選擇適當的程式碼路徑

void process(float* a, float* b, float* c, int n) {
    if (cpu_has_avx512()) {
        // AVX-512 程式碼
    } else if (cpu_has_avx()) {
        // AVX 程式碼
    } else {
        // 一般程式碼
    }
}
```

## 常見錯誤

### 1. 忘記對齊

```c
// 錯誤：導致崩潰或性能下降
__m512 a = _mm512_load_ps(ptr);  // ptr 可能未對齊

// 正確：使用未對齊載入或確保對齊
__m512 a = _mm512_loadu_ps(ptr);
```

### 2. 遮罩使用不當

```c
// 遮罩只有低位元有效
__mmask16 m = 0xFFFF;  // 正確，16 個元素
__mmask16 m = 0x1FFFF; // 錯誤，只取低 16 位元
```

## 參考資料

- [AVX-512 程式設計](https://www.google.com/search?q=AVX-512+programming+tutorial)
- [Intel Intrinsics 指南](https://www.google.com/search?q=Intel+intrinsics+guide)