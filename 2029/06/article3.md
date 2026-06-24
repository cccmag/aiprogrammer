# 自適應介面設計

## 前言

每位使用者的操作習慣、認知能力與使用情境都不相同。自適應介面（Adaptive Interface）能根據使用者的行為模式和上下文動態調整佈局與功能，提升協作效率。

## 使用者模型

### 行為追蹤基礎

自適應介面的前提是建立**使用者模型**（User Model）：

```python
import json
from collections import defaultdict
from datetime import datetime, timedelta

class UserModel:
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.feature_usage = defaultdict(int)
        self.error_count = defaultdict(int)
        self.session_times = []

    def log_action(self, feature: str, success: bool):
        self.feature_usage[feature] += 1
        if not success:
            self.error_count[feature] += 1

    def log_session(self, duration_minutes: float):
        self.session_times.append(duration_minutes)
        if len(self.session_times) > 50:
            self.session_times.pop(0)

    def get_frequent_features(self, top_n: int = 5) -> list:
        return sorted(
            self.feature_usage, key=self.feature_usage.get, reverse=True
        )[:top_n]

    def get_error_rate(self, feature: str) -> float:
        total = self.feature_usage.get(feature, 0)
        if total == 0:
            return 0.0
        return self.error_count.get(feature, 0) / total
```

## 適應性演算法

### 功能推薦

根據使用行為推薦最相關的功能按鈕：

```python
class AdaptiveLayout:
    def __init__(self):
        self.button_priority = {}

    def update_priority(self, user_model: UserModel):
        frequent = user_model.get_frequent_features(10)
        self.button_priority = {
            f: 1.0 - user_model.get_error_rate(f)
            for f in frequent
        }

    def get_layout(self, max_buttons: int = 5) -> list:
        return sorted(
            self.button_priority, key=self.button_priority.get, reverse=True
        )[:max_buttons]

    def render(self):
        layout = self.get_layout()
        print("=== 自適應工具列 ===")
        for i, btn in enumerate(layout, 1):
            bar = "█" * int(self.button_priority[btn] * 20)
            print(f"{i}. [{bar}] {btn}")
```

## 難度動態調整

### 漸進式挑戰

對於學習型任務，系統應動態調整難度：

```python
class AdaptiveDifficulty:
    def __init__(self, initial_level: float = 0.3):
        self.level = initial_level
        self.consecutive_success = 0
        self.consecutive_fail = 0

    def update(self, success: bool):
        if success:
            self.consecutive_success += 1
            self.consecutive_fail = 0
            if self.consecutive_success >= 3:
                self.level = min(1.0, self.level + 0.1)
                self.consecutive_success = 0
        else:
            self.consecutive_fail += 1
            self.consecutive_success = 0
            if self.consecutive_fail >= 2:
                self.level = max(0.1, self.level - 0.15)
                self.consecutive_fail = 0
        return self.level

    def generate_task(self) -> dict:
        complexity = int(self.level * 10)
        return {
            "prompt": f"任務難度等級 {complexity}",
            "time_limit": max(10, 60 - int(self.level * 40)),
            "hints_enabled": self.level < 0.4,
        }

ad = AdaptiveDifficulty()
for result in [True, True, True, False, False, True]:
    level = ad.update(result)
    task = ad.generate_task()
    print(f"成功={result}, 等級={level:.1f}, 任務={task}")
```

## 上下文感知

### 情境偵測

根據時間、地點、裝置等上下文調整介面：

```python
class ContextAwareAdapter:
    def __init__(self):
        self.contexts = {}

    def detect_context(self, hour: int, device: str, location: str) -> str:
        if 8 <= hour <= 17 and device == "desktop":
            return "work"
        elif 18 <= hour <= 23 and device == "mobile":
            return "leisure"
        elif location == "meeting_room":
            return "presentation"
        return "general"

    def adapt(self, context: str) -> dict:
        configs = {
            "work": {"font_size": 12, "sidebar": True, "notifications": "all"},
            "leisure": {"font_size": 16, "sidebar": False, "notifications": "important"},
            "presentation": {"font_size": 24, "sidebar": False, "notifications": "none"},
            "general": {"font_size": 14, "sidebar": True, "notifications": "all"},
        }
        return configs.get(context, configs["general"])

caa = ContextAwareAdapter()
ctx = caa.detect_context(14, "desktop", "office")
print(f"情境：{ctx}, 配置：{caa.adapt(ctx)}")
ctx2 = caa.detect_context(21, "mobile", "home")
print(f"情境：{ctx2}, 配置：{caa.adapt(ctx2)}")
```

## 結語

自適應介面透過使用者模型、動態難度調整與上下文感知，讓系統能夠「理解」使用者的需求並主動調整。好的自適應設計不會讓使用者察覺到變化——它只是讓操作變得「自然而然」更順暢。

---

**延伸閱讀**

- [自適應介面設計原則](https://www.google.com/search?q=adaptive+user+interface+design+principles)
- [使用者行為建模](https://www.google.com/search?q=user+behavior+modeling+HCI)
- [情境感知計算](https://www.google.com/search?q=context+aware+computing+adaptive+systems)
