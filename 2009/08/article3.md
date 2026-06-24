# Python 3.0：十年間最大版本改變

## 前言

2008 年 12 月，Python 3.0 正式發布，這是 Python 語言自 2000 年以來最大的版本改變。Python 3.0 引入破壞性改變，推動語言現代化。

## 主要破壞性改變

### print 成為函數

```python
# Python 2
print "Hello"           # 字串
print "Hello", "World"  # 自動空格

# Python 3
print("Hello")
print("Hello", "World") # 參數間空格
```

### Unicode 預設

```python
# Python 2
s = "中文"  # ASCII
s = u"中文" # Unicode

# Python 3
s = "中文"  # 預設 Unicode
type(s)     # <class 'str'>
```

### 除法改變

```python
# Python 2
5 / 2    # 2（整數除法）
5.0 / 2  # 2.5

# Python 3
5 / 2    # 2.5（浮點除法）
5 // 2   # 2（整數除法）
```

### 例外處理

```python
# Python 2
raise ValueError, "message"

# Python 3
raise ValueError("message")
```

## 遷移工具

### 2to3 工具

```bash
# 自動轉換 Python 2 到 Python 3
$ 2to3 -w mycode.py

# 備份
$ 2to3 -w -n mycode.py
$ cp mycode.py.bak mycode.py.orig
```

### 相容性策略

```python
# future import
from __future__ import print_function
from __future__ import unicode_literals

# 條件執行
import sys
if sys.version_info[0] >= 3:
    # Python 3
    pass
else:
    # Python 2
    pass
```

## 新功能

### 函數注解

```python
def greet(name: str) -> str:
    return "Hello, " + name
```

### 僅關鍵字參數

```python
def func(a, *, b, c):
    pass

func(1, b=2, c=3)  # OK
func(1, 2, 3)      # Error
```

### 擴充疊代

```python
# Python 2
for i in range(10**10):  # 記憶體問題

# Python 3
for i in range(10**10):  # 惰性疊代
    pass
```

## 結語

Python 3.0 是艱難但必要的改變。雖然遷移成本高，但長期來看 Python 3 解決了長期累積的設計問題。

## 延伸閱讀

- [Python 3.0 發布公告](https://www.google.com/search?q=Python+3.0+release)
- [Python 3 遷移指南](https://www.google.com/search?q=Python+3+migration+guide)
- [2to3 工具](https://www.google.com/search?q=2to3+Python+converter)

---

*本篇文章為「AI 程式人雜誌 2009 年 8 月號」文章系列之一。*