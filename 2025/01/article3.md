# 變數與資料型別深入

## 變數的本質

在 Python 中，變數更像是「標籤」而非「容器」。當我們寫 `x = 10` 時，實際上是在記憶體中建立了一個值為 10 的物件，然後將名稱 `x` 綁定到這個物件上。

### 賦值與引用

```python
# 多個變數指向同一個物件
a = [1, 2, 3]
b = a        # b 和 a 指向同一個列表
b.append(4)
print(a)     # [1, 2, 3, 4] — a 也被修改了！

# 淺拷貝 vs 深拷貝
import copy

original = [[1, 2], [3, 4]]
shallow = copy.copy(original)    # 淺拷貝
deep = copy.deepcopy(original)   # 深拷貝

shallow[0][0] = 99
print(original)  # [[99, 2], [3, 4]] — 被淺拷貝影響了
deep[0][0] = 99
print(original)  # [[99, 2], [3, 4]] — 深拷貝不受影響
```

## 可變與不可變型別

這是 Python 中最重要的概念之一。

### 不可變型別 (Immutable)

```python
# 整數
x = 5
y = x
x += 1
print(x, y)  # 6, 5 — x 指向新的物件，y 不變

# 字串
s = "hello"
t = s.upper()
print(s, t)  # hello, HELLO — 原字串不變

# 元組
t1 = (1, 2, [3, 4])
# t1[0] = 99  # TypeError: 元組不可變
t1[2].append(5)  # 但元素內的列表是可變的
print(t1)  # (1, 2, [3, 4, 5])
```

### 可變型別 (Mutable)

```python
# 列表
lst = [1, 2, 3]
lst.append(4)
lst[0] = 99
print(lst)  # [99, 2, 3, 4]

# 字典
d = {"a": 1}
d["b"] = 2
d.update({"c": 3})
print(d)  # {'a': 1, 'b': 2, 'c': 3}

# 集合
s = {1, 2, 3}
s.add(4)
s.remove(1)
print(s)  # {2, 3, 4}
```

## 型別檢查與轉換

### 檢查型別

```python
x = 42
print(type(x))           # <class 'int'>
print(isinstance(x, int)) # True
print(isinstance(x, (int, float)))  # True
```

### 鴨子型別 (Duck Typing)

「如果它走起來像鴨子、叫起來像鴨子，那它就是鴨子」：

```python
def process_data(data):
    # 不檢查型別，只檢查行為
    for item in data:  # 只要有 __iter__ 方法即可
        print(item)

process_data([1, 2, 3])     # 列表
process_data("hello")        # 字串
process_data({1, 2, 3})      # 集合
```

## 型別提示 (Type Hints)

Python 3.5+ 支援選擇性的型別註釋：

```python
from typing import List, Dict, Optional, Union

def greet(name: str) -> str:
    return f"你好, {name}"

def add(a: int, b: int) -> int:
    return a + b

def process(items: List[int]) -> Dict[str, float]:
    return {
        "mean": sum(items) / len(items),
        "max": max(items)
    }

# Optional 表示可以是 int 或 None
def find_user(user_id: Optional[int] = None) -> str:
    if user_id is None:
        return "預設使用者"
    return f"使用者 {user_id}"

# Union 表示可以是多種型別之一
def double(value: Union[int, float]) -> Union[int, float]:
    return value * 2
```

## is 與 == 的區別

```python
a = [1, 2, 3]
b = [1, 2, 3]
c = a

print(a == b)  # True — 值相等
print(a is b)  # False — 不同物件
print(a is c)  # True — 同一個物件

# None 的比較應該用 is
x = None
print(x is None)     # True (正確)
print(x == None)     # True (不建議)
```

## 特殊型別：None

`None` 是 Python 中表示「沒有值」的單例物件：

```python
def get_data():
    # 可能回傳 None 表示沒有資料
    pass

result = get_data()
if result is None:
    print("沒有資料")
else:
    print(result)
```

## 記憶體管理

Python 使用垃圾回收機制自動管理記憶體：

```python
import sys

x = 42
print(sys.getrefcount(x))  # 查看物件被引用的次數

# del 減少引用計數
y = x
del x  # 減少一次引用
# 直到引用計數歸零時，記憶體才會被回收
```

## 小結

深入理解變數與資料型別是成為 Python 進階開發者的關鍵。特別是「可變 vs 不可變」和「引用 vs 值」的概念，對於正確預測程式行為至關重要。型別提示雖然不是強制性的，但在大型專案中能大大提升程式碼的可維護性。

---

**延伸閱讀**

- [Python 官方文件 — 資料模型](https://www.google.com/search?q=Python+data+model+documentation)
- [Python 型別提示指南](https://www.google.com/search?q=Python+type+hints+guide)
