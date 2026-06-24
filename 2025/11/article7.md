# 事件溯源架構

## 以事件為中心的資料儲存模式

## 什麼是事件溯源？

事件溯源（Event Sourcing）是一種以事件為核心的資料儲存模式。不同於傳統 CRUD 只儲存當前狀態，事件溯源將每個狀態變更記錄為不可變的事件。

```
傳統 CRUD：
  UPDATE users SET name = 'Bob' WHERE id = 1
  → 只有當前的 name = 'Bob'，歷史被覆蓋

事件溯源：
  event: UserRenamed { user_id: 1, old_name: 'Alice', new_name: 'Bob' }
  event: UserRenamed { user_id: 1, old_name: 'Bob', new_name: 'Charlie' }
  → 完整記錄了所有的名稱變更
```

### 核心概念

```
Commands（命令）→ Events（事件）→ State（狀態）

用戶註冊請求 → UserRegistered 事件 → 用戶狀態
用戶改名請求 → UserRenamed 事件   → 更新後用戶狀態
用戶刪除請求 → UserDeleted 事件   → 用戶被標記為刪除
```

---

## 事件儲存

### 事件結構

```python
@dataclass
class Event:
    aggregate_id: str    # 聚合根 ID
    event_type: str      # 事件類型
    data: dict           # 事件資料
    version: int         # 版本號（樂觀鎖）
    timestamp: float     # 時間戳
    event_id: str        # 全域唯一事件 ID

# 例子
event = Event(
    aggregate_id="user-123",
    event_type="UserRegistered",
    data={"name": "Alice", "email": "alice@example.com"},
    version=1,
    timestamp=time.time(),
    event_id=uuid.uuid4().hex
)
```

### 事件儲存實作

```python
class EventStore:
    def __init__(self):
        self.events = {}  # aggregate_id → [events]

    def append(self, aggregate_id, events, expected_version):
        if aggregate_id not in self.events:
            self.events[aggregate_id] = []
        current = len(self.events[aggregate_id])
        if current != expected_version:
            raise ConcurrencyError("版本衝突")
        for event in events:
            event.version = current + 1
            self.events[aggregate_id].append(event)
            current += 1

    def get_events(self, aggregate_id):
        return self.events.get(aggregate_id, [])
```

---

## 聚合與重放

### 聚合根

聚合根負責保證業務不變量的正確性。

```python
class UserAggregate:
    def __init__(self):
        self.user_id = None
        self.name = None
        self.email = None
        self.is_deleted = False
        self.version = 0

    def apply_event(self, event):
        if event.event_type == "UserRegistered":
            self.user_id = event.data["user_id"]
            self.name = event.data["name"]
            self.email = event.data["email"]
        elif event.event_type == "UserRenamed":
            self.name = event.data["new_name"]
        elif event.event_type == "UserDeleted":
            self.is_deleted = True
        self.version += 1

    def rename(self, new_name):
        if self.is_deleted:
            raise ValueError("已刪除的用戶不能改名")
        if not new_name or len(new_name) < 2:
            raise ValueError("名稱長度不足")
        return [Event(
            aggregate_id=self.user_id,
            event_type="UserRenamed",
            data={"old_name": self.name, "new_name": new_name},
            version=self.version + 1,
            timestamp=time.time()
        )]
```

### 事件重放

從事件流重建當前狀態。

```python
def rebuild_aggregate(event_store, aggregate_id):
    aggregate = UserAggregate()
    for event in event_store.get_events(aggregate_id):
        aggregate.apply_event(event)
    return aggregate

# 使用
store = EventStore()
# ... 追加事件 ...
user = rebuild_aggregate(store, "user-123")
print(user.name)  # 當前名稱
```

---

## 快照（Snapshot）

事件重放隨著事件數量增加而變慢，快照可以加速重建過程。

