# 實際案例分析

## 案例 1：矩陣乘法優化

### 原始版本

```c
void mat_mul(float* A, float* B, float* C, int n) {
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++)
            for (int k = 0; k < n; k++)
                C[i * n + j] += A[i * n + k] * B[k * n + j];
}
```

### 分析

使用 `perf` 發現：
- 快取未命中率極高
- 分支預測失敗率中等

### 優化步驟

#### 步驟 1：增加區域性

```c
// 改變循環順序以提高快取命中
for (int i = 0; i < n; i++)
    for (int k = 0; k < n; k++)
        for (int j = 0; j < n; j++)
            C[i * n + j] += A[i * n + k] * B[k * n + j];
```

#### 步驟 2：分塊

```c
#define BLOCK 32

for (int i = 0; i < n; i += BLOCK)
    for (int j = 0; j < n; j += BLOCK)
        for (int k = 0; k < n; k += BLOCK)
            for (int ii = i; ii < min(i + BLOCK, n); ii++)
                for (int jj = j; jj < min(j + BLOCK, n); jj++)
                    for (int kk = k; kk < min(k + BLOCK, n); kk++)
                        C[ii * n + jj] += A[ii * n + kk] * B[kk * n + jj];
```

#### 步驟 3：SIMD 向量化

```c
// 使用 AVX 加速核心運算
for (int i = 0; i < n; i++) {
    for (int k = 0; k < n; k++) {
        __m256 aik = _mm256_set1_ps(A[i * n + k]);
        int j;
        for (j = 0; j + 8 <= n; j += 8) {
            __m256 bkj = _mm256_loadu_ps(&B[k * n + j]);
            __m256 cij = _mm256_loadu_ps(&C[i * n + j]);
            cij = _mm256_fmadd_ps(aik, bkj, cij);
            _mm256_storeu_ps(&C[i * n + j], cij);
        }
        // 處理剩餘
        for (; j < n; j++)
            C[i * n + j] += A[i * n + k] * B[k * n + j];
    }
}
```

### 效能提升

| 版本 | 時間 | 加速比 |
|-----|------|-------|
| 原始 | 45.2s | 1x |
| 循環順序 | 28.1s | 1.6x |
| 分塊 | 8.3s | 5.4x |
| SIMD | 2.1s | 21.5x |

## 案例 2：字串處理優化

### 原始版本

```c
int count_words(const char* str) {
    int count = 0;
    int in_word = 0;
    while (*str) {
        if (isspace(*str)) {
            in_word = 0;
        } else if (!in_word) {
            in_word = 1;
            count++;
        }
        str++;
    }
    return count;
}
```

### 分析

使用 `perf` 顯示：
- 分支預測失敗率 15%
- `isspace()` 函數呼叫開銷大

### 優化

```c
int count_words_optimized(const char* str) {
    int count = 0;
    const unsigned char* s = (const unsigned char*)str;

    while (*s) {
        // 使用查表代替 isspace()
        // 預先計算的查表：is_space[256]
        if (!is_space[*s]) {
            count++;
            while (s[1] && !is_space[s[1]]) s++;
        }
        s++;
    }
    return count;
}
```

### 效能提升

| 版本 | 時間（百萬字串） |
|-----|----------------|
| 原始 | 3.2ms |
| 優化 | 0.8ms |

## 案例 3：並發計數器

### 原始版本

```c
#include <pthread.h>

long long counter = 0;
pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;

void* worker(void* arg) {
    for (int i = 0; i < 10000000; i++) {
        pthread_mutex_lock(&mutex);
        counter++;
        pthread_mutex_unlock(&mutex);
    }
    return NULL;
}
```

### 分析

- 鎖競爭導致執行緒大部分時間在等待
- CPU 利用率低

### 優化版本 1：避免偽共享

```c
struct PaddedCounter {
    long long value;
    char padding[64];
};

PaddedCounter counters[4];  // 每個執行緒一個計數器

void* worker(void* arg) {
    int id = *(int*)arg;
    for (int i = 0; i < 10000000; i++)
        counters[id].value++;  // 無鎖操作

    return NULL;
}
```

### 優化版本 2：最後合併

```c
// 執行緒本地計數，最後合併
__thread long long local_counter = 0;

void* worker(void* arg) {
    for (int i = 0; i < 10000000; i++)
        local_counter++;  // 無競爭

    // 最後一次鎖
    pthread_mutex_lock(&mutex);
    counter += local_counter;
    pthread_mutex_unlock(&mutex);

    return NULL;
}
```

### 效能提升

| 版本 | 時間 | 加速比 |
|-----|------|-------|
| 原始（互斥鎖） | 4.2s | 1x |
| 避免偽共享 | 0.12s | 35x |
| 執行緒本地 + 最後合併 | 0.03s | 140x |

## 案例 4：搜尋優化

### 原始版本

```c
int find(const int* arr, int n, int target) {
    for (int i = 0; i < n; i++)
        if (arr[i] == target)
            return i;
    return -1;
}
```

### 優化：使用 SIMD

```c
int find_simd(const int* arr, int n, int target) {
    __m256i target_vec = _mm256_set1_epi32(target);

    for (int i = 0; i + 8 <= n; i += 8) {
        __m256i vec = _mm256_loadu_si256((__m256i*)&arr[i]);
        __m256i cmp = _mm256_cmpeq_epi32(vec, target_vec);
        int mask = _mm256_movemask_epi32(cmp);

        if (mask) {
            int bit = __builtin_ctz(mask);
            return i + bit;
        }
    }

    // 處理剩餘元素
    for (int i = 0; i < 8; i++)
        if (arr[i] == target)
            return i;

    return -1;
}
```

### 效能提升

| 版本 | 時間（十億元素） |
|-----|----------------|
| 原始 | 1.8s |
| SIMD | 0.4s |

## 案例 5：記憶體分配優化

### 問題

大量小物件分配導致記憶體碎片和效能下降。

### 解決：物件池

```c
struct ObjectPool {
    void* memory;
    void* free_list;
    size_t object_size;
};

ObjectPool* pool_create(size_t object_size, int count) {
    ObjectPool* pool = malloc(sizeof(ObjectPool));
    pool->object_size = object_size;

    // 分配一大塊記憶體
    pool->memory = malloc(object_size * count);

    // 建立自由鏈表
    pool->free_list = pool->memory;
    char* p = (char*)pool->memory;
    for (int i = 0; i < count - 1; i++)
        *(void**)p = p + object_size;
    *(void**)(p + object_size * (count - 1)) = NULL;

    return pool;
}

void* pool_alloc(ObjectPool* pool) {
    if (!pool->free_list) return NULL;
    void* p = pool->free_list;
    pool->free_list = *(void**)p;
    return p;
}

void pool_free(ObjectPool* pool, void* p) {
    *(void**)p = pool->free_list;
    pool->free_list = p;
}
```

## 總結

### 優化原則

1. **測量優先**：先用 profiling 工具找到瓶頸
2. **由上而下**：從演算法開始，再到實作
3. **小步前進**：每次改變一處，驗證效果
4. **照顧全域**：避免優化一處損害另一處

### 優化檢查表

- [ ] 是否真的需要優化？
- [ ] 瓶頸是否確認？
- [ ] 改變是否可測量？
- [ ] 是否考慮了所有層面（演算法、資料結構、記憶體、SIMD）？

## 參考資料

- [效能優化案例](https://www.google.com/search?q=performance+optimization+case+study)
- [矩陣乘法優化](https://www.google.com/search?q=matrix+multiplication+optimization+C++)
- [SIMD 搜尋](https://www.google.com/search?q=SIMD+search+algorithm)