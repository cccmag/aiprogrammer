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
    int aligned_n = n - (n % 8);

    for (; i < aligned_n; i += 8) {
        __m256 va = _mm256_loadu_ps(&a[i]);
        __m256 vb = _mm256_loadu_ps(&b[i]);
        __m256 vc = _mm256_add_ps(va, vb);
        _mm256_storeu_ps(&c[i], vc);
    }

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
        __m256 va = _mm256_load_ps(&a[i]);
        __m256 vb = _mm256_load_ps(&b[i]);
        __m256 vc = _mm256_add_ps(va, vb);
        _mm256_store_ps(&c[i], vc);
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

    float* a = allocate_aligned(N);
    float* b = allocate_aligned(N);
    float* c = allocate_aligned(N);

    for (int i = 0; i < N; i++) {
        a[i] = (float)(i % 1000) / 3.0f;
        b[i] = (float)((i * 7) % 1000) / 5.0f;
    }

    memset(c, 0, N * sizeof(float));
    double time_basic = sum_basic(a, b, c, N);
    printf("基本版本:          %.3f ms\n", time_basic * 1000);

    memset(c, 0, N * sizeof(float));
    double time_compiler = sum_compiler_opt(a, b, c, N);
    printf("Compiler 優化:      %.3f ms (加速 %.1fx)\n",
           time_compiler * 1000, time_basic / time_compiler);

    memset(c, 0, N * sizeof(float));
    double time_simd = sum_simd(a, b, c, N);
    printf("SIMD (未對齊):      %.3f ms (加速 %.1fx)\n",
           time_simd * 1000, time_basic / time_simd);

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

    memset(C, 0, mat_n * mat_n * sizeof(float));
    double time1 = get_time();
    mat_mul_basic(A, B, C, mat_n);
    double time_basic_mat = get_time() - time1;
    printf("基本矩陣乘法:       %.2f ms\n", time_basic_mat * 1000);

    memset(C, 0, mat_n * mat_n * sizeof(float));
    time1 = get_time();
    mat_mul_blocked(A, B, C, mat_n, 32);
    double time_blocked = get_time() - time1;
    printf("分塊 + SIMD:        %.2f ms (加速 %.1fx)\n",
           time_blocked * 1000, time_basic_mat / time_blocked);

    free(a); free(b); free(c);
    free(A); free(B); free(C);

    printf("\n=== 完成 ===\n");
    return 0;
}