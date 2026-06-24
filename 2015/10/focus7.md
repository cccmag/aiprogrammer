# 程式碼品質與技術債務

## 衡量、 管理與持續改進

### 前言

程式碼品質是軟體專案成敗的關鍵因素之一。低品質的程式碼導致維護困難、Bug 叢生、開發速度下降。技術債務則是為趕進度而做出的技術折衷隨時間累積的代價。本期將探討如何衡量、和管理程式碼品質，以及如何處理技術債務。

### 程式碼品質維度

#### 1. 可讀性（Readability）

**可讀的程式碼特點**：

- 變數和函數命名有意義
- 程式碼結構清晰
- 適當的註解（但不要過度註解）
- 一致的編碼風格

```python
# 不易讀
def calc(a, b):
    return a * 0.15 + b * 0.2

# 易讀
SALES_TAX_RATE = 0.15
SHIPPING_COST_RATE = 0.2

def calculate_total_cost(sales_amount, shipping_cost):
    tax = sales_amount * SALES_TAX_RATE
    handling = shipping_cost * SHIPPING_COST_RATE
    return tax + handling
```

#### 2. 可維護性（Maintainability）

**影響可維護性的因素**：

- 模組化程度
- 依賴關係複雜度
- 測試覆蓋率
- 文件完整性

#### 3. 彈性（Flexibility）

**高彈性程式碼的特點**：

- 低耦合，替換元件不影響其他部分
- 高內聚，元件職責單一
- 遵循開放/封閉原則
- 依賴注入，便於測試

#### 4. 效率（Efficiency）

**效率優化原則**：

- 先保證正確性，再優化效能
- 使用 profiling 工具找到瓶頸
- 避免過早優化（YAGNI）
- 考慮複雜度：我們通常不需要 O(n²) 的演算法

### 程式碼品質度量

#### 圈複雜度（Cyclomatic Complexity）

衡量程式的分支複雜度：

```python
# 簡單線性程式：複雜度 1
def process(data):
    return data * 2

# 一個分支：複雜度 2
def process(data):
    if data > 0:
        return data * 2
    else:
        return data * -1

# 兩個分支：複雜度 3
def process(data):
    if data > 0:
        if data > 100:
            return data * 3
        else:
            return data * 2
    else:
        return data * -1
```

**複雜度與品質的對應關係**：

| 複雜度 | 等級 | 風險 |
|-------|------|------|
| 1-10 | 低 | 簡單，低風險 |
| 11-20 | 中 | 中等風險 |
| 21-50 | 高 | 高風險，需要重構 |
| 51+ | 極高 | 必須重構 |

#### 耦合度量

- ** CBO（耦合物件數）**：一個類別依賴的其他類別數量
- ** RFC（回應類別數）**：類別的方法數 + 呼叫其他類別的方法數
- ** LCOM（缺乏內聚）**：衡量類別方法之間的相關程度

#### 程式碼覆蓋率

```bash
# 使用 coverage.py 測量覆蓋率
pip install coverage
coverage run -m pytest
coverage report
coverage html  # 生成 HTML 報告
```

**覆蓋率目標**（非絕對）：
- 語句覆蓋率：70-80% 是基本門檻
- 分支覆蓋率：60-70% 是合理目標
- 關鍵路徑應該接近 100%

### 程式碼壞味道

Martin Fowler 在《Refactoring》一書中整理了常見的壞味道：

#### 1. 重複程式碼（Duplicated Code）

```python
# 壞味道
def send_email_to_user(user):
    email_service.send(
        to=user.email,
        subject="Welcome",
        body=f"Hello {user.name}"
    )

def send_promo_to_user(user):
    email_service.send(
        to=user.email,
        subject="Promotion",
        body=f"Dear {user.name}, check out our deals!"
    )

# 重構後
def send_email(user, subject, body):
    email_service.send(
        to=user.email,
        subject=subject,
        body=body
    )

def send_email_to_user(user):
    send_email(user, "Welcome", f"Hello {user.name}")

def send_promo_to_user(user):
    send_email(user, "Promotion", f"Dear {user.name}, check out our deals!")
```

#### 2. 過長函數（Long Method）

跡象：
- 函數超過一頁螢幕
- 太多巢狀區塊
- 註解過多（說明這段在做什麼）

#### 3. 過大類別（Large Class）

跡象：
- 類別超過幾百行
- 有太多實例變數
- 方法名稱包含 "And" 或 "Or"

#### 4. 霰彈式修改（Shotgun Surgery）

跡象：修改一個功能需要同時改多個檔案

#### 5. 依賴過多（Feature Envy）

跡象：一個類別的方法過度使用另一個類別的資料

