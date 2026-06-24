# AI 預算規劃指南

## 1. 引言

AI 預算規劃是企業導入 AI 時最容易被低估的環節。缺乏完善的預算框架，專案可能在中途因資金不足而停擺。本文提供一套從零開始的 AI 預算規劃方法。

## 2. 預算三大支柱

AI 預算可分為三個層次：

- **開發階段**：一次性投資（模型選擇、資料準備、原型開發）
- **部署階段**：持續支出（推論費用、基礎設施、監控）
- **維運階段**：隱性成本（模型更新、人員培訓、法規遵循）

## 3. Python 預算規劃工具

```python
from dataclasses import dataclass, field

@dataclass
class AIBudgetItem:
    category: str
    name: str
    one_time: float = 0
    monthly: float = 0
    notes: str = ""

class AIBudgetPlanner:
    def __init__(self, project_months: int = 12):
        self.items: list[AIBudgetItem] = []
        self.project_months = project_months

    def add(self, item: AIBudgetItem):
        self.items.append(item)

    def summary(self) -> dict:
        total_one_time = sum(i.one_time for i in self.items)
        total_monthly = sum(i.monthly for i in self.items)
        total_project = total_one_time + total_monthly * self.project_months
        return {
            "one_time": total_one_time,
            "monthly": total_monthly,
            "project_total": total_project,
            "monthly_breakdown": self._monthly_breakdown(),
        }

    def _monthly_breakdown(self) -> dict[str, float]:
        breakdown = {}
        for i in self.items:
            breakdown[i.category] = breakdown.get(i.category, 0) + i.monthly
        return breakdown

    def print_plan(self):
        s = self.summary()
        print(f"=== AI 預算規劃 ({self.project_months} 個月) ===")
        print(f"一次性總費用: ${s['one_time']:,.0f}")
        print(f"每月經常性費用: ${s['monthly']:,.0f}")
        print(f"專案總預算: ${s['project_total']:,.0f}")
        print("\n每月分類支出:")
        for cat, cost in sorted(s['monthly_breakdown'].items(),
                                 key=lambda x: -x[1]):
            print(f"  {cat}: ${cost:,.0f}/月")

# 建立預算
planner = AIBudgetPlanner(project_months=24)
planner.add(AIBudgetItem("開發", "資料收集與標註", 15000, 0))
planner.add(AIBudgetItem("開發", "模型評估實驗", 8000, 0))
planner.add(AIBudgetItem("開發", "系統整合開發", 25000, 0))
planner.add(AIBudgetItem("基礎設施", "雲端 GPU 推論", 0, 3500))
planner.add(AIBudgetItem("基礎設施", "儲存與頻寬", 0, 500))
planner.add(AIBudgetItem("API", "LLM API 費用", 0, 2000))
planner.add(AIBudgetItem("維運", "系統維護", 0, 1500))
planner.add(AIBudgetItem("維運", "模型更新", 5000, 500))
planner.add(AIBudgetItem("人事", "AI 工程師", 0, 8000))
planner.add(AIBudgetItem("法規", "資安與合規審查", 10000, 200))

planner.print_plan()
```

## 4. 緩衝機制

```python
def contingency_plan(base_budget: float,
                     risk_level: str = "medium") -> dict:
    buffers = {"low": 0.15, "medium": 0.25, "high": 0.40}
    buffer = buffers.get(risk_level, 0.25)
    return {
        "base_budget": base_budget,
        "buffer_ratio": buffer,
        "buffer_amount": base_budget * buffer,
        "total_with_buffer": base_budget * (1 + buffer),
        "risk_level": risk_level,
    }

budget = 150000
plan = contingency_plan(budget, "medium")
print(f"基礎預算: ${plan['base_budget']:,.0f}")
print(f"緩衝比例: {plan['buffer_ratio']*100:.0f}%")
print(f"含緩衝總預算: ${plan['total_with_buffer']:,.0f}")
```

## 5. 預算追蹤儀表板

```python
class BudgetTracker:
    def __init__(self, planned: float):
        self.planned = planned
        self.spent: list[tuple[str, float]] = []

    def spend(self, category: str, amount: float):
        self.spent.append((category, amount))

    def status(self) -> str:
        total_spent = sum(a for _, a in self.spent)
        remaining = self.planned - total_spent
        pct = (total_spent / self.planned) * 100
        return (f"已花費: ${total_spent:,.0f} ({pct:.1f}%)\n"
                f"剩餘: ${remaining:,.0f}\n"
                f"狀態: {'正常' if remaining > 0 else '超支'}")

tracker = BudgetTracker(150000)
tracker.spend("開發", 48000)
tracker.spend("基礎設施", 22500)
print(tracker.status())
```

## 6. 結語

建議採用滾動預算（Rolling Budget），每季檢視實際支出並調整後續預算。可參考 [Google Cloud 成本管理](https://www.google.com/search?q=AI+budget+planning+best+practices+2026) 的架構來建立完整的預算管理流程。
