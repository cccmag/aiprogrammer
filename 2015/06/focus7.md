# 主題七：最佳實踐與效能優化

## C 語言程式碼風格

### 命名慣例

```c
// 變數：蛇底式小寫
int student_count;
char user_name[50];

// 常數：全大寫或 k + 駝峰
#define MAX_BUFFER_SIZE 1024
const int kMaxRetry = 3;

// 函式：蛇底式或駝峰
int calculate_sum(int *arr, int n);
void *safe_malloc(size_t size);
```

### 格式化

```c
// if 陳述
if (condition) {
    do_something();
} else {
    do_other();
}

// 指標和引用
int *ptr;
int *arr[10];
int (*func)(int, int);

// 長函式
if (some_long_condition && another_condition &&
    yet_another_condition) {
    do_something();
}
```

## 記憶體管理

### 避免記憶體洩漏

```c
void process_data(void) {
    int *data = (int*)malloc(1000 * sizeof(int));
    if (!data) {
        return;
    }

    // ... 使用 data ...

    free(data);
    data = NULL;  // 避免懸空指標
}

// 更好的模式：一次配置，一次釋放
int *create_array(int size) {
    int *arr = (int*)calloc(size, sizeof(int));
    return arr;
}
```

### 記憶體對齊

```c
#include <stdalign.h>

// C11：檢查對齊
_Static_assert(alignof(int) == 4, "int 應該 4 位元組對齊");

// aligned_alloc（C11）
int *aligned = (int*)aligned_alloc(alignof(int), 100 * sizeof(int));
```

## 效能優化

### 使用內聯函式

```c
// 內聯函式建議
inline int max(int a, int b) {
    return a > b ? a : b;
}

// 編譯器可能忽略 inline
static inline int square(int x) {
    return x * x;
}
```

### 避免不必要的函式呼叫

```c
// 不好
for (int i = 0; i < n; i++) {
    sum += get_value(i);
}

// 好
for (int i = 0; i < n; i++) {
    sum += values[i];
}
```

### 使用適當的資料結構

```c
// 靜態陣列（最快的選擇）
int arr[1000];

// 動態陣列（靈活性）
int *arr = (int*)malloc(n * sizeof(int));

// 連結串列（插入/刪除 O(1)，但查詢 O(n)）
// 根據需求選擇
```

### 編譯器優化選項

```bash
# GCC/Clang 優化選項
gcc -O1 program.c        # 基本優化
gcc -O2 program.c        # 增強優化
gcc -O3 program.c        # 最大優化（包含 -O2）
gcc -Ofast program.c     # 快速執行（可能違反嚴格標準）
gcc -Os program.c        # 最佳化大小

# 特定最佳化
gcc -march=native program.c  # 針對本機 CPU 優化
gcc -flto program.c         # 連結時間優化
```

## 除錯工具

### GDB 基本使用

```bash
gcc -g program.c -o program   # 編譯時包含除錯資訊
gdb ./program

# GDB 命令
(gdb) break main              # 在 main 設定斷點
(gdb) run                     # 執行
(gdb) next                    # 單步執行
(gdb) step                    # 進入函式
(gdb) print variable          # 印出變數
(gdb) watch variable          # 監視變數變化
(gdb) backtrace              # 顯示呼叫堆疊
(gdb) quit                   # 離開
```

### Valgrind 記憶體檢測

```bash
# 安裝
# sudo apt install valgrind

# 檢查記憶體錯誤
valgrind --leak-check=full ./program

# 輸出範例
# ==12345== Memcheck, a memory error detector
# ==12345== HEAP SUMMARY:
# ==12345==    in use at exit: 0 bytes in 0 blocks
# ==12345==    total heap usage: 10 allocs, 10 frees, 2,048 bytes allocated
```

### AddressSanitizer

```bash
# 編譯時啟用 ASan
gcc -fsanitize=address -g program.c -o program

# 檢測記憶體錯誤
./program
```

## 靜態分析

### GCC/Clang 分析

```bash
gcc -Wall -Wextra -pedantic program.c
gcc -fanalyzer program.c
clang --analyze program.c
```

### cppcheck

```bash
# 安裝
# sudo apt install cppcheck

# 執行靜態分析
cppcheck program.c
```

## 常見錯誤預防

### NULL 指標檢查

```c
int *ptr = malloc(sizeof(int));
if (ptr == NULL) {
    // 處理錯誤
    return -1;
}
```

### 陣列邊界檢查

```c
// 手動邊界檢查
for (int i = 0; i < n; i++) {
    arr[i] = i;
}

// 使用 size_t 避免負數
for (size_t i = 0; i < n; i++) {
    arr[i] = i;
}
```

### 指標別名

```c
// restrict 指標告訴編譯器沒有別名
void copy(int *restrict dest, const int *restrict src, size_t n) {
    for (size_t i = 0; i < n; i++) {
        dest[i] = src[i];
    }
}
```

## 結論

良好的 C 語言程式設計需要：
1. 一致的程式碼風格
2. 正確的記憶體管理
3. 善用編譯器優化
4. 熟練使用除錯工具
5. 遵循最佳實踐

這些技能需要時間培養，但會大幅提升程式碼品質和效率。