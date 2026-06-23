# 人類與 AI 協作：Human-in-the-Loop 設計模式

## 前言

完全自主的 AI Agent 聽起來很吸引人，但在現實世界中，許多場景仍然需要人類的參與。Human-in-the-Loop（HITL）不是系統的缺陷，而是設計上的選擇——在適當的時候讓適當的人類介入，可以大幅提升系統的可靠性、安全性和使用者信任度。

---

## 一、HITL 的核心設計模式

### 1.1 審批閘門（Approval Gate）

在關鍵動作執行前，要求人類審批：

```python
from dataclasses import dataclass, field
from typing import Optional, Callable
from enum import Enum
import json

class ApprovalStatus(Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    ESCALATED = "escalated"

@dataclass
class ApprovalRequest:
    action: str
    description: str
    risk_level: str  # low, medium, high
    context: dict = field(default_factory=dict)
    status: ApprovalStatus = ApprovalStatus.PENDING

class ApprovalGate:
    def __init__(self, human_interface: Callable):
        self.human_interface = human_interface

    def request_approval(self, request: ApprovalRequest) -> ApprovalStatus:
        """向人類請求審批"""
        if request.risk_level == "low":
            return ApprovalStatus.APPROVED

        decision = self.human_interface(
            f"需要審批：{request.description}\n"
            f"風險等級：{request.risk_level}\n"
            f"動作：{request.action}\n"
            f"請回覆 approve / reject / escalate"
        )

        decision_map = {
            "approve": ApprovalStatus.APPROVED,
            "reject": ApprovalStatus.REJECTED,
            "escalate": ApprovalStatus.ESCALATED,
        }
        return decision_map.get(decision.strip().lower(), ApprovalStatus.PENDING)
```

### 1.2 升級路徑（Escalation）

```python
class EscalationManager:
    def __init__(self):
        self.support_tiers = {
            1: "一線技術支援",
            2: "資深工程師",
            3: "系統管理員",
        }
        self.current_tier = 1

    def escalate(self, issue: dict, agent: str) -> dict:
        """升級問題到更高層級"""
        tier_info = self.support_tiers.get(self.current_tier, "未知層級")
        print(f"📤 從 {agent} 升級到 {tier_info}（第 {self.current_tier} 層）")

        if self.current_tier < max(self.support_tiers.keys()):
            self.current_tier += 1

        return {
            "status": "escalated",
            "current_tier": self.current_tier,
            "assigned_to": tier_info,
            "agent": agent,
            "issue": issue,
        }

class EscalationPolicy:
    def __init__(self):
        self.rules = []

    def add_rule(self, condition: Callable, tier: int):
        self.rules.append((condition, tier))

    def should_escalate(self, context: dict) -> Optional[int]:
        for condition, tier in self.rules:
            if condition(context):
                return tier
        return None
```

### 1.3 交接模式（Handoff）

```python
@dataclass
class HandoffContext:
    task: str
    agent_output: str
    confidence: float
    reason: str  # 為什麼需要交接
    handoff_to: str  # 交接給誰

class HandoffManager:
    def __init__(self):
        self.handoff_history = []

    def request_handoff(self, context: HandoffContext) -> bool:
        self.handoff_history.append(context)
        print(f"🔄 交接請求：{context.agent_output[:100]}...")
        print(f"   原因：{context.reason}")
        print(f"   交接給：{context.handoff_to}")
        return True
```

---

## 二、設計有效的人類介面

### 2.1 減少人類認知負荷

```python
class HumanInterface:
    def __init__(self):
        self.pending_reviews = []

    def present_for_review(self, items: list) -> str:
        """以結構化方式呈現審批項目"""
        formatted = "\n".join(
            f"[{i+1}] {item['action']}\n"
            f"    說明：{item['description']}\n"
            f"    風險：{item.get('risk', '未知')}\n"
            for i, item in enumerate(items)
        )
        return formatted

    def quick_approve(self, items: list) -> list:
        """支援批次操作"""
        print("以下項目需要審批（輸入 a=全部同意, r=全部拒絕, 或逐項處理）：")
        print(self.present_for_review(items))
        choice = input("> ").strip()

        if choice == "a":
            return ["approved"] * len(items)
        elif choice == "r":
            return ["rejected"] * len(items)
        else:
            return self._individual_review(items)

    def _individual_review(self, items: list) -> list:
        decisions = []
        for item in items:
            print(f"項目：{item['description']}")
            d = input("同意 (y) / 拒絕 (n) / 修改 (m) > ").strip()
            decisions.append({"approve": True, "reject": False, "modify": None}.get(d, False))
        return decisions
```

### 2.2 信心度閾值系統

```python
class ConfidenceThresholdSystem:
    def __init__(self):
        self.thresholds = {
            "approval": 0.85,  # 低於此需審批
            "autonomy": 0.95,  # 高於此可自主執行
            "escalation": 0.3, # 低於此需升級
        }

    def should_involve_human(self, confidence: float, action_type: str) -> bool:
        if action_type == "critical":
            return confidence < self.thresholds["approval"]
        elif action_type == "routine":
            return confidence < self.thresholds["autonomy"]
        return False

    def adjust_threshold(self, feedback: dict):
        """根據人類回饋動態調整閾值"""
        if feedback.get("false_positive"):
            self.thresholds["approval"] *= 0.95
        if feedback.get("false_negative"):
            self.thresholds["approval"] *= 1.05
```

