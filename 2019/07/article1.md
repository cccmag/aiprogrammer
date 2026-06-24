# Python 3.8 發布：海象運算子與位置-only 參數

## 前言

Python 3.8 於 2019 年 10 月正式發布，這是 Python 3 系列的最新穩定版本。這個版本帶來了多項新特性，其中最受關注的是海象運算子（Walrus Operator）和位置-only 參數。本文將深入解析這些新特性及其應用場景。

## 海象運算子（Walrus Operator）

### 語法

海象運算子 `:=` 允許在表達式內部進行賦值，這是 Python 的一項重大語法創新：

```python
# 傳統方式：需要兩行代碼
result = some_calculation()
if result > 10:
    print(f"結果很大: {result}")

# 使用海象運算子：一行搞定
if (result := some_calculation()) > 10:
    print(f"結果很大: {result}")
```

### 詳細範例

**1. 列表推導式中的重複計算**

```python
# 傳統方式：計算兩次
data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
squared = [x**2 for x in data if x**2 > 50]  # x**2 計算了兩次
print(squared)  # [64, 81, 100]

# 海象運算子：只計算一次
squared = [y := x**2 for x in data if y > 50]  # y 只計算一次
print(squared)  # [64, 81, 100]
```

**2. 正則表達式匹配**

```python
import re

# 傳統方式
text = "用戶年齡: 25"
match = re.search(r'(\d+)', text)
if match:
    age = match.group(1)
    print(f"找到年齡: {age}")

# 海象運算子
if (match := re.search(r'(\d+)', text)):
    print(f"找到年齡: {match.group(1)}")
```

**3. 迴圈中的初始化**

```python
# 傳統方式
while True:
    line = get_next_line()
    if line is None:
        break
    process(line)

# 海象運算子
while (line := get_next_line()) is not None:
    process(line)
```

### 使用注意事項

```python
# 注意：賦值表達式需要括號
x := 5  # 語法錯誤
(x := 5)  # 正確

# 在 list comprehension 中使用需要注意作用域
[print(x := i) for i in range(3)]  # 印出 0, 1, 2，x 被賦值為 2
```

---

## 位置-only 參數（Positional-Only Parameters）

### 語法

Python 3.8 引入了使用 `/` 來標記位置-only 參數的功能：

```python
def func(positional_only, /, normal, *, keyword_only):
    print(f"位置-only: {positional_only}")
    print(f"普通參數: {normal}")
    print(f"關鍵字-only: {keyword_only}")

# 使用方式
func(1, 2, keyword_only=3)  # 正確
func(positional_only=1, normal=2, keyword_only=3)  # 錯誤！positional_only 必須作為位置參數
```

### 為什麼需要位置-only 參數？

**1. API 穩定性**

當函式內部實現改變時，參數名可能變化。使用位置-only 參數可以確保使用者的代碼不會因為參數名改變而失效。

```python
# 舊 API
def create_user(name, email):
    pass

# 新 API：name 變成 username，但舊的調用方式仍然有效
def create_user(username, /, email):
    # name 和 email 仍可作為位置參數調用
    pass
```

**2. 避免關鍵字衝突**

```python
# 例如 math.sin 函式使用位置-only
import math

# 這些都是有效的調用方式
math.sin(0)
math.sin(x=0)  # 因為 sin 實現了 __call__ 允許關鍵字
```

**3. 與內建函式保持一致**

```python
# len 是一個位置-only 函式
len([1, 2, 3])  # 正確
len(obj=[1, 2, 3])  # 錯誤

# 現在我們也可以定義這樣的函式
def my_len(obj, /):
    """類似 len 但更嚴格"""
    count = 0
    for _ in obj:
        count += 1
    return count
```

---

## 其他重要新特性

### 1. 改進的 typing 模組

```python
from typing import Final

# 最終變量（不可重新賦值）
PI: Final = 3.14159

# TypedDict 改進
from typing import TypedDict

class Point2D(TypedDict):
    x: int
    y: int
```

### 2. shared_memory 模組

```python
from multiprocessing import shared_memory
import numpy as np

# 創建共享記憶體陣列
arr = np.array([1, 2, 3, 4, 5])
shm = shared_memory.SharedMemory(name="my_array", create=True, size=arr.nbytes)
arr_shm = np.ndarray(arr.shape, dtype=arr.dtype, buffer=shm.buf)
arr_shm[:] = arr[:]

# 另一個進程可以通過名稱附加到同一塊共享記憶體
```

### 3. 效能改進

- 類屬性訪問優化
- `_pyio` 模組效能提升
- 更好的 pickle 效能

---

## 遷移指南

### 向後相容性

Python 3.8 完全向後相容於 Python 3.7。現有代碼無需修改即可運行。

### 推薦遷移步驟

1. **確認 Python 版本**
   ```bash
   python --version  # 應該顯示 Python 3.8.x
   ```

2. **更新依賴**
   ```bash
   pip install -U pip
   pip install -U requirements.txt
   ```

3. **測試新特性**
   ```python
   # 測試海象運算子
   if (n := len([1, 2, 3])) > 2:
       print(f"列表長度是 {n}")

   # 測試位置-only
   def greet(name, /, greeting="Hello"):
       return f"{greeting}, {name}!"
   ```

---

## 結語

Python 3.8 的新特性——特別是海象運算子和位置-only 參數——為 Python 開發者提供了更強大的工具。這些特性借鑒自其他語言（如 Lisp 的 named let、Fortran 的位置參數），同時保持了 Python 的簡潔和可讀性。

建議開發者：
1. 在新專案中積極使用這些新特性
2. 在重構舊代碼時考慮採用
3. 注意團隊成員對新語法的熟悉程度

---

**延伸閱讀**

- [Python 3.8 官方文檔](https://www.google.com/search?q=Python+3.8+official+documentation)
- [PEP 572 Walrus Operator](https://www.google.com/search?q=PEP+572+walrus+operator)
- [Python 3.8 new features](https://www.google.com/search?q=Python+3.8+new+features)