# Mock 物件實戰

## 前言

在真實的軟體系統中，程式碼通常依賴於外部資源——資料庫、檔案系統、網路 API、電子郵件伺服器、快取系統等。在單元測試中，我們不希望實際連接這些外部資源（因為慢、不穩定、難以控制），而希望用 Mock 物件來模擬它們的行為。

## Mock 的核心概念

Mock 是一個「模擬物件」，它：
- **記錄對它的所有呼叫**：參數、次數、順序
- **回傳你指定的值**：透過 `return_value` 設定
- **可以拋出例外**：透過 `side_effect` 設定
- **可以驗證它的使用方式**：透過 `assert_called_*` 方法

## 建立 Mock

```python
from unittest.mock import Mock, MagicMock

# 基本 Mock
mock = Mock()
mock.return_value = 42
assert mock() == 42

# MagicMock：支援 magic methods（如 __len__, __iter__）
magic = MagicMock()
magic.__len__.return_value = 10
assert len(magic) == 10
```

## 設定回傳值

```python
mock = Mock()

# 固定回傳值
mock.get_data.return_value = {"key": "value"}

# 多次呼叫不同回傳值
mock.get_data.side_effect = [
    {"page": 1},
    {"page": 2},
    {"page": 3},
]

# 也可以結合 return_value
mock.query.return_value = "default"
```

## side_effect 進階用法

```python
from unittest.mock import Mock

# 拋出例外
mock = Mock()
mock.fetch.side_effect = ConnectionError("Connection refused")

# 自訂函數
def calculate(x):
    return x * 2 + 1

mock = Mock(side_effect=calculate)
assert mock(5) == 11

# 混合使用
mock = Mock()
mock.side_effect = [10, 20, ValueError("error")]
assert mock() == 10
assert mock() == 20
try:
    mock()
except ValueError:
    pass
```

## 驗證呼叫

```python
mock = Mock()

# 執行一些操作
mock(1, 2, key="value")
mock(1, 2, key="value")

# 驗證呼叫次數
mock.assert_called_once()  # 失敗：被呼叫了兩次
mock.assert_called()       # 成功：至少被呼叫一次
mock.assert_called_with(1, 2, key="value")

# 檢查呼叫次數
assert mock.call_count == 2

# 查看所有呼叫
print(mock.call_args_list)
# [call(1, 2, key='value'), call(1, 2, key='value')]
```

## patch 裝飾器

`patch` 是 mock 最強大的功能，它可以在測試範圍內暫時取代一個真實物件：

```python
from unittest.mock import patch

# 取代 myapp.module.get_user
@patch("myapp.module.get_user")
def test_get_user(mock_get_user):
    mock_get_user.return_value = {"name": "Alice"}
    result = get_user_service(1)
    assert result["name"] == "Alice"
```

### patch 上下文管理器

```python
def test_get_user():
    with patch("myapp.module.get_user") as mock_get_user:
        mock_get_user.return_value = {"name": "Alice"}
        result = get_user_service(1)
        assert result["name"] == "Alice"
```

### patch.object

```python
class EmailService:
    def send(self, to, subject, body):
        # 實際發送郵件
        pass

@patch.object(EmailService, "send")
def test_email(mock_send):
    service = EmailService()
    service.send("user@example.com", "Hello", "Body")
    mock_send.assert_called_once_with(
        "user@example.com", "Hello", "Body"
    )
```

## 實戰：測試外部 API 呼叫

```python
# weather.py
import requests

def get_weather(city):
    response = requests.get(f"https://api.weather.com/v1/{city}")
    response.raise_for_status()
    return response.json()

# test_weather.py
@patch("weather.requests.get")
def test_get_weather(mock_get):
    mock_response = Mock()
    mock_response.json.return_value = {
        "city": "Taipei",
        "temperature": 28,
        "humidity": 70
    }
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response
    
    result = get_weather("Taipei")
    assert result["temperature"] == 28
    mock_get.assert_called_once_with(
        "https://api.weather.com/v1/Taipei"
    )
```

## spec 參數：確保 Mock 與真實物件一致

```python
from unittest.mock import create_autospec

# 根據真實類別建立 Mock
class Database:
    def query(self, sql):
        pass
    def insert(self, data):
        pass
    def delete(self, id):
        pass

# 自動根據 Database 的介面建立 Mock
mock_db = create_autospec(Database)
mock_db.query.return_value = [1, 2, 3]

# 如果呼叫不存在的方法會拋出 AttributeError
# mock_db.nonexistent()  # AttributeError
```

## pytest-mock 整合

```python
# 安裝：pip install pytest-mock

def test_with_pytest_mock(mocker):
    mock_get = mocker.patch("myapp.requests.get")
    mock_get.return_value.json.return_value = {"ok": True}
    
    result = myapp.fetch_data()
    assert result["ok"] is True
```

`mocker` 提供了與 `unittest.mock` 相同的 API，但更簡潔，且自動處理 cleanup。

## 小結

Mock 是隔離測試的關鍵技術。它讓你可以測試依賴外部資源的程式碼，而不需要實際連接這些資源。使用 Mock 時，請記住兩個原則：**只 Mock 外部依賴**（不 Mock 同一專案的內部模組），**驗證公開行為**（不驗證實作細節）。

## 延伸閱讀

- [unittest.mock 官方文件](https://www.google.com/search?q=Python+unittest+mock+documentation)
- [Mock 的常見反模式](https://www.google.com/search?q=mock+anti+patterns+Python)
- [pytest-mock 文件](https://www.google.com/search?q=pytest+mock+documentation)
