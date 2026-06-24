# 生成器與迭代器

## 惰性求值的威力（2001-2026）

### 前言

迭代器（iterator）和生成器（generator）是 Python 處理序列資料的核心抽象。它們的核心思想是**惰性求值**——只在需要的時候才產生下一個值，而不是一次性把整個序列載入記憶體。

### 迭代器協定

任何實作了 `__iter__` 和 `__next__` 方法的物件都是迭代器：

```python
class Counter:
    def __init__(self, max_n):
        self.n = 0
        self.max_n = max_n
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.n >= self.max_n:
            raise StopIteration
        self.n += 1
        return self.n

for i in Counter(5):
    print(i)  # 1, 2, 3, 4, 5
```

`for` 迴圈實際上在背後呼叫了 `__iter__` 和 `__next__`。

### 生成器：簡化的迭代器

生成器使用 `yield` 關鍵字，自動實作了迭代器協定：

```python
def counter(max_n):
    n = 1
    while n <= max_n:
        yield n
        n += 1

for i in counter(5):
    print(i)
```

當函式執行到 `yield` 時，它會暫停並返回一個值，下次呼叫 `__next__` 時從暫停處繼續執行。

### 惰性求值的優勢

生成器的核心優勢是記憶體效率。比較兩種方法：

```python
# 方法 1：一次載入所有資料
def read_large_file(filename):
    with open(filename) as f:
        return f.readlines()  # 全部載入記憶體

# 方法 2：惰性讀取
def read_large_file_lazy(filename):
    with open(filename) as f:
        for line in f:
            yield line  # 逐行產生

# 方法 1 當檔案很大時會耗盡記憶體
# 方法 2 無論檔案多大都能處理
```

### send 與雙向通訊

生成器不僅可以產生值，還可以接收值：

```python
def echo():
    while True:
        received = yield
        print(f"收到: {received}")

gen = echo()
next(gen)          # 啟動生成器
gen.send("Hello")  # 輸出: 收到: Hello
gen.send("World")  # 輸出: 收到: World
```

`send` 方法允許呼叫者向生成器內部傳遞資料。

### yield from 委託

`yield from` 允許一個生成器委託給另一個生成器：

```python
def sub_generator():
    yield 1
    yield 2
    yield 3

def main_generator():
    yield "開始"
    yield from sub_generator()
    yield "結束"

list(main_generator())  # ['開始', 1, 2, 3, '結束']
```

### 生成器表達式

類似列表推導式，但返回生成器：

```python
# 列表推導式（立即求值）
squares_list = [x*x for x in range(10)]

# 生成器表達式（惰性求值）
squares_gen = (x*x for x in range(10))

# 生成器不佔用記憶體
print(sum(x*x for x in range(1000000)))  # 記憶體高效
```

### 管線模式

生成器可以串聯形成處理管線：

```python
def read(filename):
    with open(filename) as f:
        for line in f:
            yield line

def filter_lines(lines, keyword):
    for line in lines:
        if keyword in line:
            yield line

def to_upper(lines):
    for line in lines:
        yield line.upper()

# 串聯管線
pipeline = to_upper(filter_lines(read("data.txt"), "ERROR"))
for line in pipeline:
    print(line)
```

### 小結

生成器和迭代器是 Python 惰性求值的基礎設施。它們讓程式可以用固定的記憶體處理任意大的資料集，同時提供了優雅的序列處理抽象。

---

**下一步**：[上下文管理器](focus3.md)

## 延伸閱讀

- [Python 迭代器與生成器官方文件](https://www.google.com/search?q=Python+iterator+generator+documentation)
- [PEP 255: Simple Generators](https://www.google.com/search?q=PEP+255+Python+generators)
- [PEP 342: Coroutines via Enhanced Generators](https://www.google.com/search?q=PEP+342+generator+coroutines)
