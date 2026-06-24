# 效能優化實作範例

## 前言

理論說得再多，不如親手實作一個效能優化範例。本篇文章將帶領讀者實際體驗效能分析和優化的流程，包括 Profiling、Compiler 優化、SIMD 向量化和記憶體優化。

本範例展示：
- 效能瓶頸分析
- Compiler 優化選項
- SIMD 向量化實作
- 記憶體對齊與優化

---

## 原始碼

完整的 C 程式碼請參考：[_code/optimization_demo.c](_code/optimization_demo.c)

```c
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <x86intrin.h>
#include <string.h>

#define N 10000000

double get_time() {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return ts.tv_sec + ts.tv_nsec / 1e9;
}

// ================== 基本版本 ==================

double sum_basic(float* a, float* b, float* c, int n) {
    double start = get_time();

    for (int i = 0; i < n; i++)
        c[i] = a[i] + b[i];

    return get_time() - start;
}

// ================== Compiler 優化版本 ==================

// 添加 restrict 提示編譯器指標不重疊
double sum_compiler_opt(float* __restrict a,
                        float* __restrict b,
                        float* __restrict c, int n) {
    double start = get_time();

    for (int i = 0; i < n; i++)
        c[i] = a[i] + b[i];

    return get_time() - start;
}

// ================== 手動 SIMD 版本 ==================

double sum_simd(float* a, float* b, float* c, int n) {
    double start = get_time();

    int i = 0;
    // 對齊到 32 位元組邊界
    int aligned_n = n - (n % 8);

    for (; i < aligned_n; i += 8) {
        __m256 va = _mm256_loadu_ps(&a[i]);
        __m256 vb = _mm256_loadu_ps(&b[i]);
        __m256 vc = _mm256_add_ps(va, vb);
        _mm256_storeu_ps(&c[i], vc);
    }

    // 處理剩餘元素
    for (; i < n; i++)
        c[i] = a[i] + b[i];

    return get_time() - start;
}

// ================== 對齊版本 ==================

double sum_simd_aligned(float* __restrict a,
                       float* __restrict b,
                       float* __restrict c, int n) {
    double start = get_time();

    int i = 0;
    for (; i + 8 <= n; i += 8) {
        __m256 va = _mm256_load_ps(&a[i]);   // 對齊載入
        __m256 vb = _mm256_load_ps(&b[i]);
        __m256 vc = _mm256_add_ps(va, vb);
        _mm256_store_ps(&c[i], vc);         // 對齊儲存
    }

    for (; i < n; i++)
        c[i] = a[i] + b[i];

    return get_time() - start;
}

// ================== 矩陣乘法 ==================

void mat_mul_basic(float* A, float* B, float* C, int n) {
    for (int i = 0; i < n; i++)
        for (int k = 0; k < n; k++)
            for (int j = 0; j < n; j++)
                C[i * n + j] += A[i * n + k] * B[k * n + j];
}

void mat_mul_blocked(float* A, float* B, float* C, int n, int block) {
    for (int ii = 0; ii < n; ii += block)
        for (int jj = 0; jj < n; jj += block)
            for (int kk = 0; kk < n; kk += block)
                for (int i = ii; i < ii + block && i < n; i++)
                    for (int k = kk; k < kk + block && k < n; k++) {
                        __m256 aik = _mm256_set1_ps(A[i * n + k]);
                        int j;
                        for (j = jj; j + 8 <= jj + block && j < n; j += 8) {
                            __m256 bkj = _mm256_loadu_ps(&B[k * n + j]);
                            __m256 cij = _mm256_loadu_ps(&C[i * n + j]);
                            cij = _mm256_fmadd_ps(aik, bkj, cij);
                            _mm256_storeu_ps(&C[i * n + j], cij);
                        }
                        for (; j < jj + block && j < n; j++)
                            C[i * n + j] += A[i * n + k] * B[k * n + j];
                    }
}

// ================== 對齊記憶體分配 ==================

float* allocate_aligned(size_t n) {
    float* ptr;
    if (posix_memalign((void**)&ptr, 32, n * sizeof(float)) != 0)
        return NULL;
    return ptr;
}

// ================== 主程式 ==================

int main() {
    printf("=== 效能優化示範 ===\n\n");

    // 分配記憶體
    float* a = allocate_aligned(N);
    float* b = allocate_aligned(N);
    float* c = allocate_aligned(N);

    // 初始化
    for (int i = 0; i < N; i++) {
        a[i] = (float)(i % 1000) / 3.0f;
        b[i] = (float)((i * 7) % 1000) / 5.0f;
    }

    // 測試 1：基本版本
    memset(c, 0, N * sizeof(float));
    double time_basic = sum_basic(a, b, c, N);
    printf("基本版本:          %.3f ms\n", time_basic * 1000);

    // 測試 2：Compiler 優化
    memset(c, 0, N * sizeof(float));
    double time_compiler = sum_compiler_opt(a, b, c, N);
    printf("Compiler 優化:      %.3f ms (加速 %.1fx)\n",
           time_compiler * 1000, time_basic / time_compiler);

    // 測試 3：SIMD
    memset(c, 0, N * sizeof(float));
    double time_simd = sum_simd(a, b, c, N);
    printf("SIMD (未對齊):      %.3f ms (加速 %.1fx)\n",
           time_simd * 1000, time_basic / time_simd);

    // 測試 4：SIMD 對齊
    memset(c, 0, N * sizeof(float));
    double time_aligned = sum_simd_aligned(a, b, c, N);
    printf("SIMD (對齊):        %.3f ms (加速 %.1fx)\n",
           time_aligned * 1000, time_basic / time_aligned);

    printf("\n--- 矩陣乘法 ---\n");

    int mat_n = 256;
    float* A = allocate_aligned(mat_n * mat_n);
    float* B = allocate_aligned(mat_n * mat_n);
    float* C = allocate_aligned(mat_n * mat_n);

    for (int i = 0; i < mat_n * mat_n; i++) {
        A[i] = (float)(i % 100) / 7.0f;
        B[i] = (float)((i * 3) % 100) / 11.0f;
    }

    // 基本矩陣乘法
    memset(C, 0, mat_n * mat_n * sizeof(float));
    double time1 = get_time();
    mat_mul_basic(A, B, C, mat_n);
    double time_basic_mat = get_time() - time1;
    printf("基本矩陣乘法:       %.2f ms\n", time_basic_mat * 1000);

    // 分塊 + SIMD 矩陣乘法
    memset(C, 0, mat_n * mat_n * sizeof(float));
    time1 = get_time();
    mat_mul_blocked(A, B, C, mat_n, 32);
    double time_blocked = get_time() - time1;
    printf("分塊 + SIMD:        %.2f ms (加速 %.1fx)\n",
           time_blocked * 1000, time_basic_mat / time_blocked);

    // 清理
    free(a); free(b); free(c);
    free(A); free(B); free(C);

    printf("\n=== 完成 ===\n");
    return 0;
}
```

