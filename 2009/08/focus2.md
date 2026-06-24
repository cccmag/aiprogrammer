# 單元測試與 Mock 物件：隔離與控制

## 單元測試的原則

### 什麼是單元測試？

單元測試是對軟體中的最小可測試單位進行驗證的測試。通常指對函數、方法或類別的測試。

```
測試金字塔：

              ▲
             /│\
            / │ \       端到端測試
           /  │  \      （少量，耗時）
          /───┼───\
         /    │    \    整合測試
        /     │     \   （適量）
       /──────┼──────\
      /       │       \  單元測試
     /        │        \（大量，快速）
```

### FIRST 原則

好的單元測試應該符合 FIRST 原則：

```python
# F - Fast（快速）
def test_should_be_fast():
    # 單元測試應該毫秒級完成
    # 避免網路、檔案、資料庫操作
    result = string_helper.reverse("hello")
    assert result == "olleh"

# I - Isolated（隔離）
def test_isolated():
    # 每個測試獨立，不依賴其他測試
    calculator = Calculator()  # 每個測試新建
    assert calculator.add(1, 2) == 3

# R - Repeatable（可重複）
def test_repeatable():
    # 每次執行結果一致
    # 不依賴外部時間、隨機數
    random.seed(42)
    assert generate_id() == "abc123"

# S - Self-validating（自我驗證）
def test_self_validating():
    # 測試應該自動判斷通過或失敗
    # 不需要手動檢查輸出
    assert calculator.add(1, 2) == 3

# T - Timely（及時）
def test_timely():
    # 測試應該在實際程式碼之前或同時撰寫
    # 這是 TDD 的核心
```

## Mock 物件與 Stub

### Mock vs Stub

```python
# 測試替補（Test Doubles）的類型：

# 1. Dummy Object - 填補參數，不使用
def send_email(to, subject, body):
    # to 參數是 Dummy，不需要真的發送
    pass

# 2. Stub - 提供固定的回應
class FakeUserRepository:
    def find_by_id(self, id):
        return User(name="Test User")  # 固定回應

# 3. Mock - 驗證互動
class MockUserRepository:
    def __init__(self):
        self.find_called = False
        self.find_id = None

    def find_by_id(self, id):
        self.find_called = True
        self.find_id = id
        return User(name="Test User")

# 4. Spy - 記錄資訊，委託給真實物件
class UserRepositorySpy(UserRepository):
    def __init__(self):
        self.call_count = 0

    def find_by_id(self, id):
        self.call_count += 1
        return super().find_by_id(id)

# 5. Fake - 有實際邏輯，但簡化實現
class InMemoryUserRepository(FakeUserRepository):
    def __init__(self):
        self.users = {}
        self.counter = 0

    def save(self, user):
        user.id = self.counter += 1
        self.users[user.id] = user
        return user
```

### 使用 Mock 的原因

```python
# 場景：測試 OrderService
# OrderService 依賴 EmailService 和 UserRepository

class OrderService:
    def __init__(self, user_repo, email_service):
        self.user_repo = user_repo
        self.email_service = email_service

    def place_order(self, user_id, items):
        user = self.user_repo.find_by_id(user_id)
        order = Order(user, items)
        order.save()

        self.email_service.send_confirmation(user.email, order)

        return order

# 測試：驗證 email 被發送
def test_order_sends_confirmation_email():
    # 建立 Mock
    mock_repo = MockUserRepository()
    mock_email = MockEmailService()

    service = OrderService(mock_repo, mock_email)

    service.place_order(user_id=1, items=[item1, item2])

    # 驗證 Mock
    assert mock_email.send_confirmation_called
    assert mock_email.send_confirmation_args[0] == "user@example.com"
```

## 依賴注入

### 為什麼需要依賴注入？

