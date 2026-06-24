# 指針的藝術

## 指針的本質

指標是 C 語言最强大也最複雜的特性。它儲存的是變數的記憶體位址，讓我們可以直接操作記憶體。

### 什麼是指標

```c
int x = 42;
int *p = &x;  // p 儲存 x 的位址
```

指標變數本身也有自己的位址：
```c
printf("%p\n", (void*)&p);  // p 自己的位址
```

## 高級指標技巧

### 指標與 const

```c
// 指向 const 的指標
const int *p1;          // p1 可以改變，但*p1 不能
int const *p2;          // 同上
*p2 = 10;               // 錯誤

// const 指標
int *const p3;          // p3 不能改變，但*p3 可以
p3 = &x;                // 錯誤

// 兩者都不能變
const int *const p4;    // p4 和 *p4 都不能改變
```

### 指針與陣列的關係

```c
int arr[5] = {1, 2, 3, 4, 5};

// arr 等同於 &arr[0]
// arr + 1 等同於 &arr[1]

// 指針運算
int *p = arr;
p = p + 2;  // 前進 2 個元素
```

### 函式指標

```c
int (*func)(int, int);  // 指向回傳 int、接受兩個 int 的函式

int add(int a, int b) { return a + b; }
int sub(int a, int b) { return a - b; }

func = add;
printf("%d\n", func(1, 2));  // 3
func = sub;
printf("%d\n", func(5, 3));  // 2
```

## 指針與多維陣列

```c
// 指標陣列
int *arr[10];  // 10 個 int 指標的陣列

// 指向指標的指標
int **pp;     // 常見於動態二維陣列

// 指向陣列的指標
int (*p)[5];  // 指向含 5 個 int 的陣列
```

## 指針與字串

```c
// 字串常量（唯讀）
const char *s1 = "Hello";

// 可修改的字串
char s2[] = "Hello";
s2[0] = 'h';

//指標陣列
const char *days[] = {
    "Monday", "Tuesday", "Wednesday",
    "Thursday", "Friday", "Saturday", "Sunday"
};
```

## 回呼機制

```c
typedef void (*callback_t)(int);

void for_each(int *arr, int n, callback_t cb) {
    for (int i = 0; i < n; i++) {
        cb(arr[i]);
    }
}

void print_int(int x) {
    printf("%d\n", x);
}

for_each(arr, 5, print_int);
```

## 指標與資料結構

### 指標實現的結構

```c
// 連結串列節點
struct Node {
    int data;
    struct Node *next;
};

// 二叉樹節點
struct TreeNode {
    int data;
    struct TreeNode *left;
    struct TreeNode *right;
};

// 圖節點
struct GraphNode {
    int id;
    struct GraphNode **neighbors;  // 鄰接表
    int neighbor_count;
};
```

## 指針的陷阱

### 懸空指標

```c
int *p = (int*)malloc(sizeof(int));
free(p);
p = NULL;  // 重要！
```

### 記憶體洩漏

```c
while (1) {
    int *p = (int*)malloc(1000);
    // 忘記 free！
}
```

### 指標算術的陷阱

```c
double *pd;
int *pi;

// pd++ 前進 sizeof(double) 位元組
// pi++ 前進 sizeof(int) 位元組
// 不能混用指標類型
```

## 結論

掌握指標是精通 C 語言的關鍵。指標給予程式設計師極大的控制力，但也帶來了責任。理解指標的工作原理，可以幫助你寫出更高效、更安全的程式碼。