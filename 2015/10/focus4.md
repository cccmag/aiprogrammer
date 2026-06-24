# 重構技巧與最佳實踐

## 改善程式碼而不改變行為

### 前言

重構（Refactoring）是軟體開發中不可或缺的一環。隨著時間推移，程式碼庫會累積技術債務——那些當初「先求有」的決定會讓程式碼變得難以理解和維護。重構就是在不改變外部行為的前提下，改善程式碼的內部結構。

### 什麼是重構？

重構的定義：
- **不改變**：程式碼的外部行為
- **只改善**：內部結構、可讀性、可維護性

重構不是：
- 新功能開發
- 效能優化（除非是內部結構改善的副作用）
- Bug 修補
- 測試添加

### 重構的時機

#### 代碼壞味道（Code Smell）

當你聞到「壞味道」時，就是該重構的信號：

| 壞味道 | 徵兆 | 解決方案 |
|--------|------|---------|
| 重複程式碼 | 相同或相似的程式碼出現多次 | 提取公共方法 |
| 過長函數 | 函數超過 50 行 | 分解為多個小函數 |
| 過大類別 | 類別承擔過多職責 | 拆分為多個類別 |
| 過長參數列表 | 函數需要很多參數 | 封裝為物件 |
| 霰彈式修改 | 修改需要改多個檔案 | 移動功能集中 |
| 依賴過多 | 類別依賴很多其他類別 | 提取介面、依賴反轉 |
| 內幕交換 | 類別過度交換內部資料 | 移動方法到正確位置 |
| 迴避類別 | 類別大多只是轉發呼叫 | 移除中間層 |

#### 何時不重構

- 程式碼即將被廢棄
- 已經穩定不需要修改
- 沒有測試覆蓋
- 截止日期緊迫
- 你不理解這段程式碼

### 重構的關鍵原則

#### 1. 保持小步伐

每次只做一個改變，然後執行測試：

```
壞：一次做 10 個改變，測試失敗，不知道哪個改變造成的
好：一次做 1 個改變，測試失敗，很清楚問題在哪
```

#### 2. 有測試安全網

沒有測試的重構是危險的冒險。在重構前：

```bash
# 確保測試通過
pytest
# 或
python -m unittest discover
```

#### 3. 頻繁提交

每次成功的重構都應該提交：

```bash
git add -A
git commit -m "refactor: extract calculate_total to separate function"
```

#### 4. 別同時重構和加功能

如果需要加新功能：
1. 先重構
2. 確認測試通過
3. 再加新功能

### 常見重構手法

#### 1. 提取函數（Extract Method）

**Before**：
```python
def print_invoice(order):
    print(f"Order #{order.id}")
    print(f"Date: {order.date}")
    print("Items:")
    for item in order.items:
        print(f"  {item.name}: ${item.price}")
    total = sum(item.price for item in order.items)
    print(f"Total: ${total}")
```

**After**：
```python
def print_invoice(order):
    print_order_header(order)
    print_order_items(order)
    print_order_total(order)

def print_order_header(order):
    print(f"Order #{order.id}")
    print(f"Date: {order.date}")

def print_order_items(order):
    print("Items:")
    for item in order.items:
        print(f"  {item.name}: ${item.price}")

def print_order_total(order):
    total = sum(item.price for item in order.items)
    print(f"Total: ${total}")
```

#### 2. 提取類別（Extract Class）

**Before**：
```python
class Person:
    def __init__(self, name, office_area_code, office_number):
        self.name = name
        self.office_area_code = office_area_code
        self.office_number = office_number

    def get_office_phone(self):
        return f"{self.office_area_code}-{self.office_number}"
```

**After**：
```python
class PhoneNumber:
    def __init__(self, area_code, number):
        self.area_code = area_code
        self.number = number

    def __str__(self):
        return f"{self.area_code}-{self.number}"

class Person:
    def __init__(self, name, phone):
        self.name = name
        self.phone = phone

    def get_office_phone(self):
        return str(self.phone)
```

