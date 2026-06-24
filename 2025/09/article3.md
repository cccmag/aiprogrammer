# 斷言方法大全

## 前言

斷言是測試的核心。每個測試案例的核心都是一個或多個斷言——它們檢查程式的實際輸出是否符合預期。Python 的 `unittest` 提供了豐富的斷言方法，覆蓋了從基本等值比較到複雜資料結構驗證的各種場景。

## unittest 斷言方法

### 等值斷言

```python
self.assertEqual(a, b)      # a == b
self.assertNotEqual(a, b)   # a != b
```

`assertEqual` 支援大多數內建型別，包括字串、列表、字典、集合。對於自訂物件，可以實作 `__eq__` 方法。

### 布林值斷言

```python
self.assertTrue(x)          # bool(x) is True
self.assertFalse(x)         # bool(x) is False
```

### 識別斷言

```python
self.assertIs(a, b)         # a is b
self.assertIsNot(a, b)      # a is not b
self.assertIsNone(x)        # x is None
self.assertIsNotNone(x)     # x is not None
```

### 成員斷言

```python
self.assertIn(a, b)         # a in b
self.assertNotIn(a, b)      # a not in b
```

### 型別斷言

```python
self.assertIsInstance(a, cls)     # isinstance(a, cls)
self.assertNotIsInstance(a, cls)  # not isinstance(a, cls)
```

### 比較斷言

```python
self.assertLess(a, b)       # a < b
self.assertLessEqual(a, b)  # a <= b
self.assertGreater(a, b)    # a > b
self.assertGreaterEqual(a, b) # a >= b
```

### 浮點數斷言

```python
self.assertAlmostEqual(a, b)               # round(a-b, 7) == 0
self.assertAlmostEqual(a, b, places=4)     # 指定小數位數
self.assertAlmostEqual(a, b, delta=0.001)  # 指定差值上限
self.assertNotAlmostEqual(a, b)
```

### 例外斷言

```python
with self.assertRaises(ValueError):
    int("abc")

with self.assertRaises(ValueError) as cm:
    int("abc")
self.assertEqual(str(cm.exception), "invalid literal for int()")

# 檢查例外訊息
with self.assertRaisesRegex(ValueError, "invalid"):
    int("abc")
```

### 日誌斷言

```python
with self.assertLogs("myapp", level="WARNING") as log:
    myapp.do_something()
self.assertIn("warning message", log.output[0])
```

### 警告斷言

```python
with self.assertWarns(DeprecationWarning):
    legacy_function()

with self.assertWarnsRegex(DeprecationWarning, "deprecated"):
    legacy_function()
```

## 容器專用斷言

```python
# 列表/字串：無視順序比較元素
self.assertCountEqual([1, 2, 3], [3, 2, 1])

# 正則表達式匹配
self.assertRegex("hello-123", r"\w+-\d+")
self.assertNotRegex("hello!", r"\d+")

# 字串前綴/後綴（透過 assertTrue + 字串方法）
self.assertTrue("hello world".startswith("hello"))
self.assertTrue("hello world".endswith("world"))
```

## pytest 的斷言方式

pytest 使用 Python 原生的 `assert` 語句，透過斷言內省機制提供詳細的錯誤訊息：

```python
def test_addition():
    result = 1 + 2
    assert result == 3
    assert result > 0
    assert isinstance(result, int)
```

pytest 的斷言內省會自動顯示表達式的各部分值：

```
E   assert (1 + 2) == 4
E    +  where 1 + 2 = 3
```

### pytest.approx：浮點數比較

```python
from pytest import approx

def test_float():
    assert 0.1 + 0.2 == approx(0.3)
    assert 1/3 == approx(0.33333, rel=0.01)  # 相對誤差
    assert 1/3 == approx(0.33333, abs=0.001)  # 絕對誤差
```

### pytest.raises：例外測試

```python
import pytest

def test_divide_by_zero():
    with pytest.raises(ValueError, match="Cannot divide"):
        calculator.divide(1, 0)
```

## 自訂斷言訊息

好的斷言訊息可以讓測試失敗時更快定位問題：

```python
# unittest
self.assertEqual(
    actual, expected,
    f"計算結果不正確: 預期 {expected}, 實際 {actual}"
)

# pytest（自動提供詳細訊息，通常不需要自訂）
assert actual == expected, f"預期 {expected}, 實際 {actual}"
```

## 小結

斷言是測試的語言。掌握 unittest 和 pytest 的斷言方法，讓你可以用精確的方式表達「程式碼應該做什麼」。選擇斷言方法時，越具體越好——使用 `assertEqual` 而不是 `assertTrue(a == b)`，因為前者在測試失敗時提供更詳細的資訊。

## 延伸閱讀

- [unittest 斷言方法完整列表](https://www.google.com/search?q=Python+unittest+assert+methods+list)
- [pytest 斷言內省機制](https://www.google.com/search?q=pytest+assertion+introspection)
- [自訂斷言方法](https://www.google.com/search?q=custom+assert+methods+Python+unittest)
