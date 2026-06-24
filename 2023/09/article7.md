# 高階函數與組合子

## 函數作為一等公民

### 高階函數

高階函數（Higher-Order Function）是滿足以下至少一項的函數：
- 接受函數作為參數
- 返回函數作為結果

```python
# map：接受函數和可迭代物件
def double(x): return x * 2
list(map(double, [1, 2, 3]))  # [2, 4, 6]

# filter：用謂詞函數過濾
def is_even(x): return x % 2 == 0
list(filter(is_even, [1, 2, 3, 4]))  # [2, 4]

# reduce：累積計算
from functools import reduce
reduce(lambda a, b: a + b, [1, 2, 3, 4])  # 10
```

### map/filter/reduce 模式

這三者是函數式程式設計的核心組合子，可以取代大部分的迴圈：

```python
# 命令式風格
result = []
for x in range(10):
    if x % 2 == 0:
        result.append(x * x)

# 函數式風格
result = list(map(lambda x: x * x,
                   filter(lambda x: x % 2 == 0,
                          range(10))))
```

### 函數組合（Function Composition）

將多個函數結合成一個新函數：

```python
def compose(f, g):
    return lambda x: f(g(x))

def add1(x): return x + 1
def double(x): return x * 2

add1_then_double = compose(double, add1)
print(add1_then_double(5))  # (5+1)*2 = 12
```

### 柯里化（Currying）

將多參數函數轉換為一系列單參數函數：

```python
# 普通函數
def add(a, b): return a + b

# 柯里化版本
def curry_add(a):
    def inner(b):
        return a + b
    return inner

add5 = curry_add(5)
print(add5(3))  # 8
```

### Combinator Pattern

組合子（Combinator）是沒有自由變數的高階函數。著名的組合子：

```python
# I combinator（恆等函數）
I = lambda x: x

# K combinator（常數函數）
K = lambda x: lambda y: x

# S combinator（代入）
S = lambda f: lambda g: lambda x: f(x)(g(x))

# 使用 S、K、I 可以定義所有可計算函數
```

### Point-Free Style

point-free 風格（或無點風格）避免明確提及函數參數：

```python
# 有點風格
add1_twice = lambda x: add1(add1(x))

# point-free 風格（使用函數組合）
add1_twice = compose(add1, add1)
```

### 實務應用

- **Python 裝飾器**：高階函數的具體應用
- **React Hooks**：高階元件模式
- **Express/Koa 中介軟體**：函數組合的管道模式
- **Iteration 工具**：itertools、functools 模組

### 延伸閱讀

- [高階函數介紹](https://www.google.com/search?q=higher+order+functions+programming)
- [Combinator 模式](https://www.google.com/search?q=combinator+pattern+functional+programming)
