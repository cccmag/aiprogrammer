# Python 3.8 新特性搶先看

## 前言

Python 3.8 將於 2019 年 10 月發布，本篇文章搶先介紹即將到來的新特性。

## Walrus 運算子（海象運算子）

```python
# 舊寫法
n = 10
if n > 5:
    print(f"n is {n}")

# 新寫法（Walrus 運算子）
if (n := 10) > 5:
    print(f"n is {n}")

# 特別適合在迴圈中
while (line := file.readline()):
    process(line)
```

## 位置-only 參數

```python
def f(pos_only, /, normal, *, kw_only):
    print(pos_only, normal, kw_only)

f(1, 2, kw_only=3)  # OK
f(1, normal=2, kw_only=3)  # OK
# f(pos_only=1, 2, kw_only=3)  # 錯誤
```

## 改進的 typing

```python
from typing import TypedDict

class Point(TypedDict):
    x: int
    y: int
```

## f-string 支援 `=`

```python
x = 10
# 舊寫法
print(f"x = {x}")

# 新寫法
print(f"{x = }")  # x = 10
```

## 延伸閱讀

- [Python 3.8 新特性](https://www.google.com/search?q=Python+3.8+new+features)