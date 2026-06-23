# XAI 法規要求：從歐盟 AI Act 到全球治理

## 前言

2026 年，AI 可解釋性已經不只是技術問題，更是法律問題。歐盟 AI Act 已於 2025 年 8 月正式生效，2026 年的第一波執法行動正在重塑全球 AI 產業的合規標準。誰能解釋自己的模型，誰就能在市場中存活。

## 歐盟 AI Act 的核心要求

AI Act 將 AI 系統分為四個風險等級。可解釋性要求主要集中在高風險系統：

### 高風險系統的要求（第 13 條）

法規要求高風險 AI 系統必須「足夠透明，使部署者能夠理解和正確使用其輸出」。具體來說：

- **技術文件**：必須記錄模型的訓練資料、特徵選擇邏輯、預期準確度與限制。
- **透明度義務**：使用者必須被告知他們正在與 AI 系統互動。
- **人為監督**：必須設計人機互動機制，讓人類可以覆蓋或推翻 AI 的決策。

## Python 合規檢查框架

```python
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class AIActCompliance:
    model_name: str
    risk_level: str  # minimal, limited, high, unacceptable
    has_explanation: bool = False
    has_human_oversight: bool = False
    documentation_score: float = 0.0
    feature_list: list[str] = field(default_factory=list)
    bias_assessment: Optional[dict] = None

    def check_compliance(self) -> dict:
        results = {
            "model": self.model_name,
            "risk_level": self.risk_level,
            "passed": True,
            "warnings": []
        }
        if self.risk_level == "unacceptable":
            results["passed"] = False
            results["warnings"].append("Unacceptable risk: prohibited")
            return results
        if self.risk_level == "high":
            checks = []
            checks.append(("explanation_required",
                          self.has_explanation,
                          "No explanation method provided"))
            checks.append(("human_oversight_required",
                          self.has_human_oversight,
                          "No human oversight mechanism"))
            checks.append(("documentation_minimum",
                          self.documentation_score >= 0.7,
                          f"Documentation score {self.documentation_score:.1f} < 0.7"))
            for name, passed, msg in checks:
                if not passed:
                    results["passed"] = False
                    results["warnings"].append(msg)
        return results


def generate_compliance_report(compliance: AIActCompliance) -> str:
    report = f"# AI Act Compliance Report: {compliance.model_name}\n\n"
    report += f"## Risk Level: {compliance.risk_level.upper()}\n"
    checks = compliance.check_compliance()
    if checks["passed"]:
        report += "**Status: PASSED**\n"
    else:
        report += "**Status: FAILED**\n"
    for w in checks["warnings"]:
        report += f"- ⚠ {w}\n"
    report += "\n## Feature Transparency\n"
    for f in compliance.feature_list:
        report += f"- {f}\n"
    return report


loan_model = AIActCompliance(
    model_name="LoanDecisionNet v2",
    risk_level="high",
    has_explanation=True,
    has_human_oversight=True,
    documentation_score=0.85,
    feature_list=["income", "credit_score", "debt_ratio", "employment_years"]
)
print(generate_compliance_report(loan_model))
```

## 全球法規地圖（2026）

| 地區 | 法規名稱 | 生效時間 | 可解釋性要求 |
|------|---------|---------|-------------|
| 歐盟 | AI Act | 2025 年 | 高風險必須提供解釋 |
| 美國 | AI Bill of Rights | 2024 年 | 指引性質，非強制 |
| 中國 | 生成式 AI 管理辦法 | 2023 年 | 演算法備案與解釋義務 |
| 英國 | AI 監管白皮書 | 2024 年 | 原則導向，行業自律 |
| 日本 | AI 治理指引 | 2025 年 | 逐步強化合規要求 |

## 解釋的證據門檻

不同的決策場景對解釋的品質要求不同：

- **醫療診斷**：解釋必須展示因果路徑（do-calculus 層級）。
- **信貸決定**：解釋必須指出具體的改善行動（反事實層級）。
- **犯罪預測**：解釋必須滿足程序正義的要求（公平性審計）。

```python
def required_explanation_level(domain: str) -> str:
    levels = {
        "healthcare": "causal (do-calculus)",
        "finance": "counterfactual",
        "criminal_justice": "counterfactual + fairness audit",
        "hiring": "feature importance + group fairness",
        "education": "feature importance"
    }
    return levels.get(domain, "feature importance")


for domain in ["healthcare", "finance", "criminal_justice"]:
    print(f"{domain}: {required_explanation_level(domain)}")
```

## 2026 年的合規趨勢

- **解釋即服務（XaaS）**：第三方審計公司提供標準化的模型可解釋性評估。
- **自動化合規工具**：CI/CD Pipeline 整合 XAI 檢查，模型部署前必須通過解釋性閘道。
- **開源合規框架**：AIF360、AI Explainability 360 等專案提供法規對應的功能模組。

## 結語

法規要求正在推動可解釋性從「可有可無」變成「強制必要」。這對 AI 產業是好消息——當每家公司的模型都必須可解釋時，信任將不再是競爭優勢，而是基本前提。未來的 AI 從業者必須同時具備技術與法規素養。

---

**延伸閱讀**
- [EU AI Act 全文](https://www.google.com/search?q=EU+AI+Act+full+text+2025+explainability)
- [AI Bill of Rights](https://www.google.com/search?q=AI+Bill+of+Rights+White+House+blueprint)
- [XAI 合規實戰指南](https://www.google.com/search?q=explainable+AI+compliance+guide+2026)
