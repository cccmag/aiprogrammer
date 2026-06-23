# AI Agent 的行為追蹤（2024-2026）

## Agent 執行的可觀測性挑戰

AI Agent 與傳統 API 的最大不同：一個 Agent 呼叫不是一個請求-回應週期，而是一個**多步驟的自主推理過程**。Agent 可能：

1. 接收使用者輸入
2. 思考需要哪些資訊
3. 呼叫搜尋 API 獲取資料
4. 分析搜尋結果
5. 呼叫計算器處理數字
6. 綜合所有資訊生成回答

每一步都可能出錯，而且錯誤會累積。更糟糕的是，Agent 的決策過程是非確定的——同一個提示詞可能產生不同的行為軌跡。

這就是為什麼 Agent 需要專門的可觀測性基礎設施，而不只是傳統的日誌記錄。

```python
# Agent 執行軌跡的資料結構
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

@dataclass
class AgentStep:
    step_id: int
    action: str           # 思考、工具呼叫、回應
    input: dict           # 此步驟的輸入
    output: Any           # 此步驟的輸出
    tool_name: str | None # 使用的工具名稱
    latency_ms: float     # 耗時
    token_usage: dict     # token 使用量
    error: str | None     # 錯誤訊息
    timestamp: datetime   # 時間戳

@dataclass
class AgentTrajectory:
    session_id: str
    user_query: str
    steps: list[AgentStep] = field(default_factory=list)
    start_time: datetime = field(default_factory=datetime.now)
    end_time: datetime | None = None
    final_response: str = ""
    total_tokens: int = 0
    total_latency_ms: float = 0.0
    success: bool = True
```

## 工具呼叫的監控與除錯

Agent 的威力來自於工具呼叫。但工具呼叫也帶來了複雜性：第三方 API 可能不穩定、工具回傳的資料可能異常、Agent 可能以錯誤的方式使用工具。

```python
# 工具呼叫監控
class ToolCallMonitor:
    def __init__(self):
        self.calls: dict[str, list[dict]] = {}
    
    def record_call(self, tool_name: str, params: dict, 
                    result: Any, latency_ms: float, success: bool):
        if tool_name not in self.calls:
            self.calls[tool_name] = []
        self.calls[tool_name].append({
            "params": params,
            "result": result,
            "latency_ms": latency_ms,
            "success": success,
            "timestamp": datetime.now(),
        })
    
    def tool_health_report(self) -> dict:
        report = {}
        for tool, calls in self.calls.items():
            total = len(calls)
            errors = sum(1 for c in calls if not c["success"])
            latencies = [c["latency_ms"] for c in calls]
            report[tool] = {
                "total_calls": total,
                "error_rate": errors / max(total, 1),
                "p50_latency": sorted(latencies)[len(latencies) // 2] if latencies else 0,
                "p99_latency": sorted(latencies)[int(len(latencies) * 0.99)] if latencies else 0,
            }
        return report
    
    def detect_anomalous_calls(self, tool_name: str, threshold_z=3) -> list[dict]:
        """使用 Z-score 檢測異常工具呼叫"""
        calls = self.calls.get(tool_name, [])
        latencies = [c["latency_ms"] for c in calls]
        if len(latencies) < 2:
            return []
        mean = sum(latencies) / len(latencies)
        std = (sum((l - mean) ** 2 for l in latencies) / len(latencies)) ** 0.5
        return [c for c, l in zip(calls, latencies) if abs(l - mean) / max(std, 0.001) > threshold_z]
```

## 多步驟推理的軌跡記錄

軌跡記錄（Trajectory Logging）是 Agent 除錯的核心工具。你需要能夠重播 Agent 的每一步：

```python
# Agent 執行軌跡追蹤器
import json

class AgentTracer:
    def __init__(self):
        self.trajectories: list[AgentTrajectory] = []
    
    def start_session(self, query: str) -> str:
        session_id = f"agent_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{len(self.trajectories)}"
        traj = AgentTrajectory(session_id=session_id, user_query=query)
        self.trajectories.append(traj)
        return session_id
    
    def record_step(self, session_id: str, step: AgentStep):
        for traj in self.trajectories:
            if traj.session_id == session_id:
                traj.steps.append(step)
                traj.total_tokens += sum(step.token_usage.values())
                traj.total_latency_ms += step.latency_ms
                break
    
    def end_session(self, session_id: str, response: str, success: bool):
        for traj in self.trajectories:
            if traj.session_id == session_id:
                traj.end_time = datetime.now()
                traj.final_response = response
                traj.success = success
                break
    
    def replay(self, session_id: str) -> str:
        """人類可讀的軌跡重播"""
        for traj in self.trajectories:
            if traj.session_id == session_id:
                output = [f"=== Agent 軌跡重播 ===",
                          f"使用者: {traj.user_query}", ""]
                for step in traj.steps:
                    output.append(f"[步驟 {step.step_id}] {step.action} ({step.latency_ms:.0f}ms)")
                    if step.tool_name:
                        output.append(f"  工具: {step.tool_name}")
                    if step.error:
                        output.append(f"  錯誤: {step.error}")
                    output.append(f"  輸出: {str(step.output)[:200]}...")
                    output.append("")
                output.append(f"最終回應: {traj.final_response[:200]}")
                return "\n".join(output)
        return "Session not found"
    
    def export_for_audit(self, session_id: str) -> dict:
        """匯出審計用 JSON"""
        for traj in self.trajectories:
            if traj.session_id == session_id:
                return {
                    "session_id": traj.session_id,
                    "user_query": traj.user_query,
                    "steps": [
                        {
                            "step": s.step_id,
                            "action": s.action,
                            "tool": s.tool_name,
                            "input": str(s.input)[:500],
                            "output": str(s.output)[:500],
                            "latency_ms": s.latency_ms,
                            "error": s.error,
                            "timestamp": s.timestamp.isoformat(),
                        }
                        for s in traj.steps
                    ],
                    "total_latency_ms": traj.total_latency_ms,
                    "total_tokens": traj.total_tokens,
                    "success": traj.success,
                }
        return {}
```

