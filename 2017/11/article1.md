# Python 3.6 發布：async/await 原生支援

## 前言

Python 3.6 於 2016 年 12 月發布，在 2017 年獲得廣泛採用。這個版本帶來了多項重要的新特性，使得 Python 成為更好的非同步程式設計語言。

## f-strings：更簡潔的字串格式化

```python
# f-strings 讓程式碼更簡潔
name = "Alice"
age = 30

# 之前
print("Name: {}, Age: {}".format(name, age))
print("Name: %(name)s, Age: %(age)d" % locals())

# Python 3.6+
print(f"Name: {name}, Age: {age}")
print(f"In 5 years, age will be: {age + 5}")
```

## 數字字面值改進

```python
# 數字分隔符
million = 1_000_000
price = 1_234_567.89

# 二進位、八進位、十六進位
binary = 0b_1010_1010
hexa = 0x_DEAD_BEEF
```

## 型別提示增強

```python
from typing import List, Dict, Optional

def process_items(items: List[int]) -> Dict[str, int]:
    return {str(i): i for i in items}

class Config:
    def __init__(self, data: Optional[Dict[str, List[int]]] = None) -> None:
        self.data = data or {}
```

## asyncio 改進

```python
import asyncio

async def main():
    # Python 3.7 會有更好的 asyncio
    await asyncio.gather(
        process_one(),
        process_two(),
        process_three()
    )
```

## 對 AI 生態的影響

Python 3.6 的新特性對深度學習框架有所幫助：

```python
# 更好的型別提示有利於大型專案
import torch

# 模型定義更清晰
def forward(self, x: torch.Tensor) -> torch.Tensor:
    return self.net(x)
```

---

**延伸閱讀**

- [Python 3.6 Release Notes](https://www.google.com/search?q=Python+3.6+release+notes)
- [PEP 498: f-strings](https://www.google.com/search?q=PEP+498+f-strings)