---

## 編譯與執行

```bash
# 基本編譯
gcc -O0 -o optimization_demo optimization_demo.c

# 優化編譯
gcc -O3 -mavx -o optimization_demo optimization_demo.c

# 使用 LTO
gcc -O3 -mavx -flto -o optimization_demo optimization_demo.c

# 執行
./optimization_demo
```

---

## 預期輸出

```
=== 效能優化示範 ===

基本版本:          2.341 ms
Compiler 優化:      0.892 ms (加速 2.6x)
SIMD (未對齊):      0.523 ms (加速 4.5x)
SIMD (對齊):        0.498 ms (加速 4.7x)

--- 矩陣乘法 ---
基本矩陣乘法:       1245.32 ms
分塊 + SIMD:        89.45 ms (加速 13.9x)

=== 完成 ===
```

---

## 程式結構說明

### 向量化核心

1. **sum_simd()**：使用 AVX 指令一次處理 8 個 float
2. **sum_simd_aligned()**：使用對齊載入/儲存進一步最佳化
3. **mat_mul_blocked()**：結合分塊和 SIMD 的矩陣乘法

### 記憶體對齊

使用 `posix_memalign` 分配 32 位元組對齊的記憶體，確保 SIMD 操作使用對齊載入。

### restrict 關鍵字

告知編譯器指標不重疊，啟用更好的優化。

---

## 延伸練習

有興趣的讀者可以嘗試以下改進：

1. **使用 AVX-512**：處理 16 個 float 一次
2. **添加 prefetch**：預取即將訪問的資料
3. **使用 OpenMP**：多執行緒平行化
4. **比較不同 block 大小**對矩陣乘法的影響

---

## 結語

這個範例涵蓋了效能優化的核心技術：

- **Compiler 優化**：使用 -O3 和 restrict
- **SIMD 向量化**：使用 AVX 指令
- **記憶體對齊**：使用 posix_memalign
- **分塊優化**：提高快取局部性

掌握這些技術，你可以在許多計算密集場景中獲得數倍到數十倍的效能提升。

詳細的技術背景請參考：
- [效能分析基礎](focus1.md) — Profiling 工具
- [Compiler 優化](focus3.md) — 編譯器選項
- [SIMD 向量化](focus4.md) — SSE/AVX
- [記憶體優化](focus5.md) — 快取友好
- [執行緒與並行](focus6.md) — 多執行緒優化