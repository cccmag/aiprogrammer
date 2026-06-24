# Python 3.6 正式發布：性能與生產力雙重提升

## 前言

2016 年 12 月 23 日，Python 3.6 正式發布，代號「金色的薩克斯風」。這是 Python 3 系列的第八個版本，帶來了多項重要改進，讓 Python 在效能和開發者體驗上都邁向了新的台階。

## f-string：革命性的字串格式化

Python 3.6 最重要的新特性是 f-string（格式化字串字面量）：

```python
# 舊方式
name = "Alice"
age = 30
print("Name: %s, Age: %d" % (name, age))
print("Name: {}, Age: {}".format(name, age))

# f-string（Python 3.6+）
print(f"Name: {name}, Age: {age}")

# 表達式支援
a, b = 10, 20
print(f"{a} + {b} = {a + b}")  # 10 + 20 = 30

# 格式化選項
import math
print(f"Pi: {math.pi:.4f}")  # Pi: 3.1416
```

f-string 不僅語法簡潔，效能也比 `%format` 和 `.format()` 更高。

## 字典優化：更快的速度和更小的記憶體

Python 3.6 採用了「compact dict」實現，帶來了顯著的效能提升：

- 記憶體使用減少約 20-30%
- 迭代速度提升約 3-5%
- 保持插入順序成為語言特性（之前是實現細節）

```python
# Python 3.6+ 的字典現在「保序」
d = {}
d['a'] = 1
d['b'] = 2
d['c'] = 3
print(list(d.keys()))  # ['a', 'b', 'c'] - 確定有序！
```

這個改變影響深遠，許多原本需要 `collections.OrderedDict` 的場景現在可以直接使用普通字典。

## asyncio 改進

Python 3.6 增強了 asyncio 模組：

```python
import asyncio

async def fetch_data():
    await asyncio.sleep(1)
    return {"data": "result"}

async def main():
    result = await fetch_data()
    print(f"Got: {result}")

asyncio.run(main())  # Python 3.7+，3.6 需要用其他方式
```

asyncio 在 3.6 版本中更穩定，記憶體使用也更低。

## secrets 模組：密碼學安全的亂數

Python 3.6 新增了 `secrets` 模組，終於有了標準的密碼學安全亂數生成方法：

```python
import secrets

# 生成安全的令牌
token = secrets.token_hex(32)  # 64 字元的十六進制字串
print(f"Token: {token}")

# URL 安全的令牌
url_token = secrets.token_urlsafe(32)
print(f"URL Token: {url_token}")

# 安全的密碼
import string
alphabet = string.ascii_letters + string.digits + string.punctuation
password = ''.join(secrets.choice(alphabet) for _ in range(16))
print(f"Password: {password}")
```

## 變數注解（PEP 526）

Python 3.6 支援更整潔的變數類型標注：

```python
from typing import List, Dict

# Python 3.5
count = 0  # type: int

# Python 3.6+
count: int = 0
names: List[str] = []
scores: Dict[str, int] = {}
```

這讓靜態類型檢查工具（如 mypy）能提供更好的支援。

## 效能提升

Python 3.6 在多個方面帶來了效能提升：

| 改進項目 | 效能提升 |
|---------|---------|
| 字典實現 | ~20-30% 更快，更少記憶體 |
| f-string | 比 %format 快 30% |
| 解釋器啟動 | ~10% 更快 |
| 模組導入 | 改善 |

## 升級建議

### 應該升級的情況
- 新專案從一開始就使用 Python 3.6
- 需要 f-string 的簡潔語法
- 記憶體或效能敏感的应用
- 已經使用 Python 3.5 的專案

### 可以稍等的情況
- 依賴的庫還不支持 Python 3.6
- 需要支援 Python 2 的專案
- 等待第一個 bugfix 版本（3.6.1）

## 結語

Python 3.6 是一個令人振奮的版本。f-string、字典優化、secrets 模組和類型注解改進，每一項都直擊開發者的痛點。如果你還在使用 Python 2 或早期 Python 3 版本，現在是時候認真考慮升級了。

---

## 延伸閱讀

- [Python 3.6 官方發布說明](https://www.google.com/search?q=Python+3.6+release+announcement+what%27s+new)
- [PEP 498 - f-string](https://www.google.com/search?q=PEP+498+f-string+Python+3.6)
- [Python 3.6效能測試結果](https://www.google.com/search?q=Python+3.6+performance+benchmark)
- [Python 3.6 新特性詳解](https://www.google.com/search?q=Python+3.6+new+features+tutorial)

---

*本篇文章為「AI 程式人雜誌 2017 年 1 月號」文章系列之一。*