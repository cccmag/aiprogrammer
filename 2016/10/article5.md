# Mock 物件與測試隔離

## 前言

Mock 物件讓我們能隔離測試對象，排除外部依賴的影響，實現真正的單元測試。

## 何時使用 Mock

1. 依賴外部 API 或服務
2. 依賴資料庫連線
3. 依賴時間或隨機數
4. 依賴尚未實作的介面

## Python Mock

### 使用 unittest.mock

```python
from unittest.mock import Mock, patch, MagicMock
import pytest

def test_with_mock():
    # 建立 Mock 物件
    mock_db = Mock()
    mock_db.query.return_value = [{'id': 1, 'name': 'Test'}]
    
    # 注入依賴
    service = UserService(mock_db)
    
    # 測試
    users = service.get_all_users()
    assert len(users) == 1
    assert users[0].name == 'Test'
    
    # 驗證 Mock 被正確調用
    mock_db.query.assert_called_once()
```

### 使用 patch

```python
@patch('myapp.database.get_connection')
def test_with_patch(mock_get_conn):
    mock_conn = Mock()
    mock_cursor = Mock()
    mock_cursor.fetchall.return_value = [('test',)]
    mock_conn.cursor.return_value = mock_cursor
    mock_get_conn.return_value = mock_conn
    
    result = fetch_users()
    assert result == [('test',)]
```

### MagicMock 自動建立屬性

```python
def test_magic_mock():
    mock_obj = MagicMock()
    
    # 自動建立屬性
    mock_obj.user.name = 'Test'
    mock_obj.user.get_id.return_value = '123'
    
    assert mock_obj.user.name == 'Test'
    assert mock_obj.user.get_id() == '123'
```

## Mock 實戰範例

### 測試電子郵件服務

```python
from unittest.mock import Mock, patch
import pytest

class TestEmailService:
    
    @patch('myapp.mail.SMTPServer')
    def test_send_email(self, mock_smtp):
        mock_server = Mock()
        mock_smtp.return_value = mock_server
        
        service = EmailService()
        result = service.send(
            to='user@example.com',
            subject='Test',
            body='Hello'
        )
        
        assert result == True
        mock_server.send.assert_called_once()
    
    @patch('myapp.mail.SMTPServer')
    def test_send_email_failure(self, mock_smtp):
        mock_server = Mock()
        mock_server.send.side_effect = ConnectionError('SMTP error')
        mock_smtp.return_value = mock_server
        
        service = EmailService()
        
        with pytest.raises(ConnectionError):
            service.send(
                to='user@example.com',
                subject='Test',
                body='Hello'
            )
```

### Mock 檔案系統

```python
from unittest.mock import patch, mock_open
import json

@patch('builtins.open', new_callable=mock_open, read_data='{"key": "value"}')
def test_read_config(mock_file):
    with open('config.json') as f:
        data = json.load(f)
    
    assert data == {'key': 'value'}
    mock_file.assert_called_with('config.json')
```

## Mock 進階技巧

### spy：監控真實物件

```python
def test_with_spy():
    real_object = RealClass()
    spy = Mock(wraps=real_object)
    
    spy.method('arg')
    
    assert spy.method.called
    assert real_object.method.called  # 真實方法也被調用
```

### Stub：固定回傳值

```python
def test_with_stub():
    stub = Mock()
    stub.get_user.return_value = User(id=1, name='Test')
    stub.get_config.return_value = {'debug': True}
    
    service = Service(stub)
    user = service.get_user()
    
    assert user.name == 'Test'
    assert service.is_debug_mode() == True
```

## Mock 最佳實踐

1. **只 Mock 外部依賴**：不要 Mock 自己模組
2. **驗證互動次數**：`assert_called_once_with()`
3. **清理 Mock 狀態**：`mock.reset_mock()`
4. **避免過度 Mock**：回歸測試應使用真實物件

## 常見問題

```python
# 問題：Mock 位置錯誤
@patch('myapp.module.ClassName')  # 正確：Mock 被使用的位置
def test_wrong_patch(mock):
    # ...
```

## 延伸閱讀

- [Python Mock 教學](https://www.google.com/search?q=python+unittest+mock+tutorial+2016)
- [Mock 物件模式](https://www.google.com/search?q=mock+object+pattern+2016)
- [測試隔離策略](https://www.google.com/search?q=test+isolation+strategy+2016)

---

*本篇文章為「AI 程式人雜誌 2016 年 10 月號」軟體測試系列之一。*