#### 3. 替換條件式（Replace Conditional with Polymorphism）

**Before**：
```python
class Employee:
    def calculate_pay(self):
        if self.type == "HOURLY":
            return self.hours_worked * self.hourly_rate
        elif self.type == "SALARIED":
            return self.monthly_salary
        elif self.type == "COMMISSION":
            return self.base_salary + self.commission
```

**After**：
```python
from abc import ABC, abstractmethod

class Employee(ABC):
    @abstractmethod
    def calculate_pay(self):
        pass

class HourlyEmployee(Employee):
    def calculate_pay(self):
        return self.hours_worked * self.hourly_rate

class SalariedEmployee(Employee):
    def calculate_pay(self):
        return self.monthly_salary

class CommissionEmployee(Employee):
    def calculate_pay(self):
        return self.base_salary + self.commission
```

#### 4. 替換壞味道：過長參數列表

**Before**：
```python
def create_user(name, email, age, address, phone, company, title):
    pass

# 呼叫
create_user("John", "john@example.com", 30, "123 Main St", "555-1234", "Acme Inc", "Engineer")
```

**After**：
```python
class UserProfile:
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.age = None
        self.address = None
        self.phone = None
        self.company = None
        self.title = None

def create_user(profile):
    pass

# 呼叫
profile = UserProfile("John", "john@example.com")
profile.age = 30
create_user(profile)
```

#### 5. 內聯函數（Inline Method）

當一個方法只是簡單轉發給另一個方法時，可以內聯：

**Before**：
```python
def get_rating(self):
    return more_than_five_late_deliveries()

def more_than_five_late_deliveries(self):
    return self.late_deliveries > 5
```

**After**：
```python
def get_rating(self):
    return self.late_deliveries > 5
```

### 重構工具與自動化

#### IDE 重構支援

現代 IDE 提供了許多重構工具：

- **PyCharm/IntelliJ**：重構Rename、Extract Method、Inline 等
- **Visual Studio**：重構工具豐富
- **VS Code**：通過擴展提供基礎重構功能

#### 自動化工具

- **Rope**（Python）：Python 重構庫
- **Pyflakes**：Python 靜態分析
- **Pylint**：Python 程式碼檢查

### 重構的安全檢查清單

在開始重構前：

- [ ] 有測試覆蓋嗎？
- [ ] 測試通過了嗎？
- [ ] 理解即將修改的程式碼嗎？
- [ ] 知道這個改變的風險嗎？
- [ ] 準備好隨時還原嗎？

在重構過程中：

- [ ] 每次只做一個改變？
- [ ] 每次改變後執行測試？
- [ ] 頻繁提交嗎？

### 重構與技術債務

技術債務（Technical Debt）是 Ward Cunningham 提出的概念，描述了「現在走捷徑，未來還債」的現象。

**管理技術債務的策略**：

1. **辨識**：識別程式碼中的壞味道
2. **量化**：估計債務的成本（維護時間、風險）
3. **優先級**：決定先處理哪些債務
4. **還款計劃**：每週/每月固定時間處理技術債務
5. **預防**：通過 Code Review、 Coding Standards 預防新債務產生

### 小結

重構是維持程式碼健康的必要活動。關鍵是：

1. **有測試安全網** - 測試是重構的前提
2. **小步伐前進** - 每次只做一個改變
3. **頻繁提交** - 每個成功的改變都值得保存
4. **識別壞味道** - 知道什麼時候該重構
5. **持續投入** - 把技術債務還款列入日程

記住：重構不是一次性活動，而是持續的過程。

---

**下一步**：[軟體架構設計原則](focus5.md)

## 延伸閱讀

- [Refactoring: Improving the Design of Existing Code](https://www.google.com/search?q=Refactoring+Martin+Fowler)
- [Code Smell Catalog](https://www.google.com/search?q=code+smell+catalog)
- [Refactoring Guru](https://www.google.com/search?q=refactoring+guru+techniques)