---

## 三、何時需要人類介入

### 3.1 判斷標準

```python
class HumanInvolvementDecider:
    def should_involve_human(self, task: dict, agent_state: dict) -> str:
        """決定是否需要人類介入，回傳決策類型"""
        reasons = []

        # 1. 高風險操作
        if task.get("risk_level") in ("high", "critical"):
            reasons.append("high_risk")

        # 2. 信心度不足
        if agent_state.get("confidence", 1.0) < 0.7:
            reasons.append("low_confidence")

        # 3. 超出 scope
        if task.get("requires_domain_knowledge"):
            reasons.append("domain_expertise_needed")

        # 4. 成本考量
        if agent_state.get("estimated_cost", 0) > 0.5:  # $0.50 以上
            reasons.append("cost_concern")

        # 5. 法律/法規要求
        if task.get("requires_compliance"):
            reasons.append("compliance_required")

        if not reasons:
            return "automatic"
        elif len(reasons) == 1 and reasons[0] == "low_confidence":
            return "supervised"
        else:
            return "manual"
```

---

## 四、完整 HITL 工作流

```python
class HITLWorkflow:
    def __init__(self, agent, approval_gate: ApprovalGate, escalation: EscalationManager):
        self.agent = agent
        self.approval_gate = approval_gate
        self.escalation = escalation
        self.decider = HumanInvolvementDecider()

    def run(self, task: dict) -> dict:
        print(f"📋 任務：{task.get('description', '未知')}")

        # 步驟 1：Agent 產生提議
        proposal = self.agent.generate_proposal(task)
        confidence = self.agent.get_confidence(proposal)

        # 步驟 2：決定模式
        mode = self.decider.should_involve_human(task, {
            "confidence": confidence,
            "estimated_cost": proposal.get("estimated_cost", 0),
        })

        if mode == "manual":
            print("👤 需要人工處理（高風險或合規需求）")
            request = ApprovalRequest(
                action=json.dumps(proposal),
                description=task["description"],
                risk_level=task.get("risk_level", "medium"),
            )
            status = self.approval_gate.request_approval(request)

            if status == ApprovalStatus.APPROVED:
                return {"mode": "manual_approved", "result": self._execute(proposal)}
            elif status == ApprovalStatus.ESCALATED:
                return self.escalation.escalate(task, self.agent.name)
            else:
                return {"mode": "rejected", "result": None}

        elif mode == "supervised":
            print("👤 代理執行中（人類可隨時介入）")
            result = self._execute_with_monitoring(proposal)
            return {"mode": "supervised", "result": result}

        else:
            print("🤖 自動執行")
            return {"mode": "automatic", "result": self._execute(proposal)}

    def _execute(self, proposal: dict):
        return self.agent.execute(proposal)

    def _execute_with_monitoring(self, proposal: dict):
        step_count = 0
        for step in proposal.get("steps", []):
            step_count += 1
            print(f"  步驟 {step_count}：{step.get('action', '未知')}")
            if step_count % 3 == 0:
                cont = input("    繼續執行？(y/n) > ").strip()
                if cont != "y":
                    print("    ⏸ 已被使用者暫停")
                    return {"status": "paused", "completed_steps": step_count}
        return {"status": "completed", "steps": step_count}
```

---

## 五、HITL 最佳實踐

1. **預設最小干預**：只在必要時打擾人類，建立明確的「人類介入條件」
2. **提供充分的上下文**：人類做決策時需要完整的背景資訊，而非單一請求
3. **批次處理**：將多個審批請求批次呈現，減少上下文切換成本
4. **支援多種決策**：不僅是通過/拒絕，還應允許修改、附註、升級
5. **記錄決策軌跡**：所有 HITL 互動都應記錄，用於後續分析和稽核
6. **動態調整**：根據人類回饋調整信心度閾值，逐步減少不必要的介入

---

## 結語

Human-in-the-Loop 不是 AI Agent 的妥協，而是智慧系統設計的必要組成部分。透過審批閘門、升級路徑和交接模式，我們可以在效率與安全之間取得平衡。隨著 Agent 信心度評估技術的進步，未來的 HITL 系統將能更精準地判斷何時需要人類介入，實現真正的人機協作。

---

**參考資料**

- "Human-in-the-Loop AI: A Guide", https://www.nist.gov/publications/human-loop-artificial-intelligence
- "Interactive Agents: Learning from Human Feedback", https://arxiv.org/abs/2302.05442
- LangChain Human-in-the-Loop 文檔：https://python.langchain.com/docs/use_cases/human_in_the_loop
- "A Survey of Human-in-the-loop for Machine Learning", https://arxiv.org/abs/2109.03321
