# 分支預測優化

## 分支預測原理

現代 CPU 使用分支預測器來猜測分支走向，提前執行可能的路徑。

### 預測失敗的代價

```
正確預測：1 個週期
預測失敗：10-20 個週期（取決於管線深度）
```

## 幫助分支預測器

### 1. 排序資料

```c
// 不好：如果排序，幾乎每次都預測錯誤
for (int i = 0; i < n; i++)
    if (array[i] > threshold)
        process(array[i]);

// 好：將為 true 的元素集中在一起
for (int i = 0; i < n; i++)
    if (array[i] <= threshold)
        process(array[i]);
```

### 2. 使用 likely/unlikely

```c
#include <linux/compiler.h>

if (likely(error == 0)) {
    // 大多數情況是 true
}

if (unlikely(ptr == NULL)) {
    // 很少發生
}
```

### 3. 避免過多分支

```c
// 不好：過多分支導致預測困難
switch (status) {
    case 0: result = a; break;
    case 1: result = b; break;
    // ... 超過 10 個 case
}

// 好：使用查找表或映射
static int lookup[] = {a, b, c, d, e, f, g, h, i, j};
result = lookup[status];
```

## 條件移動

### 使用 ?: 代替 if

```c
// 編譯器可能優化為條件移動
int result = (condition) ? value_if_true : value_if_false;

// 等價於
int result;
if (condition)
    result = value_if_true;
else
    result = value_if_false;
```

### 使用 bit 操作

```c
// 不好
int result = (x > 0) ? x : 0;

// 好：使用 max 操作
int result = x > 0 ? x : 0;  // 仍然可能有分支
```

## 迴圈中的分支

### 將分支移到迴圈外

```c
// 不好：每次迭代都要檢查
for (int i = 0; i < n; i++)
    if (condition)
        array[i] *= 2;

// 好：將處理分開
if (condition) {
    for (int i = 0; i < n; i++)
        array[i] *= 2;
} else {
    // 不做任何事或執行其他操作
}
```

## 二分搜尋優化

```c
// 不好：每次比較都有分支
while (left <= right) {
    int mid = (left + right) / 2;
    if (array[mid] == target)
        return mid;
    else if (array[mid] < target)
        left = mid + 1;
    else
        right = mid - 1;
}

// 好：使用位操作計算
while (right > left) {
    int mid = left + ((right - left) >> 1);
    // ...
}
```

## 測量分支預測失敗

```bash
perf stat -e branch-misses,branches ./program
```

## 參考資料

- [分支預測優化](https://www.google.com/search?q=branch+prediction+optimization+C++)
- [分支預測原理](https://www.google.com/search?q=branch+prediction+原理)