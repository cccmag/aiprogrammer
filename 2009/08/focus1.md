# TDD 的起源與核心概念：從 XP 到主流

## TDD 的起源

### 極限編程（Extreme Programming）

1999 年，Kent Beck 出版了《Extreme Programming Explained》，提出了極限編程（XP）方法論。XP 包含了一系列實踐，其中最重要的就是 TDD。

```
XP 的核心實踐：
┌─────────────────────────────────────┐
│ ▪ 測試先行（Test First）            │
│ ▪ 結對編程（Pair Programming）       │
│ ▪ 重構（Refactoring）              │
│ ▪ 持續整合（Continuous Integration）│
│ ▪ 簡單設計（Simple Design）         │
│ ▪ 回饋（Feedback）                  │
└─────────────────────────────────────┘
```

### Kent Beck 與 TDD 的發明

2000 年，Kent Beck 在開發 C3 專案時發明了 TDD。他描述了這個發現的過程：

> 「我只是改變了程式設計的順序。先寫測試，然後再寫通過測試的程式碼。這樣做的結果讓我震驚——程式設計變得更快樂了。」

## TDD 的核心概念

### 紅-綠-重構循環

TDD 的核心是三個步驟的循環：

```python
def test_add_two_numbers():
    # Step 1: 紅 - 寫一個會失敗的測試
    result = add(2, 3)

    # Step 2: 綠 - 寫最少的程式碼讓測試通過
    assert result == 5

def add(a, b):
    # 這是臨時的實現
    return 5  # 只為了讓測試通過
```

```python
def test_add_two_numbers():
    result = add(2, 3)
    assert result == 5

def add(a, b):
    # Step 3: 重構 - 改善程式碼
    # 這個時候才實現真正的邏輯
    return a + b
```

### 測試隔離原則

每個測試應該：
- 獨立於其他測試
- 可以任意順序執行
- 不依賴外部狀態

```python
class TestCalculator:
    def setup(self):
        # 每個測試前執行
        self.calc = Calculator()

    def teardown(self):
        # 每個測試後執行
        self.calc = None

    def test_add(self):
        assert self.calc.add(2, 3) == 5

    def test_subtract(self):
        assert self.calc.subtract(5, 3) == 2
```

## TDD 的價值

### 為什麼要 TDD？

```
TDD 的價值：

1. 信心
   - 有了測試，修改程式碼不再害怕
   - 知道什麼時候破壞了功能

2. 文件
   - 測試就是程式的規格文件
   - 永遠與程式碼同步

3. 設計
   - 測試驅動設計
   - 強制關注點分離

4. 回饋
   - 快速知道程式的正確性
   - 縮短開發週期
```

### TDD 帶來的改變

```python
# 沒有 TDD
class Order:
    def __init__(self, items, customer):
        self.items = items
        self.customer = customer

    def calculate_total(self):
        total = 0
        for item in self.items:
            total += item.price * item.quantity
        return total

    def apply_discount(self, discount):
        self.total = self.total * (1 - discount)
```

```python
# 有 TDD - 先寫測試
def test_order_total():
    order = Order()
    order.add_item(Item('Book', price=100, quantity=2))
    assert order.calculate_total() == 200

def test_order_discount():
    order = Order()
    order.add_item(Item('Book', price=100, quantity=2))
    order.apply_discount(0.1)
    assert order.total == 180
```

## TDD 的挑戰

### 常見誤解

```
TDD 誤解：

1. 「TDD 意味著 100% 測試覆蓋」
   - 現實：測試重要的部分，而非追求數字

2. 「TDD 會讓開發變慢」
   - 現實：短期看起來慢，長期節省除錯時間

3. 「有測試就不需要 Code Review」
   - 現實：兩者互補，不是替代

4. 「所有程式碼都應該先寫測試」
   - 現實：探索性程式碼不需要
```

### 適用場景

```markdown
適合 TDD 的場景：
✓ 新功能開發
✓ 重構
✓ 複雜的業務邏輯
✓ 公共 API
✓ 高風險程式碼

不適合 TDD 的場景：
✗ 探索性實驗
✗ 一次性腳本
✗ 極度簡單的程式碼
✗ UI 布局（部分）
```

## TDD 與其他方法

### TDD vs 傳統測試

```
傳統測試 vs TDD：

傳統測試：
- 開發完程式後寫測試
- 測試是事後補上的
- 測試覆蓋率往往不足

TDD：
- 先寫測試再寫程式
- 測試是設計的一部分
- 強制達到高覆蓋率
```

### TDD vs BDD

```
TDD vs BDD：

TDD：
- 測試的是「功能是否正確」
- 使用單元測試框架
- 測試者通常是開發者

BDD：
- 測試的是「行為是否符合預期」
- 使用自然語言風格
- 測試者包括開發者和業務人員
```

## 結語

TDD 的發明改變了軟體開發的方式。2009 年，TDD 已經從一個極端的實踐，變成了被廣泛接受的方法論。

下一篇文章將介紹單元測試與 Mock 物件，這是 TDD 的核心工具。

---

## 延伸閱讀

- [Kent Beck 與 TDD 的發明](https://www.google.com/search?q=Kent+Beck+TDD+origin)
- [TDD 最佳化實踐](https://www.google.com/search?q=TDD+best+practices+2009)
- [紅-綠-重構循環](https://www.google.com/search?q=red+green+refactor+TDD)
- [TDD vs 傳統測試](https://www.google.com/search?q=TDD+vs+traditional+testing)

---

*本篇文章為「AI 程式人雜誌 2009 年 8 月號」焦點系列之一。*