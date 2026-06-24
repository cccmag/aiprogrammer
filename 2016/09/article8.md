# 鎖優化策略

## 鎖的成本

- 獲取鎖：數十到數百個時鐘週期
- 釋放鎖：數個時鐘週期
- 鎖競爭：執行緒等待導致 CPU 空轉

## 減少鎖持有時間

```c
// 不好：鎖內做過多操作
pthread_mutex_lock(&mutex);
process_large_data();  // 耗時操作
shared_data.result = compute_result();
pthread_mutex_unlock(&mutex);

// 好：縮短臨界區
process_large_data();  // 無鎖操作
pthread_mutex_lock(&mutex);
shared_data.result = compute_result();
pthread_mutex_unlock(&mutex);
```

## 讀寫鎖

```c
#include <pthread.h>

pthread_rwlock_t rwlock = PTHREAD_RWLOCK_INITIALIZER;

// 讀操作：可以並發
void read_data() {
    pthread_rwlock_rdlock(&rwlock);
    use_data();
    pthread_rwlock_unlock(&rwlock);
}

// 寫操作：獨占
void write_data() {
    pthread_rwlock_wrlock(&rwlock);
    update_data();
    pthread_rwlock_unlock(&rwlock);
}
```

## 無鎖技術

### 使用 Compare-and-Swap

```c
#include <stdatomic.h>

void increment_counter(atomic_int* counter) {
    int expected = atomic_load(counter);
    while (!atomic_compare_exchange_weak(counter, &expected, expected + 1))
        expected = atomic_load(counter);
}
```

### 使用原子變數

```c
atomic_int counter = ATOMIC_VAR_INIT(0);

// 簡單的遞增
atomic_fetch_add(&counter, 1);

// 使用 fetch_add 的返回值
int old = atomic_fetch_add(&counter, 1);
// old 是增加前的值
```

## 鎖的粒度

### 粗粒度鎖

簡單但可能成為瓶頸。

### 細粒度鎖

更高的並發度，但實現更複雜。

```c
// 不好：單一鎖保護所有資料
pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;
int counter1, counter2, counter3;

// 好：每個計數器有自己的鎖
pthread_mutex_t mutex1 = PTHREAD_MUTEX_INITIALIZER;
pthread_mutex_t mutex2 = PTHREAD_MUTEX_INITIALIZER;
pthread_mutex_t mutex3 = PTHREAD_MUTEX_INITIALIZER;
```

## 避免死結

### 固定鎖順序

```c
// 不好：可能死結
pthread_mutex_lock(&a);
pthread_mutex_lock(&b);
// ...
pthread_mutex_unlock(&b);
pthread_mutex_unlock(&a);

// 好：總是以相同順序請求鎖
pthread_mutex_lock(&a);
pthread_mutex_lock(&b);
// ...
pthread_mutex_unlock(&a);
pthread_mutex_unlock(&b);
```

### 使用 timed lock

```c
struct timespec ts;
clock_gettime(CLOCK_REALTIME, &ts);
ts.tv_sec += 1;  // 1 秒超時

if (pthread_mutex_timedlock(&mutex, &ts) == 0) {
    // 成功獲取
} else {
    // 處理超時
}
```

## 條例無鎖佇列

```c
#include <stdatomic.h>

typedef struct Node {
    void* data;
    struct Node* next;
} Node;

_Atomic(Node*) head = NULL;

void push(void* data) {
    Node* node = malloc(sizeof(Node));
    node->data = data;
    node->next = atomic_load(&head);
    while (!atomic_compare_exchange_weak(&head, &node->next, node))
        ;  // 重試
}

void* pop() {
    Node* head_node = atomic_load(&head);
    while (head_node && !atomic_compare_exchange_weak(&head, &head_node, head_node->next))
        ;  // 重試

    void* data = head_node ? head_node->data : NULL;
    free(head_node);
    return data;
}
```

## 參考資料

- [鎖優化技術](https://www.google.com/search?q=lock+optimization+techniques+C++)
- [無鎖程式設計](https://www.google.com/search?q=lock-free+programming+tutorial)