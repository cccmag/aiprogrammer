# 依賴注入容器詳解

## 前言

依賴注入（Dependency Injection, DI）是實現控制反轉（IoC）的一種方式。依賴注入容器則是自動化依賴管理和注入的工具。

## 基本概念

```python
# 手動注入
class UserService:
    def __init__(self, db: Database):
        self.db = db

db = MySQLDatabase()
service = UserService(db)

# 依賴注入
container.register(Database, MySQLDatabase)
service = container.resolve(UserService)
```

## 簡單的 DI 容器

```python
class Container:
    def __init__(self):
        self._services = {}

    def register(self, interface, implementation):
        self._services[interface] = implementation

    def resolve(self, cls):
        deps = []
        for param_type in cls.__init__.__annotations__.values():
            if param_type in self._services:
                deps.append(self._resolve(param_type))

        return cls(*deps)

    def _resolve(self, cls):
        if cls in self._services:
            impl = self._services[cls]
            return impl() if callable(impl) else impl
        return cls()
```

## 使用場景

1. **測試**：容易替換為 Mock 物件
2. **配置**：根據環境注入不同實作
3. **大型專案**：管理大量依賴關係

## 優點

- 降低耦合度
- 提高可測試性
- 簡化物件建立
- 支援生命週期管理

## 小結

依賴注入是建立彈性、可測試系統的關鍵技術。

---

## 延伸閱讀

- [Dependency Injection](https://www.google.com/search?q=dependency+injection+python)
- [Inversion of Control](https://www.google.com/search?q=inversion+of+control+container)