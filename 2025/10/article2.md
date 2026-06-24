# 生成器與 yield

## 1. 引言

生成器（generator）是 Python 處理序列資料的秘密武器。它讓你可以用迭代的方式處理無限或超大型資料集，而記憶體使用量始終保持不變。本文將深入探討生成器的底層機制與實戰應用。

## 2. Generator 與 Iterator 的關係

所有生成器都是迭代器，但迭代器不一定是生成器。生成器是使用 `yield` 關鍵字的函式：

```python
# 迭代器
class Squares:
    def __init__(self, n):
        self.n = n
        self.i = 0
    def __iter__(self):
        return self
    def __next__(self):
        if self.i >= self.n:
            raise StopIteration
        self.i += 1
        return (self.i - 1) ** 2

# 生成器（約簡了 10 行）
def squares(n):
    for i in range(n):
        yield i ** 2
```

## 3. yield 的執行模型

當 Python 執行到 `yield` 時，函式的狀態被「凍結」——區域變數、指令指針、堆疊幀都被保存：

```python
def generator():
    print("step 1")
    yield "A"
    print("step 2")
    yield "B"
    print("step 3")
    yield "C"

gen = generator()
print(next(gen))  # step 1 → A
print(next(gen))  # step 2 → B
print(next(gen))  # step 3 → C
print(next(gen))  # StopIteration
```

## 4. send：雙向通訊

`send` 方法可以向生成器內部傳遞值：

```python
def accumulator():
    total = 0
    while True:
        value = yield total
        total += value

acc = accumulator()
next(acc)          # 啟動生成器
print(acc.send(10))  # 10
print(acc.send(20))  # 30
print(acc.send(30))  # 60
```

## 5. yield from 委託

`yield from` 允許一個生成器委託給子生成器：

```python
def flatten(nested):
    for item in nested:
        if isinstance(item, (list, tuple)):
            yield from flatten(item)
        else:
            yield item

nested = [1, [2, [3, 4], 5], 6]
print(list(flatten(nested)))  # [1, 2, 3, 4, 5, 6]
```

## 6. 實戰案例

### 大型檔案處理

```python
def read_chunks(file_path, chunk_size=1024):
    with open(file_path, 'rb') as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            yield chunk

def process_logs(file_path):
    for chunk in read_chunks(file_path):
        lines = chunk.split(b'\n')
        # 處理每一行
        for line in lines:
            if b'ERROR' in line:
                yield line

# 無論檔案多大，記憶體使用量固定
for error in process_logs("server.log"):
    print(error.decode('utf-8', errors='replace'))
```

### 無限序列

```python
def primes():
    yield 2
    n = 3
    while True:
        for p in range(3, int(n**0.5) + 1, 2):
            if n % p == 0:
                break
        else:
            yield n
        n += 2

# 取前 100 個質數
import itertools
first_100 = list(itertools.islice(primes(), 100))
```

## 7. 生成器 vs 列表推導式

```python
# 列表推導式：立即計算，佔記憶體
squares_list = [x**2 for x in range(1000000)]

# 生成器表達式：惰性計算，幾乎不佔記憶體
squares_gen = (x**2 for x in range(1000000))

# 當只需要迭代一次時，生成器更高效
print(sum(x**2 for x in range(1000000)))
```

## 8. 總結

生成器是 Python 惰性求值的基礎設施。使用 `yield` 可以建立優雅的管線處理模式，在不犧牲可讀性的前提下大幅降低記憶體使用。

## 延伸閱讀

- [PEP 255: Simple Generators](https://www.google.com/search?q=PEP+255+Python+generators)
- [Python Generator 官方指南](https://www.google.com/search?q=Python+generator+official+tutorial)