## 決策過程分析

除了記錄軌跡，你還需要分析 Agent 的決策品質：

```python
# Agent 決策分析
class AgentDecisionAnalyzer:
    def __init__(self, tracer: AgentTracer):
        self.tracer = tracer
    
    def analyze_efficiency(self, session_id: str) -> dict:
        """分析 Agent 的執行效率"""
        traj = None
        for t in self.tracer.trajectories:
            if t.session_id == session_id:
                traj = t
                break
        if not traj:
            return {}
        
        tool_calls = [s for s in traj.steps if s.tool_name]
        thoughts = [s for s in traj.steps if s.action == "think"]
        
        return {
            "total_steps": len(traj.steps),
            "tool_calls": len(tool_calls),
            "thinking_steps": len(thoughts),
            "unique_tools": len(set(s.tool_name for s in tool_calls)),
            "avg_step_latency": traj.total_latency_ms / max(len(traj.steps), 1),
            "tokens_per_step": traj.total_tokens / max(len(traj.steps), 1),
        }
    
    def detect_loop(self, session_id: str, threshold=5) -> bool:
        """檢測 Agent 是否陷入迴圈"""
        for t in self.tracer.trajectories:
            if t.session_id == session_id:
                actions = [s.action for s in t.steps]
                # 檢查是否重複相同的動作模式
                for window in range(1, len(actions) // 2 + 1):
                    if len(actions) >= window * 2:
                        if actions[-window:] == actions[-window*2:-window]:
                            return True
        return False
```

## Agent 行為的安全審計

Agent 的安全問題不同於傳統系統——Agent 可能自主做出有安全風險的決策。這需要專門的審計機制：

- **工具使用審計**：Agent 是否呼叫了不該呼叫的工具？呼叫參數是否合理？
- **資料存取審計**：Agent 是否存取了不該存取的資料？
- **決策審計**：Agent 的決策邏輯是否符合預期？
- **偏見檢測**：Agent 的決策是否存在偏見？

```python
# Agent 安全審計
class AgentSecurityAuditor:
    def __init__(self):
        self.allowed_tools = {"search", "calculator", "database_query"}
        self.sensitive_patterns = [r"password", r"token", r"secret", r"api_key"]
    
    def audit_tool_usage(self, trajectory: AgentTrajectory) -> list[str]:
        violations = []
        for step in trajectory.steps:
            if step.tool_name and step.tool_name not in self.allowed_tools:
                violations.append(f"未授權工具呼叫: {step.tool_name}")
            if step.tool_name == "database_query":
                # 檢查 SQL 注入
                query = str(step.input.get("query", ""))
                if "DROP" in query.upper() or "DELETE" in query.upper():
                    violations.append(f"危險的資料庫操作: {query[:100]}")
        return violations
    
    def audit_data_access(self, trajectory: AgentTrajectory) -> list[str]:
        violations = []
        for step in trajectory.steps:
            output_str = str(step.output)
            for pattern in self.sensitive_patterns:
                import re
                if re.search(pattern, output_str, re.IGNORECASE):
                    violations.append(f"敏感資料洩露於步驟 {step.step_id}: 含 {pattern}")
        return violations
    
    def full_audit(self, trajectory: AgentTrajectory) -> dict:
        return {
            "session_id": trajectory.session_id,
            "tool_violations": self.audit_tool_usage(trajectory),
            "data_violations": self.audit_data_access(trajectory),
            "total_steps": len(trajectory.steps),
            "audit_passed": True,  # 無違規才為 True
            "audited_at": datetime.now().isoformat(),
        }
```

Agent 可觀測性不是一個可選項——它是 AI 系統可以安全上線的前提條件。沒有軌跡記錄，你無法除錯；沒有審計機制，你無法追責；沒有決策分析，你無法最佳化。

---

**下一步**：[AI 應用的持續交付](focus7.md)

## 延伸閱讀

- [AI Agent 可觀測性](https://www.google.com/search?q=AI+agent+observability+tracing)
- [Agent 軌跡分析工具](https://www.google.com/search?q=agent+trajectory+analysis+tools)
- [AI Agent 安全審計](https://www.google.com/search?q=AI+agent+security+audit)
- [LangSmith Agent Tracing](https://www.google.com/search?q=LangSmith+agent+tracing)
