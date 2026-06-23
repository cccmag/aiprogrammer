# 錯誤恢復設計

## 前言

錯誤恢復設計決定了系統在異常情況下的表現。好的錯誤恢復機制能將使用者的挫敗感降到最低，並維持對系統的信任。本文討論錯誤預防、偵測與恢復策略。

## 錯誤預防層

```python
class InputValidator:
    def __init__(self):
        self.rules = []

    def add_rule(self, field, validator, error_msg):
        self.rules.append((field, validator, error_msg))

    def validate(self, data):
        errors = {}
        for field, validator, msg in self.rules:
            if field in data and not validator(data[field]):
                errors[field] = msg
        return errors

    def safe_execute(self, data, action):
        errors = self.validate(data)
        if errors:
            return {"success": False, "errors": errors}
        try:
            result = action(data)
            return {"success": True, "result": result}
        except Exception as e:
            return {"success": False, "errors": {"system": str(e)}}

class SafeCalculator:
    def add(self, a, b):
        return a + b

    def divide(self, a, b):
        return a / b

validator = InputValidator()
validator.add_rule("a", lambda x: isinstance(x, (int, float)), "a 必須是數字")
validator.add_rule("b", lambda x: isinstance(x, (int, float)), "b 必須是數字")

calc = SafeCalculator()
print(validator.safe_execute({"a": 10, "b": 0}, lambda d: calc.divide(d["a"], d["b"])))
print(validator.safe_execute({"a": "abc", "b": 5}, lambda d: calc.add(d["a"], d["b"])))
```

## 優雅降級策略

```python
class GracefulDegradation:
    def __init__(self):
        self.service_level = 3  # 最高等級

    def degrade(self):
        if self.service_level > 0:
            self.service_level -= 1
        return self.get_current_mode()

    def get_current_mode(self):
        modes = {
            3: {"mode": "full", "features": "所有功能可用"},
            2: {"mode": "reduced", "features": "僅核心功能，無 AI 建議"},
            1: {"mode": "minimal", "features": "唯讀模式，僅顯示既有資料"},
            0: {"mode": "offline", "features": "顯示離線提示"},
        }
        return modes.get(self.service_level, modes[0])

    def attempt_recovery(self):
        import random
        if random.random() > 0.5:
            self.service_level = min(self.service_level + 1, 3)
            return True
        return False

class ServiceOrchestrator:
    def __init__(self):
        self.services = {
            "ai_predict": {"available": True, "priority": 1},
            "data_sync": {"available": True, "priority": 2},
            "notification": {"available": True, "priority": 3},
        }

    def check_health(self):
        return [s for s, info in self.services.items() if info["available"]]

    def handle_failure(self, failed_service):
        self.services[failed_service]["available"] = False
        available = self.check_health()
        if len(available) <= 1:
            return "critical_degradation"
        return "partial_degradation"

    def recover(self, service):
        self.services[service]["available"] = True

orch = ServiceOrchestrator()
orch.handle_failure("ai_predict")
print("可用服務:", orch.check_health())
```

## 使用者導向錯誤訊息

```python
class UserFriendlyError:
    def __init__(self):
        self.error_db = {
            "network_timeout": {
                "title": "連線逾時",
                "detail": "無法連接到伺服器，請檢查網路連線",
                "action": "重試 / 切換到離線模式",
            },
            "model_failed": {
                "title": "AI 模型回應異常",
                "detail": "AI 暫時無法處理請求，請稍後再試",
                "action": "重新發送 / 切換到規則模式",
            },
            "invalid_input": {
                "title": "輸入格式錯誤",
                "detail": "請檢查輸入格式是否正確",
                "action": "查看格式範例 / 重新輸入",
            },
        }

    def get_error_message(self, error_code, context=None):
        error = self.error_db.get(error_code, {
            "title": "未知錯誤",
            "detail": "系統發生未預期的錯誤",
            "action": "重試 / 聯絡客服",
        })
        msg = f"❌ {error['title']}\n{error['detail']}"
        if context:
            msg += f"\n📋 上下文：{context}"
        msg += f"\n💡 建議操作：{error['action']}"
        return msg

    def suggest_recovery(self, error_code):
        strategies = {
            "network_timeout": ["retry", "offline_mode"],
            "model_failed": ["retry", "fallback_rule"],
            "invalid_input": ["show_example", "guided_input"],
        }
        return strategies.get(error_code, ["retry"])

handler = UserFriendlyError()
print(handler.get_error_message("model_failed", "文字分類請求"))
```

## 自動重試與回退

```python
import time
import random

class RetryStrategy:
    def __init__(self, max_retries=3, base_delay=1):
        self.max_retries = max_retries
        self.base_delay = base_delay

    def execute(self, func, *args, **kwargs):
        last_error = None
        for attempt in range(self.max_retries):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_error = e
                delay = self.base_delay * (2 ** attempt)
                print(f"第 {attempt + 1} 次重試，等待 {delay} 秒...")
                time.sleep(delay)
        raise last_error

def unstable_service():
    if random.random() < 0.6:
        raise ConnectionError("模擬連線失敗")
    return "success"

retry = RetryStrategy(max_retries=3)
try:
    result = retry.execute(unstable_service)
    print(f"結果：{result}")
except ConnectionError as e:
    print(f"最終失敗：{e}")
    print("已啟動離線模式")
```

---

**延伸閱讀**

- [Error Recovery in UX](https://www.google.com/search?q=error+recovery+UX+design+patterns)
- [Graceful Degradation Patterns](https://www.google.com/search?q=graceful+degradation+system+design)
- [Resilient AI Systems](https://www.google.com/search?q=resilient+AI+system+error+handling)
