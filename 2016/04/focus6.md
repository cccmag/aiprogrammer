# 主題六：高階函式與閉包

## 什麼是高階函式？

高階函式（Higher-Order Function）是接受函式作為輸入或返回函式作為輸出的函式。

```python
# 高階函式範例
def apply_twice(f, x):
    """將函式 f 應用兩次"""
    return f(f(x))

def double(x):
    return x * 2

result = apply_twice(double, 5)  # 20
```

## 為什麼高階函式如此強大？

### 抽象化重複模式

高階函式允許你將常見模式抽象化：

```python
# 原始方式：每個映射都要寫迴圈
result1 = []
for x in items1:
    result1.append(transform1(x))

result2 = []
for x in items2:
    result2.append(transform2(x))

# 高階函式方式：將模式抽象為 map
result1 = list(map(transform1, items1))
result2 = list(map(transform2, items2))
```

### 組合性

小而專注的函式可以組合成複雜行為：

```python
def compose(f, g):
    """組合兩個函式：先套用 g，再套用 f"""
    return lambda x: f(g(x))

def add_one(x):
    return x + 1

def double(x):
    return x * 2

# compose(add_one, double) = add_one(double(x))
add_then_double = compose(add_one, double)
print(add_then_double(5))  # (5 * 2) + 1 = 11
```

## 常見高階函式

### Map：轉換每個元素

```python
# 將每個數字平方
numbers = [1, 2, 3, 4, 5]
squares = list(map(lambda x: x ** 2, numbers))
# [1, 4, 9, 16, 25]
```

### Filter：篩選元素

```python
# 只保留偶數
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
evens = list(filter(lambda x: x % 2 == 0, numbers))
# [2, 4, 6, 8, 10]
```

### Reduce：聚合運算

```python
from functools import reduce

# 計算總和
numbers = [1, 2, 3, 4, 5]
total = reduce(lambda acc, x: acc + x, numbers, 0)
# 15

# 計算乘積
product = reduce(lambda acc, x: acc * x, numbers, 1)
# 120
```

### Compose：組合函式

```python
def compose(*functions):
    """將多個函式由右到左組合"""
    def inner(x):
        result = x
        for f in reversed(functions):
            result = f(result)
        return result
    return inner

# 管道：由左到右執行
def pipe(*functions):
    """將多個函式由左到右組合"""
    def inner(x):
        result = x
        for f in functions:
            result = f(result)
        return result
    return inner

# 使用示例
process = pipe(
    lambda x: x * 2,
    lambda x: x + 1,
    lambda x: x ** 2
)
print(process(3))  # ((3 * 2) + 1) ** 2 = 49
```

### Currying

Currying 將多參數函式轉換為一系列單參數函式：

```python
def curried_add(x):
    def inner(y):
        return x + y
    return inner

# 每個呼叫都返回新函式
add5 = curried_add(5)
add10 = curried_add(10)

print(add5(3))   # 8
print(add10(3))  # 13
```

### Partial Application

Partial Application 固定函式的部分參數：

```python
from functools import partial

def power(base, exponent):
    return base ** exponent

square = partial(power, exponent=2)
cube = partial(power, exponent=3)

print(square(5))  # 25
print(cube(5))    # 125
```

## 閉包：記住環境的函式

閉包（Closure）是一個函式，記住其建立時的詞法環境。

```python
def make_counter():
    count = 0
    def counter():
        nonlocal count
        count += 1
        return count
    return counter

# 每次呼叫 make_counter 都創建新的閉包
counter1 = make_counter()
counter2 = make_counter()

print(counter1())  # 1
print(counter1())  # 2
print(counter1())  # 3
print(counter2())  # 1（獨立的 count）
print(counter2())  # 2
```

## 閉包的實際應用

### 工廠函式

```python
def make_linear_transform(slope, intercept):
    """建立線性轉換函式"""
    def transform(x):
        return slope * x + intercept
    return transform

# 建立特定的線性轉換
normalize = make_linear_transform(1/255, 0)  # 標準化像素值
celsius_to_fahrenheit = make_linear_transform(9/5, 32)  # 溫度轉換

print(normalize(128))                        # 0.502
print(celsius_to_fahrenheit(100))            # 212.0
```

### 回調工廠

```python
def make_click_handler(action, data):
    """建立帶有封閉資料的回調"""
    def handler(event):
        print(f"Action: {action}, Data: {data}")
        # 執行實際動作
    return handler

# 為不同按鈕建立不同處理器
save_button.onclick = make_click_handler("save", {"user_id": 123})
delete_button.onclick = make_click_handler("delete", {"confirm": True})
```

### 記憶化（Memoization）

```python
def memoize(f):
    """將函式結果快取"""
    cache = {}
    def inner(*args):
        if args not in cache:
            cache[args] = f(*args)
        return cache[args]
    return inner

@memoize
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

# 原本指數複雜度，現在變成線性
print(fibonacci(100))  # 快速返回
```

## 函式作為資料

在 JavaScript 和 Python 等語言中，函式是一等公民（First-Class Citizen），可以：

- 賦值給變數
- 作為參數傳遞
- 作為返回值返回
- 存儲在資料結構中

```python
# 函式可以存儲在列表中
operations = [lambda x: x + 1, lambda x: x * 2, lambda x: x ** 2]

# 動態選擇操作
result = operations[1](5)  # 10
```

## Monad：組合計算的模式

Monad 是一種高階概念，用於組合計算。即使你不使用 Haskell，理解 Monad 的思想也能幫助你寫出更好的程式。

Monad 定律：

1. **左單位元**：return a >>= f ≡ f a
2. **右單位元**：m >>= return ≡ m
3. **結合性**：(m >>= f) >>= g ≡ m >>= (\x -> f x >>= g)

以 Python 為例：

```python
# 一個簡化的 Maybe Monad
class Maybe:
    def __init__(self, value):
        self.value = value

    def bind(self, f):
        if self.value is None:
            return Maybe(None)
        return f(self.value)

    def __repr__(self):
        return f"Maybe({self.value})"

# 使用
result = Maybe(5) \
    .bind(lambda x: Maybe(x * 2)) \
    .bind(lambda x: Maybe(x + 1))

print(result)  # Maybe(11)
```

## 小結

高階函式和閉包是函式式程式設計的核心概念。它們使得我們能夠：

- 抽象化常見模式
- 創建灵活的通用组件
- 以宣告式而非命令式思考
- 實現強大的元程式設計能力

這些概念不僅限於純函式語言，現代主流語言（Python、JavaScript、C#、Java）都支援這些特性。善用它們可以顯著提升程式碼品質。

下一篇文章中，我們將探討函式式反應式程式設計（FRP）——如何用函式式的方式處理時間變化的值。