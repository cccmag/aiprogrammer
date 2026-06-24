# 記憶體優化

## 記憶體階層

```
┌─────────────────────────────┐
│         Register            │ ← 1 個週期
├─────────────────────────────┤
│      L1 Cache (Data)        │ ← ~4 個週期
├─────────────────────────────┤
│      L2 Cache               │ ← ~12 個週期
├─────────────────────────────┤
│      L3 Cache               │ ← ~30-40 個週期
├─────────────────────────────┤
│         Main Memory         │ ← ~200 個週期
├─────────────────────────────┤
│          Storage            │ ← 非挥发
└─────────────────────────────┘
```

## 快取行（Cache Line）

- 典型大小：64 位元組
- 載入是以快取行為單位
- 未對齊的訪問可能觸發多次快取載入

## 快取友好的程式設計

### 優先順序：註冊 > L1 > L2 > L3 > 主記憶體

```c
// 慢：隨機記憶體訪問
for (int i = 0; i < N; i++)
    sum += array[rand() % N];

// 快：順序記憶體訪問
for (int i = 0; i < N; i++)
    sum += array[i];
```

### 巢狀循環的順序

```c
int A[100][100];

// 慢：j 在外層會導致非連續訪問
for (int j = 0; j < 100; j++)
    for (int i = 0; i < 100; i++)
        A[i][j]++;

// 快：i 在外層，j 在內層
for (int i = 0; i < 100; i++)
    for (int j = 0; j < 100; j++)
        A[i][j]++;
```

## 資料局部性

### 時間局部性

最近訪問的資料很可能再次被訪問。

```c
// 好的例子：重複使用同一筆資料
for (int i = 0; i < iterations; i++)
    sum += process(data);  // data 在暫存器中

// 不好的例子：每次都從記憶體讀取
for (int i = 0; i < iterations; i++)
    sum += data[i % data_size];  // 可能不在快取中
```

### 空間局部性

相鄰的記憶體位置很可能被連續訪問。

```c
// 好的例子：順序訪問
for (int i = 0; i < n; i++)
    process(arr[i]);

// 不好的例子：跳躍訪問
for (int i = 0; i < n; i += stride)
    process(arr[i]);  // stride > 1 時快取效率低
```

## 陣列結構 vs 結構陣列

### SoA（Structure of Arrays）

```c
struct PointArray {
    float* x;
    float* y;
    float* z;
};

// 好的：同一資料型別連續儲存
for (int i = 0; i < n; i++)
    points.x[i] += dx;
```

### AoS（Array of Structures）

```c
struct Point {
    float x, y, z;
};
Point points[1000];

// 不好的例子：不同資料型別交錯
for (int i = 0; i < n; i++)
    points[i].x += dx;  // x, y, z 可能不在同一快取行
```

### 根據訪問模式選擇

```c
// 計算所有 x 座標：SoA 較好
for (int i = 0; i < n; i++)
    sum += points.x[i];

// 計算每個點的距離：AoS 較好
for (int i = 0; i < n; i++)
    dist = sqrt(p.x*p.x + p.y*p.y + p.z*p.z);
```

## 預取（Prefetching）

### 手動預取

```c
#include <x86intrin.h>

for (int i = 0; i < n; i++) {
    // 預取未來將訪問的資料
    _mm_prefetch(&data[i + 16], _MM_HINT_T0);

    process(data[i]);
}
```

### 編譯器預取

```c
#pragma GCC prefetch arr
for (int i = 0; i < n; i++)
    process(arr[i]);
```

## 記憶體對齊

### 手動對齊

```c
// 對齊到 32 位元組邊界
__attribute__((aligned(32))) float buffer[1024];

// 或者使用 posix_memalign
void* aligned_malloc(size_t size, size_t alignment) {
    void* ptr;
    posix_memalign(&ptr, alignment, size);
    return ptr;
}
```

### 對齊與 SIMD

```c
// 未對齊的載入可能觸發兩次記憶體訪問
__m256 a = _mm256_loadu_ps(ptr);  // 可能慢

// 對齊的載入只需要一次記憶體訪問
__m256 a = _mm256_load_ps(ptr);   // 要求 32 位元組對齊
```

## 鎖優化與快取

### 假共享（False Sharing）

不同執行緒訪問同一快取行中的不同變數，導致快取失效。

```c
// 不好的例子：導致假共享
struct Counter {
    long long counter[4];  // 4 個執行緒各用一個
};

// 每個執行緒
void worker(Counter* c, int id) {
    for (int i = 0; i < N; i++)
        c->counter[id]++;  // 每次寫入都使其他核心的快取失效
}
```

### 解決方法：填充

```c
struct Counter {
    long long counter[4];
    char pad[64 - sizeof(long long) * 4];  // 填充到快取行大小
};
```

## 大型資料結構

### 分塊（Blocking）

```c
// 不好的例子：每行訪問間隔太大
for (int i = 0; i < n; i++)
    for (int j = 0; j < n; j++)
        C[i][j] += A[i][k] * B[k][j];

// 好的例子：分塊提高快取局部性
#define BLOCK 32
for (int bi = 0; bi < n; bi += BLOCK)
    for (int bj = 0; bj < n; bj += BLOCK)
        for (int bk = 0; bk < n; bk += BLOCK)
            for (int i = bi; i < min(bi+BLOCK, n); i++)
                for (int j = bj; j < min(bj+BLOCK, n); j++)
                    for (int k = bk; k < min(bk+BLOCK, n); k++)
                        C[i][j] += A[i][k] * B[k][j];
```

## 測量快取效能

### 使用 perf

```bash
perf stat -e cache-misses,cache-references ./program
```

### 使用 cachegrind

```bash
valgrind --tool=cachegrind --cache-sim=yes ./program
cg_annotate cachegrind.out.*
```

## 參考資料

- [快取友好程式設計](https://www.google.com/search?q=cache+友好+程式設計)
- [記憶體階層優化](https://www.google.com/search?q=memory+hierarchy+optimization)
- [偽共享問題](https://www.google.com/search?q=false+sharing+optimization)