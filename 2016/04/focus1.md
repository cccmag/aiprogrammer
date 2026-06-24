# 主題一：函數式程式設計的基礎

## Lambda Calculus：一切的起點

1936 年，Alonzo Church 在 Princeton 大學發明了 Lambda Calculus（一種描述計算的形式系統）。這是理解函數式程式設計的數學基礎，也是現代所有函數式語言的理論根源。

Lambda Calculus 的核心概念極為簡單，僅由三個元素組成：

1. **變數引用**：`x` 表示一個變數
2. **函式抽象**：`λx.M` 表示一個以 `x` 為參數、表達式 `M` 為函式體的函式
3. **函式應用**：`M N` 表示將函式 `M` 應用於參數 `N`

例如，傳統數學中的函式 `f(x) = x + 1` 在 Lambda Calculus 中寫為 `λx. x + 1`。而 `f(5)` 則寫成 `(λx. x + 1) 5`。

## 函數式思維的本質

### 從語句到運算式

傳統命令式程式設計以「語句」為基礎：「做這個，然後做那個」。函數式程式設計以「運算式」為基礎：「這個運算式的值是什麼」。

```python
# 命令式思維
result = []
for x in items:
    if x > 0:
        result.append(x * 2)

# 函數式思維
result = list(map(lambda x: x * 2, filter(lambda x: x > 0, items)))
```

### 無副作用

純函式不修改任何全域狀態，不進行 I/O 操作，不拋出異常。相同的輸入永遠產生相同的輸出。

```python
# 不純的函式（依賴外部狀態）
total = 0
def add_to_total(x):
    global total
    total += x
    return total

# 純函式（無副作用）
def add(a, b):
    return a + b
```

### 資料轉換而非修改

在函數式世界中，我們不修改資料，而是通過轉換創建新資料。

```python
# 命令式：修改陣列
arr = [1, 2, 3, 4, 5]
for i in range(len(arr)):
    arr[i] *= 2

# 函數式：創建新陣列
arr = [1, 2, 3, 4, 5]
new_arr = list(map(lambda x: x * 2, arr))
```

## Python 中的函數式特性

Python 從誕生之初就支援多種函數式特性：

### Lambda 表達式

```python
square = lambda x: x ** 2
add = lambda x, y: x + y
```

### map、filter、reduce

```python
from functools import reduce

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# map：轉換每個元素
squares = list(map(lambda x: x ** 2, numbers))

# filter：篩選元素
evens = list(filter(lambda x: x % 2 == 0, numbers))

# reduce：聚合運算
total = reduce(lambda acc, x: acc + x, numbers, 0)
```

### 列表推导式（List Comprehension）

Python 的列表推导式是函數式思維的體現：

```python
squares = [x ** 2 for x in range(10)]
evens = [x for x in range(20) if x % 2 == 0]
matrix = [[i * j for j in range(5)] for i in range(5)]
```

### 生成器表達式

生成器表達式延遲求值，只有在需要時才計算：

```python
sum_of_squares = sum(x ** 2 for x in range(1000000))
```

## 閉包與高階函式

閉包（Closure）是函數式程式設計的核心概念，指的是一個函式記住其建立時的詞法環境（lexical environment）。

```python
def make_adder(n):
    def adder(x):
        return x + n
    return adder

add5 = make_adder(5)
add10 = make_adder(10)

print(add5(3))   # 8
print(add10(3))  # 13
```

高階函式接受函式作為輸入或返回函式作為輸出：

```python
def apply_twice(f, x):
    return f(f(x))

def double(x):
    return x * 2

print(apply_twice(double, 5))  # 20
```

## Currying 與 Partial Application

Currying 將接受多個參數的函式轉換為一系列接受單一參數的函式：

```python
def curried_add(x):
    def inner(y):
        return x + y
    return inner

add5 = curried_add(5)
print(add5(10))  # 15
```

Partial Application（偏函數應用）固定函式的部分參數：

```python
from functools import partial

def power(base, exponent):
    return base ** exponent

square = partial(power, exponent=2)
cube = partial(power, exponent=3)

print(square(5))  # 25
print(cube(5))    # 125
```

## 組合與管線

函數式程式設計強調小型、 可組合的構建模塊：

```python
def compose(f, g):
    return lambda x: f(g(x))

def inc(x):
    return x + 1

def double(x):
    return x * 2

# compose 創建新函式：先加倍再遞增
inc_then_double = compose(double, inc)

print(inc_then_double(5))  # (5 + 1) * 2 = 12
```

## 小結

函數式程式設計不僅是一種技術，更是一種思維方式。它教會我們：

- 以運算式而非語句思考
- 追求透明引用（ Referential Transparency）
- 利用抽象而非重複
- 將複雜問題分解為簡單函式的組合

這些原則不僅適用於 Haskell 或 Clojure，也能幫助我們寫出更好的 Java、Python 或 JavaScript 程式。下一篇文章中，我們將深入探討純函式語言的典範——Haskell。