```python
class SnapshotStore:
    def __init__(self, event_store, snapshot_frequency=100):
        self.event_store = event_store
        self.snapshot_frequency = snapshot_frequency
        self.snapshots = {}

    def save_snapshot(self, aggregate, version):
        self.snapshots[aggregate.user_id] = {
            "state": {
                "user_id": aggregate.user_id,
                "name": aggregate.name,
                "email": aggregate.email,
                "is_deleted": aggregate.is_deleted,
            },
            "version": version
        }

    def rebuild_with_snapshot(self, aggregate_id):
        # 從最近的快照開始
        snapshot = self.snapshots.get(aggregate_id)
        if snapshot:
            aggregate = UserAggregate()
            aggregate.__dict__.update(snapshot["state"])
            aggregate.version = snapshot["version"]
            start_version = snapshot["version"]
        else:
            aggregate = UserAggregate()
            start_version = 0

        # 重放快照之後的事件
        for event in self.event_store.get_events(aggregate_id):
            if event.version > start_version:
                aggregate.apply_event(event)

        # 是否需要建立新快照
        if aggregate.version - start_version >= self.snapshot_frequency:
            self.save_snapshot(aggregate, aggregate.version)

        return aggregate
```

---

## 命令與查詢責任分離（CQRS）

事件溯源常與 CQRS 一起使用。

```python
# 命令端（寫）
class UserCommandHandler:
    def __init__(self, event_store):
        self.event_store = event_store

    def handle_rename(self, user_id, new_name):
        aggregate = rebuild_aggregate(self.event_store, user_id)
        events = aggregate.rename(new_name)
        self.event_store.append(
            user_id, events, aggregate.version
        )

# 查詢端（讀）
class UserQueryHandler:
    def __init__(self, read_db):
        self.db = read_db  # 預先處理好的讀取模型

    def get_user(self, user_id):
        return self.db.query("SELECT * FROM users WHERE id = ?", user_id)
```

---

## 優勢與挑戰

### 優勢

**完整的審計軌跡**：知道誰在何時做了什麼

**時光回溯**：可以重建任意時間點的狀態

```
# 重建 2026-01-01 的使用者狀態
events = event_store.get_events_before("user-123", "2026-01-01")
state = rebuild_from_events(events)
```

**除錯能力**：可以重放事件模擬 bug

### 挑戰

**事件結構演化**：事件模式會隨時間改變

```python
# 向前相容處理
def migrate_event(event):
    if event.version < 2:
        # 舊格式：{name}
        # 新格式：{first_name, last_name}
        event.data["first_name"] = event.data.pop("name")
        event.data["last_name"] = ""
    return event
```

**查詢複雜**：需要建立專門的讀取模型

**儲存量**：事件會持續增長，需要歸檔策略

---

## 實際案例：銀行帳戶系統

```python
class AccountAggregate:
    def __init__(self):
        self.balance = 0
        self.is_frozen = False

    def apply(self, event):
        if event.type == "AccountCreated":
            self.account_id = event.data["account_id"]
        elif event.type == "MoneyDeposited":
            self.balance += event.data["amount"]
        elif event.type == "MoneyWithdrawn":
            self.balance -= event.data["amount"]
        elif event.type == "AccountFrozen":
            self.is_frozen = True

    def withdraw(self, amount):
        if self.is_frozen:
            raise ValueError("帳戶已凍結")
        if self.balance < amount:
            raise ValueError("餘額不足")
        return [Event(
            aggregate_id=self.account_id,
            event_type="MoneyWithdrawn",
            data={"amount": amount, "new_balance": self.balance - amount}
        )]
```

---

## 總結

事件溯源提供了一個強大的資料儲存範式，特別適合需要完整審計軌跡、複雜業務規則和時間點查詢的系統。但它並非銀彈——對於簡單的 CRUD 應用，傳統的 CRUD 更直接高效。關鍵在於辨識哪些領域真正需要事件溯源帶來的價值。

---

## 延伸閱讀

- [Event Sourcing Pattern](https://www.google.com/search?q=event+sourcing+pattern+microservices)
- [CQRS and Event Sourcing](https://www.google.com/search?q=CQRS+event+sourcing+architecture)
- [Event Store Database](https://www.google.com/search?q=event+store+database+event+sourcing)

---

*本篇文章為「AI 程式人雜誌 2026 年 11 月號」文章系列之七。*
