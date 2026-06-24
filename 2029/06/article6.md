# 信任建立機制

## 前言

人機協作的成敗取決於**信任**。當使用者不信任 AI 時，會不斷覆核、確認甚至拒絕 AI 的建議，失去了協作的意義。信任不是與生俱來的，而是透過設計逐步建立的。

## 信任的維度

### 能力、可靠度與善意

信任可拆分為三個核心維度：

```python
class TrustModel:
    def __init__(self):
        self.competence = 0.5
        self.reliability = 0.5
        self.benevolence = 0.5
        self.alpha = 0.1

    def update_competence(self, success: bool):
        delta = self.alpha if success else -self.alpha * 2
        self.competence = max(0, min(1, self.competence + delta))

    def update_reliability(self, consistent: bool):
        delta = self.alpha if consistent else -self.alpha * 3
        self.reliability = max(0, min(1, self.reliability + delta))

    def update_benevolence(self, helpful: bool):
        delta = self.alpha if helpful else -self.alpha
        self.benevolence = max(0, min(1, self.benevolence + delta))

    def overall_trust(self) -> float:
        return (self.competence * 0.5 +
                self.reliability * 0.3 +
                self.benevolence * 0.2)

    def should_trust(self, threshold: float = 0.6) -> tuple:
        score = self.overall_trust()
        return score >= threshold, score
```

## 信心校準

### 不確定性表達

AI 需要準確表達自己的信心程度：

```python
class ConfidenceCalibrator:
    def __init__(self):
        self.level_labels = {
            0.9: "非常有信心",
            0.7: "有一定的把握",
            0.5: "不太確定",
            0.3: "建議人工確認",
            0.0: "無法判斷",
        }

    def predict_with_confidence(self, input_data: str) -> tuple:
        confidence = self._estimate_confidence(input_data)
        prediction = self._predict(input_data)
        label = self._get_label(confidence)
        return prediction, confidence, label

    def _estimate_confidence(self, data: str) -> float:
        if len(data) < 3:
            return 0.3
        if data.isnumeric():
            return 0.9
        return 0.7

    def _predict(self, data: str) -> str:
        return f"預測結果：{data}"

    def _get_label(self, confidence: float) -> str:
        for threshold, label in sorted(self.level_labels.items(), reverse=True):
            if confidence >= threshold:
                return label
        return self.level_labels[0.0]

cc = ConfidenceCalibrator()
pred, conf, label = cc.predict_with_confidence("42")
print(f"{pred}（信心：{conf:.1f}，{label}）")
```

## 漸進式授權

### 由淺入深的信任建立

不應一開始就賦予 AI 完整權限：

```python
class ProgressiveAuthorization:
    def __init__(self):
        self.levels = {
            "observe": 0,
            "suggest": 1,
            "auto_with_confirm": 2,
            "auto": 3,
        }
        self.current_level = "observe"
        self.success_count = 0

    def authorize(self, action: str) -> str:
        action_level = self.levels.get(action, 0)
        if action_level <= self.levels[self.current_level]:
            return f"已授權執行 {action}"
        return f"需要升級權限至 {action}，目前為 {self.current_level}"

    def record_outcome(self, success: bool):
        if success:
            self.success_count += 1
            if self.success_count >= 5 and self.current_level == "observe":
                self.current_level = "suggest"
            elif self.success_count >= 15 and self.current_level == "suggest":
                self.current_level = "auto_with_confirm"
            elif self.success_count >= 30 and self.current_level == "auto_with_confirm":
                self.current_level = "auto"
        else:
            self.success_count = max(0, self.success_count - 3)
```

## 可預測性設計

### 保持一致的行為模式

可預測性直接影響信任感：

```python
class BehaviorPredictor:
    def __init__(self):
        self.patterns = {}

    def record_pattern(self, context: str, action: str):
        if context not in self.patterns:
            self.patterns[context] = {}
        self.patterns[context][action] = self.patterns[context].get(action, 0) + 1

    def predict_action(self, context: str) -> str:
        if context not in self.patterns:
            return "default"
        return max(self.patterns[context], key=self.patterns[context].get)

    def consistency_score(self, context: str, expected_action: str) -> float:
        if context not in self.patterns:
            return 0.5
        total = sum(self.patterns[context].values())
        freq = self.patterns[context].get(expected_action, 0)
        return freq / total if total > 0 else 0.5
```

## 失誤補償

### 信任修復機制

犯錯後如何修復信任是關鍵：

```python
class TrustRepair:
    def __init__(self):
        self.repair_actions = [
            "apologize", "explain", "offer_alternative", "learn_from_error"
        ]

    def handle_error(self, error_type: str) -> List[str]:
        responses = {
            "false_positive": [
                "抱歉，我誤判了這個情況",
                "以下是判斷過程的詳細原因",
                "建議改為以下方案",
                "已記錄此案例以避免再次發生",
            ],
            "missed_detection": [
                "抱歉，我遺漏了這個項目",
                "下次會加強這個方向的監控",
            ],
        }
        return responses.get(error_type, ["抱歉發生錯誤"])

    def calculate_repair_effectiveness(self, trust_before: float, trust_after: float) -> float:
        return (trust_after - trust_before) / max(1 - trust_before, 0.01)
```

## 結語

信任建立不是一蹴可幾的工程問題，而是持續的關係經營。透過信心校準、漸進式授權、可預測性設計與失誤補償，系統可以在每一次互動中逐步累積使用者的信賴。

---

**延伸閱讀**

- [人機信任模型研究](https://www.google.com/search?q=human+AI+trust+model+calibration)
- [漸進式自動化授權](https://www.google.com/search?q=progressive+automation+trust+levels)
- [AI 失誤修復策略](https://www.google.com/search?q=AI+error+recovery+trust+repair)
