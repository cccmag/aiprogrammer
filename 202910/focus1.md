# 負責任 AI 框架

## NIST AI RMF、EU AI Act 分級制度、OECD 原則（2019-2029）

### 從口號到標準

2019 年 OECD 發布 AI 原則，揭開了負責任 AI 框架化的序幕。六年後，全球已有超過 70 個國家發布 AI 治理框架。這些框架雖然細節各異，但核心訴求高度一致：**AI 系統必須是安全、公平、透明且可問責的**。

### NIST AI 風險管理框架（AI RMF 1.0, 2023）

美國 NIST 在 2023 年發布 AI RMF 1.0，將 AI 風險管理分為四個核心功能：

```python
# NIST AI RMF 四大功能：GOVERN → MAP → MEASURE → MANAGE
class NistAiRmf:
    def __init__(self):
        self.functions = {
            "GOVERN": 0.0,   # 治理：政策、程序、問責
            "MAP": 0.0,      # 映射：評估使用情境
            "MEASURE": 0.0,  # 測量：量化風險程度
            "MANAGE": 0.0,   # 管理：緩解措施
        }

    def score_assessment(self, answers: dict) -> dict:
        for func in self.functions:
            raw = answers.get(func, [])
            self.functions[func] = sum(raw) / len(raw) if raw else 0
        return self.functions

    def risk_level(self) -> str:
        avg = sum(self.functions.values()) / len(self.functions)
        if avg >= 0.8:
            return "Low Risk"
        return "High Risk" if avg < 0.5 else "Medium Risk"
```

### EU AI Act 分級制度（2024通過，2026實施）

歐盟 AI Act 採用風險分級方法，將 AI 系統分為四類：

| 風險等級 | 規範要求 | 範例 |
|----------|---------|------|
| 不可接受 | ❌ 禁止 | 社會評分、即時人臉辨識 |
| 高風險 | ✅ 嚴格審查 | 醫療診斷、徵才篩選 |
| 有限風險 | 📋 透明度義務 | 聊天機器人揭露 |
| 極小風險 | ➡️ 無規範 | AI 電玩、垃圾郵件過濾 |

```python
# EU AI Act 風險分類器
class EuAiActClassifier:
    def __init__(self):
        self.high_risk_domains = {
            "biometric": False, "critical_infra": False,
            "education": False, "employment": False,
            "public_service": False, "law_enforcement": False,
            "migration": False, "justice": False,
        }

    def classify(self, domain: str, is_real_time: bool = False) -> str:
        if domain == "social_credit" or (domain == "biometric" and is_real_time):
            return "Unacceptable Risk"
        if self.high_risk_domains.get(domain, False):
            return "High Risk"
        if domain in ("chatbot", "deepfake"):
            return "Limited Risk"
        return "Minimal Risk"
```

### OECD AI 原則

OECD 的五項原則是最廣為接受的 AI 倫理基石：包容性成長、以人為本、透明度、穩健性、問責性。

### 框架的實踐落差

框架雖然完善，但從原則到實作仍有巨大鴻溝。2024 年的一項調查顯示，87% 的企業表示重視 AI 倫理，但僅有 18% 具備可操作的評估流程。接下來的文章將深入探討偏見檢測、公平性評估、可解釋性等具體技術方法。

---

**下一步**：[偏見檢測與緩解](focus2.md)

## 延伸閱讀

- [NIST AI RMF](https://www.google.com/search?q=NIST+AI+RMF+1.0)
- [EU AI Act](https://www.google.com/search?q=EU+AI+Act+risk+categories)
- [OECD AI Principles](https://www.google.com/search?q=OECD+AI+principles)
