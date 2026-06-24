# 指針別名問題

## 什麼是指針別名？

當兩個指標指向同一個記憶體位置時，稱為別名（aliasing）。

```c
void func(int* a, int* b) {
    *a = 5;    // 影響 *b 如果 a == b
    *b = 6;
}
```

## 別名對優化的影響

```c
void process(float* __restrict a, float* __restrict b, int n) {
    for (int i = 0; i < n; i++)
        a[i] = b[i] * 2;
    // 編譯器可以安全地對齊這兩個指標的訪問
}
```

如果沒有 `__restrict`，編譯器必須假設指標可能重疊，導致無法最佳化。

## restrict 關鍵字

```c
// 告知編譯器指標不重疊
void copy(float* __restrict dest, const float* __restrict src, int n) {
    for (int i = 0; i < n; i++)
        dest[i] = src[i];
}
```

## 指標別名的風險

```c
// 危險的程式碼
void update(int* a, int* b) {
    *a = calculate(*a);  // 如果 a == b，結果會不同
    *b = 0;
}

// 安全版本：使用臨時變數
void update_safe(int* a, int* b) {
    int temp = calculate(*a);
    *a = temp;
    *b = 0;
}
```

## GCC 的別名分析

```bash
# 開啟嚴格的別名分析
gcc -fstrict-aliasing -O3 program.c

# 警告潛在的別名問題
gcc -Wstrict-aliasing program.c
```

## 避免別名的模式

### 使用本地副本

```c
// 不好
void process(Point* p) {
    p->x = compute(p->x);
    p->y = compute(p->y);
}

// 好
void process(Point* p) {
    float x = p->x;
    float y = p->y;
    x = compute(x);
    y = compute(y);
    p->x = x;
    p->y = y;
}
```

### 結構指標 vs 陣列

```c
// 不好：編譯器必須假設可能別名
void scale_vector(float* x, float* y, float s, int n) {
    for (int i = 0; i < n; i++) {
        x[i] *= s;
        y[i] *= s;
    }
}

// 好：使用獨立參數
void scale_vector(float* __restrict x, float* __restrict y,
                  float s, int n) {
    for (int i = 0; i < n; i++) {
        x[i] *= s;
        y[i] *= s;
    }
}
```

## 參考資料

- [C restrict 關鍵字](https://www.google.com/search?q=restrict+keyword+C)
- [指標別名分析](https://www.google.com/search?q=pointer+aliasing+analysis)