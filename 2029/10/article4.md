# AI 影響評估：系統化分析部署前後的社會風險

## 前言

AI 影響評估（AI Impact Assessment）是歐盟 AI Act 及其他監管框架中的核心要求。它要求開發者在 AI 系統部署前，系統性地評估對個人、群體和社會的潛在影響。

## 影響評估框架的 Python 實現

```python
from enum import Enum
from dataclasses import dataclass, field
from typing import List, Optional

class RiskLevel(Enum):
    LOW = "低風險"
    LIMITED = "有限風險"
    HIGH = "高風險"
    UNACCEPTABLE = "不可接受風險"

@dataclass
class ImpactFactor:
    category: str
    description: str
    likelihood: float  # 0.0 ~ 1.0
    severity: int      # 1 ~ 5
    mitigation: Optional[str] = None

    @property
    def risk_score(self) -> float:
        return self.likelihood * self.severity

class AIImpactAssessment:
    def __init__(self, system_name: str, description: str):
        self.system_name = system_name
        self.description = description
        self.factors: List[ImpactFactor] = []

    def add_factor(self, factor: ImpactFactor):
        self.factors.append(factor)

    def assess_risk_level(self) -> RiskLevel:
        scores = [f.risk_score for f in self.factors]
        avg_score = sum(scores) / len(scores) if scores else 0
        if avg_score > 15: return RiskLevel.UNACCEPTABLE
        if avg_score > 8: return RiskLevel.HIGH
        if avg_score > 3: return RiskLevel.LIMITED
        return RiskLevel.LOW

    def generate_report(self) -> str:
        lines = [f"# AI 影響評估報告：{self.system_name}"]
        lines.append(f"系統描述：{self.description}\n")
        for f in self.factors:
            lines.append(
                f"## {f.category}\n"
                f"- 描述：{f.description}\n"
                f"- 可能性：{f.likelihood:.0%}\n"
                f"- 嚴重程度：{f.severity}/5\n"
                f"- 風險分數：{f.risk_score}\n"
                f"- 緩解措施：{f.mitigation or '無'}\n"
            )
        lines.append(f"**整體風險等級：{self.assess_risk_level().value}**")
        return "\n".join(lines)

assessment = AIImpactAssessment("人臉辨識門禁", "基於人臉辨識的辦公大樓門禁系統")
assessment.add_factor(ImpactFactor("隱私", "未經同意的生物特徵收集", 0.8, 4, "部署前取得書面同意"))
assessment.add_factor(ImpactFactor("偏見", "對特定膚色的辨識準確度差異", 0.6, 3, "定期進行公平性審計"))

print(assessment.generate_report())
```

## 結語

AI 影響評估不是一次性作業。建議在系統開發的各個階段持續進行評估，建立動態風險管理機制，並保留完整的評估歷程以供監管稽核。

---

**延伸閱讀**

- [EU AI Act 影響評估指南](https://www.google.com/search?q=EU+AI+Act+impact+assessment+requirements)
- [NIST AI 風險管理架構](https://www.google.com/search?q=NIST+AI+Risk+Management+Framework)
- [OECD AI 原則](https://www.google.com/search?q=OECD+AI+principles+responsible+AI)
