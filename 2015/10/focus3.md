# 測試驅動開發 TDD

## 紅-綠-重構循環

### 前言

測試驅動開發（Test-Driven Development, TDD）是一種軟體開發方法論，要求開發者在撰寫功能程式碼之前先撰寫測試。這種方法在 2000 年代初由 Kent Beck 和其他 Extreme Programming 的先驅推廣，如今已成為敏捷開發的核心實踐之一。

### TDD 的核心循環

TDD 的開發循環非常簡單：

```
┌─────────────────────────────────────────────────────────────┐
│                      TDD 開發循環                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│     ┌──────────┐                                           │
│     │   紅     │  Write a failing test                     │
│     └────┬─────┘                                           │
│          │                                                 │
│          ▼                                                 │
│     ┌──────────┐                                           │
│     │   綠     │  Write minimal code to pass the test      │
│     └────┬─────┘                                           │
│          │                                                 │
│          ▼                                                 │
│     ┌──────────┐                                           │
│     │   重構    │  Improve code structure                  │
│     └────┬─────┘                                           │
│          │                                                 │
│          └──────────────────────────────────────────────   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

1. **紅（Red）**：先撰寫一個會失敗的測試
2. **綠（Green）**：撰寫最少量、功能正確的程式碼讓測試通過
3. **重構（Refactor）**：改善程式碼結構，消除重複，但不改變行為

### 為什麼先寫測試？

#### 從使用者角度思考

先寫測試迫使我們從「這個功能應該做什麼」的角度思考，而不是「這個功能應該怎麼實作」。這有助於澄清需求，發現規格不清的地方。

```python
# 先問：這個函數應該做什麼？
def test_add_with_empty_string_returns_zero():
    result = add("")  # 什麼是 add 函數的預期行為？
    assert result == 0

def test_add_with_single_number():
    result = add("5")
    assert result == 5

def test_add_with_two_numbers():
    result = add("1,2")
    assert result == 3
```

這些測試清楚地定義了 `add` 函數的行為規格。

#### 避免測試被跳過

傳統開發流程中，開發者常常在功能完成後「忘記」寫測試，或者寫出無用的測試（TDD 稱之為「空氣測試」）。TDD 確保測試是開發流程的必要組成部分。

#### 提高測試覆蓋率

在 TDD 中，測試率可以接近 100%。每行程式碼都有對應的測試，任何新程式碼都需要先有測試。

### TDD 的實際案例

讓我們用一個簡單的例子來展示 TDD 的開發過程：實作一個 `Stack` 資料結構。

#### 第一步：紅

```python
import unittest

class StackTest(unittest.TestCase):
    def test_new_stack_is_empty(self):
        stack = Stack()
        self.assertTrue(stack.is_empty())

    def test_push_increases_size(self):
        stack = Stack()
        stack.push(1)
        self.assertFalse(stack.is_empty())

if __name__ == "__main__":
    unittest.main()
```

執行測試 → 失敗（`Stack` 類別不存在）

#### 第二步：綠

```python
class Stack:
    def __init__(self):
        self._items = []

    def is_empty(self):
        return len(self._items) == 0

    def push(self, item):
        self._items.append(item)
```

執行測試 → 通過

#### 第三步：重構

程式碼已經足夠簡單，重構可以跳過。

#### 繼續：更多測試

```python
def test_pop_returns_last_pushed(self):
    stack = Stack()
    stack.push(1)
    stack.push(2)
    self.assertEqual(stack.pop(), 2)

def test_pop_decreases_size(self):
    stack = Stack()
    stack.push(1)
    stack.push(2)
    stack.pop()
    self.assertFalse(stack.is_empty())

def test_pop_on_empty_raises(self):
    stack = Stack()
    with self.assertRaises(IndexError):
        stack.pop()
