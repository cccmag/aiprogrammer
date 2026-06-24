# 指針在機器學習中的應用

## 為何 C 在 ML 中重要

機器學習需要大量數值計算，這正是 C 語言擅長的領域。

## 基礎：向量和矩陣

```c
// 簡單的向量結構
typedef struct {
    size_t size;
    double *data;
} Vector;

Vector* vector_create(size_t size) {
    Vector *v = (Vector*)malloc(sizeof(Vector));
    v->size = size;
    v->data = (double*)calloc(size, sizeof(double));
    return v;
}

void vector_free(Vector *v) {
    free(v->data);
    free(v);
}
```

## 矩陣運算

```c
typedef struct {
    size_t rows;
    size_t cols;
    double *data;  // 行優先儲存
} Matrix;

double* matrix_at(Matrix *m, size_t i, size_t j) {
    return &m->data[i * m->cols + j];
}

Matrix* matrix_multiply(Matrix *a, Matrix *b) {
    Matrix *result = matrix_create(a->rows, b->cols);

    for (size_t i = 0; i < a->rows; i++) {
        for (size_t k = 0; k < a->cols; k++) {
            double a_ik = *matrix_at(a, i, k);
            for (size_t j = 0; j < b->cols; j++) {
                *matrix_at(result, i, j) += a_ik * *matrix_at(b, k, j);
            }
        }
    }
    return result;
}
```

## 指標與 BLAS

BLAS（Basic Linear Algebra Subprograms）是線性代數的標準介面：

```c
// dgemm：雙精度矩陣乘法
void dgemm_(char *transa, char *transb,
            int *m, int *n, int *k,
            double *alpha, double *a, int *lda,
            double *b, int *ldb, double *beta,
            double *c, int *ldc);
```

使用指標傳遞矩陣：

```c
double *A, *B, *C;
int m = 1000, n = 1000, k = 1000;
double alpha = 1.0, beta = 0.0;

dgemm_("N", "N", &m, &n, &k,
       &alpha, A, &m, B, &k, &beta, C, &m);
```

## 記憶體管理策略

### 預先配置

```c
// 避免重複 malloc/free
typedef struct {
    double *weights;
    double *gradient;
    double *cache;
    size_t size;
} OptimizerState;

OptimizerState* optimizer_create(size_t size) {
    OptimizerState *state = (OptimizerState*)malloc(sizeof(OptimizerState));
    state->size = size;
    state->weights = (double*)malloc(size * sizeof(double));
    state->gradient = (double*)malloc(size * sizeof(double));
    state->cache = (double*)malloc(size * sizeof(double));
    return state;
}
```

### 記憶體池

```c
// 大型模型的連續記憶體
typedef struct {
    double *data;
    size_t size;
    size_t offset;
} MemoryPool;

double* pool_alloc(MemoryPool *pool, size_t size) {
    if (pool->offset + size > pool->size) {
        return NULL;
    }
    double *ptr = &pool->data[pool->offset];
    pool->offset += size;
    return ptr;
}
```

## SIMD 優化

指標用於手動 SIMD 操作：

```c
// 假設有 16 位元組對齊
double* a, *b, *c;
__m256d va, vb, vc;

for (size_t i = 0; i < n; i += 4) {
    va = _mm256_load_pd(a + i);
    vb = _mm256_load_pd(b + i);
    vc = _mm256_add_pd(va, vb);
    _mm256_store_pd(c + i, vc);
}
```

## 與 Python 的結合

```c
// 提供乾淨的 C API
#include <Python.h>

static PyObject* predict(PyObject *self, PyObject *args) {
    double *input;
    Py_buffer view;

    if (!PyArg_ParseTuple(args, "s*", &input, &view)) {
        return NULL;
    }

    double result = model_predict(input);
    PyBuffer_Release(&view);

    return PyFloat_FromDouble(result);
}
```

## 結論

雖然機器學習的 high-level 程式通常用 Python 編寫，但底層的數值計算離不開 C 和指標。理解 C 的指標和記憶體管理，對於優化機器學習效能和實現高效的自定義層至關重要。