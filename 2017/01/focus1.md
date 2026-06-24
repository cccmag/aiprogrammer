# Python 3.6 的新特性：f-string、效能優化與開發者體驗

## 前言

Python 3.6 於 2016 年 12 月 23 日正式發布，代號「金色的薩克斯風」（Gilver Snafu）。這個版本帶來了多項令人振奮的新特性，特別是在開發者體驗和效能方面。本篇文章將深入介紹 Python 3.6 的重要新功能。

## f-string：格式化字串的新標準

### 為什麼需要新的格式化方式？

Python 的字串格式化經歷了三個階段：

```python
# 第一代：% 格式化（Python 2 時代）
name = "Alice"
age = 30
print("Name: %s, Age: %d" % (name, age))

# 第二代：str.format()（Python 2.6+）
print("Name: {}, Age: {}".format(name, age))
print("Name: {0}, Age: {1}".format(name, age))
print("Name: {name}, Age: {age}".format(name=name, age=age))

# 第三代：f-string（Python 3.6+）
print(f"Name: {name}, Age: {age}")
```

f-string 使用字首 `f` 或 `F` 標記，允許在字串中直接嵌入 Python 表達式。

### f-string 的強大功能

```python
# 基本用法
name = "Alice"
age = 30
print(f"Name: {name}, Age: {age}")

# 表達式求值
a = 10
b = 20
print(f"{a} + {b} = {a + b}")  # 10 + 20 = 30
print(f"{a} * {b} = {a * b}")  # 10 * 20 = 200

# 呼叫方法
name = "alice"
print(f"Upper: {name.upper()}")  # Upper: ALICE

# 呼叫函式
import math
print(f"Pi: {math.pi:.4f}")  # Pi: 3.1416

# 巢狀屬性
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

p = Person("Bob", 25)
print(f"Person: {p.name}, Age: {p.age}")
```

### 格式化規格

f-string 支援豐富的格式化選項：

```python
# 數字格式化
x = 3.14159
print(f"Pi: {x:.2f}")      # Pi: 3.14
print(f"Pi: {x:10.2f}")    # Pi:       3.14（右對齊）
print(f"Pi: {x:<10.2f}")   # Pi: 3.14       （左對齊）

# 整數格式化
n = 255
print(f"Hex: {n:#x}")      # Hex: 0xff
print(f"Bin: {n:#b}")      # Bin: 0b11111111
print(f"Oct: {n:#o}")      # Oct: 0o377

# 千分位
large = 1234567
print(f"{large:,}")        # 1,234,567
print(f"{large:_}")        # 1_234_567

# 百分比
ratio = 0.756
print(f"{ratio:.1%}")      # 75.6%
```

### 與舊方式的效能比較

```python
import timeit

name = "Alice"
age = 30

# % 格式化
t1 = timeit.timeit('"%s %d" % (name, age)', globals=globals())

# .format()
t2 = timeit.timeit('"{} {}".format(name, age)', globals=globals())

# f-string
t3 = timeit.timeit('f"{name} {age}"', globals=globals())

print(f"% formatting: {t1:.4f}s")
print(f".format():    {t2:.4f}s")
print(f"f-string:     {t3:.4f}s")
# f-string 通常是最快的！
```

## 協程與 asyncio 改進

### asyncio 回顧

Python 3.4 引入的 asyncio 模組為異步程式設計提供了標準框架。Python 3.6 繼續強化了這個模組。

```python
# Python 3.4+ 的基本 async/await 語法
import asyncio

async def fetch_data():
    await asyncio.sleep(1)
    return "data"

async def main():
    result = await fetch_data()
    print(f"Got: {result}")

asyncio.run(main())
```

### Python 3.6 的 asyncio 改進

```python
# asyncio.Runner()：更好的異步執行控制
async def main():
    # 使用 asyncio.Runner() 封裝
    pass

# Python 3.7+ 有 asyncio.run()
# 但 Python 3.6 可以這樣做：
runner = asyncio.Runner()
runner.run(main())
```

### 協程的底層改進

Python 3.6 減少了 asyncio 的記憶體使用，並提升了效能：

