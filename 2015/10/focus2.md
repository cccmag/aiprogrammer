# MVC 架構模式

## 模型-視圖-控制器設計模式

### 前言

MVC（Model-View-Controller）是軟體工程中最著名的架構模式之一。它起源於 1970 年代的 Smalltalk 語言，用於 GUI 應用程式的開發。如今，MVC 及其變體被廣泛應用於 Web 開發、行動應用和桌面應用程式中。

### MVC 的組成部分

#### Model（模型）

Model 是應用程式的核心，負責：

- **商業邏輯**：處理業務規則和計算
- **資料管理**：與資料庫或外部服務互動
- **狀態管理**：維護應用程式的內部狀態
- **資料驗證**：確保資料的完整性和一致性

Model 應該是「胖子」——它包含了大部分的商業邏輯，而 View 和 Controller 只是輔助角色。

```
Model 的職責：
┌─────────────────────────────────────────┐
│                                         │
│  ┌─────────────┐   ┌─────────────────┐ │
│  │ 商業邏輯    │   │  資料存取       │ │
│  │             │   │                 │ │
│  │ • 計算      │   │ • 資料庫操作   │ │
│  │ • 驗證      │   │ • 快取管理      │ │
│  │ • 規則      │   │ • 資料轉換      │ │
│  └─────────────┘   └─────────────────┘ │
│                                         │
│  ┌─────────────┐   ┌─────────────────┐ │
│  │ 狀態管理    │   │  事件通知       │ │
│  │             │   │                 │ │
│  │ • 資料結構  │   │ • 狀態變更事件 │ │
│  │ • 快取      │   │ • 觀察者模式   │ │
│  └─────────────┘   └─────────────────┘ │
│                                         │
└─────────────────────────────────────────┘
```

#### View（視圖）

View 負責：

- **呈現資料**：將 Model 的資料以使用者可見的形式呈現
- **使用者介面**：處理 UI 佈局和視覺元素
- **輸入轉發**：將使用者輸入傳遞給 Controller
- **展示邏輯**：格式化資料以供展示

View 應該是「瘦子」——只包含最少的展示邏輯，不應該包含商業邏輯。

#### Controller（控制器）

Controller 負責：

- **請求處理**：接收並解析使用者請求
- **流程控制**：決定應用程式如何回應請求
- **協調工作**：調用 Model 處理業務邏輯，選擇 View 呈現結果
- **輸入驗證**：基本輸入檢查和錯誤處理

Controller 是 Model 和 View 之間的協調者，但本身不應該包含複雜的商業邏輯。

### MVC 的運作流程

```
┌─────────────────────────────────────────────────────────────────┐
│                        MVC 請求處理流程                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   使用者                    Controller                          │
│     │                          │                                │
│     │  1. 發送請求             │                                │
│     │ ────────────────────────>│                                │
│     │                          │                                │
│     │                          │  2. 解析請求                    │
│     │                          │  ──────────                    │
│     │                          │                                │
│     │                          │  3. 調用 Model                  │
│     │                          │ ────────────────               │
│     │                          │        │                      │
│     │                          │        ▼                      │
│     │                          │   ┌─────────┐                 │
│     │                          │   │  Model  │                 │
│     │                          │   │ 商業   │                 │
│     │                          │   │ 邏輯   │                 │
│     │                          │   └────┬────┘                 │
│     │                          │        │                      │
│     │                          │  4. 處理結果                   │
│     │                          │ <──────────────               │
│     │                          │                                │
│     │                          │  5. 選擇 View                  │
│     │                          │ ────────────────               │
│     │                          │                                │
│     │                          │  6. 傳遞資料                   │
│     │                          │ ────────────────               │
│     │                          │                                │
│     │   7. 呈現 UI             │                                │
│     │ <────────────────────────│                                │
│     │                          │                                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### MVC 的優點

1. **關注點分離**：商業邏輯、使用者介面和流程控制分開，提高程式碼組織性
2. **易於測試**：Model 可以獨立於 View 進行測試
3. **團隊分工**：不同角色可以並行開發不同部分
4. **維護性**：修改某一部分不影響其他部分
5. **重用性**：同一個 Model 可以配合不同的 View 使用

### MVC 的缺點

1. **複雜性**：對於簡單應用程式，MVC 可能過度複雜
2. **Controller 肥厚化**：容易將過多邏輯放在 Controller
3. **View 和 Model 的連接**：有時 View 需要直接存取 Model 資料
4. **學習曲線**：初學者需要理解各元件的職責邊界

### MVC 的變體

#### MVP（Model-View-Presenter）

MVP 是 MVC 的演變，主要區別在於 Presenter 和 View 的互動方式：

- **View** 是被動的，只執行 Presenter 給出的指令
- **Presenter** 負責所有的使用者介面邏輯
- View 和 Model 不直接互動

```
MVC:
  View <──> Controller <──> Model
  (View 可以直接呼叫 Model 的某些方法)

