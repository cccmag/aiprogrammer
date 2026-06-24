# 微基準測試

## 什麼是微基準測試？

微基準測試（Microbenchmark）用於測量小程式碼片段的效能，如單一函數或演算法的效能。

## 微基準測試的挑戰

### 謹慎處理

編譯器可能會：
- 刪除「無用」的程式碼
- 將結果快取
- 內聯函數

```c
// 編譯器可能直接計算出結果
int result = 0;
for (int i = 0; i < 1000; i++)
    result += i;
// 優化後：result = 499500
```

### 解決方法

```c
// 使用 volatile 防止優化
volatile int result = 0;
for (int i = 0; i < 1000; i++)
    result += i;

// 或使用回傳值
int compute_sum(int n) {
    int result = 0;
    for (int i = 0; i < n; i++)
        result += i;
    return result;
}

// 或使用 clobber 列表
asm volatile("" : : "r"(result) : "memory");
```

## 測量框架

### Google Benchmark

```cpp
#include <benchmark/benchmark.h>

static void BM_StringCreation(benchmark::State& state) {
    for (auto _ : state)
        std::string s = "hello";
}
BENCHMARK(BM_StringCreation);

static void BM_StringCopy(benchmark::State& state) {
    std::string s = "hello";
    for (auto _ : state) {
        std::string copy = s;
    }
}
BENCHMARK(BM_StringCopy);

BENCHMARK_MAIN();
```

編譯和執行：
```bash
g++ -O2 -std=c++11 benchmark.cpp -o benchmark -lpthread
./benchmark --benchmark_format=csv
```

### C 語言計時框架

```c
#include <time.h>
#include <stdio.h>

#define ITERATIONS 1000000

double get_time() {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return ts.tv_sec + ts.tv_nsec / 1e9;
}

void benchmark(const char* name, void (*func)()) {
    // 預熱
    for (int i = 0; i < 100; i++) func();

    // 測量
    double start = get_time();
    for (int i = 0; i < ITERATIONS; i++) func();
    double end = get_time();

    printf("%s: %.3f ns/iter\n", name, (end - start) / ITERATIONS * 1e9);
}
```

## 統計處理

### 需要多次執行

```c
#define RUNS 10

double times[RUNS];
for (int i = 0; i < RUNS; i++) {
    double start = get_time();
    // 測量的程式碼
    double end = get_time();
    times[i] = end - start;
}

// 計算平均值和標準差
double mean = 0, variance = 0;
for (int i = 0; i < RUNS; i++) mean += times[i];
mean /= RUNS;

for (int i = 0; i < RUNS; i++)
    variance += (times[i] - mean) * (times[i] - mean);
variance /= RUNS;

double stddev = sqrt(variance);
printf("Mean: %.3f ns, Stddev: %.3f ns\n", mean * 1e9, stddev * 1e9);
```

### 忽略異常值

```c
// 去除最大值和最小值
qsort(times, RUNS, sizeof(double), compare_double);
double trimmed_mean = 0;
for (int i = 1; i < RUNS - 1; i++)
    trimmed_mean += times[i];
trimmed_mean /= (RUNS - 2);
```

## 常見陷阱

### 誤用計時器

```c
// 錯誤：時脈可能不準確
clock_t start = clock();
func();
clock_t end = clock();
double time = (double)(end - start) / CLOCKS_PER_SEC;

// 正確：使用高精度計時器
struct timespec start, end;
clock_gettime(CLOCK_MONOTONIC, &start);
func();
clock_gettime(CLOCK_MONOTONIC, &end);
double time = (end.tv_sec - start.tv_sec) +
              (end.tv_nsec - start.tv_nsec) / 1e9;
```

### 快取效應

```c
// 第一次可能很慢（快取未命中）
// 後續可能很快（快取命中）

// 解決：每次測量前清除快取
#include <emmintrin.h>
_mm_clflush(cache_line_ptr);
```

### 分支預測

```c
// 資料導致分支預測變化
// 解決：使用亂數或不重複資料

// 測量分支預測失敗影響
for (int i = 0; i < N; i++) {
    if (predictable_pattern)
        func1();
    else
        func2();
}
```

## 測量內容

### 延遲（Latency）

完成單次操作所需的時間。

```c
// 測量單次記憶體訪問延遲
for (int i = 0; i < N; i++) {
    clock_gettime(...);
    access(array[i]);
    clock_gettime(...);
}
```

### 頻寬（Bandwidth）

單位時間內處理的資料量。

```c
// 測量記憶體頻寬
size_t bytes = N * sizeof(int);
double time = measure_time();
printf("Bandwidth: %.2f GB/s\n", bytes / time / 1e9);
```

### 吞吐量（Throughput）

單位時間內完成的操作數。

```c
// 測量每秒運算次數
int operations = 0;
auto start = now();
while (now() - start < 1.0) {
    operation();
    operations++;
}
printf("Throughput: %d ops/sec\n", operations);
```

## 微基準測試範例

### 字串拼接比較

```c
// 使用 strcat
void test_strcat() {
    char buf[10000];
    buf[0] = '\0';
    for (int i = 0; i < 100; i++)
        strcat(buf, "hello");
}

// 使用 sprintf
void test_sprintf() {
    char buf[10000];
    buf[0] = '\0';
    for (int i = 0; i < 100; i++)
        sprintf(buf + strlen(buf), "hello");
}

// 使用 memcpy
void test_memcpy() {
    char buf[10000];
    const char* src = "hello";
    for (int i = 0; i < 100; i++)
        memcpy(buf + i * 5, src, 5);
}
```

## 參考資料

- [Google Benchmark 教程](https://www.google.com/search?q=Google+Benchmark+tutorial)
- [微基準測試最佳實踐](https://www.google.com/search?q=microbenchmarking+best+practices)
- [延遲 vs 頻寬](https://www.google.com/search?q=latency+vs+bandwidth+benchmarking)