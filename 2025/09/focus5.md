# Mock 與隔離測試

## 在不依賴外部服務的情況下測試你的程式碼

### 前言

在真實的軟體系統中，很少有元件是完全孤立的。一個函數可能需要讀取資料庫、呼叫遠端 API、寫入檔案系統，或者發送電子郵件。如果每次測試都要實際連接這些外部資源，測試就會變得緩慢、不穩定且難以維護。這就是 Mock 派上用場的時候。

### 什麼是 Mock？

Mock 是一個「模擬物件」，它模仿真實物件的行為，但由你控制它的輸入和輸出。你可以：
- **指定回傳值**：當 Mock 被呼叫時應該回傳什麼
- **驗證呼叫**：檢查 Mock 是否被正確地呼叫（參數、次數、順序）
- **模擬例外**：讓 Mock 拋出特定例外來測試錯誤處理

### Python 的 unittest.mock

Python 從 3.3 開始將 `unittest.mock` 納入標準函式庫。核心類別是 `Mock` 和 `MagicMock`（支援 magic methods）。

```python
from unittest.mock import Mock, patch

# 建立一個 Mock 物件
mock_service = Mock()
mock_service.get_user.return_value = {"id": 1, "name": "Alice"}

# 使用 Mock
user = mock_service.get_user(1)
assert user["name"] == "Alice"
mock_service.get_user.assert_called_once_with(1)
```

### patch：在測試中取代真實物件

`patch` 是 mock 最強大的功能之一。它可以在測試的上下文範圍內暫時取代一個真實物件：

```python
from unittest.mock import patch

def test_get_user():
    with patch("myapp.database.get_user") as mock_get_user:
        mock_get_user.return_value = {"id": 1, "name": "Alice"}
        
        result = get_user_service(1)
        assert result["name"] == "Alice"
```

也可以使用 decorator：

```python
@patch("myapp.database.get_user")
def test_get_user(mock_get_user):
    mock_get_user.return_value = {"id": 1, "name": "Alice"}
    result = get_user_service(1)
    assert result["name"] == "Alice"
```

### side_effect：更複雜的模擬行為

`side_effect` 可以指定更複雜的行為——多次呼叫回傳不同值、拋出例外、或者執行自訂函數：

```python
# 每次呼叫回傳不同值
mock = Mock()
mock.side_effect = [10, 20, 30]
assert mock() == 10
assert mock() == 20
assert mock() == 30

# 拋出例外
mock = Mock()
mock.side_effect = ValueError("Invalid input")
try:
    mock()
except ValueError:
    pass  # 預期行為

# 自訂函數
def custom_function(x):
    return x * 2

mock = Mock(side_effect=custom_function)
assert mock(5) == 10
```

### 驗證測試

Mock 提供了多種驗證方法來檢查它是否被正確使用：

```python
mock = Mock()

mock(1, 2, key="value")

# 驗證被呼叫過
mock.assert_called()

# 驗證被呼叫一次
mock.assert_called_once()

# 驗證特定參數
mock.assert_called_with(1, 2, key="value")

# 驗證呼叫次數
assert mock.call_count == 1

# 查看所有呼叫記錄
print(mock.call_args_list)
```

### 實戰範例：測試電子郵件發送

假設你的應用程式在使用者註冊後會發送歡迎郵件：

```python
# myapp/services.py
def send_welcome_email(user_email):
    email_service = EmailService()
    email_service.send(
        to=user_email,
        subject="歡迎加入！",
        body="感謝您的註冊..."
    )

# tests/test_services.py
@patch("myapp.services.EmailService")
def test_send_welcome_email(MockEmailService):
    mock_service = MockEmailService.return_value
    send_welcome_email("user@example.com")
    
    mock_service.send.assert_called_once_with(
        to="user@example.com",
        subject="歡迎加入！",
        body="感謝您的註冊..."
    )
```

### 實戰範例：測試資料庫操作

```python
# myapp/repository.py
class UserRepository:
    def __init__(self, db_connection):
        self.db = db_connection
    
    def find_by_id(self, user_id):
        return self.db.execute(
            "SELECT * FROM users WHERE id = ?", (user_id,)
        )

# tests/test_repository.py
def test_find_by_id():
    mock_db = Mock()
    mock_db.execute.return_value = {"id": 1, "name": "Alice"}
    
    repo = UserRepository(mock_db)
    user = repo.find_by_id(1)
    
    assert user["name"] == "Alice"
    mock_db.execute.assert_called_once_with(
        "SELECT * FROM users WHERE id = ?", (1,)
    )
```

### Mock 的注意事項

**過度使用 Mock**

Mock 太好用了，有時候開發者會「什麼都 Mock」。這是一個陷阱——如果你 Mock 了所有東西，你的測試只是在測試自己寫的 Mock，而不是真實的程式碼。**只 Mock 外部依賴**，不要 Mock 同一專案中的內部模組。

**Mock 與真實行為的偏離**

Mock 的回傳值可能與真實物件的行為不一致。例如，真實的 API 可能會回傳 `None`，但你的 Mock 回傳了空字典。這會導致測試通過但上線後出錯。使用 `spec` 參數可以讓 Mock 遵循真實物件的介面。

```python
from unittest.mock import create_autospec

# 根據真實類別建立 Mock
mock_service = create_autospec(RealEmailService)
```

**測試實作細節**

不要 Mock 和驗證「內部實作細節」，應該測試「公開行為」。測試應該關注「做了什麼」而不是「怎麼做的」。

### 什麼時候該使用 Mock？

| 場景 | 應該 Mock？ | 替代方案 |
|------|------------|---------|
| 外部 API 呼叫 | 是 | 使用 VCR/錄製技術 |
| 資料庫操作 | 是（單元測試） | 整合測試用真實資料庫 |
| 檔案系統操作 | 是 | 使用 TemporaryFile |
| 內部工具函數 | 否 | 直接測試 |
| 第三方 SDK | 是 | 檢查 SDK 是否提供測試模式 |

### 小結

Mock 是一把雙面刃——用得好，可以寫出快速、可靠、隔離的單元測試；用得不好，會產生脆弱、無意義的測試。關鍵是把握原則：**Mock 外部依賴，測試內部邏輯**。

---

**下一步**：[整合測試與端到端測試](focus6.md)

## 延伸閱讀

- [unittest.mock 官方文件](https://www.google.com/search?q=Python+unittest+mock+documentation)
- [pytest-mock 使用指南](https://www.google.com/search?q=pytest+mock+usage+guide)
- [Mock 的陷阱與最佳實踐](https://www.google.com/search?q=mock+testing+best+practices)
