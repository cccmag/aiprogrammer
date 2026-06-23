# 信任建立機制

## 前言

信任是人機協作的基石。當使用者信任 AI 系統時，更願意採納建議、分享資訊並長期使用。本文探討如何透過介面設計建立並維持使用者信任。

## 可解釋性模組

```python
class ExplanationEngine:
    def __init__(self):
        self.decision_log = []

    def recommend(self, item, user_profile, reason):
        entry = {
            "item": item,
            "user_profile": user_profile,
            "reason": reason,
            "confidence": self.calculate_confidence(user_profile, reason),
        }
        self.decision_log.append(entry)
        return entry

    def calculate_confidence(self, profile, reason):
        score = 0.5
        if profile.get("history", 0) > 10:
            score += 0.2
        if reason in ("preference", "trending"):
            score += 0.15
        return min(score, 1.0)

    def explain(self, decision_id):
        entry = self.decision_log[decision_id]
        return (
            f"推薦 {entry['item']} 的原因是：{entry['reason']}\n"
            f"信心度：{entry['confidence']:.0%}\n"
            f"您的偏好設定：{entry['user_profile']}"
        )

    def show_relevant_factors(self, decision_id):
        entry = self.decision_log[decision_id]
        factors = {
            "您的瀏覽歷史": 4,
            "同類型使用者偏好": 3,
            "近期熱門項目": 2,
        }
        return sorted(factors.items(), key=lambda x: -x[1])

engine = ExplanationEngine()
decision = engine.recommend("Python 課程", {"history": 15}, "preference")
print(engine.explain(0))
```

## 信心度指示器

```python
class ConfidenceIndicator:
    def __init__(self, threshold_low=0.4, threshold_high=0.8):
        self.thresholds = (threshold_low, threshold_high)

    def get_level(self, confidence):
        if confidence >= self.thresholds[1]:
            return "high"
        elif confidence >= self.thresholds[0]:
            return "medium"
        return "low"

    def format_display(self, confidence):
        level = self.get_level(confidence)
        displays = {
            "high": "🟢 高信心度 — 建議可直接採用",
            "medium": "🟡 中等信心度 — 建議人工審閱",
            "low": "🔴 低信心度 — 建議人工處理",
        }
        return displays[level]

    def should_delegate(self, confidence):
        level = self.get_level(confidence)
        return level == "high"

class TrustAwareSystem:
    def __init__(self):
        self.indicator = ConfidenceIndicator()
        self.override_count = 0
        self.follow_count = 0

    def suggest(self, action, confidence):
        display = self.indicator.format_display(confidence)
        print(f"建議動作：{action}")
        print(display)

    def record_feedback(self, followed):
        if followed:
            self.follow_count += 1
        else:
            self.override_count += 1

    def get_trust_score(self):
        total = self.follow_count + self.override_count
        if total == 0:
            return 0.5
        return self.follow_count / total

system = TrustAwareSystem()
system.suggest("自動回覆此郵件", 0.85)
system.record_feedback(True)
system.suggest("調整訂單金額", 0.35)
system.record_feedback(False)
print(f"信任分數：{system.get_trust_score():.0%}")
```

## 漸進式授權

```python
class ProgressiveAuthorization:
    def __init__(self):
        self.permission_levels = {
            "suggest": 1,
            "auto_reply": 2,
            "execute": 3,
        }
        self.current_level = 0

    def increase_trust(self, amount=1):
        self.current_level = min(self.current_level + amount, 3)

    def decrease_trust(self, amount=1):
        self.current_level = max(self.current_level - amount, 0)

    def can_perform(self, action):
        required = self.permission_levels.get(action, 99)
        return self.current_level >= required

    def get_allowed_actions(self):
        return [
            a for a, l in self.permission_levels.items()
            if self.current_level >= l
        ]

auth = ProgressiveAuthorization()
for action in ["suggest", "auto_reply", "execute"]:
    print(f"{action}: {auth.can_perform(action)}")
auth.increase_trust(2)
print(f"提升信任後：{auth.get_allowed_actions()}")
```

---

**延伸閱讀**

- [Trust in Human-AI Interaction](https://www.google.com/search?q=trust+human+AI+interaction+design)
- [Explainable AI Systems](https://www.google.com/search?q=explainable+AI+XAI+design+patterns)
- [Calibrated Trust in Automation](https://www.google.com/search?q=calibrated+trust+automation+AI)
