# 策略模式與彈性設計

## 前言

策略模式定義了一系列演算法，將它們封裝成獨立物件，使得它們可以互相替換。

## 基本結構

```python
class SortStrategy(ABC):
    @abstractmethod
    def sort(self, data):
        pass

class QuickSort(SortStrategy):
    def sort(self, data):
        # 快速排序實作
        return sorted(data)

class MergeSort(SortStrategy):
    def sort(self, data):
        # 合併排序實作
        return sorted(data)
```

## 使用範例

```python
class DataSorter:
    def __init__(self, strategy: SortStrategy):
        self.strategy = strategy

    def set_strategy(self, strategy):
        self.strategy = strategy

    def sort(self, data):
        return self.strategy.sort(data)

# 使用
sorter = DataSorter(QuickSort())
sorter.sort([3, 1, 2])  # 使用快速排序

sorter.set_strategy(MergeSort())
sorter.sort([3, 1, 2])  # 使用合併排序
```

## 與其他模式的比較

| 模式 | 目的 | 封裝內容 |
|------|------|---------|
| 策略 | 可替換的演算法 | 演算法 |
| 狀態 | 物件行為隨狀態改變 | 狀態 |
| 命令 | 請求封裝為物件 | 操作 |

## 優點

1. **演算法可替換**：執行時可以改變策略
2. **消除條件判斷**：用多型替代 if/else
3. **隔離複雜度**：將複雜邏輯封裝在策略類別中
4. **易於測試**：每個策略可以獨立測試

## 小結

策略模式是實現彈性設計的重要工具。當你發現程式碼中充滿 if/else 判斷處理不同演算法時，考慮使用策略模式。

---

## 延伸閱讀

- [Strategy Pattern](https://www.google.com/search?q=strategy+pattern+design+patterns)
- [Strategy vs State Pattern](https://www.google.com/search?q=strategy+vs+state+pattern)