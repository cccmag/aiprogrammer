# 測試資料管理與工廠模式

## 前言

良好的測試資料管理讓測試更穩定、更易維護。工廠模式（Factory Pattern）是常用的解決方案。

## 測試資料的挑戰

1. 測試之間需要隔離
2. 需要可預測的測試資料
3. 大量測試需要快速建立資料
4. 測試資料不應依賴外部狀態

## 工廠模式實作

### Python：Factory Boy

```python
# factories.py
import factory
from factory import Faker
from myapp.models import User, Order

class UserFactory(factory.Factory):
    class Meta:
        model = User
    
    id = factory.Sequence(lambda n: n)
    name = Faker('name')
    email = factory.LazyAttribute(lambda obj: f'{obj.name.lower().replace(" ", ".")}@example.com')
    active = True

class OrderFactory(factory.Factory):
    class Meta:
        model = Order
    
    id = factory.Sequence(lambda n: n)
    user = factory.SubFactory(UserFactory)
    amount = factory.Faker('pydecimal', left_digits=5, right_digits=2, positive=True)
    status = 'pending'
    created_at = Faker('date_time_this_year')
```

### 使用工廠

```python
# test_with_factory.py
import pytest
from factories import UserFactory, OrderFactory

def test_user_factory():
    user = UserFactory()
    assert user.name is not None
    assert '@example.com' in user.email

def test_user_factory_with_override():
    user = UserFactory(name='Custom Name')
    assert user.name == 'Custom Name'

def test_order_factory():
    order = OrderFactory()
    assert order.user is not None
    assert order.amount > 0

def test_multiple_orders():
    user = UserFactory()
    orders = OrderFactory.create_batch(5, user=user)
    
    assert len(orders) == 5
    assert all(o.user == user for o in orders)
```

## Fixture 工廠

```python
# conftest.py
import pytest
from factories import UserFactory, OrderFactory

@pytest.fixture
def user(db):
    return UserFactory()

@pytest.fixture
def admin_user(db):
    return UserFactory(is_admin=True)

@pytest.fixture
def user_with_orders(db):
    user = UserFactory()
    orders = OrderFactory.create_batch(3, user=user)
    return {'user': user, 'orders': orders}

@pytest.fixture
def sample_data(db):
    users = UserFactory.create_batch(10)
    for user in users[:5]:
        OrderFactory.create_batch(2, user=user)
    return {'users': users}
```

## Mock 資料庫

```python
# test_db.py
import pytest
from unittest.mock import MagicMock

@pytest.fixture
def mock_db():
    db = MagicMock()
    db.users = [
        {'id': 1, 'name': 'User 1', 'email': 'user1@example.com'},
        {'id': 2, 'name': 'User 2', 'email': 'user2@example.com'}
    ]
    db.query.return_value = db.users
    return db

def test_query_users(mock_db):
    result = mock_db.query('SELECT * FROM users')
    assert len(result) == 2
    mock_db.query.assert_called_once()
```

## 測試資料清理

```python
# test_cleanup.py
import pytest

@pytest.fixture
def clean_users(db):
    # 先清理
    db.users.delete_all()
    yield
    # 測試後清理
    db.users.delete_all()

def test_with_clean_data(clean_users):
    db.users.insert({'name': 'Test User'})
    assert len(db.users.all()) == 1
```

## Faker 產生器

```python
from factories import UserFactory
from factory import Faker

# 自訂 Faker
class CustomUserFactory(UserFactory):
    name = Faker('name', locale='zh_TW')
    email = Faker('email')
    address = Faker('address', locale='zh_TW')
    phone = Faker('phone_number', locale='zh_TW')
    company = Faker('company', locale='zh_TW')
    job = Faker('job')

# 使用
user = CustomUserFactory()
print(user.name)  # "陳大文"
print(user.address)  # "台北市信義區..."
```

## 測試資料策略

1. **盡量使用工廠而非固定資料**：更靈活
2. **每個測試建立自己的資料**：避免相互依賴
3. **使用有意義的資料**：讓測試更易讀
4. **考慮效能**：大量測試時使用 in-memory DB

## 延伸閱讀

- [Factory Boy 文檔](https://www.google.com/search?q=factory+boy+python+tutorial+2016)
- [測試資料管理](https://www.google.com/search?q=test+data+management+2016)
- [Faker 資料產生](https://www.google.com/search?q=faker+python+library+2016)

---

*本篇文章為「AI 程式人雜誌 2016 年 10 月號」軟體測試系列之一。*