# pytest Fixtures 與參數化測試

## Fixtures 基礎

Fixture 是一種提供測試依賴的機制。不同於在每個測試中重複建立對象，Fixtures 集中管理依賴的建立和清理。

```python
@pytest.fixture
def database():
    db = create_test_database()
    yield db
    db.cleanup()

def test_query(database):
    result = database.query("SELECT * FROM users")
    assert len(result) > 0
```

使用 `yield` 而非 `return`，是為了確保 `yield` 後的程式碼在測試後執行。

## Fixture 作用域

Scope 控制 fixture 的生命週期：

```python
@pytest.fixture(scope="function")  # 每個測試新建
def user(): ...

@pytest.fixture(scope="class")  # 每個類別一個
def config(): ...

@pytest.fixture(scope="module")  # 每個模組一個
def db_connection(): ...

@pytest.fixture(scope="session")  # 整個測試 session 一個
def test_env(): ...
```

正確的作用域選擇能提高測試效率。

## Fixture 工廠

當需要多個相似對象時，工廠模式很有用：

```python
@pytest.fixture
def user_factory():
    def create_user(name, email):
        return User(name=name, email=email)
    return create_user

def test_create_multiple_users(user_factory):
    user1 = user_factory("Alice", "alice@example.com")
    user2 = user_factory("Bob", "bob@example.com")
    assert user1.id != user2.id
```

## Fixture 依賴

Fixtures 可以依賴其他 Fixtures：

```python
@pytest.fixture
def db():
    return Database(":memory:")

@pytest.fixture
def user_service(db):  # 依賴 db fixture
    return UserService(db)
```

pytest 會自動解析依賴關係。

## 參數化測試

```python
@pytest.mark.parametrize("input,expected", [
    (1, 2),
    (2, 4),
    (3, 6),
    (0, 0),
    (-1, -2),
])
def test_double(input, expected):
    assert double(input) == expected
```

一次定義，多個測試案例，極大減少重複。

## 多參數參數化

```python
@pytest.mark.parametrize("a,b,expected", [
    (1, 1, 2),
    (2, 3, 5),
    (-1, 1, 0),
])
def test_add(a, b, expected):
    assert add(a, b) == expected
```

## 組合參數化

使用 `pytest.mark.parametrize` 裝飾器組合：

```python
@pytest.mark.parametrize("x", [1, 2, 3])
@pytest.mark.parametrize("y", [10, 20])
def test_combinations(x, y):
    # 會產生 3*2=6 個組合
    pass
```

## 結論

Fixture 和參數化是 pytest 最強大的功能。掌握它們，能寫出簡潔、高效、易維護的測試程式碼。