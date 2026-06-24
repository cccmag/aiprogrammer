# unittest 標準庫的強大功能

## unittest 概述

unittest 是 Python 標準庫提供的測試框架，源自 JUnit 的設計理念，採用物件導向的測試組織方式。雖然語法較 pytest 冗長，但其完整的功能和無需額外依賴的特點使其在許多場景下仍是首選。

## 基本的測試類別

```python
import unittest

class TestMathOperations(unittest.TestCase):
    def test_addition(self):
        self.assertEqual(1 + 1, 2)

    def test_division(self):
        self.assertRaises(ZeroDivisionError, lambda: 1 / 0)
```

每個測試方法以 `test_` 開頭，繼承自 `unittest.TestCase`。

## SetUp 和 TearDown

生命週期鉤子用於管理測試資源：

```python
class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.db = create_test_database()
        self.db.connect()

    def tearDown(self):
        self.db.disconnect()
        self.db.destroy()
```

每個測試方法前後都會執行對應的鉤子，確保測試隔離。

## 測試資料與子測試

`subTest` 允許在單一測試方法中執行多個子測試：

```python
def test_matrix_operations(self):
    for i in range(3):
        with self.subTest(row=i):
            for j in range(3):
                result = self.matrix.get(i, j)
                self.assertEqual(result, expected[i][j])
```

即使某個子測試失敗，其他子測試仍會繼續執行。

## 斷言方法豐富

TestCase 提供了多樣化的斷言方法：

- `assertEqual(a, b)`：值相等
- `assertTrue(x)` / `assertFalse(x)`：布林值
- `assertIs(a, b)`：同一物件
- `assertIsNone(x)` / `assertIsNotNone(x)`
- `assertIn(a, coll)` / `assertNotIn(a, coll)`
- `assertIsInstance(a, type)` / `assertNotIsInstance(a, type)`
- `assertRaises(exc)`：異常捕獲
- `assertAlmostEqual(a, b)`：浮點數近似比較

## 測試組織與套件

```python
loader = unittest.TestLoader()
suite = loader.loadTestsFromTestCase(TestMathOperations)
suite.addTests(loader.loadTestsFromTestCase(TestStringOperations))

runner = unittest.TextTestRunner(verbosity=2)
runner.run(suite)
```

可以自由組合測試套件，控制執行順序。

## 測試發现機制

命令列 `python -m unittest` 會自動發現測試，支援指定模組、類別、甚至個別方法：

```bash
python -m unittest tests.test_module
python -m unittest tests.test_module.TestClass.test_method
```

## 與標準庫的整合

unittest 的設計與 Python 標準庫緊密整合，可以測試任何 Python 程式碼，無需額外依賴。這使其成為標準工具和快速原型測試的理想選擇。