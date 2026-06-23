# 自適應介面設計

## 前言

自適應介面能根據使用者行為、偏好和上下文動態調整呈現方式，提升人機協作效率。本文探討自適應介面的核心設計模式與 Python 實作。

## 行為追蹤與分析

```python
from collections import defaultdict
import time

class UserBehaviorTracker:
    def __init__(self):
        self.sessions = defaultdict(list)
        self.preferences = {}

    def log_action(self, user_id, action, context=None):
        self.sessions[user_id].append({
            "action": action,
            "context": context or {},
            "timestamp": time.time(),
        })

    def get_most_used_action(self, user_id, window=3600):
        sessions = self.sessions.get(user_id, [])
        recent = [s for s in sessions
                  if time.time() - s["timestamp"] < window]
        if not recent:
            return None
        counts = defaultdict(int)
        for s in recent:
            counts[s["action"]] += 1
        return max(counts, key=counts.get)

    def infer_preference(self, user_id):
        actions = self.sessions.get(user_id, [])
        if not actions:
            return {}
        shortcuts = sum(1 for a in actions if a["action"] == "shortcut")
        menu_clicks = sum(1 for a in actions if a["action"] == "menu_click")
        if shortcuts > menu_clicks:
            return {"interface": "compact", "show_shortcuts": True}
        return {"interface": "detailed", "show_shortcuts": False}

tracker = UserBehaviorTracker()
tracker.log_action("user1", "shortcut", {"key": "Ctrl+S"})
tracker.log_action("user1", "shortcut", {"key": "Ctrl+Z"})
tracker.log_action("user1", "menu_click", {"item": "file"})
print(tracker.infer_preference("user1"))
print(tracker.get_most_used_action("user1"))
```

## 動態佈局調整

```python
class AdaptiveLayout:
    def __init__(self):
        self.panels = {
            "nav": {"active": True, "weight": 1},
            "content": {"active": True, "weight": 3},
            "sidebar": {"active": True, "weight": 1},
            "toolbar": {"active": True, "weight": 0.5},
        }

    def adjust_by_role(self, role):
        configs = {
            "developer": {"nav": False, "sidebar": True, "toolbar": True},
            "analyst": {"nav": True, "sidebar": True, "toolbar": False},
            "viewer": {"nav": True, "sidebar": False, "toolbar": False},
        }
        config = configs.get(role, {})
        for panel, active in config.items():
            if panel in self.panels:
                self.panels[panel]["active"] = active
        return self.get_layout()

    def adjust_by_device(self, device_type):
        if device_type == "mobile":
            for p in self.panels:
                self.panels[p]["active"] = p == "content"
        elif device_type == "tablet":
            self.panels["sidebar"]["active"] = False
        return self.get_layout()

    def get_layout(self):
        return {k: v for k, v in self.panels.items() if v["active"]}

layout = AdaptiveLayout()
print("開發者模式:", layout.adjust_by_role("developer"))
print("行動裝置:", layout.adjust_by_device("mobile"))
```

## 內容難度自適應

```python
class DifficultyAdapter:
    def __init__(self):
        self.levels = {1: "beginner", 2: "intermediate", 3: "advanced"}
        self.user_progress = {}

    def assess_level(self, user_id, correct, total):
        if total == 0:
            return 1
        accuracy = correct / total
        if accuracy > 0.8:
            self.user_progress[user_id] = min(
                self.user_progress.get(user_id, 1) + 1, 3
            )
        elif accuracy < 0.4:
            self.user_progress[user_id] = max(
                self.user_progress.get(user_id, 1) - 1, 1
            )
        return self.user_progress.get(user_id, 1)

    def get_content_prompt(self, user_id, base_content):
        level = self.user_progress.get(user_id, 1)
        level_name = self.levels.get(level, "beginner")
        prefixes = {
            "beginner": "[入門] ",
            "intermediate": "[進階] ",
            "advanced": "[專家] ",
        }
        return prefixes[level_name] + base_content

adapter = DifficultyAdapter()
user = "alice"
for correct, total in [(5, 5), (4, 5), (1, 5), (2, 5)]:
    level = adapter.assess_level(user, correct, total)
    prompt = adapter.get_content_prompt(user, "Python 自適應介面教學")
    print(f"答對率 {correct}/{total} -> 等級 {level}, {prompt}")
```

---

**延伸閱讀**

- [Adaptive User Interfaces](https://www.google.com/search?q=adaptive+user+interface+design+patterns)
- [Context-Aware Computing](https://www.google.com/search?q=context+aware+computing+adaptive+systems)
- [Dynamic Layout Adaptation](https://www.google.com/search?q=dynamic+layout+adaptation+UI+design)
