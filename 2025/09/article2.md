# unittest.TestCase 入門

## 前言

`unittest.TestCase` 是 Python 標準測試框架的核心類別。雖然 pytest 在現代 Python 生態中更受歡迎，但 unittest 仍然是 Python 開發者應該掌握的基本技能——它零依賴、與標準函式庫深度整合，並且在許多大型專案（如 CPython 本身）中廣泛使用。

## 基本使用

撰寫 unittest 測試的第一步是繼承 `unittest.TestCase` 並定義 `test_` 開頭的方法：

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
        with self.assertRaises(TypeError):
            s.split(2)
```

執行測試：

```bash
python -m unittest test_module.py
python -m unittest test_module.TestStringMethods
python -m unittest test_module.TestStringMethods.test_upper
```

## 測試生命週期

`TestCase` 提供了四個層級的生命週期控制：

```python
class TestDatabase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """在類別中所有測試前執行一次"""
        cls.connection = create_database_connection()

    def setUp(self):
        """每個測試前執行"""
        self.connection.begin_transaction()
        self.user = create_test_user()

    def tearDown(self):
        """每個測試後執行"""
        self.connection.rollback()

    @classmethod
    def tearDownClass(cls):
        """在類別中所有測試後執行一次"""
        cls.connection.close()
```

## 常見的測試模式

### 測試例外

```python
def test_divide_by_zero(self):
    with self.assertRaises(ValueError) as cm:
        calculator.divide(10, 0)
    self.assertEqual(str(cm.exception), "Cannot divide by zero")
```

### 測試浮點數

```python
def test_float_precision(self):
    result = 1 / 3
    self.assertAlmostEqual(result, 0.33333, places=4)
    # 或使用 delta 參數
    self.assertAlmostEqual(result, 0.33333, delta=0.0001)
```

### 測試容器

```python
def test_list_contents(self):
    items = [1, 2, 3, 4, 5]
    self.assertIn(3, items)
    self.assertNotIn(6, items)
    self.assertGreater(len(items), 0)
    self.assertCountEqual(items, [5, 4, 3, 2, 1])  # 無視順序
```

### 使用子測試進行參數化

unittest 沒有內建的參數化裝飾器，但可以透過 `subTest` 實現類似功能：

```python
def test_addition(self):
    cases = [
        (1, 2, 3),
        (-1, 1, 0),
        (0, 0, 0),
        (100, -50, 50),
    ]
    for a, b, expected in cases:
        with self.subTest(a=a, b=b):
            self.assertEqual(add(a, b), expected)
```

## 測試發現與執行

```bash
# 發現並執行所有測試
python -m unittest discover

# 指定搜尋目錄和模式
python -m unittest discover -s tests/ -p "test_*.py"

# 詳細輸出
python -m unittest -v

# 在失敗時停止
python -m unittest -f
```

## 與 pytest 的整合

pytest 可以直接執行 unittest 的測試案例：

```bash
pytest test_module.py -v  # 完全相容
```

這讓團隊可以逐步從 unittest 遷移到 pytest，而不需要一次重寫所有測試。

## 小結

`unittest.TestCase` 是 Python 測試的基石。雖然它的語法比 pytest 更冗長，但零依賴、穩定的 API 和與標準函式庫的深度整合讓它成為許多專案的可靠選擇。掌握了 unittest，你不僅可以閱讀和維護 Python 標準函式庫和許多開源專案的測試，也為理解其他 xUnit 風格框架（如 JUnit、GUnit）打下了基礎。

## 延伸閱讀

- [unittest 官方教學](https://www.google.com/search?q=Python+unittest+tutorial)
- [unittest.TestCase API 參考](https://www.google.com/search?q=Python+unittest+TestCase+API)
- [unittest 實戰模式](https://www.google.com/search?q=Python+unittest+patterns)
