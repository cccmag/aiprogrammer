# Mock 與 Patch：隔離測試技巧

## 為何需要 Mock？

測試一個依賴外部系統的函式時，你不希望實際連接那個系統。Mock 允許你模擬外部依賴，隔離待測程式碼。

## 基本 Mock 物件

```python
from unittest.mock import Mock

def test_api_call():
    mock_api = Mock()
    mock_api.get_user.return_value = {"name": "Alice", "id": 1}

    result = get_user_name(mock_api, user_id=1)

    assert result == "Alice"
    mock_api.get_user.assert_called_once_with(1)
```

## Mock 的斷言方法

- `assert_called_once_with(*args, **kwargs)`：確認呼叫一次
- `assert_called_with(*args, **kwargs)`：確認最後一次呼叫
- `assert_any_call(*args, **kwargs)`：確認曾呼叫過
- `call_count`：存取呼叫次數
- `call_args_list`：取得所有呼叫參數

## Patch 上下文管理器

`patch` 用于替换模块中的对象：

```python
from unittest.mock import patch

def test_send_email():
    with patch("my_module.smtp_client") as mock_smtp:
        mock_smtp.send.return_value = True

        send_welcome_email("user@example.com")

        mock_smtp.send.assert_called_once()
```

## Patch 作為裝飾器

```python
@patch("my_module.Database")
def test_save_user(mock_db):
    mock_db.get_connection.return_value = mock_conn

    save_user({"name": "Bob"})

    mock_db.get_connection.return_value.insert.assert_called_once()
```

## 側寫（Side Effects）

當你需要模擬更複雜的行為：

```python
def fetch_user(user_id):
    if user_id < 0:
        raise ValueError("Invalid user ID")
    return {"name": "User", "id": user_id}

mock_api = Mock()
mock_api.fetch_user.side_effect = fetch_user

# 現在 mock 會根據參數返回不同結果或拋出異常
result = mock_api.fetch_user(1)
assert result == {"name": "User", "id": 1}

with pytest.raises(ValueError):
    mock_api.fetch_user(-1)
```

## Spy：部分 Mock

Spy 允許你包裝真實物件，同時追蹤呼叫：

```python
from unittest.mock import MagicMock

# 與 Mock 不同，Spy 可以呼叫真實方法
real_obj = SomeClass()
spy_obj = MagicMock(wraps=real_obj)

spy_obj.some_method()
spy_obj.some_method.assert_called()
# 同時真的執行了 some_method
```

## 常見陷阱

1. 確認路徑正確：`patch("module.ClassName")` 不是 `patch("module.class_name")`
2. 不要過度 Mock：單元測試應該測試單一單元
3. 清理 Mock 狀態：每個測試應該有乾淨的 Mock

## 結論

Mock 是隔離測試的關鍵技術。學會在適當的場景使用 Mock，能大幅提升測試的穩定性和執行速度。