```python
# 壞設計：Hard-coded 依賴
class OrderService:
    def __init__(self):
        # 緊密耦合，難以測試
        self.user_repo = UserRepository()
        self.email_service = EmailService()

# 好設計：依賴注入
class OrderService:
    def __init__(self, user_repo, email_service):
        # 可以注入任何實現
        self.user_repo = user_repo
        self.email_service = email_service
```

### 注入方式

```python
# 1. 建構子注入（推薦）
class OrderService:
    def __init__(self, user_repo, email_service):
        self.user_repo = user_repo
        self.email_service = email_service

# 2. 屬性注入
class OrderService:
    user_repo = None
    email_service = None

# 3. 方法注入
def process_order(self, user_repo, email_service):
    pass
```

## Mock 框架

### Python Mock

```python
# 使用 unittest.mock（Python 3.3+）
# 2009 年主要使用 mock 庫

from mock import Mock, MagicMock, patch

# Mock 物件
def test_with_mock():
    mock_repo = Mock()
    mock_repo.find_by_id.return_value = User(name="Test")

    service = OrderService(mock_repo, Mock())

    result = service.place_order(1, [])

    assert result.user.name == "Test"
    mock_repo.find_by_id.assert_called_once_with(1)

# MagicMock - 自動建立屬性
def test_magic_mock():
    mock = MagicMock()

    mock.user_repository.find_by_id.return_value = User(name="Test")

    # 可以鏈式調用
    assert mock.user_repository.find_by_id(1).name == "Test"

# Patch - 替換物件
@patch('OrderService.email_service')
def test_with_patch(mock_email):
    mock_email.send.return_value = True

    service = OrderService(Mock(), mock_email)
    service.process()

    mock_email.send.assert_called_once()
```

### Ruby RSpec Mocks

```ruby
# RSpec 中的 Mock

describe OrderService do
  it "sends confirmation email" do
    # 建立 mock
    user_repo = double("user_repository")
    email_service = double("email_service")

    user = User.new(email: "test@example.com")

    # 設定 mock 行為
    allow(user_repo).to receive(:find_by_id).with(1).and_return(user)
    allow(email_service).to receive(:send_confirmation)

    service = OrderService.new(user_repo, email_service)

    # 執行並驗證
    service.place_order(1, [])

    expect(email_service).to have_received(:send_confirmation)
      .with(user.email, anything)
  end
end
```

## 測試隔離的藝術

### 隔離外部依賴

```python
# 避免外部呼叫
def test_without_network():
    with patch('requests.get') as mock_get:
        mock_get.return_value = Mock(json=lambda: {"key": "value"})

        result = fetch_data("http://api.example.com/data")

        assert result == {"key": "value"}

# 避免時間依賴
def test_without_time():
    with patch('time.time') as mock_time:
        mock_time.return_value = 1234567890

        result = get_timestamp()

        assert result == "2009-02-13"
```

### 測試資料管理

```python
# 工廠方法模式
class UserFactory:
    @staticmethod
    def create_user(name="Test User", email="test@example.com"):
        return User(name=name, email=email)

# Fixture 工廠
class TestFixtures:
    @classmethod
    def setup_class(cls):
        cls.users = [
            UserFactory.create_user("User 1"),
            UserFactory.create_user("User 2"),
        ]

    def test_with_fixture(self):
        user = self.users[0]
        assert user.name == "User 1"
```

## 結語

單元測試和 Mock 物件是 TDD 的核心工具。正確使用這些工具可以讓測試快速、可靠、易於維護。

下一篇文章將介紹 BDD 與行為驅動開發，這是 TDD 的自然延伸。

---

## 延伸閱讀

- [單元測試原則](https://www.google.com/search?q=unit+testing+principles+FIRST)
- [Mock 物件模式](https://www.google.com/search?q=mock+object+pattern)
- [依賴注入](https://www.google.com/search?q=dependency+injection+testing)
- [Python mock 庫](https://www.google.com/search?q=python+mock+library)

---

*本篇文章為「AI 程式人雜誌 2009 年 8 月號」焦點系列之一。*