# 主題六：例外處理與測試

## 例外處理基礎

### try/except

```python
try:
    result = 10 / 0
except ZeroDivisionError:
    print("不能除以零")

# 或者
try:
    result = 10 / 0
except Exception as e:
    print(f"發生錯誤：{e}")
```

### 多個 except

```python
try:
    value = int(input("輸入數字："))
    result = 10 / value
except ValueError:
    print("請輸入有效的數字")
except ZeroDivisionError:
    print("不能除以零")
except Exception as e:
    print(f"其他錯誤：{e}")
```

### else 子句

```python
try:
    value = int(input("輸入數字："))
except ValueError:
    print("無效輸入")
else:
    print(f"你輸入的是 {value}")  # 只有在沒有例外時執行
```

### finally 子句

```python
try:
    file = open("data.txt", "r")
    content = file.read()
except IOError as e:
    print(f"檔案錯誤：{e}")
finally:
    print("清理資源")
    # file.close()  # 最好使用 with 語句
```

## 常見例外類型

### 內建例外層次

```
BaseException
├── SystemExit
├── KeyboardInterrupt
└── Exception
    ├── StopIteration
    ├── ArithmeticError
    │   ├── FloatingPointError
    │   ├── OverflowError
    │   └── ZeroDivisionError
    ├── LookupError
    │   ├── IndexError
    │   └── KeyError
    ├── ImportError
    │   └── ModuleNotFoundError
    ├── NameError
    ├── TypeError
    ├── ValueError
    ├── IOError
    └── RuntimeError
```

### 常見例外範例

```python
# IndexError：索引超出範圍
my_list = [1, 2, 3]
print(my_list[5])  # IndexError

# KeyError：鍵不存在
my_dict = {"a": 1}
print(my_dict["b"])  # KeyError

# TypeError：類型錯誤
print("a" + 1)  # TypeError

# ValueError：值錯誤
print(int("abc"))  # ValueError

# AttributeError：屬性錯誤
x = 5
print(x.upper())  # AttributeError
```

## 拋出例外

### raise 語句

```python
def divide(a, b):
    if b == 0:
        raise ValueError("除數不能為零")
    return a / b

try:
    divide(10, 0)
except ValueError as e:
    print(e)  # 除數不能為零
```

### 自訂例外

```python
class ValidationError(Exception):
    """驗證錯誤"""
    pass

class PositiveNumberError(ValidationError):
    """必須是正數"""
    def __init__(self, value):
        self.value = value
        super().__init__(f"數值必須是正數，得到了 {value}")

def process_value(value):
    if value < 0:
        raise PositiveNumberError(value)
    return value * 2

try:
    process_value(-5)
except PositiveNumberError as e:
    print(e)  # 數值必須是正數，得到了 -5
```

## 斷言

### assert

```python
def withdraw(balance, amount):
    assert amount > 0, "提款金額必須為正數"
    assert amount <= balance, "餘額不足"
    return balance - amount

print(withdraw(100, 30))  # 70
print(withdraw(100, -10))  # AssertionError
```

## 測試基礎

### unittest 模組

```python
import unittest

class TestMathOperations(unittest.TestCase):
    def setUp(self):
        """每個測試方法執行前的準備"""
        self.data = [1, 2, 3, 4, 5]

    def test_add(self):
        self.assertEqual(1 + 1, 2)

    def test_sum(self):
        result = sum(self.data)
        self.assertEqual(result, 15)

    def test_average(self):
        result = sum(self.data) / len(self.data)
        self.assertAlmostEqual(result, 3.0)

    def test_max(self):
        result = max(self.data)
        self.assertEqual(result, 5)

    def test_raises(self):
        with self.assertRaises(ZeroDivisionError):
            1 / 0

if __name__ == "__main__":
    unittest.main()
```

### 常用斷言方法

```python
# 相等
self.assertEqual(a, b)
self.assertNotEqual(a, b)

# 布林
self.assertTrue(x)
self.assertFalse(x)
self.assertIsNone(x)
self.assertIsNotNone(x)

# 包含
self.assertIn(item, container)
self.assertNotIn(item, container)

# 例外
self.assertRaises(ExceptionType)
with self.assertRaises(ExceptionType):
    code_that_raises()

# 浮點數比較
self.assertAlmostEqual(a, b, places=7)
```

### 測試案例

```python
import unittest

class TestStringMethods(unittest.TestCase):
    def test_upper(self):
        self.assertEqual("hello".upper(), "HELLO")

    def test_isupper(self):
        self.assertTrue("HELLO".isupper())
        self.assertFalse("Hello".isupper())

    def test_split(self):
        s = "hello world"
        self.assertEqual(s.split(), ["hello", "world"])

    def test_strip(self):
        self.assertEqual("  hello  ".strip(), "hello")

    def test_replace(self):
        self.assertEqual("hello".replace("l", "L"), "heLLo")

if __name__ == "__main__":
    unittest.main()
```

## doctest

```python
def add(a, b):
    """相加

    >>> add(1, 2)
    3
    >>> add(-1, 1)
    0
    >>> add(0, 0)
    0
    """
    return a + b

if __name__ == "__main__":
    import doctest
    doctest.testmod()
```

## 使用 pytest

```bash
pip install pytest
```

```python
# test_sample.py
def add(a, b):
    return a + b

def test_add():
    assert add(1, 2) == 3
    assert add(-1, 1) == 0
    assert add(0, 0) == 0

def test_add_strings():
    assert add("a", "b") == "ab"
```

```bash
pytest test_sample.py
```

## 測試驅動開發（TDD）

```python
# TDD 範例：簡單的 Stack 類別

# 步驟 1：撰寫測試
import unittest

class TestStack(unittest.TestCase):
    def setUp(self):
        self.stack = Stack()

    def test_push(self):
        self.stack.push(1)
        self.assertFalse(self.stack.is_empty())

    def test_pop(self):
        self.stack.push(1)
        self.stack.push(2)
        self.assertEqual(self.stack.pop(), 2)
        self.assertEqual(self.stack.pop(), 1)

    def test_pop_empty(self):
        with self.assertRaises(IndexError):
            self.stack.pop()

    def test_is_empty(self):
        self.assertTrue(self.stack.is_empty())
        self.stack.push(1)
        self.assertFalse(self.stack.is_empty())

# 步驟 2：實作（讓測試通過）
class Stack:
    def __init__(self):
        self._items = []

    def push(self, item):
        self._items.append(item)

    def pop(self):
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self._items.pop()

    def is_empty(self):
        return len(self._items) == 0

if __name__ == "__main__":
    unittest.main()
```

## 結論

例外處理和測試是編寫穩固 Python 程式的重要組成部分。學會合理使用 try/except，並建立完善的測試機制，可以大幅提升程式碼品質。