```python
# Feature Envy
class Order:
    def calculate_total(self):
        discount = 0
        if self.customer.is_premium:
            discount = self.customer.loyalty_points * 0.01
        return self.amount - discount

# 較好的設計
class Customer:
    def calculate_discount(self):
        if self.is_premium:
            return self.loyalty_points * 0.01
        return 0
```

#### 6. 資料團（Data Clumps）

跡象：多處出現相同的變數群組

```python
# 資料團
def send_invoice(order, customer_name, customer_email, customer_address):
    pass

def send_receipt(order, customer_name, customer_email, customer_address):
    pass

# 應該是
class Customer:
    def __init__(self, name, email, address):
        self.name = name
        self.email = email
        self.address = address

def send_invoice(order, customer):
    pass
```

### 技術債務

#### 什麼是技術債務？

技術債務（Technical Debt）是一個比喻，指開發團隊為加速軟體開發而在品質上做的折衷，隨時間推移會累積「利息」。

**類型**：

1. **故意的**：知道這是捷徑，但計畫未來重構
2. **無意的**：缺乏經驗，不知道更好的方式
3. **懈怠的**：知道但因為時間壓力選擇忽略

#### 技術債務的影響

```
技術債務累積示意圖

時間 ───────────────────────────────────────────────────>

程式碼品質
    │
100%│                          ╭─────────────
    │                     ╭────╯  (債務累積)
 80%│                ╭────╯
    │           ╭────╯   (債務開始)
 60%│      ╭────╯
    │ ────╯  (開始專案)
    │
    └───────────────────────────────────────────────────> 功能
```

#### 債務還款策略

**策略 1：分配固定時間**

每週或每兩週分配固定時間（如 20%）處理技術債務。

**策略 2：童子軍規則**

「每次離開時都比到達時更乾淨」。每當你修改一個檔案，也順便改善一點品質。

**策略 3：重構優先**

任何新功能開發前，先評估並處理相關技術債務。

**策略 4：追蹤與優先級**

建立技術債務清單，按影響程度和還款成本排序。

```markdown
# 技術債務追蹤

| ID | 描述 | 影響 | 還款成本 | 優先級 | 狀態 |
|----|------|------|---------|--------|------|
| TD-001 | 認證模組缺少測試 | 高 | 中 | P1 | To Do |
| TD-002 | ORM 查詢效能問題 | 中 | 高 | P2 | To Do |
| TD-003 | 過時的 UI 函式庫 | 低 | 低 | P3 | Backlog |
```

### 程式碼審查（Code Review）

程式碼審查是保持程式碼品質的重要實踐：

**審查清單**：

- [ ] 程式碼是否正確？
- [ ] 是否有測試覆蓋？
- [ ] 命名是否有意義？
- [ ] 是否有壞味道？
- [ ] 是否遵循團隊的程式碼規範？
- [ ] 是否有安全漏洞？
- [ ] 錯誤處理是否完善？

**審查技巧**：

1. **少量多次**：每次審查不超過 30 分鐘
2. **關注重點**：不要過度挑剔格式問題
3. **提出建議**：而不是只指出問題
4. **尊重對方**：程式碼是人寫的，批評要對事不對人

### 持續改進實踐

#### 1. 自動化測試

```
測試金字塔：

         /\
        /  \     E2E 測試 (少量)
       /    \
      /──────\    整合測試 (中等)
     /        \
    /──────────\  單元測試 (大量)
```

#### 2. 持續整合（CI）

每次提交自動執行：
- 測試
- 程式碼品質檢查
- 建構

#### 3. 技術分享

- 程式碼讀書會
- 內部分享會
- 設計文件 Review

#### 4. 監控與度量

- 追蹤程式碼覆蓋率趨勢
- 監控複雜度變化
- 記錄技術債務變化

### 小結

程式碼品質和技術債務管理是軟體開發中長期、持續的工作。關鍵要點：

1. **理解品質維度**：可讀性、可維護性、彈性、效率
2. **使用度量工具**：複雜度、覆蓋率、耦合度
3. **識別壞味道**：知道什麼時候需要重構
4. **管理技術債務**：追蹤、優先級、還款計劃
5. **團隊協作**：Code Review、技術分享、持續改進
6. **持續投入**：把品質維護當作日常工作的一部分

記住：程式碼品質是團隊的共同責任，需要每個人的努力和持續投入。

---

## 延伸閱讀

- [Code Complete 2](https://www.google.com/search?q=Code+Complete+Steve+McConnell)
- [Refactoring: Improving the Design of Existing Code](https://www.google.com/search?q=Refactoring+Martin+Fowler)
- [Technical Debt概念](https://www.google.com/search?q=technical+debt+concept+ward+cunningham)
- [SonarQube程式碼品質管理](https://www.google.com/search?q=sonarqube+code+quality+management)