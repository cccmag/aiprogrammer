# 主題三：指標與記憶體管理

## 指標基礎

指標是 C 語言最强大也最危險的特性。指標儲存的是變數的記憶體位址。

### 指標宣告

```c
int *p;          // 指標，指向 int
char *c;         // 指標，指向 char
float *f;        // 指標，指向 float
double *d;       // 指標，指向 double
void *v;         // void 指標，可以指向任何類型
```

### & 和 * 運算子

```c
int x = 42;
int *p = &x;     // & 取得變數的位址

printf("%p\n", (void*)p);     // 印出位址
printf("%d\n", *p);           // 42，* 解參考取得值

*p = 100;         // 透過指標修改值
printf("%d\n", x);             // 100
```

### 指標大小

```c
printf("指標大小：%zu 位元組\n", sizeof(int*));
// 在 64 位元系統上通常是 8 位元組
```

## 指標與陣列

### 陣列名作為指標

```c
int arr[5] = {1, 2, 3, 4, 5};
int *p = arr;        // arr 等同於 &arr[0]

printf("%d\n", *p);          // 1
printf("%d\n", *(p + 1));    // 2
printf("%d\n", p[0]);        // 1（指標語法）
```

### 指標算術

```c
int arr[] = {10, 20, 30, 40, 50};
int *p = arr;

p++;              // 移動到下一個 int
printf("%d\n", *p);  // 20

p += 2;           // 前進 2 個元素
printf("%d\n", *p);  // 40

int diff = &arr[4] - &arr[0];  // 4（指標相減）
```

## 字串指標

```c
char *str = "Hello";  // 字串常量指標
printf("%s\n", str);
printf("%c\n", str[0]);    // 'H'
printf("%c\n", *(str + 1)); // 'e'

// 注意：字串常量不可修改
// str[0] = 'h';  // 危險！未定義行為
```

```c
// 可修改的字串
char str[] = "Hello";
str[0] = 'h';  // OK
printf("%s\n", str);  // "hello"
```

## 指標與函式

### 指標作為參數

```c
void swap(int *a, int *b) {
    int temp = *a;
    *a = *b;
    *b = temp;
}

int main(void) {
    int x = 1, y = 2;
    swap(&x, &y);
    printf("%d %d\n", x, y);  // 2 1
}
```

### 指標作為返回值

```c
int* find_max(int *arr, int n) {
    int *max = arr;
    for (int i = 1; i < n; i++) {
        if (arr[i] > *max) {
            max = &arr[i];
        }
    }
    return max;
}
```

### 函式指標

```c
int add(int a, int b) { return a + b; }
int sub(int a, int b) { return a - b; }

int main(void) {
    int (*op)(int, int) = add;
    printf("%d\n", op(1, 2));  // 3

    op = sub;
    printf("%d\n", op(5, 3)); // 2
}
```

## 動態記憶體配置

### malloc 和 free

```c
#include <stdlib.h>

int *arr = (int*)malloc(5 * sizeof(int));
if (arr == NULL) {
    // 配置失敗
    return;
}

for (int i = 0; i < 5; i++) {
    arr[i] = i * 10;
}

free(arr);  // 釋放記憶體
arr = NULL; // 避免懸空指標
```

### calloc

```c
// calloc 初始化為零
int *arr = (int*)calloc(5, sizeof(int));
// 等同於 malloc 後 memset 為 0
```

### realloc

```c
int *arr = (int*)malloc(5 * sizeof(int));
arr = (int*)realloc(arr, 10 * sizeof(int));  // 擴展大小

// 更好的做法
int *new_arr = (int*)realloc(arr, 10 * sizeof(int));
if (new_arr != NULL) {
    arr = new_arr;
}
```

## 記憶體佈局

```
+------------------+ 高位址
|     核心         |
+------------------+
|     堆疊         |  <- grows down
|       ↓          |
|                  |
|       ↑          |
|     堆積         |  <- grows up
+------------------+
|     BSS          |  <- 未初始化全域變數
+------------------+
|     資料         |  <- 初始化全域變數
+------------------+
|     文字         |  <- 程式碼
+------------------+ 低位址
```

## 記憶體相關函式

```c
#include <string.h>

// 記憶體操作
memset(arr, 0, sizeof(arr));  // 設定記憶體
memcpy(dest, src, n);           // 複製記憶體
memmove(dest, src, n);          // 安全複製
memcmp(a, b, n);                // 比較記憶體
```

## 常見錯誤

### 指標未初始化

```c
int *p;        // 未初始化，指向未知位址
*p = 42;       // 危險！可能崩潰或破壞記憶體

// 正確做法
int *p = NULL;  // 初始化為 NULL
if (p != NULL) {
    *p = 42;
}
```

### 記憶體洩漏

```c
while (1) {
    int *arr = (int*)malloc(1000 * sizeof(int));
    // 忘記 free！
}
```

### 釋放後使用

```c
int *p = (int*)malloc(sizeof(int));
*p = 42;
free(p);
*p = 100;  // 危險！已釋放的記憶體
```

### 緩衝區溢位

```c
char buf[10];
gets(buf);  // 危險！可能溢出
```

## 結論

指標和記憶體管理是 C 語言的核心。正確理解和使用指標，可以寫出高效能的程式；忽視它們，則會導致各種錯誤和安全性問題。