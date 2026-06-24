# 主題四：函式與模組

## 函式定義

### 基本語法

```python
def greet(name):
    """問候函式"""
    return f"你好，{name}！"

result = greet("張小明")
print(result)  # 你好，張小明！
```

### 參數類型

#### 位置參數

```python
def power(base, exponent):
    return base ** exponent

print(power(2, 3))  # 8
```

#### 關鍵字參數

```python
def power(base, exponent):
    return base ** exponent

print(power(base=2, exponent=3))  # 8
print(power(exponent=3, base=2))  # 8（順序無所謂）
```

#### 預設參數值

```python
def greet(name, greeting="你好"):
    return f"{greeting}，{name}！"

print(greet("張小明"))           # 你好，張小明！
print(greet("李小華", "早安"))    # 早安，李小華！
```

#### 可變參數

```python
# *args：可變位置參數
def sum_all(*numbers):
    total = 0
    for n in numbers:
        total += n
    return total

print(sum_all(1, 2, 3))       # 6
print(sum_all(1, 2, 3, 4, 5)) # 15

# **kwargs：可變關鍵字參數
def print_info(**info):
    for key, value in info.items():
        print(f"{key}: {value}")

print_info(name="張小明", age=28, city="台北")
```

#### 組合使用

```python
def func(required, *args, default="預設值", **kwargs):
    print(f"必要參數: {required}")
    print(f"額外位置參數: {args}")
    print(f"預設參數: {default}")
    print(f"額外關鍵字參數: {kwargs}")

func("必填", 1, 2, default="修改", extra="其他")
```

## 特殊函式特性

### Lambda 表達式

```python
# 匿名函式
square = lambda x: x ** 2
print(square(5))  # 25

# 與內建函式搭配
numbers = [1, 2, 3, 4, 5]
filtered = list(filter(lambda x: x % 2 == 0, numbers))
print(filtered)  # [2, 4]

mapped = list(map(lambda x: x ** 2, numbers))
print(mapped)  # [1, 4, 9, 16, 25]

from functools import reduce
total = reduce(lambda x, y: x + y, numbers)
print(total)  # 15
```

### 巢狀函式與閉包

```python
def outer(x):
    def inner(y):
        return x + y
    return inner

add_5 = outer(5)
print(add_5(10))  # 15
print(add_5(3))   # 8
```

### 裝飾器

```python
def log_calls(func):
    def wrapper(*args, **kwargs):
        print(f"呼叫 {func.__name__}")
        result = func(*args, **kwargs)
        print(f"{func.__name__} 完成")
        return result
    return wrapper

@log_calls
def add(a, b):
    return a + b

print(add(1, 2))
# 呼叫 add
# add 完成
# 3
```

## 模組基礎

### 創建模組

```python
# mymodule.py
"""我的模組"""

def add(a, b):
    return a + b

class Calculator:
    def __init__(self):
        self.result = 0

    def add(self, n):
        self.result += n
        return self.result

__version__ = "1.0.0"
```

### 匯入模組

```python
# 匯入整個模組
import mymodule
result = mymodule.add(1, 2)
calc = mymodule.Calculator()

# 匯入特定項目
from mymodule import add, Calculator
result = add(1, 2)

# 匯入並指定別名
from mymodule import Calculator as Calc
calc = Calc()

# 匯入所有（不建議）
from mymodule import *
```

### 模組搜尋路徑

```python
import sys
print(sys.path)

# 新增搜尋路徑
sys.path.append("/path/to/my/modules")
```

## 標準庫常用模組

### os：作業系統介面

```python
import os

os.getcwd()          # 取得當前目錄
os.listdir(".")      # 列出目錄內容
os.mkdir("new_dir")  # 建立目錄
os.remove("file.txt") # 刪除檔案
os.path.exists("file.txt")  # 檢查是否存在
os.path.join("dir", "file.txt")  # 路徑連接
```

### sys：系統相關

```python
import sys

sys.argv           # 命令列參數列表
sys.exit(0)        # 退出程式
sys.version        # Python 版本
sys.path           # 模組搜尋路徑
```

### json：JSON 處理

```python
import json

data = {"name": "張小明", "age": 28}
json_str = json.dumps(data)   # 轉為 JSON 字串
parsed = json.loads(json_str)  # 解析 JSON

# 檔案操作
with open("data.json", "w") as f:
    json.dump(data, f, indent=2)

with open("data.json", "r") as f:
    loaded = json.load(f)
```

### datetime：日期時間

```python
from datetime import datetime, date, timedelta

now = datetime.now()
print(now)  # 2025-01-01 12:30:45.123456

today = date.today()
print(today)  # 2025-01-01

future = now + timedelta(days=7)
print(future)  # 7 天後

print(now.strftime("%Y-%m-%d %H:%M:%S"))
```

### random：隨機數

```python
import random

random.random()          # 0.0 ~ 1.0 之間的浮點數
random.randint(1, 100)   # 1 ~ 100 之間的整數
random.choice(["a", "b", "c"])  # 隨機選擇
random.shuffle([1, 2, 3, 4, 5])  # 洗牌
```

### collections：容器資料型態

```python
from collections import namedtuple, defaultdict, Counter

# 命名元組
Point = namedtuple('Point', ['x', 'y'])
p = Point(10, 20)
print(p.x, p.y)

# 預設字典
d = defaultdict(int)
d["a"] += 1
print(d)  # {'a': 1}

# 計數器
c = Counter("abracadabra")
print(c)  # Counter({'a': 5, 'b': 2, 'r': 2, 'c': 1, 'd': 1})
```

## 套件（Package）

### 結構

```
mypackage/
    __init__.py
    module1.py
    module2.py
    subpackage/
        __init__.py
        module3.py
```

### __init__.py

```python
# __init__.py
# 可以用來控制匯入行為
from .module1 import some_function
from .subpackage import something

__all__ = ["some_function", "something"]
```

### 相對匯入

```python
# 在 mypackage/module1.py 中
from . import module2        # 匯入同層級模組
from .subpackage import module3  # 匯入子套件
from .. import parent_module  # 從上層套件匯入
```

## 作用域與命名空間

```python
# LEGB 規則：Local -> Enclosing -> Global -> Built-in

x = "global"

def outer():
    x = "enclosing"

    def inner():
        x = "local"
        print(x)  # local

    inner()
    print(x)  # enclosing

outer()
print(x)  # global
```

## 結論

函式和模組是組織 Python 程式碼的基本單位。掌握這些概念，可以寫出結構清晰、可維護性高的程式碼。