MVP:
  View <──> Presenter <──> Model
  (View 和 Model 完全隔離)
```

MVP 常用於 Android 開發和桌面應用程式。

#### MVVM（Model-View-ViewModel）

MVVM 是 Microsoft 推出的模式，特別適用於 WPF 和 Silverlight 應用：

- **ViewModel** 是 View 的抽象，提供資料綁定
- View 和 ViewModel 之間透過資料綁定同步
- 雙向資料流動：View 變更自動反映到 ViewModel，反之亦然

```
┌────────────────────────────────────────────┐
│                  MVVM                       │
│                                            │
│   View ──── 資料綁定 ────> ViewModel       │
│    │                        │              │
│    │      雙向同步          │              │
│    ◄────────────────────────               │
│                                            │
│                  ViewModel                 │
│                   │    │                   │
│                   ▼    ▼                   │
│               Model  命令                  │
│                                            │
└────────────────────────────────────────────┘
```

MVVM 的優點是大幅減少 View 的程式碼，缺點是資料綁定機制可能隱藏過多細節。

### MVC 實作範例

```python
# Model: 負責商業邏輯和資料
class UserModel:
    def __init__(self):
        self._users = []

    def add_user(self, name, email):
        if not name or not email:
            raise ValueError("Name and email are required")
        user = {"name": name, "email": email}
        self._users.append(user)
        return user

    def get_all_users(self):
        return self._users.copy()

    def find_by_email(self, email):
        for user in self._users:
            if user["email"] == email:
                return user
        return None

# View: 負責呈現
class UserView:
    def show_users(self, users):
        if not users:
            print("No users found.")
            return
        print("Users:")
        for user in users:
            print(f"  - {user['name']} ({user['email']})")

    def show_error(self, message):
        print(f"Error: {message}")

    def show_success(self, message):
        print(f"Success: {message}")

    def get_user_input(self):
        name = input("Enter name: ")
        email = input("Enter email: ")
        return name, email

# Controller: 協調 Model 和 View
class UserController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def list_users(self):
        users = self.model.get_all_users()
        self.view.show_users(users)

    def add_user(self):
        name, email = self.view.get_user_input()
        try:
            user = self.model.add_user(name, email)
            self.view.show_success(f"User {user['name']} added!")
        except ValueError as e:
            self.view.show_error(str(e))

# 組合使用
model = UserModel()
view = UserView()
controller = UserController(model, view)

# 測試
controller.add_user()
controller.list_users()
```

### MVC 在 Web 框架中的應用

現代 Web 框架多採用 MVC 或其變體：

- **Django**（Python）：MTV（Model-Template-View）
- **Rails**（Ruby）：MVC
- **Spring MVC**（Java）：MVC
- **ASP.NET MVC**（C#）：MVC

這些框架在傳統 MVC 基礎上有所調整，例如：
- Template（範本）系統作為 View 層
- ORM（物件關聯對映）處理 Model 層
- Router（路由）系統處理 Controller 映射

### 選擇 MVC 還是其他模式？

| 場景 | 推薦模式 |
|------|---------|
| 簡單的 Web 應用 | MVC |
| 複雜的桌面應用 | MVP |
| 強調 UI 自動更新的應用 | MVVM |
| 事件驅動的應用 | Observer/Event-Driven |
| 服務導向架構 | SOA/微服務 |

### 小結

MVC 是一個經過時間考驗的架構模式，它將應用程式分為 Model、View 和 Controller 三個部分，實現了關注點分離。雖然對於簡單應用可能顯得繁瑣，但對於中大型應用程式，MVC 提供了一個清晰的組織結構。

理解 MVC 的核心概念不僅幫助我們開發更好的應用程式，也為學習其他更複雜的架構模式打下了基礎。

---

**下一步**：[測試驅動開發 TDD](focus3.md)

## 延伸閱讀

- [MVC Pattern Wikipedia](https://www.google.com/search?q=MVC+pattern+definition)
- [MVP vs MVC vs MVVM](https://www.google.com/search?q=MVP+MVC+MVVM+comparison)
- [Django MTV Pattern](https://www.google.com/search?q=Django+MTV+pattern)