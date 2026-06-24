# 函式程式設計

## 函式作為一等公民

```python
def square(x):
    return x ** 2

f = square  # 函式可以指派給變數
print(f(5))  # 25

# 可以作為參數傳遞
def apply_twice(func, x):
    return func(func(x))

print(apply_twice(square, 2))  # 16
```

## Lambda 表達式

```python
# 匿名函式
square = lambda x: x ** 2
print(square(5))  # 25

# 多參數
add = lambda x, y: x + y
print(add(3, 4))  # 7

# 經常與 sorted, map, filter 一起使用
pairs = [(1, 'one'), (3, 'three'), (2, 'two')]
sorted(pairs, key=lambda x: x[0])
```

## Map, Filter, Reduce

```python
from functools import reduce

# map：對每個元素應用函式
nums = [1, 2, 3, 4, 5]
squares = list(map(lambda x: x ** 2, nums))
print(squares)  # [1, 4, 9, 16, 25]

# filter：過濾元素
evens = list(filter(lambda x: x % 2 == 0, nums))
print(evens)  # [2, 4]

# reduce：累計計算
product = reduce(lambda x, y: x * y, nums)
print(product)  # 120
```

## 列表推導式

```python
# 等價於 map
squares = [x ** 2 for x in range(5)]

# 等價於 filter + map
evens_squared = [x ** 2 for x in range(10) if x % 2 == 0]

# 巢狀
matrix = [[i * j for j in range(3)] for i in range(3)]
```

## 生成器

```python
# 生成器函式
def count_up_to(n):
    i = 1
    while i <= n:
        yield i
        i += 1

for num in count_up_to(5):
    print(num)

# 生成器表達式
gen = (x ** 2 for x in range(10))
print(list(gen))
```

## 裝飾器

```python
def timer(func):
    import time
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print(f"Took {time.time() - start:.2f}s")
        return result
    return wrapper

@timer
def slow_function():
    import time
    time.sleep(1)
    return "Done"

slow_function()
```

## 部分應用

```python
from functools import partial

def power(base, exponent):
    return base ** exponent

square = partial(power, exponent=2)
cube = partial(power, exponent=3)

print(square(5))  # 25
print(cube(5))   # 125
```

## 閉包

```python
def make_counter():
    count = 0
    def counter():
        nonlocal count
        count += 1
        return count
    return counter

c = make_counter()
print(c())  # 1
print(c())  # 2
print(c())  # 3
```

## 總結

函式程式設計技巧可以讓代碼更簡潔：
- Lambda 表達式用於簡單函式
- map/filter/reduce 處理集合
- 生成器處理大型資料
- 裝飾器添加橫切關注功能