# 記憶體屏障與 Cache

## 記憶體屏障（Memory Barrier）

### 為什麼需要記憶體屏障

在多執行緒和 reorder 優化下，記憶體操作的順序可能與程式碼順序不同。

```c
// 執行緒 1
data = 42;           // A
valid = true;        // B

// 執行緒 2
if (valid)           // C
    use(data);       // D
```

如果沒有記憶體屏障，執行緒 2 可能看到 `valid=true` 但 `data=0`。

### 編譯器屏障

```c
#define CompilerBarrier() asm volatile("" ::: "memory")

data = 42;
CompilerBarrier();  // 防止編譯器重排序
valid = true;
```

### CPU 記憶體屏障

```c
#include <stdatomic.h>

// C11 編譯器屏障
atomic_signal_fence(memory_order_seq_cst);

// x86 記憶體屏障
asm volatile("mfence" ::: "memory");

// ARM/ARM64
asm volatile("dmb ish" ::: "memory");
```

### C11 原子操作

```c
#include <stdatomic.h>

atomic_int data = 0;
atomic_bool valid = ATOMIC_FLAG_INIT;

void producer() {
    atomic_store(&data, 42);
    atomic_store_explicit(&valid, true, memory_order_release);
}

void consumer() {
    if (atomic_load_explicit(&valid, memory_order_acquire))
        use(atomic_load(&data));
}
```

## 快取一致性

### MESI 協定

| 狀態 | 說明 |
|-----|------|
| Modified | 已修改，與主記憶體不同 |
| Exclusive | 乾淨，在這個核心的快取中 |
| Shared | 乾淨，可能在其他核心的快取中 |
| Invalid | 不在快取中 |

### 快取一致性流量

當一個核心修改資料時，其他核心的快取行會被無效化。

## volatile 的局限性

```c
volatile int flag = 0;

// 這個模式不安全
while (flag == 0);  // 可能在某些架構上永遠等待

// 正確使用原子操作
while (atomic_load(&flag) == 0);  // 安全
```

## 緩衝區

### 使用屏障確保 I/O 順序

```c
void write_data(volatile void* addr, int value) {
    *addr = value;
    asm volatile("mfence" ::: "memory");  // 確保寫入完成
}
```

## 參考資料

- [記憶體屏障](https://www.google.com/search?q=memory+barrier+tutorial)
- [MESI 協定](https://www.google.com/search?q=MESI+protocol)