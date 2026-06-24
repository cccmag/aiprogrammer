# 記憶體管理與效能

## C 語言的記憶體模型

```
+------------------+ 高位址
|     核心         |
+------------------+
|     堆疊         |  <- 區域變數、函式呼叫
|       ↓          |
|                  |
|       ↑          |
|     堆積         |  <- malloc/free
+------------------+
|     BSS          |  <- 未初始化全域變數
+------------------+
|     資料         |  <- 已初始化全域變數
+------------------+
|     文字         |  <- 程式碼
+------------------+ 低位址
```

## malloc 的藝術

### 基本使用

```c
int *arr = (int*)malloc(n * sizeof(int));
if (arr == NULL) {
    // 處理錯誤
}
free(arr);
```

### 記憶體配置函式比較

```c
// malloc：配置記憶體，不初始化
void *malloc(size_t size);

// calloc：配置並初始化為零
void *calloc(size_t nmemb, size_t size);

// realloc：調整已配置記憶體大小
void *realloc(void *ptr, size_t size);
```

## 常見記憶體錯誤

### 未初始化指標

```c
int *p;      // 未初始化
*p = 42;     // 危險！可能破壞任意記憶體
```

### 記憶體洩漏

```c
void leak_example(void) {
    int *p = (int*)malloc(sizeof(int));
    *p = 42;
    // 忘記 free(p)
    // 每次呼叫都會洩漏 sizeof(int) 位元組
}
```

### 釋放後使用

```c
int *p = (int*)malloc(sizeof(int));
*p = 42;
free(p);
*p = 100;  // 未定義行為！
```

### 雙重釋放

```c
int *p = (int*)malloc(sizeof(int));
free(p);
free(p);  // 雙重釋放，危險！
```

## 效能優化

### 配置優化

```c
// 預先配置記憶體池
#define POOL_SIZE 1024
char memory_pool[POOL_SIZE];
size_t pool_offset = 0;

void* pool_alloc(size_t size) {
    if (pool_offset + size > POOL_SIZE) {
        return NULL;
    }
    void *ptr = &memory_pool[pool_offset];
    pool_offset += size;
    return ptr;
}
```

### 記憶體對齊

```c
#include <stdalign.h>

// C11：aligned_alloc
void *aligned_ptr = aligned_alloc(alignof(double), 1024);

// GCC/Clang 擴展
void *ptr = __builtin_assume_aligned(ptr, 16);
```

### 使用 static

```c
// static 區域變數在函式多次呼叫間保持
int* get_buffer(void) {
    static int buffer[1024];
    return buffer;
}
```

## 記憶體池

```c
typedef struct memory_pool {
    char *memory;
    size_t size;
    size_t offset;
} MemoryPool;

MemoryPool* pool_create(size_t size) {
    MemoryPool *pool = (MemoryPool*)malloc(sizeof(MemoryPool));
    pool->memory = (char*)malloc(size);
    pool->size = size;
    pool->offset = 0;
    return pool;
}

void* pool_alloc(MemoryPool *pool, size_t size) {
    if (pool->offset + size > pool->size) {
        return NULL;
    }
    void *ptr = &pool->memory[pool->offset];
    pool->offset += size;
    return ptr;
}

void pool_destroy(MemoryPool *pool) {
    free(pool->memory);
    free(pool);
}
```

## 效能分析工具

### Valgrind

```bash
valgrind --leak-check=full ./program
```

### AddressSanitizer

```bash
gcc -fsanitize=address -g program.c -o program
./program
```

### Massif（堆積分析）

```bash
valgrind --tool=massif ./program
```

## 結論

良好的記憶體管理是系統程式設計的基礎。正確使用 malloc/free，理解記憶體模型，可以避免大多數記憶體相關的錯誤和效能問題。