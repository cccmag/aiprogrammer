# 主題二：記憶體管理

## 記憶體的基本概念

電腦記憶體是一個大型的位元組陣列，每個位元組都有唯一的位址。程式透過位址來讀寫資料。

```
記憶體位址：  0x00  0x01  0x02  0x03  0x04  ...
記憶體內容： [ 65 ] [ 66 ] [ 67 ] [ 00 ] [ ?? ]
              'A'   'B'   'C'   '\0'
```

## 堆與棧

記憶體分為兩大區域：

### 棧（Stack）

- **特點**：先進後出（LIFO）
- **用途**：儲存函式呼叫、區域變數
- **管理**：自動管理，函式返回時自動釋放
- **速度**：非常快
- **大小**：相對較小，通常 1-8 MB

```python
def foo():
    x = 10        # 分配在棧上
    y = 20
    return x + y  # 棧框被彈出，x, y 自動釋放
```

### 堆（Heap）

- **特點**：動態分配，大小可變
- **用途**：儲存需要長期存在的物件
- **管理**：手動（C/C++）或自動（Java/Python）
- **速度**：較慢
- **大小**：可達數 GB

```python
# Python：所有物件都在堆上
x = [1, 2, 3]  # 列表物件在堆上，只有指標在棧上
```

## 指標與引用

### C 風格的指標

```c
int x = 5;
int *ptr = &x;     // 取地址
printf("%d", *ptr); // 解引用

// 指標算術
int arr[] = {1, 2, 3, 4, 5};
int *p = arr;
p++;               // 移動到下一個元素
```

### 指標的危險

```c
// 緩衝區溢出
char buf[8];
strcpy(buf, "This string is too long!"); // 危險！

// 空指標解引用
int *ptr = NULL;
*ptr = 5; // 崩潰！

// 懸空指標
int *ptr = malloc(sizeof(int));
free(ptr);
*ptr = 5; // 使用已釋放記憶體（use-after-free）
```

### 引用（Reference）

```cpp
// C++ 引用：指標的安全替代
int x = 5;
int &ref = x;   // ref 是 x 的引用
ref = 10;       // 修改 x
```

### 智慧指標

自動釋放記憶體的指標：

```cpp
// C++11 智慧指標
#include <memory>

// unique_ptr：獨佔所有權
std::unique_ptr<int> p1(new int(5));

// shared_ptr：共享所有權
std::shared_ptr<int> p2 = std::make_shared<int>(10);

// weak_ptr：不影響引用計數
std::weak_ptr<int> p3 = p2;
```

## 記憶體分配

### C 的 malloc/free

```c
// 手動記憶體管理
int *arr = (int *)malloc(n * sizeof(int));
if (arr == NULL) {
    // 處理錯誤
}
free(arr);
```

### C++ 的 new/delete

```cpp
// new 和 delete
int *x = new int(5);
delete x;  // 釋放

int *arr = new int[100];
delete[] arr;  // 釋放陣列
```

### 棧分配

簡單快速的分配方式：

```cpp
// 棧分配：自動釋放
void foo() {
    int arr[100];  // 棧上分配，自動釋放
}
```

### 記憶體池

預先分配的記憶體池：

```c
// 記憶體池分配器
typedef struct Block {
    struct Block *next;
} Block;

Block *pool_alloc(BlockPool *pool, size_t size) {
    if (pool->free_list == NULL) {
        // 記憶體池不夠，擴展
    }
    Block *block = pool->free_list;
    pool->free_list = block->next;
    return block;
}
```

## 記憶體佈局

典型程式的記憶體佈局：

```
高位址
+-----------+
|   核心    | 作業系統核心
+-----------+
|   棧     |  向低地址生長
|    ↓     |
|          |
|    ↑     |
|   堆     |  向高地址生長
+-----------+
| 全域/靜態 |
+-----------+
|   程式碼  |
+-----------+
低位址
```

## 記憶體對齊

資料需要對齊到特定邊界：

```c
// 結構成員對齊
struct Foo {
    char a;     // 1 byte + 3 padding
    int b;      // 4 bytes
    char c;     // 1 byte + 3 padding
};
// 總大小：12 bytes（而非 6）
```

## 常見記憶體錯誤

### 緩衝區溢出

```c
// 危險
char buf[10];
gets(buf);  // 不安全！

// 安全替代
fgets(buf, sizeof(buf), stdin);
```

### 記憶體洩漏

```c
// 記憶體洩漏
void leak() {
    int *ptr = malloc(sizeof(int));
    // 忘記 free(ptr)
}
```

### 雙重釋放

```c
free(ptr);
free(ptr);  // 危險！雙重釋放
```

### 釋放後使用

```c
free(ptr);
*ptr = 5;  // 危險！use-after-free
```

## 現代記憶體管理

### Rust 的所有權系統

Rust 使用編譯時檢查杜絕記憶體錯誤：

```rust
fn main() {
    let s1 = String::from("hello");
    let s2 = s1;  // s1 無效，所有權轉移
    // println!("{}", s1);  // 編譯錯誤！
    println!("{}", s2);
}
```

### 區域性原理

程式的時間和空間區域性：

```python
# 時間區域性：最近訪問的資料可能再次訪問
def matrix_multiply(A, B, C, n):
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]

# 空間區域性：訪問某個位置後，可能訪問相鄰位置
# 應該使用行優先或列優先訪問匹配記憶體佈局
```

## 小結

記憶體管理是系統程式設計的核心。正確理解堆與棧、指標與引用，以及記憶體佈局，是寫出高效、安全程式的基礎。