```python
# 任務取消的穩定性提升
async def long_task():
    try:
        for i in range(100):
            await asyncio.sleep(0.1)
            print(f"Step {i}")
    except asyncio.CancelledError:
        print("Task was cancelled")
        raise

async def main():
    task = asyncio.ensure_future(long_task())
    await asyncio.sleep(0.5)
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        print("Main: task cancelled")

asyncio.run(main())
```

## 字典效能優化

### Python 3.6 的 Dict 實現

Python 3.6 優化了字典的內部實現，使用了更緊湊的記憶體佈局：

```python
# Python 3.5 及之前：dict 保持插入順序是副作用
d1 = {}
d1['a'] = 1
d1['b'] = 2
d1['c'] = 3

# Python 3.6+：dict 保持插入順序是語言特性
d2 = {}
d2['a'] = 1
d2['b'] = 2
d2['c'] = 3

# 兩者現在都能保證順序，但效能不同
```

### 效能提升

```python
import sys

# Python 3.6 的 dict 更節省記憶體
d = {f"key_{i}": i for i in range(1000)}
print(f"Dict size: {sys.getsizeof(d)} bytes")

# 新聞：dict 的實現變成了 "compact" 形式
# 這是 CPython 實現細節的改變
```

## secrets 模組：安全的亂數生成

### 為什麼需要 secrets？

密碼學安全的亂數在現代應用中非常重要，但之前 Python 沒有標準庫來處理這個需求。

```python
# Python 3.6 新增的 secrets 模組
import secrets

# 生成安全的亂數位元組
token = secrets.token_bytes(16)
print(f"Token: {token.hex()}")

# 生成 URL 安全的隨機字串
token_url = secrets.token_urlsafe(16)
print(f"URL token: {token_url}")

# 生成十六進制字串
token_hex = secrets.token_hex(16)
print(f"Hex token: {token_hex}")

# 密碼學安全的比較
a = "some_value"
b = "some_value"
print(f"Equals: {secrets.compare_digest(a, b)}")
```

### 實際應用場景

```python
import secrets
import string

def generate_password(length=16):
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def generate_verification_code():
    return ''.join(secrets.choice(string.digits) for _ in range(6))

print(f"Password: {generate_password()}")
print(f"Code: {generate_verification_code()}")
```

## 變數注解語法（PEP 526）

### 型別提示

Python 3.6 支援了更整潔的變數注解語法：

```python
# Python 3.5+ 支援函式注解
def greet(name: str) -> str:
    return f"Hello, {name}"

# Python 3.6+ 支援變數注解
count: int = 0
name: str = "Alice"
scores: list[int] = []  # Python 3.9+ 支援 list[int]
```

### 在真實程式碼中的應用

```python
from typing import List, Dict, Optional

class Person:
    name: str
    age: int
    email: Optional[str]

    def __init__(self, name: str, age: int, email: Optional[str] = None):
        self.name = name
        self.age = age
        self.email = email

def process_data(data: List[Dict[str, int]]) -> int:
    return sum(item['value'] for item in data)

people: List[Person] = []
```

## 結論

Python 3.6 是一個重要的版本，它帶來的 f-string、字典優化和 secrets 模組深受開發者喜愛。這個版本為 Python 3 的全面勝利奠定了基礎，也為後續版本（Python 3.7+）的發展指明了方向。

如果你的專案還在使用 Python 2 或早期 Python 3 版本，升級到 Python 3.6 將帶來顯著的开发体验提升和效能改善。

---

## 延伸閱讀

- [Python 3.6 官方文件](https://www.google.com/search?q=Python+3.6+official+documentation+what%27s+new)
- [PEP 498 - f-string](https://www.google.com/search?q=PEP+498+f-string+Python)
- [PEP 526 - 變數注解](https://www.google.com/search?q=PEP+526+variable+annotations+Python)
- [Python 3.6 效能測試](https://www.google.com/search?q=Python+3.6+performance+benchmarks)

---

*本篇文章為「AI 程式人雜誌 2017 年 1 月號」焦點系列之一。*