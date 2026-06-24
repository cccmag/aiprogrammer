# 錯誤恢復設計

## 前言

在人機協作中，錯誤不可避免——無論是人類誤操作還是 AI 誤判。關鍵不在於避免所有錯誤，而在於設計**優雅的錯誤恢復**（Error Recovery）機制。好的恢復設計能將一次錯誤轉化為學習機會。

## 錯誤分類

### 類型與嚴重程度

```python
import enum
from dataclasses import dataclass
from typing import Optional

class ErrorSeverity(enum.Enum):
    COSMETIC = 1
    MINOR = 2
    MAJOR = 3
    CRITICAL = 4

class ErrorType(enum.Enum):
    MISINTERPRETATION = "誤解"
    WRONG_OUTPUT = "錯誤輸出"
    TIMEOUT = "超時"
    RESOURCE_EXHAUSTION = "資源耗盡"
    USER_MISTAKE = "使用者錯誤"

@dataclass
class AIError:
    error_type: ErrorType
    severity: ErrorSeverity
    message: str
    context: str
    recoverable: bool = True
    recovery_suggestion: Optional[str] = None
```

## 復原機制

### 通用復原框架

不同類型的錯誤需要不同的復原策略：

```python
class ErrorRecoveryFramework:
    def __init__(self):
        self.history = []
        self.checkpoints = []

    def create_checkpoint(self, state: dict) -> int:
        cp_id = len(self.checkpoints)
        self.checkpoints.append(state.copy())
        return cp_id

    def rollback(self, checkpoint_id: int) -> dict:
        if 0 <= checkpoint_id < len(self.checkpoints):
            return self.checkpoints[checkpoint_id].copy()
        return {}

    def handle_error(self, error: AIError) -> str:
        self.history.append(error)
        handlers = {
            ErrorType.MISINTERPRETATION: self._handle_misinterpretation,
            ErrorType.WRONG_OUTPUT: self._handle_wrong_output,
            ErrorType.TIMEOUT: self._handle_timeout,
            ErrorType.USER_MISTAKE: self._handle_user_mistake,
        }
        handler = handlers.get(error.error_type, self._handle_generic)
        return handler(error)

    def _handle_misinterpretation(self, error: AIError) -> str:
        return (f"我誤解了您的意思。您說的是「{error.context}」"
                f"對嗎？請重新描述，我會仔細確認。")

    def _handle_wrong_output(self, error: AIError) -> str:
        return (f"抱歉產生錯誤輸出。已記錄此問題，"
                f"建議方案：{error.recovery_suggestion}")

    def _handle_timeout(self, error: AIError) -> str:
        return "處理時間過長，已自動中止。請簡化您的請求後重試。"

    def _handle_user_mistake(self, error: AIError) -> str:
        return f"操作提示：{error.recovery_suggestion}（錯誤代碼：{error.message}）"

    def _handle_generic(self, error: AIError) -> str:
        return f"發生錯誤：{error.message}，建議重新操作"
```

## 自動糾正

### 預測與修正

AI 應能預測常見錯誤並主動修正：

```python
class AutoCorrector:
    def __init__(self):
        self.correction_rules = {
            "missing_dot": (r"\w\s+\w", lambda m: m.group(0).replace(" ", ".")),
            "double_space": (r"\s{2,}", lambda m: " "),
            "common_typo": {
                "teh": "the", "recieve": "receive",
                "occurrance": "occurrence",
            },
        }
        self.applied_count = 0

    def auto_correct(self, text: str) -> tuple:
        import re
        corrections = []
        corrected = text

        for typo, correct in self.correction_rules["common_typo"].items():
            if typo in corrected:
                corrected = corrected.replace(typo, correct)
                corrections.append(f"{typo}→{correct}")

        for rule_name, (pattern, replacer) in self.correction_rules.items():
            if rule_name == "common_typo":
                continue
            matches = re.findall(pattern, corrected)
            if matches:
                corrected = re.sub(pattern, replacer, corrected)
                corrections.append(f"{rule_name}: {len(matches)} 處修正")

        return corrected, corrections

ac = AutoCorrector()
text = "teh  quick  brown fox"
corrected, fixes = ac.auto_correct(text)
print(f"原始：{text}")
print(f"修正：{corrected}")
for f in fixes:
    print(f"  - {f}")
```

## 優雅降級

### 功能逐步簡化

當系統發生錯誤時，不應直接崩潰，而應降級運行：

```python
class GracefulDegradation:
    def __init__(self):
        self.feature_matrix = {
            "full": {"speed": "fast", "accuracy": "high", "features": "all"},
            "reduced": {"speed": "medium", "accuracy": "medium", "features": "core"},
            "minimal": {"speed": "slow", "accuracy": "low", "features": "essential"},
            "fallback": {"speed": "fast", "accuracy": "basic", "features": "text_only"},
        }
        self.current_mode = "full"

    def degrade(self, error_cause: str) -> str:
        order = ["full", "reduced", "minimal", "fallback"]
        idx = order.index(self.current_mode)
        if idx < len(order) - 1:
            self.current_mode = order[idx + 1]
        config = self.feature_matrix[self.current_mode]
        return (f"因 {error_cause}，系統降級至「{self.current_mode}」模式："
                f"速度={config['speed']}, 準確度={config['accuracy']}")

    def attempt_restore(self) -> bool:
        import random
        if random.random() < 0.3:
            self.current_mode = "full"
            return True
        return False
```

## 錯誤報告

### 結構化回饋

錯誤發生後應收集結構化資訊以持續改進：

```python
class ErrorReporter:
    def __init__(self):
        self.error_log = []

    def report(self, error: AIError, recovery_result: str):
        entry = {
            "timestamp": __import__("datetime").datetime.now().isoformat(),
            "type": error.error_type.value,
            "severity": error.severity.name,
            "context": error.context,
            "recovery": recovery_result,
        }
        self.error_log.append(entry)
        return entry

    def get_statistics(self) -> dict:
        stats = {"total": len(self.error_log), "by_type": {}, "by_severity": {}}
        for entry in self.error_log:
            t = entry["type"]
            stats["by_type"][t] = stats["by_type"].get(t, 0) + 1
            s = entry["severity"]
            stats["by_severity"][s] = stats["by_severity"].get(s, 0) + 1
        return stats
```

## 結語

錯誤恢復設計的黃金法則是：**永遠不要讓使用者面對無法挽回的情況**。透過分級復原、自動糾正、優雅降級與結構化回饋，每一次錯誤都可以轉化為更順暢的協作體驗。

---

**延伸閱讀**

- [人機互動錯誤恢復模式](https://www.google.com/search?q=error+recovery+HCI+design+patterns)
- [自動錯誤修正技術](https://www.google.com/search?q=automatic+error+correction+NLP+2026)
- [優雅降級系統設計](https://www.google.com/search?q=graceful+degradation+system+design)
