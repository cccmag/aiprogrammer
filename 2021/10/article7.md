# 重構與測試：安全改碼的藝術

## 測試是重構的保障

重構是在不改變外部行為的前提下改善程式碼結構。沒有測試的保護，重構就像在黑暗中施工。測試讓你能安心地改變程式碼結構。

## 重構的基本步驟

1. **確認測試覆蓋**：先增加測試，確保現有行為被記錄
2. **小步前進**：每次只做一個改變
3. **持續測試**：每步後執行測試
4. ** Commit**：每個小步都是一個 commit

## 典型重構模式

### 提取函式

```python
# 重構前
def process_order(order):
    # 驗證訂單
    if order.total <= 0:
        raise ValueError("Invalid total")
    if not order.items:
        raise ValueError("Empty order")
    # 計算折扣
    discount = order.total * 0.1
    # ... 更多邏輯

# 重構後
def validate_order(order):
    if order.total <= 0:
        raise ValueError("Invalid total")
    if not order.items:
        raise ValueError("Empty order")

def calculate_discount(order):
    return order.total * 0.1
```

### 引入參數物件

```python
# 重構前
def create_user(name, email, age, address, phone):
    ...

# 重構後
from dataclasses import dataclass

@dataclass
class UserRegistration:
    name: str
    email: str
    age: int
    address: str
    phone: str

def create_user(registration: UserRegistration):
    ...
```

## 避免破壞性改變

使用 deprecation warning 過渡：

```python
import warnings

def old_function(a, b):
    warnings.warn(
        "old_function is deprecated, use new_function instead",
        DeprecationWarning,
        stacklevel=2
    )
    return new_function(a, b)
```

## 測試幫助理解程式碼

閱讀複雜程式碼時，寫測試是理解它的好方法。當你嘗試為一段程式碼寫測試時，你會更深入理解它的行為和邊界。

## 大型重構策略

1. 識別穩定的公共 API
2. 為公共 API 撰寫完整測試
3. 逐步將內部實現遷移到新結構
4. 每次遷移後測試確保行為一致
5. 移除舊的中間層

## 結論

測試讓重構從冒險變成安全可控的過程。投資測試是對未來的保障，讓你將來能夠自信地改善程式碼。