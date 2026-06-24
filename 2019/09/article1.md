# Python 3.8 正式發布：新特性總覽

## 前言

Python 3.8 於 2019 年 10 月正式發布，成為 Python 3 系列的最新穩定版本。本月社區熱烈討論其新特性，特別是海象運算子和位置-only 參數。

## 海象運算子

### 語法新特性

```python
# 可以在表達式中賦值
if (n := len([1, 2, 3])) > 2:
    print(f"n 是 {n}")

# 列表推導式中避免重複計算
data = [1, 2, 3, 4, 5]
squared = [y := x**2 for x in data if y > 10]  # y 只計算一次
```

---

## 位置-only 參數

### 增強的函式定義

```python
def func(positional_only, /, normal, *, keyword_only):
    pass

func(1, 2, keyword_only=3)  # 正確
func(positional_only=1, normal=2, keyword_only=3)  # 錯誤
```

---

## 其他新特性

### typing 改進

```python
from typing import Final

PI: Final = 3.14159  # 最終變量，不可修改
```

---

## 結語

Python 3.8 為 Python 開發者帶來了更現代的語法特性，提升了代碼的可讀性和簡潔性。

---

**延伸閱讀**

- [Python 3.8 Release](https://www.google.com/search?q=Python+3.8+release+2019)
- [Python+3.8+new+features](https://www.google.com/search?q=Python+3.8+new+features)