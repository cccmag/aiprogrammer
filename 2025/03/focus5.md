# 特殊方法與運算子重載

## 什麼是特殊方法？

Python 的特殊方法（也稱為魔術方法）是以雙底線開頭和結尾的方法，例如 `__init__`、`__str__`、`__add__`。它們讓自訂類別可以與 Python 的內建操作無縫整合。

```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):          # 給使用者看的字串
        return f"({self.x}, {self.y})"

    def __repr__(self):         # 給開發者看的字串
        return f"Point({self.x}, {self.y})"

p = Point(3, 4)
print(str(p))    # (3, 4)
print(repr(p))   # Point(3, 4)
```

## 運算子重載

運算子重載讓自訂類別可以使用 `+`、`-`、`*` 等運算子：

```python
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"Vector({self.x}, {self.y})"

v1 = Vector(1, 2)
v2 = Vector(3, 4)
print(v1 + v2)         # Vector(4, 6)
print(v1 - v2)         # Vector(-2, -2)
print(v1 * 3)          # Vector(3, 6)
print(v1 == Vector(1, 2))  # True
```

## 常用魔術方法一覽

### 建立與銷毀
| 方法 | 用途 |
|------|------|
| `__init__(self, ...)` | 建構子 |
| `__del__(self)` | 解構子 |

### 字串表示
| 方法 | 用途 |
|------|------|
| `__str__(self)` | `print()` 與 `str()` 呼叫 |
| `__repr__(self)` | `repr()` 與除錯資訊 |

### 比較運算子
```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __eq__(self, other):
        return self.name == other.name and self.age == other.age

    def __lt__(self, other):
        return self.age < other.age

    def __hash__(self):
        return hash((self.name, self.age))
```

### 容器方法

```python
class Playlist:
    def __init__(self):
        self._songs = []

    def __getitem__(self, index):
        return self._songs[index]

    def __setitem__(self, index, song):
        self._songs[index] = song

    def __len__(self):
        return len(self._songs)

    def __contains__(self, song):
        return song in self._songs

    def __iter__(self):
        return iter(self._songs)

    def add(self, song):
        self._songs.append(song)

pl = Playlist()
pl.add("Bohemian Rhapsody")
pl.add("Stairway to Heaven")
print(len(pl))           # 2
print(pl[0])             # Bohemian Rhapsody
print("Hey Jude" in pl)  # False
for s in pl:
    print(s)
```

### 可呼叫物件

```python
class Multiplier:
    def __init__(self, factor):
        self.factor = factor

    def __call__(self, x):
        return x * self.factor

double = Multiplier(2)
triple = Multiplier(3)

print(double(5))   # 10
print(triple(5))   # 15
```

### 上下文管理器

```python
class File:
    def __init__(self, filename):
        self.filename = filename

    def __enter__(self):
        print(f"開啟 {self.filename}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"關閉 {self.filename}")
        if exc_type:
            print(f"發生錯誤: {exc_val}")
        return True

with File("test.txt") as f:
    print("正在讀取...")
# 開啟 test.txt
# 正在讀取...
# 關閉 test.txt
```

## 小結

特殊方法是 Python OOP 的精華所在。它們讓自訂類別可以融入 Python 語言生態，使用起來就像內建類型一樣自然。理解並善用魔術方法，是成為 Python 進階開發者的必經之路。

## 延伸閱讀

- [Python 資料模型官方文件](https://www.google.com/search?q=Python+data+model)
- [Python 魔術方法指南](https://www.google.com/search?q=Python+magic+methods+guide)
