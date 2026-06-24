# 參數化測試

## 前言

參數化測試（Parameterized Testing）是一種技術，讓你可以用不同的輸入資料執行同一個測試邏輯。這在測試「同一種行為應該對多組輸入產生正確結果」的場景中特別有用——例如測試一個加法函數對正數、負數、零、浮點數等不同組合的表現。

## 為什麼需要參數化測試？

考慮一個加法函數的測試。如果不使用參數化，你可能會這樣寫：

```python
def test_add_positive():
    assert add(1, 2) == 3

def test_add_negative():
    assert add(-1, -2) == -3

def test_add_zero():
    assert add(0, 5) == 5

def test_add_mixed():
    assert add(-1, 1) == 0
```

這四個測試幾乎一模一樣——差別只在於輸入參數和預期結果。程式碼重複導致維護成本增加：如果你想改變測試的結構（例如從 `assertEqual` 改為其他驗證方式），你需要修改四個地方。

參數化測試將資料與邏輯分離：

```python
@pytest.mark.parametrize("a,b,expected", [
    (1, 2, 3),
    (-1, -2, -3),
    (0, 5, 5),
    (-1, 1, 0),
])
def test_add(a, b, expected):
    assert add(a, b) == expected
```

## pytest 的參數化

### 基本語法

```python
@pytest.mark.parametrize("param1, param2", [
    (val1, val2),
    (val3, val4),
])
def test_something(param1, param2):
    ...
```

### 多組參數

```python
@pytest.mark.parametrize("text,expected", [
    ("hello", "HELLO"),
    ("world", "WORLD"),
    ("pytest", "PYTEST"),
])
def test_upper(text, expected):
    assert text.upper() == expected
```

### 測試 ID

為了讓測試輸出更可讀，可以為每組參數指定 ID：

```python
@pytest.mark.parametrize("text,expected", [
    ("hello", "HELLO"),
    pytest.param("world", "WORLD", id="world-uppercase"),
    pytest.param("", "", id="empty-string"),
])
def test_upper(text, expected):
    assert text.upper() == expected
```

執行結果：

```
test_module.py::test_upper[hello-HELLO] PASSED
test_module.py::test_upper[world-uppercase] PASSED
test_module.py::test_upper[empty-string] PASSED
```

### 多層參數化

可以堆疊多個 `@pytest.mark.parametrize` 裝飾器，產生笛卡兒積：

```python
@pytest.mark.parametrize("operation", ["add", "subtract"])
@pytest.mark.parametrize("a", [1, 10, 100])
@pytest.mark.parametrize("b", [2, 20, 200])
def test_calculator(a, b, operation):
    calc = Calculator()
    ...
```

## unittest 的參數化

unittest 沒有內建的參數化裝飾器，但有幾種替代方案：

### 使用 subTest

```python
class TestAdd(unittest.TestCase):
    def test_add(self):
        cases = [
            (1, 2, 3),
            (-1, 1, 0),
            (0, 0, 0),
        ]
        for a, b, expected in cases:
            with self.subTest(a=a, b=b):
                self.assertEqual(add(a, b), expected)
```

### 使用第三方套件

```python
from parameterized import parameterized

class TestAdd(unittest.TestCase):
    @parameterized.expand([
        (1, 2, 3),
        (-1, 1, 0),
        (0, 0, 0),
    ])
    def test_add(self, a, b, expected):
        self.assertEqual(add(a, b), expected)
```

## 參數化的實戰應用

### 測試邊界條件

```python
@pytest.mark.parametrize("value", [
    0,
    1,
    -1,
    2**31 - 1,     # 整數上限
    -2**31,        # 整數下限
    0.5,
    1e-10,         # 非常小的數
    1e10,          # 非常大的數
])
def test_square_root(value):
    result = sqrt(value)
    assert result >= 0
```

### 測試錯誤輸入

```python
@pytest.mark.parametrize("input_value,expected_error", [
    ("abc", ValueError),
    ("", ValueError),
    ("12.5.3", ValueError),
    (None, TypeError),
    ([1, 2, 3], TypeError),
])
def test_invalid_inputs(input_value, expected_error):
    with pytest.raises(expected_error):
        parse_number(input_value)
```

### 結合 Fixture

```python
@pytest.fixture
def calculator():
    return Calculator()

@pytest.mark.parametrize("a,b,expected", [
    (1, 2, 3),
    (10, 20, 30),
])
def test_add(calculator, a, b, expected):
    assert calculator.add(a, b) == expected
```

## 參數化的注意事項

**測試命名要清晰**：參數化測試在失敗時只顯示參數值，而不是「哪個測試案例」。使用有意義的測試 ID 或參數名稱來幫助定位失敗的案例。

**不要過度參數化**：如果每組參數需要不同的測試邏輯或不同的斷言，不應該強迫使用參數化。參數化適用於「邏輯相同、資料不同」的場景。

**關注測試的可讀性**：參數化測試的資料集可能很大。確保資料集的格式清晰易懂，必要時加入註解。

## 小結

參數化測試是減少測試程式碼重複、提高測試覆蓋率的有效技術。pytest 的 `@pytest.mark.parametrize` 裝飾器讓參數化變得簡單而優雅。記住：參數化適用於「相同邏輯、不同資料」的場景——如果測試邏輯不同，不要強迫參數化。

## 延伸閱讀

- [pytest 參數化官方文件](https://www.google.com/search?q=pytest+parametrize+documentation)
- [參數化測試模式](https://www.google.com/search?q=parameterized+testing+patterns)
- [unittest 參數化擴展](https://www.google.com/search?q=Python+unittest+parameterized+tests)
