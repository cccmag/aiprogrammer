# 測試資料管理與工廠模式

## 測試資料的挑戰

測試需要資料，但測試資料的建立、維護和清理往往複雜。測試資料管理不當會導致測試之間相互影響、維護困難等問題。

## 直接建立測試資料

最簡單的方式：

```python
def test_user_creation():
    user = User(name="Alice", email="alice@example.com")
    db.add(user)
    db.commit()

    retrieved = db.query(User).filter_by(email="alice@example.com").first()
    assert retrieved.name == "Alice"
```

問題：重複程式碼、難以擴展。

## 工廠模式

使用工廠集中建立測試資料：

```python
class UserFactory:
    def __init__(self):
        self.counter = 0

    def create(self, **kwargs):
        self.counter += 1
        defaults = {
            "name": f"User {self.counter}",
            "email": f"user{self.counter}@example.com",
            "created_at": datetime.now()
        }
        defaults.update(kwargs)
        return User(**defaults)

@pytest.fixture
def user_factory():
    return UserFactory()

def test_user_exists(user_factory):
    user = user_factory.create(name="Special User")
    assert user.name == "Special User"
    assert "@example.com" in user.email
```

## Faker 生成真實資料

```python
from faker import Faker

fake = Faker()

@pytest.fixture
def fake_user():
    return User(
        name=fake.name(),
        email=fake.email(),
        address=fake.address(),
        phone=fake.phone_number()
    )
```

Faker 能產生各種逼真的測試資料。

## Fixture 管理資料庫

```python
@pytest.fixture
def clean_db():
    db = create_test_db()
    yield db
    db.cleanup()  # 測試後清理

@pytest.fixture
def db_with_users(clean_db):
    clean_db.add(User(name="Alice"))
    clean_db.add(User(name="Bob"))
    clean_db.commit()
    return clean_db

def test_count_users(db_with_users):
    assert db_with_users.query(User).count() == 2
```

## 測試資料隔離

每個測試應該有獨立資料，避免相互依賴：

```python
@pytest.fixture
def unique_user(db):
    user = User(email=f"unique-{uuid.uuid4()}@test.com")
    db.add(user)
    db.commit()
    return user
```

使用唯一識別符確保測試隔離。

## 測試資料的組織

```
tests/
    fixtures/
        __init__.py
        user_fixtures.py
        product_fixtures.py
    conftest.py  # 全域 fixtures
```

將常用的 fixtures 放在 `conftest.py` 或專門檔案中。

## 結論

好的測試資料管理讓測試更穩定、易讀、易維護。投資在測試資料基礎設施上，長期回報顯著。