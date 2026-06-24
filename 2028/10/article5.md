# AI 專案 ROI 計算方法

## 1. 引言

投入 AI 專案前，必須回答一個關鍵問題：這項投資能帶來多少回報？ROI（Return on Investment）計算將 AI 的成本與效益量化，幫助決策者判斷專案是否值得推進。

## 2. ROI 基本公式

```
ROI = (淨收益 - 總成本) / 總成本 × 100%
```

AI 專案的總成本包含：開發成本、運算成本、維護成本。淨收益包含：節省的人力成本、增加的營收、效率提升的價值。

## 3. Python ROI 計算工具

```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class AIProjectROI:
    name: str
    dev_cost: float       # 開發成本（美元）
    monthly_infra: float   # 每月基礎設施費用
    monthly_api: float     # 每月 API 費用
    monthly_maintenance: float  # 每月維護費用
    monthly_labor_saving: float # 每月節省人力
    monthly_revenue: float      # 每月新增營收
    project_months: int = 12    # 評估期

    def total_cost(self) -> float:
        infra = (self.monthly_infra + self.monthly_api
                 + self.monthly_maintenance) * self.project_months
        return self.dev_cost + infra

    def total_benefit(self) -> float:
        return (self.monthly_labor_saving + self.monthly_revenue) \
               * self.project_months

    def roi(self) -> float:
        cost = self.total_cost()
        benefit = self.total_benefit()
        return (benefit - cost) / cost * 100

    def payback_months(self) -> Optional[float]:
        monthly_net = (self.monthly_labor_saving + self.monthly_revenue
                       - self.monthly_infra - self.monthly_api
                       - self.monthly_maintenance)
        if monthly_net <= 0:
            return None  # 無法回本
        return self.dev_cost / monthly_net

# 案例：客服機器人
project = AIProjectROI(
    name="客服 AI 機器人",
    dev_cost=50000,
    monthly_infra=2000,
    monthly_api=3000,
    monthly_maintenance=1000,
    monthly_labor_saving=15000,  # 減少 3 名客服
    monthly_revenue=5000,        # 提升轉換率
    project_months=24,
)

print(f"專案: {project.name}")
print(f"總成本: ${project.total_cost():,.0f}")
print(f"總效益: ${project.total_benefit():,.0f}")
print(f"ROI: {project.roi():.1f}%")
if pm := project.payback_months():
    print(f"回本時間: {pm:.1f} 個月")
```

## 4. 靈敏度分析

ROI 受到多個變數影響，應進行靈敏度分析：

```python
def sensitivity_analysis(base: AIProjectROI):
    scenarios = {
        "最佳情況": {"monthly_revenue": base.monthly_revenue * 1.5},
        "基本情況": {},
        "最差情況": {"monthly_labor_saving": base.monthly_labor_saving * 0.5},
    }
    for name, changes in scenarios.items():
        params = {k: getattr(base, k) for k in base.__dataclass_fields__}
        params.update(changes)
        scenario = AIProjectROI(**params)
        print(f"{name:8s} ROI: {scenario.roi():.1f}%  "
              f"回本: {scenario.payback_months() or 'N/A'}")

sensitivity_analysis(project)
```

## 5. 非量化效益

ROI 計算無法捕捉的價值：品牌形象提升、技術壁壘建立、客戶體驗改善。建議在 ROI 報表中加入質性評估。

## 6. 常見陷阱

- 忽略維護成本（通常佔每年 15-25% 的初始開發成本）
- 高估人力節省（AI 通常輔助而非完全取代）
- 低估模型迭代更新費用

## 7. 結語

ROI 計算不是一次性的工作，應在專案過程中持續追蹤與調整。可參考 [Google Cloud ROI Framework](https://www.google.com/search?q=AI+ROI+framework+best+practices) 建立標準化的評估流程。
