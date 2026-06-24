# 主題二：C 語法基礎

## 基本程式結構

```c
#include <stdio.h>

int main(int argc, char *argv[]) {
    printf("Hello, World!\n");
    return 0;
}
```

每個 C 程式都從 `main()` 函式開始執行。

## 資料類型

### 基本類型

```c
// 整數類型
char c = 'A';           // 1 位元組
int i = 42;             // 通常 4 位元組
short s = 32767;        // 通常 2 位元組
long l = 2147483647L;   // 平臺相關
long long ll = 9223372036854775807LL;

// 浮點類型
float f = 3.14f;        // 4 位元組
double d = 3.1415926535; // 8 位元組

// 無符號類型
unsigned int ui = 100;
unsigned char uc = 255;
```

### sizeof 運算子

```c
printf("int 大小：%zu 位元組\n", sizeof(int));
printf("指標大小：%zu 位元組\n", sizeof(int*));
```

## 變數宣告

```c
int a = 10;              // 宣告並初始化
int b;                   // 宣告（未初始化，值未定義）
int c = 20, d = 30;      // 多個變數

// 常數
const int MAX = 100;
#define MAX_SIZE 1024    // 巨集常量
```

## 運算子

### 算術運算子

```c
int a = 10, b = 3;

printf("%d\n", a + b);   // 13
printf("%d\n", a - b);   // 7
printf("%d\n", a * b);   // 30
printf("%d\n", a / b);   // 3（整數除法）
printf("%d\n", a % b);   // 1（餘數）
```

### 比較和邏輯運算子

```c
int x = 5, y = 10;

if (x > 0 && y > 0) {    // 邏輯 AND
    printf("兩者都為正\n");
}

if (x < 0 || y < 0) {    // 邏輯 OR
    printf("至少有一個為正\n");
}

if (!(x == y)) {         // 邏輯 NOT
    printf("x 不等於 y\n");
}
```

### 位元運算子

```c
int a = 5;   // 0101
int b = 3;   // 0011

printf("%d\n", a & b);   // 1  (0001)
printf("%d\n", a | b);   // 7  (0111)
printf("%d\n", a ^ b);   // 6  (0110)
printf("%d\n", ~a);      // -6 (位元反轉)
printf("%d\n", a << 1);   // 10 (1010)
printf("%d\n", a >> 1);   // 2  (0010)
```

## 控制流程

### if-else

```c
int score = 85;

if (score >= 90) {
    printf("A\n");
} else if (score >= 80) {
    printf("B\n");
} else if (score >= 70) {
    printf("C\n");
} else {
    printf("D\n");
}
```

### switch

```c
int day = 3;

switch (day) {
    case 1:
        printf("星期一\n");
        break;
    case 2:
        printf("星期二\n");
        break;
    case 3:
        printf("星期三\n");
        break;
    default:
        printf("其他\n");
}
```

### while 迴圈

```c
int i = 0;
while (i < 5) {
    printf("%d ", i);
    i++;
}
// 輸出：0 1 2 3 4

// do-while（至少執行一次）
int j = 0;
do {
    printf("%d ", j);
    j++;
} while (j < 5);
```

### for 迴圈

```c
// 傳統 for 迴圈
for (int i = 0; i < 5; i++) {
    printf("%d ", i);
}

// C99 的 for 迴圈（初始化區塊）
for (int i = 0; i < 5; i++) {
    printf("%d ", i);
}

// 無限迴圈
for (;;) {
    // 會一直執行
    break;  // 需要 break 退出
}
```

### break 和 continue

```c
for (int i = 0; i < 10; i++) {
    if (i == 3) {
        continue;  // 跳過這次迭代
    }
    if (i == 7) {
        break;      // 退出迴圈
    }
    printf("%d ", i);
}
// 輸出：0 1 2 4 5 6
```

## 函式

### 函式定義

```c
int add(int a, int b) {
    return a + b;
}

// void 函式
void print_hello(void) {
    printf("Hello!\n");
}
```

### 函式原型

```c
// 在使用之前宣告函式原型
int add(int a, int b);

int main(void) {
    int result = add(1, 2);
    return 0;
}

int add(int a, int b) {
    return a + b;
}
```

### 遞迴

```c
int factorial(int n) {
    if (n <= 1) {
        return 1;
    }
    return n * factorial(n - 1);
}

int fibonacci(int n) {
    if (n <= 1) {
        return n;
    }
    return fibonacci(n - 1) + fibonacci(n - 2);
}
```

## 陣列

```c
// 宣告和初始化
int arr[5] = {1, 2, 3, 4, 5};
int arr2[] = {1, 2, 3, 4, 5};

// 走訪
for (int i = 0; i < 5; i++) {
    printf("%d ", arr[i]);
}

// 字串
char str[] = "Hello";
printf("%s\n", str);
printf("%c\n", str[0]);  // 'H'
```

## 列舉

```c
enum Color { RED, GREEN, BLUE };
enum Color c = RED;

printf("%d\n", RED);    // 0
printf("%d\n", GREEN);  // 1
printf("%d\n", BLUE);   // 2

// 指定值
enum Day { MON = 1, TUE, WED, THU, FRI, SAT, SUN };
```

## typedef

```c
typedef unsigned int uint;
typedef int (*func_ptr)(int, int);

uint a = 100;
```

## 結論

這些是 C 語言基礎語法的核心內容。熟練掌握這些基本概念，是進一步學習指標、記憶體管理和系統程式設計的基礎。