# 可及性與包容性設計

## 前言

可及性設計確保所有人（包括身障使用者）都能有效使用 AI 系統。包容性設計則考慮多元文化、語言和背景的使用者需求。兩者相輔相成，是人機協作介面的重要組成。

## 螢幕閱讀器支援

```python
class AccessibleElement:
    def __init__(self, role, label, description=""):
        self.role = role
        self.label = label
        self.description = description
        self.focused = False

    def to_aria(self):
        return {
            "role": self.role,
            "aria-label": self.label,
            "aria-description": self.description,
        }

    def speak(self):
        text = self.label
        if self.description:
            text += f"。{self.description}"
        return text

class ScreenReader:
    def __init__(self):
        self.focus_queue = []

    def register(self, element):
        self.focus_queue.append(element)

    def announce(self, element):
        return f"[朗讀] {element.speak()}"

    def navigate_next(self):
        if self.focus_queue:
            current = self.focus_queue.pop(0)
            return self.announce(current)
        return "沒有更多元素"

button = AccessibleElement("button", "送出表單", "點擊後提交您的資料")
slider = AccessibleElement("slider", "調整音量", "左右滑動調整音量大小")
reader = ScreenReader()
reader.register(button)
reader.register(slider)
print(reader.navigate_next())
print(reader.navigate_next())
```

## 多語言支援

```python
class I18nManager:
    def __init__(self):
        self.translations = {
            "zh-TW": {
                "welcome": "歡迎使用人機協作系統",
                "confirm": "確認",
                "cancel": "取消",
                "error": "發生錯誤",
                "retry": "重試",
            },
            "en": {
                "welcome": "Welcome to the Human-AI Collaboration System",
                "confirm": "Confirm",
                "cancel": "Cancel",
                "error": "An error occurred",
                "retry": "Retry",
            },
        }

    def get_text(self, key, lang="zh-TW"):
        return self.translations.get(lang, {}).get(key, key)

    def detect_language(self, text):
        import re
        if re.search(r'[\u4e00-\u9fff]', text):
            return "zh-TW"
        return "en"

class InclusiveInterface:
    def __init__(self):
        self.i18n = I18nManager()
        self.font_size = 16
        self.high_contrast = False
        self.lang = "zh-TW"

    def set_font_size(self, size):
        self.font_size = max(12, min(size, 32))

    def toggle_contrast(self):
        self.high_contrast = not self.high_contrast

    def render(self):
        theme = "高對比模式" if self.high_contrast else "普通模式"
        lang_name = "繁體中文" if self.lang == "zh-TW" else "English"
        return {
            "text": self.i18n.get_text("welcome", self.lang),
            "font_size": f"{self.font_size}px",
            "theme": theme,
            "language": lang_name,
        }

    def get_shortcuts(self):
        shortcuts = {
            "Ctrl++": "放大字體",
            "Ctrl+-": "縮小字體",
            "Ctrl+H": "切換高對比",
            "Ctrl+L": "切換語言",
        }
        return shortcuts

interface = InclusiveInterface()
print(interface.render())
```

## 認知負荷管理

```python
class CognitiveLoadManager:
    def __init__(self):
        self.complexity = {
            "simple": {"info_density": 0.3, "max_options": 3, "use_icons": True},
            "moderate": {"info_density": 0.6, "max_options": 5, "use_icons": True},
            "complex": {"info_density": 1.0, "max_options": 10, "use_icons": False},
        }

    def assess_user(self, expertise, fatigue_level):
        if expertise == "beginner" or fatigue_level > 7:
            return "simple"
        elif expertise == "intermediate":
            return "moderate"
        return "complex"

    def simplify_content(self, content, level):
        config = self.complexity.get(level, self.complexity["simple"])
        if config["info_density"] < 0.5:
            content = content[:100]
        return {
            "content": content,
            "max_options": config["max_options"],
            "show_icons": config["use_icons"],
        }

    def suggest_break(self, session_duration_minutes):
        if session_duration_minutes > 45:
            return "建議休息一下，連續操作超過 45 分鐘可能影響判斷力"
        return ""

load = CognitiveLoadManager()
level = load.assess_user("beginner", 8)
print(f"建議介面複雜度：{level}")
print(load.simplify_content("這是一段很長的操作說明..." * 10, level))
print(load.suggest_break(50))
```

---

**延伸閱讀**

- [Accessible AI Design](https://www.google.com/search?q=accessible+AI+design+guidelines+WCAG)
- [Inclusive Human-AI Interaction](https://www.google.com/search?q=inclusive+human+AI+interaction+design)
- [Cognitive Load in UI Design](https://www.google.com/search?q=cognitive+load+UX+design+guidelines)
