# 信任與透明度設計（2023-2029）

## 看不見的設計要素

信任是 AI 介面中最關鍵卻最容易被忽略的設計維度。沒有信任，再強大的功能也不會被採用。

### 透明度的三個層次

```python
class TransparencyLayer:
    def __init__(self):
        self.confidence: float = 0.0
        self.reasoning_path: list[str] = []
        self.uncertainty_bounds: tuple[float, float] = (0.0, 0.0)
        self.data_sources: list[str] = []

    def explain(self, level: str) -> str:
        explanations = {
            "low": f"信心度：{self.confidence:.0%}",
            "medium": f"信心度：{self.confidence:.0%}\n"
                      f"推論路徑：{'→'.join(self.reasoning_path[-3:])}",
            "high": f"信心度：{self.confidence:.0%} (±{self._uncertainty():.1%})\n"
                    f"完整推理：{'→'.join(self.reasoning_path)}\n"
                    f"資料來源：{', '.join(self.data_sources)}"
        }
        return explanations.get(level, explanations["low"])

    def _uncertainty(self) -> float:
        return self.uncertainty_bounds[1] - self.uncertainty_bounds[0]
```

參見：[AI 可解釋性研究](https://www.google.com/search?q=AI+explainability+trust+interface+design)

### 信任校準

信任不是越高越好，而是要「校準」——使用者對 AI 的信任程度應與 AI 的實際能力匹配：

```python
class TrustCalibrator:
    def __init__(self):
        self.actual_accuracy: float = 0.85
        self.user_trust: float = 0.5

    def show_confidence(self, prediction: str, confidence: float) -> str:
        if confidence > self.actual_accuracy + 0.1:
            return f"【高信心】{prediction}（但請注意，我有時會出錯）"
        if confidence < self.actual_accuracy - 0.2:
            return f"【低信心】可能是「{prediction}」，建議您手動確認"
        return f"【中等信心】我認為是「{prediction}」"

    def update_user_trust(self, feedback: bool):
        if feedback:
            self.user_trust = min(1.0, self.user_trust + 0.1)
        else:
            self.user_trust = max(0.0, self.user_trust - 0.2)

    def is_calibrated(self) -> bool:
        return abs(self.user_trust - self.actual_accuracy) < 0.15
```

### 可撤銷性設計

使用者必須能隨時撤銷 AI 的決策：

```python
class UndoSystem:
    def __init__(self):
        self.stack: list[dict] = []

    def apply(self, action: dict):
        self.stack.append(action)
        self._execute(action)

    def undo(self) -> bool:
        if not self.stack:
            return False
        action = self.stack.pop()
        self._reverse(action)
        return True

    def _execute(self, a: dict):
        print(f"執行：{a['type']} — {a.get('desc', '')}")

    def _reverse(self, a: dict):
        print(f"復原：{a['type']} — {a.get('desc', '')}")

    def preview_undo(self) -> str | None:
        if self.stack:
            return f"將復原：{self.stack[-1].get('desc', '上一步')}"
        return None
```

### 信任建立策略

| 策略 | 做法 | 效果 |
|------|------|------|
| **透明度** | 顯示推論過程與信心度 | 增加可預測性 |
| **可控制性** | 使用者可調整 AI 行為 | 增加掌控感 |
| **一致性** | 相同輸入產生相同輸出 | 建立可靠印象 |
| **容錯設計** | 優雅處理錯誤 | 減少挫敗感 |
| **漸進授權** | 從低風險任務開始建立信任 | 逐步累積信任 |

### 透明度設計模式

```python
class ConfidenceDisplay:
    def visualize(self, conf: float) -> str:
        bar = "█" * int(conf * 20)
        space = " " * (20 - int(conf * 20))
        label = "高" if conf > 0.8 else ("中" if conf > 0.4 else "低")
        return f"[{bar}{space}] {label} ({conf:.0%})"
```

參見：
- [AI 信任度校準](https://www.google.com/search?q=trust+calibration+human+AI+interaction)
- [可解釋 AI 設計](https://www.google.com/search?q=explainable+AI+design+patterns)
- [撤銷機制設計](https://www.google.com/search?q=undo+system+AI+interface+design)

## 結語

信任不是憑空產生的，而是透過每一次透明、一致、可控制的互動逐步累積而成。

---

*本篇文章為「AI 程式人雜誌 2026 年 9 月號」人機協作介面設計系列之六。*
