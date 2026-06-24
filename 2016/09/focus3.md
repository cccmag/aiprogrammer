# Compiler 優化

## 編譯器優化概述

現代編譯器可以執行多種優化，包括：
- 常數折疊
- 死碼消除
- 內聯
- 循環優化
- 向量化

## GCC/Clang 優化選項

### 基本優化級別

| 選項 | 說明 |
|-----|------|
| -O0 | 無優化（預設，調試用）|
| -O1 | 基本優化，快速的編譯時間 |
| -O2 | 更積極的優化（推薦） |
| -O3 | 激進優化，可能增加程式碼大小 |
| -Os | 優化大小 |
| -Ofast | 快速浮點（放寬 IEEE） |

### 特定優化

```bash
# 內聯
gcc -O3 -finline-functions program.c

# 向量化
gcc -O3 -ftree-vectorize program.c

# 連結時優化（LTO）
gcc -O3 -flto program.c

# 過程間分析
gcc -O3 -fipa-ra program.c
```

## Link Time Optimization（LTO）

跨翻譯單元進行優化：

```bash
# 編譯時開啟 LTO
gcc -flto -O3 a.c b.c -o program

# 或分步
gcc -flto -c a.c
gcc -flto -c b.c
gcc -flto -O3 a.o b.o -o program
```

## 過程間分析（IPA）

### 常數傳播

```c
// 編譯器可以直接計算結果
int foo(int x) { return x * 2 + 3; }
int bar() { return foo(5); }
// 優化後：bar() 直接 return 13
```

### 內聯

```c
// 小函數自動內聯
static inline int min(int a, int b) {
    return a < b ? a : b;
}
```

## 循環優化

### 循環展開

```bash
gcc -O3 -funroll-loops program.c
```

```c
// 原始
for (int i = 0; i < 4; i++)
    sum += a[i];

// 可能優化為
sum = a[0] + a[1] + a[2] + a[3];
```

### 循環合併

```c
// 兩個循環合併為一個
for (int i = 0; i < N; i++)
    a[i] = b[i] * 2;

for (int i = 0; i < N; i++)
    c[i] = a[i] + 1;

// 合併後
for (int i = 0; i < N; i++) {
    a[i] = b[i] * 2;
    c[i] = a[i] + 1;
}
```

### 循環置換

改變巢狀循環的順序以提高快取局部性：

```c
// 慢：大多數記憶體訪問不在快取中
for (int i = 0; i < N; i++)
    for (int j = 0; j < M; j++)
        a[j][i] = b[j][i] * 2;

// 快：記憶體訪問是連續的
for (int i = 0; i < N; i++)
    for (int j = 0; j < M; j++)
        a[i][j] = b[i][j] * 2;
```

## 自動向量化

### 開啟向量化

```bash
gcc -O3 -ftree-vectorize program.c
```

### 向量化報告

```bash
gcc -O3 -ftree-vectorize -fopt-info-vec-optimized program.c
```

### 範例

```c
// 編譯器自動使用 SIMD
void vector_add(float* a, float* b, float* c, int n) {
    for (int i = 0; i < n; i++)
        c[i] = a[i] + b[i];
}

// 可能被向量化為使用 SSE/AVX
// 每次迭代處理 4 個（float）或 8 個 float
```

## 目標架構

### 指定 CPU

```bash
# 使用特定 CPU 的指令集
gcc -O3 -march=native program.c    # 本機最佳化
gcc -O3 -march=skylake program.c
gcc -O3 -march=haswell program.c
```

### AVX 支援

```bash
# 包含 AVX 指令
gcc -O3 -mavx program.c

# AVX2
gcc -O3 -mavx2 program.c

# AVX-512
gcc -O3 -mavx512f -mavx512dq program.c
```

## 優化提示

### likely / unlikely

```c
#include <linux/compiler.h>

if (likely(condition)) {
    // 編譯器更好地安排分支預測
}

if (unlikely(error)) {
    // 處理罕見的錯誤情況
}
```

### 屬性提示

```c
// 告訴編譯器這個函數是熱門的
__attribute__((hot)) void hot_function() {
    // ...
}

// 告訴編譯器不要內聯
__attribute__((noinline)) void large_function() {
    // ...
}

// 告訴編譯器記憶體對齊
__attribute__((aligned(16))) char buffer[256];
```

## 診斷工具

### 查看產生的組合語言

```bash
# 產生組合語言
gcc -O3 -S program.c -o program.s

# 或者帶注釋的
gcc -O3 -S -fverbose-asm program.c -o program.s
```

### 查看優化決策

```bash
# 所有優化報告
gcc -O3 -fopt-info-all program.c

# 向量化報告
gcc -O3 -fopt-info-vec-optimized program.c

# 内联報告
gcc -O3 -fopt-info-inline program.c
```

## 浮點優化

### 浮點模型

```bash
# 快速但可能不符合 IEEE
gcc -Ofast -ffast-math program.c

# 合理的快速數學
gcc -O3 -funsafe-math-optimizations -ffinite-math-only
```

### 注意事項

```c
// -ffast-math 可能改變結果
// 只有在確定可以接受時使用
double a = 1e20, b = -1e20, c = 1.0;
double result1 = (a + b) + c;  // (a+b) = 0
double result2 = a + (b + c);  // (b+c) = 1
```

## 參考資料

- [GCC 優化選項](https://www.google.com/search?q=GCC+optimization+options)
- [編譯器優化教程](https://www.google.com/search?q=compiler+optimization+tutorial+C++)
- [LLVM 優化傳遞](https://www.google.com/search?q=LLVM+optimization+passes)