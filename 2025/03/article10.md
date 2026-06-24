# 模組化專案組織

## 從類別到模組

當專案規模成長時，把所有類別放在同一個檔案中會變得難以維護。模組化專案組織將相關的類別分組到不同的模組和套件中，讓專案結構清晰、易於導航。

## Python 專案結構

### 小型專案

```
my_project/
├── main.py
├── models.py
├── services.py
└── utils.py
```

### 中型專案

```
my_project/
├── main.py
├── config.py
├── models/
│   ├── __init__.py
│   ├── user.py
│   └── product.py
├── services/
│   ├── __init__.py
│   ├── auth.py
│   └── payment.py
└── utils/
    ├── __init__.py
    ├── validators.py
    └── formatters.py
```

### 大型專案

```
my_project/
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── config/
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   └── logging.py
│   ├── domain/
│   │   ├── __init__.py
│   │   ├── models/
│   │   ├── repositories/
│   │   └── services/
│   ├── infrastructure/
│   │   ├── __init__.py
│   │   ├── database/
│   │   ├── cache/
│   │   └── queue/
│   └── presentation/
│       ├── __init__.py
│       ├── api/
│       └── cli/
├── tests/
│   ├── __init__.py
│   ├── unit/
│   └── integration/
├── requirements.txt
└── pyproject.toml
```

## __init__.py 的妙用

`__init__.py` 不僅標記目錄為 Python 套件，還可以控制匯出行為：

```python
# models/__init__.py
from .user import User
from .product import Product
from .order import Order

__all__ = ["User", "Product", "Order"]
```

現在客戶端可以簡潔地匯入：

```python
# main.py
from models import User, Product  # 而不是 from models.user import User
```

## 絕對匯入 vs 相對匯入

```python
# 絕對匯入（推薦）
from my_project.models.user import User
from my_project.services.auth import AuthService

# 相對匯入（謹慎使用）
from ..models.user import User
from .auth import AuthService
```

## 模組化實戰案例：電子商務系統

### 專案結構

```
ecommerce/
├── __init__.py
├── main.py
├── config.py
├── models/
│   ├── __init__.py
│   ├── user.py
│   ├── product.py
│   └── order.py
├── services/
│   ├── __init__.py
│   ├── cart.py
│   ├── payment.py
│   └── shipping.py
├── repositories/
│   ├── __init__.py
│   ├── user_repo.py
│   └── product_repo.py
└── utils/
    ├── __init__.py
    ├── validators.py
    └── helpers.py
```

### 核心模組實作

```python
# models/user.py
from dataclasses import dataclass
from typing import List

@dataclass
class User:
    id: int
    username: str
    email: str
    cart: List["Product"] = None

    def __post_init__(self):
        if self.cart is None:
            self.cart = []

# models/product.py
@dataclass
class Product:
    id: int
    name: str
    price: float
    stock: int

# services/cart.py
from models import User, Product

class CartService:
    def add_to_cart(self, user: User, product: Product, qty: int = 1):
        for _ in range(qty):
            user.cart.append(product)
        return f"{product.name} x{qty} 已加入購物車"

    def checkout(self, user: User) -> float:
        total = sum(p.price for p in user.cart)
        user.cart.clear()
        return total

# services/payment.py
class PaymentService:
    def process(self, user, amount):
        print(f"{user.username} 支付 ${amount}")
        return True

# main.py
from models import User, Product
from services.cart import CartService
from services.payment import PaymentService

user = User(id=1, username="Alice", email="alice@test.com")
product = Product(id=1, name="Python 書", price=599, stock=10)

cart = CartService()
payment = PaymentService()

cart.add_to_cart(user, product, 2)
total = cart.checkout(user)
payment.process(user, total)
```

## 模組化原則

### 1. 單一職責原則

每個模組只負責一個特定的功能領域：

```python
# 好的設計
# validators.py - 只有驗證邏輯
# formatters.py - 只有格式化邏輯
# models/user.py - 只有使用者資料模型

# 不好的設計
# utils.py - 所有雜項功能混在一起
```

### 2. 依賴反轉原則

高層模組不應該直接依賴低層模組，兩者都應該依賴抽象：

```python
from abc import ABC, abstractmethod

class UserRepository(ABC):
    @abstractmethod
    def find_by_id(self, user_id): ...

class PostgresUserRepository(UserRepository):
    def find_by_id(self, user_id):
        return f"從 PostgreSQL 查詢使用者 {user_id}"

class UserService:
    def __init__(self, repo: UserRepository):
        self._repo = repo

    def get_user(self, user_id):
        return self._repo.find_by_id(user_id)
```

### 3. 循環依賴避免

```python
# 錯誤：循環依賴
# a.py: from b import B
# b.py: from a import A

# 解決：提取共同介面到第三個模組
# common.py: 定義介面
# a.py: from common import InterfaceA
# b.py: from common import InterfaceB
```

## 小結

好的模組化組織是大型專案成功的關鍵。透過明確的目錄結構、恰當的套件劃分和依賴管理，你可以讓專案在持續成長的同時保持可維護性。從小型專案開始建立良好的模組化習慣，將會在專案擴大時得到巨大的回報。

## 延伸閱讀

- [Python 專案結構指南](https://www.google.com/search?q=Python+project+structure+best+practices)
- [Python 模組與套件](https://www.google.com/search?q=Python+modules+and+packages)
