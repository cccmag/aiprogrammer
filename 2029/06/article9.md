# 可及性與包容性設計

## 前言

真正的人機協作必須服務於**所有人**。可及性（Accessibility）與包容性設計（Inclusive Design）確保不同能力、不同背景的使用者都能平等地與 AI 協作。這不是附加功能，而是核心設計原則。

## 多通道輸出

### 視覺替代方案

資訊不應只依賴單一感官通道：

```python
class MultichannelOutput:
    def __init__(self):
        self.channels = {
            "visual": self._visual_output,
            "auditory": self._auditory_output,
            "text": self._text_output,
        }

    def _visual_output(self, data: str) -> str:
        return f"[圖表] {data}"

    def _auditory_output(self, data: str) -> str:
        return f"[語音] {data}"

    def _text_output(self, data: str) -> str:
        return f"[文字] {data}"

    def broadcast(self, data: str, preferred: str = None) -> dict:
        results = {}
        channels_to_use = [preferred] if preferred else self.channels.keys()
        for ch in channels_to_use:
            if ch in self.channels:
                results[ch] = self.channels[ch](data)
        return results

    def auto_select_channel(self, user_profile: dict) -> str:
        preferences = {
            "visually_impaired": "auditory",
            "hearing_impaired": "visual",
            "dyslexic": "auditory",
            "default": "text",
        }
        return preferences.get(
            user_profile.get("condition", "default"), "text"
        )
```

## 語言包容性

### 多語言與簡潔表達

AI 應支援多語言並避免專業術語：

```python
class InclusiveLanguageProcessor:
    def __init__(self):
        self.translations = {
            "zh-TW": {"hello": "你好", "error": "錯誤", "confirm": "確認"},
            "en": {"hello": "Hello", "error": "Error", "confirm": "Confirm"},
            "vi": {"hello": "Xin chào", "error": "Lỗi", "confirm": "Xác nhận"},
        }
        self.jargon_alternatives = {
            "實例化": "建立",
            "迭代": "重複處理",
            "非同步": "背景執行",
            "遞迴": "自我呼叫",
        }

    def process_message(self, message: str, lang: str = "zh-TW") -> str:
        processed = message
        for jargon, plain in self.jargon_alternatives.items():
            processed = processed.replace(jargon, plain)
        return processed

    def greet(self, lang: str) -> str:
        return self.translations.get(lang, self.translations["en"]).get("hello", "Hello")
```

## 認知負載管理

### 簡化與分階

不同使用者的認知能力差異很大：

```python
class CognitiveLoadManager:
    def __init__(self):
        self.load_levels = {"low", "medium", "high"}
        self.current_load = "low"

    def assess_load(self, user_actions: List[str], time_spent: float) -> str:
        action_rate = len(user_actions) / max(time_spent, 1)
        if action_rate > 5:
            return "high"
        elif action_rate > 2:
            return "medium"
        return "low"

    def simplify_ui(self, current_load: str) -> dict:
        configs = {
            "high": {
                "visible_elements": 3,
                "auto_complete": True,
                "confirmation_dialogs": False,
                "font_size": "large",
            },
            "medium": {
                "visible_elements": 7,
                "auto_complete": True,
                "confirmation_dialogs": True,
                "font_size": "normal",
            },
            "low": {
                "visible_elements": 12,
                "auto_complete": False,
                "confirmation_dialogs": True,
                "font_size": "normal",
            },
        }
        return configs.get(current_load, configs["low"])

    def adapt_difficulty(self, error_rate: float) -> str:
        if error_rate > 0.3:
            self.current_load = self._reduce_complexity()
        elif error_rate < 0.1:
            self.current_load = self._increase_complexity()
        return self.current_load

    def _reduce_complexity(self) -> str:
        return "low"

    def _increase_complexity(self) -> str:
        return "medium"
```

## 自適應輸入法

### 多種輸入替代方案

支援不同的輸入偏好與限制：

```python
class AdaptiveInputMethod:
    def __init__(self):
        self.methods = {
            "keyboard": self._keyboard_input,
            "voice": self._voice_input,
            "switch": self._switch_input,
            "eye_tracking": self._eye_tracking_input,
        }

    def _keyboard_input(self, text: str) -> str:
        return f"鍵盤輸入：{text}"

    def _voice_input(self, text: str) -> str:
        return f"語音輸入：{text}"

    def _switch_input(self, text: str) -> str:
        words = text.split()
        return f"切換輸入：{' → '.join(w + '[選取]' for w in words)}"

    def _eye_tracking_input(self, text: str) -> str:
        chars = list(text)
        return f"視線輸入：{' '.join(f'{c}[凝視0.5秒]' for c in chars)}"

    def get_available_methods(self, user_capabilities: dict) -> List[str]:
        available = []
        if user_capabilities.get("can_type", True):
            available.append("keyboard")
        if user_capabilities.get("can_speak", True):
            available.append("voice")
        if user_capabilities.get("needs_switch", False):
            available.append("switch")
        if user_capabilities.get("can_use_eyes", True):
            available.append("eye_tracking")
        return available

    def input_with_method(self, method: str, text: str) -> str:
        handler = self.methods.get(method, self._keyboard_input)
        return handler(text)
```

## WCAG 遵循檢查

### 自動可及性檢測

```python
class AccessibilityChecker:
    def __init__(self):
        self.checks = {
            "contrast_ratio": self._check_contrast,
            "keyboard_nav": self._check_keyboard,
            "alt_text": self._check_alt_text,
            "aria_labels": self._check_aria,
        }

    def _check_contrast(self, ui_config: dict) -> bool:
        fg, bg = ui_config.get("foreground", "#000"), ui_config.get("background", "#FFF")
        return True

    def _check_keyboard(self, interactive_elements: List[str]) -> List[str]:
        missing = [e for e in interactive_elements if not e.startswith("btn_")]
        return missing if missing else []

    def _check_alt_text(self, images: List[str]) -> List[str]:
        missing = [img for img in images if not img]
        return missing

    def _check_aria(self, elements: dict) -> List[str]:
        issues = []
        for elem_id, attrs in elements.items():
            if attrs.get("role") and "aria-label" not in attrs:
                issues.append(f"{elem_id} 缺少 aria-label")
        return issues

    def run_all_checks(self, ui: dict) -> dict:
        results = {}
        for name, check in self.checks.items():
            results[name] = check(ui)
        return results
```

## 結語

可及性與包容性不是功能檢查清單，而是設計思維的轉變。當我們為**邊緣案例**設計時，往往會發現這些設計讓**所有使用者**都受益。語音輸出幫助視障者，也方便駕駛中的使用者；簡潔語言幫助失讀症患者，也讓所有人更快理解。

---

**延伸閱讀**

- [WCAG 2.2 標準](https://www.google.com/search?q=WCAG+2.2+accessibility+standards)
- [包容性設計方法論](https://www.google.com/search?q=inclusive+design+methodology)
- [認知無障礙設計](https://www.google.com/search?q=cognitive+accessibility+design+patterns)
