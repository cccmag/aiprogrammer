# 生成器與迭代器的魔力

## 迭代器協定

在了解生成器之前，先理解 Python 的迭代器協定：

```python
# 迭代器必須實現 __iter__ 和 __next__ 方法
class Counter:
    def __init__(self, limit):
        self.limit = limit
        self.current = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.current >= self.limit:
            raise StopIteration
        result = self.current
        self.current += 1
        return result

for i in Counter(5):
    print(i)  # 0, 1, 2, 3, 4
```

## 生成器函式

生成器函式使用 `yield` 關鍵字：

```python
def count_up_to(limit):
    current = 0
    while current < limit:
        yield current
        current += 1

# 生成器物件
counter = count_up_to(5)

# 逐步取值
print(next(counter))  # 0
print(next(counter))  # 1
print(next(counter))  # 2

# 迭代
for i in count_up_to(5):
    print(i)
```

## 生成器表達式

```python
# 類似列表推導，但使用圓括號
gen = (x ** 2 for x in range(10))

print(list(gen))  # [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

# 使用 next 取值
gen = (x for x in range(3))
print(next(gen))  # 0
print(next(gen))  # 1
print(next(gen))  # 2
```

## 惰性求值

生成器的一個重要特點是惰性求值——只在需要時才計算：

```python
def expensive_computation(n):
    print(f"計算 {n}")
    return n * 2

# 生成器：不會立即執行計算
gen = (expensive_computation(i) for i in range(5))

print("還沒開始計算")
print(next(gen))  # 計算 0, 回傳 0
print(next(gen))  # 計算 1, 回傳 1
```

## 實際應用場景

### 無限序列

```python
def fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

# 可以產生無限多個費波那契數
fib = fibonacci()
for _ in range(10):
    print(next(fib))
```

### 處理大檔案

```python
def read_large_file(filename):
    """逐行讀取大檔案，不會將整個檔案載入記憶體"""
    with open(filename, 'r') as f:
        for line in f:
            yield line.strip()

# 使用
for line in read_large_file("huge_file.txt"):
    process(line)
```

### 串流處理

```python
def process_items(items):
    for item in items:
        yield process(item)

def filter_items(items, condition):
    for item in items:
        if condition(item):
            yield item

# 鏈式處理
data = range(1000)
result = process_items(filter_items(data, lambda x: x % 2 == 0))
```

### 置換巢狀迴圈

```python
# 巢狀迴圈
for x in range(5):
    for y in range(5):
        print((x, y))

# 使用生成器置換
def pairs(n):
    for x in range(n):
        for y in range(n):
            yield (x, y)

for pair in pairs(5):
    print(pair)
```

## 生成器的方法

### send()

```python
def echo():
    while True:
        received = yield
        print(received)

gen = echo()
next(gen)  # 啟動生成器
gen.send("第一條訊息")  # 印出：第一條訊息
gen.send("第二條訊息")  # 印出：第二條訊息
```

### throw() 和 close()

```python
def gen():
    try:
        while True:
            yield "hello"
    except ValueError:
        print("收到 ValueError")
        yield "world"

g = gen()
print(next(g))  # hello
g.throw(ValueError)  # 印出 "收到 ValueError"，生成器繼續
print(next(g))  # world
```

## itertools 模組

```python
import itertools

# 無限迭代器
count = itertools.count(10)  # 10, 11, 12, ...
cycle = itertools.cycle([1, 2, 3])  # 1, 2, 3, 1, 2, 3, ...
repeat = itertools.repeat(5, times=3)  # 5, 5, 5

# 有限迭代器
chain = itertools.chain([1, 2], [3, 4])  # 1, 2, 3, 4
islice = itertools.islice(range(10), 2, 8, 2)  # 2, 4, 6

# 排列組合
permutations = itertools.permutations([1, 2, 3], 2)  # (1,2), (1,3), (2,1), ...
combinations = itertools.combinations([1, 2, 3], 2)  # (1,2), (1,3), (2,3)
```

## yield from

```python
def flatten(nested):
    for item in nested:
        if isinstance(item, (list, tuple)):
            yield from flatten(item)
        else:
            yield item

data = [1, [2, 3], [4, [5, 6]], 7]
print(list(flatten(data)))  # [1, 2, 3, 4, 5, 6, 7]
```

## 結論

生成器是 Python 中處理惰性求值和記憶體效率問題的強大工具。它們允許你用聲明式的方式表達複雜的資料處理流程，同時保持記憶體使用的效率。