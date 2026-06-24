# TDD 實戰演練

## 前言

在之前的文章中，我們介紹了 TDD 的理論。現在讓我們透過一個真實的案例來實踐 TDD——開發一個「購物車」系統。我們將嚴格遵循紅-綠-重構的循環，逐步完善功能。

## 專案需求

我們需要一個購物車系統，支援：
1. 加入商品到購物車
2. 移除商品
3. 計算總價
4. 應用折扣
5. 計算最終金額

## 第一輪：空購物車

**紅（Red）**：先寫會失敗的測試。

```python
def test_empty_cart_total():
    cart = ShoppingCart()
    assert cart.total == 0
```

**綠（Green）**：寫最簡單的程式碼讓測試通過。

```python
class ShoppingCart:
    def __init__(self):
        self.total = 0
```

**重構（Refactor）**：這個階段太簡單了，不需要重構。

## 第二輪：加入一個商品

**紅（Red）**：

```python
def test_add_item():
    cart = ShoppingCart()
    cart.add_item("Apple", 30)
    assert cart.total == 30
```

**綠（Green）**：

```python
class ShoppingCart:
    def __init__(self):
        self.items = []
        self.total = 0

    def add_item(self, name, price):
        self.items.append({"name": name, "price": price})
        self.total += price
```

**重構（Refactor）**：暫時不需要。

## 第三輪：加入多個商品

**紅（Red）**：

```python
def test_add_multiple_items():
    cart = ShoppingCart()
    cart.add_item("Apple", 30)
    cart.add_item("Banana", 20)
    cart.add_item("Cherry", 50)
    assert cart.total == 100
```

**綠（Green）**：現有實作已經支援——測試通過！

**重構（Refactor）**：不需要。

## 第四輪：移除商品

**紅（Red）**：

```python
def test_remove_item():
    cart = ShoppingCart()
    cart.add_item("Apple", 30)
    cart.add_item("Banana", 20)
    cart.remove_item("Apple")
    assert cart.total == 20

def test_remove_nonexistent_item():
    cart = ShoppingCart()
    cart.add_item("Apple", 30)
    with pytest.raises(ValueError, match="not found"):
        cart.remove_item("Orange")
```

**綠（Green）**：

```python
def remove_item(self, name):
    for i, item in enumerate(self.items):
        if item["name"] == name:
            self.total -= item["price"]
            self.items.pop(i)
            return
    raise ValueError(f"Item '{name}' not found")
```

**重構（Refactor）**：`remove_item` 使用 for-else 可以更 Pythonic：

```python
def remove_item(self, name):
    for i, item in enumerate(self.items):
        if item["name"] == name:
            self.total -= item["price"]
            self.items.pop(i)
            break
    else:
        raise ValueError(f"Item '{name}' not found")
```

測試仍然通過——重構成功！

## 第五輪：數量支援

**紅（Red）**：

```python
def test_add_item_with_quantity():
    cart = ShoppingCart()
    cart.add_item("Apple", 30, quantity=3)
    assert cart.total == 90
    assert len(cart.items) == 1
```

**綠（Green）**：

```python
def add_item(self, name, price, quantity=1):
    for item in self.items:
        if item["name"] == name:
            item["quantity"] += quantity
            self.total += price * quantity
            return
    self.items.append({
        "name": name,
        "price": price,
        "quantity": quantity
    })
    self.total += price * quantity
```

**重構（Refactor）**：計算總價的邏輯可以提取為方法。

```python
def _calculate_item_total(self, item):
    return item["price"] * item["quantity"]

def add_item(self, name, price, quantity=1):
    for item in self.items:
        if item["name"] == name:
            item["quantity"] += quantity
            self.total += self._calculate_item_total(item)
            return
    self.items.append({
        "name": name, "price": price, "quantity": quantity
    })
    self.total += self._calculate_item_total(self.items[-1])
```

## 第六輪：折扣功能

**紅（Red）**：

```python
def test_apply_discount():
    cart = ShoppingCart()
    cart.add_item("Apple", 100)
    cart.apply_discount(10)  # 10% 折扣
    assert cart.discounted_total == 90
```

**綠（Green）**：

```python
class ShoppingCart:
    def __init__(self):
        self.items = []
        self.total = 0
        self.discount = 0

    def apply_discount(self, percent):
        if not 0 <= percent <= 100:
            raise ValueError("Discount must be 0-100")
        self.discount = percent

    @property
    def discounted_total(self):
        return self.total * (100 - self.discount) / 100
```

**重構（Refactor）**：檢查折扣範圍可以提取為驗證方法。

## 最終測試結果

```python
def test_complete_cart_flow():
    cart = ShoppingCart()
    cart.add_item("Apple", 30, quantity=2)
    cart.add_item("Banana", 20)
    assert cart.total == 80

    cart.remove_item("Banana")
    assert cart.total == 60

    cart.apply_discount(10)
    assert cart.discounted_total == 54

def test_invalid_discount():
    cart = ShoppingCart()
    with pytest.raises(ValueError):
        cart.apply_discount(150)
```

## TDD 實戰心得

**迭代粒度要小**：每個循環加入一個小功能，保持測試簡單。如果你發現一個測試太複雜，把它拆分成多個更小的測試。

**不跳過紅燈**：不要同時寫測試和實作。先讓測試失敗（紅色），再讓它通過（綠色）。跳過紅燈就失去了 TDD 的核心價值。

**重構是 TDD 的一部分**：許多開發者只做紅-綠，跳過重構。這會導致程式碼品質隨著迭代而下降。重構是 TDD 的第三步——讓程式碼保持乾淨。

**測試是安全的，不是負擔**：TDD 產生的測試套件是一張安全網。當你需要重構、修改、擴展功能時，你會感覺到的安全感和自由。

## 小結

TDD 不僅是一種測試技術，更是一種設計方法論。紅-綠-重構的循環讓開發者持續地關注程式碼的設計品質，同時確保每一個行為都有測試覆蓋。從簡單的購物車案例可以看出，TDD 讓程式碼的演進變得可預測、可控制、可信任。

## 延伸閱讀

- [TDD by Example（Kent Beck）](https://www.google.com/search?q=TDD+by+example+Kent+Beck)
- [TDD 的實戰模式](https://www.google.com/search?q=TDD+patterns+and+practices)
- [購物車 TDD 完整案例](https://www.google.com/search?q=Shopping+cart+TDD+Python)
