# 執行緒與並行

## 執行緒基礎

### 創建執行緒

```c
#include <pthread.h>

void* worker(void* arg) {
    int id = *(int*)arg;
    printf("Thread %d\n", id);
    return NULL;
}

int main() {
    pthread_t threads[4];
    int args[4] = {0, 1, 2, 3};

    for (int i = 0; i < 4; i++)
        pthread_create(&threads[i], NULL, worker, &args[i]);

    for (int i = 0; i < 4; i++)
        pthread_join(threads[i], NULL);

    return 0;
}
```

### 共享資源

```c
// 共享變數需要同步
int shared_counter = 0;
pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;

void* worker(void* arg) {
    for (int i = 0; i < 100000; i++) {
        pthread_mutex_lock(&mutex);
        shared_counter++;
        pthread_mutex_unlock(&mutex);
    }
    return NULL;
}
```

## 鎖優化

### 減少鎖持有時間

```c
// 不好的例子：鎖內做過多操作
pthread_mutex_lock(&mutex);
compute_something();  // 耗時操作在鎖內
update_shared_data();
pthread_mutex_unlock(&mutex);

// 好的例子：盡量縮短臨界區
compute_something();  // 無鎖操作
pthread_mutex_lock(&mutex);
update_shared_data();
pthread_mutex_unlock(&mutex);
```

### 讀寫鎖

```c
#include <pthread.h>

pthread_rwlock_t rwlock = PTHREAD_RWLOCK_INITIALIZER;

// 讀操作：可以並發
pthread_rwlock_rdlock(&rwlock);
read_data();
pthread_rwlock_unlock(&rwlock);

// 寫操作：獨占
pthread_rwlock_wrlock(&rwlock);
write_data();
pthread_rwlock_unlock(&rwlock);
```

### 無鎖資料結構

```c
// 使用比較並交換（CAS）
#include <stdatomic.h>

atomic_int counter = ATOMIC_VAR_INIT(0);

void increment() {
    int old, new;
    do {
        old = atomic_load(&counter);
        new = old + 1;
    } while (!atomic_compare_exchange_weak(&counter, &old, new));
}
```

## 執行緒區域儲存

### Thread-Local Storage

```c
// 使用 __thread 或 thread_local
__thread int tls_variable;

void* worker(void* arg) {
    tls_variable = *(int*)arg;  // 每個執行緒有自己的副本
    // ...
}
```

## 偽共享（False Sharing）

### 問題描述

```c
struct CacheLine {
    long long counter;  // 64 位元組，剛好一個快取行
};

// 問題：多個執行緒修改同一快取行的不同變數
struct {
    long long counter[4];
} stats;

// 每個執行緒修改 stats.counter[i]
// 導致其他執行緒的快取行失效
```

### 解決方案

```c
struct PaddedCounter {
    long long counter;
    char padding[64 - sizeof(long long)];  // 填充到快取行
};

struct {
    PaddedCounter counters[4];
} stats;
```

## 生產者-消費者模式

### 使用佇列

```c
#include <semaphore.h>

sem_t empty, full;
pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;

void* producer(void* arg) {
    for (int i = 0; i < 1000; i++) {
        sem_wait(&empty);
        pthread_mutex_lock(&mutex);
        enqueue(i);
        pthread_mutex_unlock(&mutex);
        sem_post(&full);
    }
    return NULL;
}

void* consumer(void* arg) {
    for (int i = 0; i < 1000; i++) {
        sem_wait(&full);
        pthread_mutex_lock(&mutex);
        int data = dequeue();
        pthread_mutex_unlock(&mutex);
        sem_post(&empty);
        process(data);
    }
    return NULL;
}
```

## 任務平行

### 工作佇列

```c
#include <pthread.h>

typedef struct {
    void (*function)(void*);
    void* arg;
} Task;

Task queue[1000];
int task_count = 0;
pthread_mutex_t queue_mutex = PTHREAD_MUTEX_INITIALIZER;

void submit_task(void (*func)(void*), void* arg) {
    pthread_mutex_lock(&queue_mutex);
    queue[task_count].function = func;
    queue[task_count].arg = arg;
    task_count++;
    pthread_mutex_unlock(&queue_mutex);
}
```

## OpenMP

### 基本使用

```c
#include <omp.h>

// 並列 for 循環
#pragma omp parallel for
for (int i = 0; i < n; i++) {
    result[i] = process(data[i]);
}
```

### reduction

```c
long long sum = 0;

#pragma omp parallel for reduction(+:sum)
for (int i = 0; i < n; i++) {
    sum += data[i];
}
```

### schedule

```c
// 靜態分發（預設）
#pragma omp parallel for schedule(static)
// 每個執行緒分到固定數量的迭代

// 動態分發
#pragma omp parallel for schedule(dynamic, 10)
// 每次給每個執行緒 10 個迭代，動態調整

// 引導分發
#pragma omp parallel for schedule(guided)
// 初始較大區塊，逐漸變小
```

## 常見錯誤

### 競爭條件

```c
// 不好：競爭條件
if (ptr == NULL) {  // 檢查
    ptr = allocate();  // 使用
}

// 可能：兩個執行緒同時通過檢查，都分配記憶體
```

### 死結

```c
// 不好：有可能死結
pthread_mutex_lock(&a);
pthread_mutex_lock(&b);
// 操作
pthread_mutex_unlock(&b);
pthread_mutex_unlock(&a);

// 好：總是以相同順序請求鎖
pthread_mutex_lock(&a);
pthread_mutex_lock(&b);
// 操作
pthread_mutex_unlock(&a);
pthread_mutex_unlock(&b);
```

## 效能考量

### 執行緒數量

```c
// 根據核心數量設定執行緒數
int num_threads = omp_get_max_threads();

// 或使用系統核心數
int num_threads = sysconf(_SC_NPROCESSORS_ONLN);
```

### 負載平衡

```c
// 不好的例子：工作不均
#pragma omp parallel for
for (int i = 0; i < n; i++) {
    if (i < 10)
        heavy_work(i);  // 執行緒 0 處理大部分工作
}

// 好的例子：工作均分
#pragma omp parallel for
for (int i = 0; i < n; i++)
    normal_work(i);
```

## 參考資料

- [Pthreads 教程](https://www.google.com/search?q=pthread+tutorial)
- [OpenMP 指南](https://www.google.com/search?q=OpenMP+tutorial)
- [偽共享優化](https://www.google.com/search?q=false+sharing+optimization+C++)