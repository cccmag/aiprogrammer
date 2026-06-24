# 遞迴程式設計

## 什麼是遞迴？

遞迴（Recursion）是函數呼叫自身的程式設計技巧。它讓複雜問題的解法變得簡潔優雅。

## 遞迴的三個要素

1. **終止條件（Base Case）**：問題最小化時的答案
2. **遞迴關係（Recursive Relation）**：將大問題轉化為較小問題
3. **逐步逼近終止（Progress Toward Base）**：每次呼叫都讓問題變小

## 經典範例

### 階乘

```python
def factorial(n):
    if n <= 1:        # base case
        return 1
    return n * factorial(n - 1)  # recursive step
```

### 費氏數列

```python
def fibonacci(n):
    if n <= 1:        # base case
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)
```

### 河內塔

```python
def hanoi(n, source, target, auxiliary):
    if n == 1:
        print(f"移動盤子 1 從 {source} 到 {target}")
        return
    hanoi(n - 1, source, auxiliary, target)
    print(f"移動盤子 {n} 從 {source} 到 {target}")
    hanoi(n - 1, auxiliary, target, source)

hanoi(3, 'A', 'C', 'B')
```

## 遞迴的記憶體行為

每次遞迴呼叫會建立新的 Stack Frame，儲存區域變數和返回地址。遞迴太深會造成 Stack Overflow。

```python
import sys
print(sys.getrecursionlimit())  # 預設 1000
sys.setrecursionlimit(10000)    # 可調高
```

## 尾遞迴優化

當遞迴呼叫是函數的最後一個操作時，稱為尾遞迴（Tail Recursion）。Python 不支援尾遞迴優化。

```python
# 尾遞迴版本 — Python 中無效能優勢
def factorial_tail(n, acc=1):
    if n <= 1:
        return acc
    return factorial_tail(n - 1, n * acc)

# 仍是 O(n) 空間
```

## 遞迴 vs 迭代

| 面向 | 遞迴 | 迭代 |
|------|------|------|
| 程式碼 | 簡潔優雅 | 較長 |
| 可讀性 | 高（適合分治問題） | 高（適合線性問題） |
| 空間 | O(n) Stack | O(1) |
| 速度 | 函數呼叫開銷 | 較快 |

## 參考資源

- https://www.google.com/search?q=recursion+programming+explained+simply
- https://www.google.com/search?q=Python+recursion+examples

## 小結

遞迴是理解高階演算法（如 Tree DFS、Divide and Conquer、Dynamic Programming）的必備基礎，值得花時間深入掌握。
