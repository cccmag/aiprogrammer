# 單元測試的藝術（2010-2016）

## 前言

單元測試是軟體測試的基石——針對程式的最小單位進行驗證，確保每個函數、每個模組都正確運作。

## 單元測試的核心原則

### FIRST 原則

- **F**ast（快速）：測試必須快速執行，才能即時回饋
- **I**solated（隔離）：每個測試獨立，不依賴其他測試
- **R**epeatable（可重複）：結果穩定，任意執行皆相同
- **S**elf-validating（自我驗證）：測試自己判斷通過或失敗
- **T**imely（即時）：測試在程式碼產生後立即撰寫

## 測試結構：AAA 模式

```python
def test_calculate_total():
    # Arrange：準備測試資料
    items = [{"price": 10}, {"price": 20}, {"price": 30}]
    
    # Act：執行要測試的函數
    result = calculate_total(items)
    
    # Assert：驗證結果
    assert result == 60
```

## 常見測試框架

### JavaScript：Jest

```javascript
describe('calculateTotal', () => {
  it('should sum all item prices', () => {
    const items = [{price: 10}, {price: 20}];
    expect(calculateTotal(items)).toBe(30);
  });
  
  it('should return 0 for empty array', () => {
    expect(calculateTotal([])).toBe(0);
  });
});
```

### Python：pytest

```python
import pytest

def calculate_total(items):
    return sum(item['price'] for item in items)

def test_calculate_total_with_items():
    items = [{"price": 10}, {"price": 20}]
    assert calculate_total(items) == 30

def test_calculate_total_empty():
    assert calculate_total([]) == 0

def test_calculate_total_single_item():
    assert calculate_total([{"price": 42}]) == 42
```

## 測試 double 技術

### Stub：回傳固定值

```python
class UserRepositoryStub:
    def find_by_id(self, user_id):
        return {"id": user_id, "name": "Test User"}

def test_user_service(user_repo=UserRepositoryStub()):
    service = UserService(user_repo)
    user = service.get_user(123)
    assert user["name"] == "Test User"
```

### Mock：驗證互動行為

```python
from unittest.mock import Mock

def test_email_sent():
    mailer = Mock()
    service = UserService(mailer)
    service.notify_user("test@example.com", "Hello")
    mailer.send.assert_called_once_with("test@example.com", "Hello")
```

## 邊界條件測試

```python
def test_boundaries():
    # 邊界值測試
    assert calculate_total([{"price": 0}]) == 0
    assert calculate_total([{"price": -1}]) == -1  # 負數處理
    assert calculate_total([{"price": 10**12}]) == 10**12  # 大數
```

## 2016 年工具生態

- [Jest 官方文檔](https://www.google.com/search?q=jest+javascript+testing+framework+2016)
- [pytest 教程](https://www.google.com/search?q=pytest+python+testing+tutorial+2016)
- [單元測試最佳實踐](https://www.google.com/search?q=unit+testing+best+practices+2016)
- [測試覆蓋率工具](https://www.google.com/search?q=javascript+code+coverage+tools+2016)

## 結語

單元測試是高品質軟體的第一步。遵循 FIRST 原則與 AAA 模式，建立完善的測試習慣，是每個開發者的必備技能。

---

*本篇文章為「AI 程式人雜誌 2016 年 10 月號」軟體測試系列之一。*