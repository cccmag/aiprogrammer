# C 語言效能技巧

## 內聯函數

```c
// 巨集
#define MIN(a, b) ((a) < (b) ? (a) : (b))

// 更好的方式：inline
static inline int min(int a, int b) {
    return a < b ? a : b;
}
```

## 避免函數指標呼叫開銷

```c
// 函數指標呼叫可能阻止內聯
typedef int (*OpFunc)(int, int);
int execute_op(OpFunc op, int a, int b) {
    return op(a, b);  // 編譯器可能無法內聯
}

// 如果操作固定，使用普通函數或模板
```

## 結構體填充

```c
// 不好：自動填充導致結構體變大
struct Data {
    char a;     // + 3 padding
    double b;
    char c;     // + 7 padding
    int d;
};

// 好：手動排序減少填充
struct Data {
    double b;   // 8 位元組
    int d;      // 4 位元組
    char a;     // 1 位元組
    char c;     // 1 位元組
    char pad[2]; // 2 padding
};
```

## 預測執行

```c
// 幫助分支預測器
if (likely(x > 0)) {
    // 大多數情況是 true
}

if (unlikely(error)) {
    // 很少發生的錯誤情況
}

// 使用 __builtin_expect
if (__builtin_expect(x > 0, 1)) {  // 1 表示 likely
    // ...
}
```

## 避免不必要的初始化

```c
// 不好：初始化後馬上賦值
int array[1000];
memset(array, 0, sizeof(array));  // 初始化為 0
for (int i = 0; i < 1000; i++)
    array[i] = compute_value();  // 覆蓋之前的值

// 好：只在需要時初始化
int array[1000];
for (int i = 0; i < 1000; i++)
    array[i] = compute_value();
```

## 堆疊 vs 暫存器

```c
// 小型陣列在堆疊上可能比動態分配慢
// 但過大的堆疊分配也有問題

#define MAX_SIZE 64  // 適合堆疊
int buffer[MAX_SIZE];
```

## 延遲計算

```c
// 不好：每次都計算
for (int i = 0; i < n; i++)
    process(array[i], n * 2);  // n * 2 每次重新計算

// 好：預先計算
int twice_n = n * 2;
for (int i = 0; i < n; i++)
    process(array[i], twice_n);
```

## 使用合適的資料型別

```c
// 不好的例子：過度使用較大的型別
unsigned long long counter = 0;  // 只需要 32 位元
counter++;  // 額外的零擴展開銷

// 好的例子：使用最小足夠的型別
uint32_t counter = 0;
counter++;
```

## 參考資料

- [C 效能優化](https://www.google.com/search?q=C+performance+optimization+tips)
- [程式碼效能技巧](https://www.google.com/search?q=code+performance+tips+C)