```

每次只撰寫一個測試，然後實作讓它通過。

### TDD 的優點

1. **確保測試被撰寫**：不會有「忘了寫測試」的問題
2. **提高設計品質**：迫使你在實作前先思考介面設計
3. **更快的錯誤發現**：問題在剛產生時就被發現
4. **提供安全網**：可以放心重構而不破壞功能
5. **文件化**：測試本身就是規格文件
6. **簡化除錯**：失敗的測試清楚指出問題位置

### TDD 的挑戰與批評

#### 學習曲線

TDD 需要時間學習和適應。一開始開發速度會變慢，但長期來看整體產出會更高。

#### 不是所有場景都適用

- 探索性程式設計：還不知道問題怎麼解
- UI 密集的程式：難以單元測試
- 效能關鍵程式：測試程式碼可能影響效能測試
- 一次性腳本：不需要測試

#### 測試品質

壞測試比沒有測試更糟糕。壞測試會：
- 讓重構變得困難
- 誤導開發者
- 浪費維護時間

好的測試應該：
- 測試行為，不是實作細節
- 獨立的，不依賴其他測試
- 快速執行
- 可讀性高

### TDD 與傳統測試的比較

| 面向 | TDD | 傳統測試 |
|------|-----|---------|
| 測試時機 | 功能程式碼之前 | 功能程式碼之後 |
| 測試目標 | 驗證功能正確性 | 發現 Bug |
| 測試覆蓋 | 接近 100% | 通常較低 |
| 設計影響 | 正面影響 | 負面影響（測試往往被忽略） |
| 學習曲線 | 陡峭 | 平緩 |
| 初期速度 | 較慢 | 較快 |
| 長期速度 | 較快 | 較慢 |

### TDD 進階技巧

#### 測試命名

好的測試名稱應該描述預期行為：

```python
# 不好
def test1(self):
    pass

def test_calc(self):
    pass

# 好
def test_add_with_empty_string_returns_zero(self):
    pass

def test_divide_by_zero_raises_division_error(self):
    pass

def test_user_cannot_login_with_wrong_password(self):
    pass
```

#### Arrange-Act-Assert 模式

```python
def test_transfer_moves_money_between_accounts(self):
    # Arrange: 準備測試資料
    from_account = Account(balance=1000)
    to_account = Account(balance=500)

    # Act: 執行被測試的操作
    from_account.transfer(to_account, 200)

    # Assert: 驗證結果
    self.assertEqual(from_account.balance, 800)
    self.assertEqual(to_account.balance, 700)
```

#### 測試隔離

每個測試應該獨立，不依賴其他測試的執行順序或結果：

```python
def setUp(self):
    self.calculator = Calculator()  # 每個測試都有乾淨的狀態

def tearDown(self):
    # 清理資源
    pass
```

### 測試金字塔與 TDD

TDD 主要用於金字塔底層的單元測試：

```
         /\        手動探索測試 (少量)
        /  \
       /    \
      / E2E  \     端到端測試 (少量)
     /────────\
    /          \
   /  整合測試  \   整合測試 (中等)
  /──────────────\
 /                \
/    單元測試      \  單元測試 (大量) ← TDD 主要應用區域
────────────────────
```

### 小結

TDD 是一種經過驗證的開發方法，它要求先寫測試再寫程式碼。這個看似反直覺的做法，其實能帶來更好的設計、更高的程式碼品質和更快的長期開發速度。

當然，TDD 不是萬能的。它需要時間學習，對某些場景可能不適用。但對大多數商業應用程式開發來說，TDD 是一個值得掌握的技能。

---

**下一步**：[重構技巧與最佳實踐](focus4.md)

## 延伸閱讀

- [Test Driven Development: By Example](https://www.google.com/search?q=Test+Driven+Development+Kent+Beck)
- [TDD Guidelines](https://www.google.com/search?q=how+to+practice+TDD)
- [Red Green Refactor cycle](https://www.google.com/search?q=red+green+refactor+cycle)