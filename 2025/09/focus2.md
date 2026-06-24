# 單元測試基礎 unittest

## Python 內建測試框架的完整指南

### 前言

`unittest` 是 Python 標準函式庫中的測試框架，靈感來自 Java 的 JUnit 4。它提供了測試自動化所需的全部基礎設施：測試案例的組織、測試執行、斷言方法和測試報告。雖然 pytest 在現代 Python 生態中更受歡迎，但 unittest 作為標準庫的一部分，零依賴的優勢讓它在某些場景下仍然是首選。

### TestCase 類別

`unittest.TestCase` 是 unittest 的核心類別。每個測試案例都繼承自 `TestCase`，測試方法以 `test_` 開頭：

```python
import unittest

class TestMath(unittest.TestCase):
    def test_addition(self):
        self.assertEqual(1 + 1, 2)

    def test_subtraction(self):
        self.assertEqual(3 - 1, 2)
```

執行測試的方式：

```bash
python3 -m unittest test_module.py
python3 -m unittest test_module.TestMath
python3 -m unittest test_module.TestMath.test_addition
```

### setUp 和 tearDown 生命週期

`setUp` 方法在每個測試方法之前執行，`tearDown` 在每個測試方法之後執行：

```python
class TestDatabase(unittest.TestCase):
    def setUp(self):
        # 每個測試前建立資料庫連線
        self.db = create_database()
        self.db.insert({"name": "test"})

    def tearDown(self):
        # 每個測試後清理資料
        self.db.clear()
        self.db.close()

    def test_query(self):
        result = self.db.find_by_name("test")
        self.assertIsNotNone(result)

    def test_delete(self):
        self.db.delete("test")
        result = self.db.find_by_name("test")
        self.assertIsNone(result)
```

這種設計確保了測試之間的隔離——每個測試都在一個乾淨的環境中執行。

### setUpClass 和 tearDownClass

如果某些準備工作只需要執行一次（例如建立資料庫連線池），可以使用類別層級的生命週期方法：

```python
class TestExpensive(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.connection = create_expensive_connection()

    @classmethod
    def tearDownClass(cls):
        cls.connection.close()
```

### 斷言方法概覽

unittest 提供了豐富的斷言方法，以下是常用方法：

| 斷言方法 | 用途 |
|----------|------|
| `assertEqual(a, b)` | a == b |
| `assertNotEqual(a, b)` | a != b |
| `assertTrue(x)` | bool(x) is True |
| `assertFalse(x)` | bool(x) is False |
| `assertIs(a, b)` | a is b |
| `assertIsNone(x)` | x is None |
| `assertIn(a, b)` | a in b |
| `assertAlmostEqual(a, b)` | 浮點數近似相等 |
| `assertRaises(Exc, fun)` | 預期拋出例外 |
| `assertRegex(s, r)` | 字串符合正則表達式 |

完整列表可見 [unittest 文件](https://www.google.com/search?q=Python+unittest+assert+methods)。

### 測試組織與發現

unittest 支援自動測試發現。假設專案結構如下：

```
project/
├── src/
│   └── calculator.py
└── tests/
    ├── __init__.py
    ├── test_calculator.py
    └── test_utils.py
```

執行所有測試：

```bash
python3 -m unittest discover -s tests
```

`discover` 會遞迴搜尋 `tests/` 目錄下所有匹配 `test_*.py` 的檔案，並執行其中的 `TestCase` 子類別。

### 測試跳過與預期失敗

```python
class TestSkip(unittest.TestCase):
    @unittest.skip("暫時跳過")
    def test_not_ready(self):
        pass

    @unittest.skipIf(sys.version_info < (3, 10),
                     "需要 Python 3.10+")
    def test_new_feature(self):
        pass

    @unittest.expectedFailure
    def test_known_bug(self):
        self.assertEqual(1, 2)  # 已知的 Bug
```

### 子測試（SubTest）

當一個測試方法需要測試多組參數時，可以使用 `subTest`：

```python
class TestParametrize(unittest.TestCase):
    def test_multiple_cases(self):
        cases = [
            (1, 2, 3),
            (-1, 1, 0),
            (0, 0, 0),
            (100, 200, 300),
        ]
        for a, b, expected in cases:
            with self.subTest(a=a, b=b):
                self.assertEqual(add(a, b), expected)
```

### unittest 的優缺點

**優點**：
- 零依賴，Python 內建
- 穩定的 API，向後相容性極佳
- 與 IDE 整合良好
- 適合大型專案的結構化測試

**缺點**：
- 語法較為冗長，需要較多彩版程式碼
- 測試方法必須是類別的方法，不能是簡單函數
- 斷言訊息預設較不友善
- 缺乏現代測試框架的便利功能（如 fixture、參數化）

### 小結

unittest 是 Python 測試的基石。即使你最終選擇 pytest 作為主要測試框架，理解 unittest 仍然很有價值——因為 pytest 支援直接執行 unittest.TestCase，而且許多 Python 專案仍然使用 unittest。掌握 unittest 的基礎知識，能讓你在任何 Python 專案中都能快速開始撰寫測試。

---

**下一步**：[pytest 進階測試](focus3.md)

## 延伸閱讀

- [unittest 官方文件](https://www.google.com/search?q=Python+unittest+official+documentation)
- [Python 測試最佳實踐](https://www.google.com/search?q=Python+testing+best+practices)
- [unittest.mock 文件](https://www.google.com/search?q=Python+unittest+mock+documentation)
