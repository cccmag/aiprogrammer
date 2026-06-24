# AI Agent 可觀測性：軌跡追蹤與行為分析

## 前言

AI Agent 是 2027 年 AI 應用最重要的架構轉變。與傳統 API 的請求-回應模式不同，Agent 是一個**多步驟的自主決策引擎**——它會思考、規劃、呼叫工具、分析結果，然後決定下一步。這個過程是非確定的，同一輸入可能產生完全不同的行為軌跡。

這帶來了前所未有的可觀測性挑戰：如何知道 Agent 正在做什麼？如何判斷它的決策是否合理？如何在出錯時找出問題根源？本文將從實戰角度探討 Agent 可觀測性的設計原則與實作方法。

## Agent 執行模型的資料結構

Agent 的執行模型與傳統程式完全不同。我們需要一個能夠完整描述 Agent 行為軌跡的資料結構：

```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
from enum import Enum

class AgentAction(Enum):
    THINK = "think"           # 推理步驟
    OBSERVE = "observe"       # 觀察（接收工具回傳）
    ACT = "act"               # 行動（呼叫工具）
    RESPOND = "respond"       # 最終回應

@dataclass
class ToolCall:
    tool_name: str
    arguments: dict
    result: Any
    latency_ms: float
    success: bool
    error_message: str | None = None

@dataclass
class AgentStep:
    step_number: int
    action: AgentAction
    thought: str | None = None         # 推理過程的文字
    tool_call: ToolCall | None = None  # 如果是工具呼叫步驟
    token_usage: dict | None = None    # {prompt_tokens, completion_tokens}
    latency_ms: float = 0.0
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class AgentSession:
    session_id: str
    user_query: str
    system_prompt: str
    steps: list[AgentStep] = field(default_factory=list)
    start_time: datetime = field(default_factory=datetime.now)
    end_time: datetime | None = None
    final_response: str = ""
    total_tokens: int = 0
    total_cost: float = 0.0
    success: bool = True
    error: str | None = None
```

## Agent 軌跡追蹤器實作

```python
import json
import hashlib

class AgentTracer:
    def __init__(self):
        self.sessions: dict[str, AgentSession] = {}
        self._current_session: AgentSession | None = None

    def start_session(self, query: str, system_prompt: str = "") -> str:
        """開始新的 Agent 會話"""
        import uuid
        session_id = f"agent_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:6]}"
        session = AgentSession(
            session_id=session_id,
            user_query=query,
            system_prompt=system_prompt
        )
        self.sessions[session_id] = session
        self._current_session = session
        return session_id

    def record_step(self, step: AgentStep):
        """記錄 Agent 的每一步"""
        if self._current_session:
            self._current_session.steps.append(step)
            self._current_session.total_tokens += sum(
                step.token_usage.values()
            ) if step.token_usage else 0

    def end_session(self, response: str, success: bool = True,
                    error: str | None = None):
        """結束會話"""
        if self._current_session:
            self._current_session.end_time = datetime.now()
            self._current_session.final_response = response
            self._current_session.success = success
            self._current_session.error = error

            total_latency = (
                self._current_session.end_time -
                self._current_session.start_time
            ).total_seconds() * 1000

            # 計算成本（簡化版）
            self._current_session.total_cost = (
                self._current_session.total_tokens * 0.000003
            )
            self._current_session = None

    def replay(self, session_id: str) -> str:
        """人類可讀的軌跡重播"""
        session = self.sessions.get(session_id)
        if not session:
            return f"Session {session_id} not found"

        output = [
            f"{'='*60}",
            f"Agent 軌跡重播",
            f"{'='*60}",
            f"使用者: {session.user_query[:200]}",
            f"會話 ID: {session.session_id}",
            f"總步驟: {len(session.steps)}",
            f"總耗時: {self._calc_total_latency(session):.0f}ms",
            f"總 Token: {session.total_tokens}",
            f"狀態: {'成功' if session.success else '失敗'}",
            f"",
        ]
        if session.error:
            output.append(f"錯誤: {session.error}")
            output.append("")

        for i, step in enumerate(session.steps, 1):
            output.append(f"  [{i:03d}] {step.action.value.upper()}",)
            output.append(f"        耗時: {step.latency_ms:.0f}ms")

            if step.thought:
                thought_preview = step.thought[:150]
                output.append(f"        思考: {thought_preview}...")

            if step.tool_call:
                tc = step.tool_call
                status = "✓" if tc.success else "✗"
                output.append(
                    f"        工具: {tc.tool_name}({json.dumps(tc.arguments)[:100]}) {status}"
                )
                if tc.error_message:
                    output.append(f"        錯誤: {tc.error_message[:200]}")
                output.append(f"        耗時: {tc.latency_ms:.0f}ms")

            if step.action == AgentAction.RESPOND:
                output.append(f"        回應: {session.final_response[:200]}...")

            output.append("")

        return "\n".join(output)

    def _calc_total_latency(self, session: AgentSession) -> float:
        if session.end_time:
            return (session.end_time - session.start_time).total_seconds() * 1000
        return sum(s.latency_ms for s in session.steps)

    def export_for_audit(self, session_id: str) -> dict:
        """匯出審計用 JSON"""
        session = self.sessions.get(session_id)
        if not session:
            return {}

        return {
            "session_id": session.session_id,
            "user_query": session.user_query,
            "timing": {
                "start": session.start_time.isoformat(),
                "end": session.end_time.isoformat() if session.end_time else None,
                "total_latency_ms": self._calc_total_latency(session),
            },
            "token_usage": session.total_tokens,
            "cost": session.total_cost,
            "success": session.success,
            "error": session.error,
            "steps": [
                {
                    "step": s.step_number,
                    "action": s.action.value,
                    "thought": s.thought,
                    "tool_call": {
                        "tool": s.tool_call.tool_name,
                        "args": s.tool_call.arguments,
                        "result_preview": str(s.tool_call.result)[:500],
                        "latency_ms": s.tool_call.latency_ms,
                        "success": s.tool_call.success,
                        "error": s.tool_call.error_message,
                    } if s.tool_call else None,
                    "latency_ms": s.latency_ms,
                    "token_usage": s.token_usage,
                    "timestamp": s.timestamp.isoformat(),
                }
                for s in session.steps
            ],
            "final_response_preview": session.final_response[:1000],
        }
```

## Agent 行為分析引擎

記錄軌跡只是第一步，真正的價值來自於行為分析：

```python
class AgentBehaviorAnalyzer:
    def __init__(self, tracer: AgentTracer):
        self.tracer = tracer

    def analyze_session(self, session_id: str) -> dict:
        """分析單個會話的行為特徵"""
        session = self.tracer.sessions.get(session_id)
        if not session:
            return {}

        tool_calls = [
            s for s in session.steps
            if s.action == AgentAction.ACT and s.tool_call
        ]
        think_steps = [
            s for s in session.steps
            if s.action == AgentAction.THINK
        ]

        # 效率分析
        efficiency = self._measure_efficiency(session, tool_calls, think_steps)

        # 決策品質分析
        decision_quality = self._assess_decision_quality(
            session, tool_calls
        )

        # 異常檢測
        anomalies = self._detect_anomalies(session)

        return {
            "session_id": session_id,
            "overview": {
                "total_steps": len(session.steps),
                "tool_calls": len(tool_calls),
                "thinking_steps": len(think_steps),
                "unique_tools": len(set(
                    s.tool_call.tool_name for s in tool_calls
                )),
            },
            "efficiency": efficiency,
            "decision_quality": decision_quality,
            "anomalies": anomalies,
        }

    def _measure_efficiency(self, session: AgentSession,
                             tool_calls: list,
                             think_steps: list) -> dict:
        """衡量執行效率"""
        total_latency = self.tracer._calc_total_latency(session)
        tool_latency = sum(
            s.tool_call.latency_ms for s in tool_calls if s.tool_call
        )
        think_ratio = len(think_steps) / max(len(session.steps), 1)

        return {
            "total_latency_ms": total_latency,
            "tool_latency_ratio": tool_latency / max(total_latency, 1),
            "think_to_act_ratio": think_ratio,
            "avg_step_latency_ms": total_latency / max(len(session.steps), 1),
            "tokens_per_step": session.total_tokens / max(len(session.steps), 1),
        }

    def _assess_decision_quality(self, session: AgentSession,
                                   tool_calls: list) -> dict:
        """評估決策品質"""
        # 工具成功率
        success_rate = sum(
            1 for s in tool_calls
            if s.tool_call and s.tool_call.success
        ) / max(len(tool_calls), 1)

        # 重複工具呼叫
        tool_names = [
            s.tool_call.tool_name for s in tool_calls if s.tool_call
        ]
        repeated_calls = len(tool_names) - len(set(tool_names))

        return {
            "tool_success_rate": success_rate,
            "repeated_tool_calls": repeated_calls,
            "redundancy_ratio": repeated_calls / max(len(tool_names), 1),
            "tool_diversity": len(set(tool_names)),
        }

    def _detect_anomalies(self, session: AgentSession) -> list[dict]:
        """檢測異常行為"""
        anomalies = []

        # 檢測迴圈（重複相同的工具呼叫模式）
        tool_seq = [
            s.tool_call.tool_name if s.tool_call else None
            for s in session.steps
        ]
        for i in range(1, min(5, len(tool_seq) // 2 + 1)):
            if len(tool_seq) >= i * 3:
                recent = tool_seq[-i:]
                prev = tool_seq[-i*2:-i]
                if recent == prev and all(r is not None for r in recent):
                    anomalies.append({
                        "type": "loop_detected",
                        "severity": "high",
                        "description": f"檢測到工具呼叫迴圈模式: {recent}",
                        "affected_steps": len(tool_seq) - i
                    })

        # 檢測過長的推理
        for step in session.steps:
            if (step.action == AgentAction.THINK
                and step.latency_ms > 10000):
                anomalies.append({
                    "type": "slow_thinking",
                    "severity": "medium",
                    "description": f"推理步驟耗時過長: {step.latency_ms:.0f}ms",
                    "step": step.step_number
                })

        # 檢測工具錯誤模式
        tool_errors = {}
        for step in session.steps:
            if step.tool_call and not step.tool_call.success:
                name = step.tool_call.tool_name
                tool_errors[name] = tool_errors.get(name, 0) + 1

        for tool, count in tool_errors.items():
            if count >= 3:
                anomalies.append({
                    "type": "repeated_tool_failure",
                    "severity": "high",
                    "description": f"工具 {tool} 連續失敗 {count} 次",
                })

        # 檢測 Token 消耗異常
        if session.total_tokens > 10000:
            anomalies.append({
                "type": "excessive_token_usage",
                "severity": "low",
                "description": f"Token 消耗過高: {session.total_tokens}",
            })

        return anomalies
```

## 與監控系統的整合

Agent 可觀測性需要與現有監控基礎設施整合：

```python
class AgentMonitoringIntegration:
    def __init__(self, tracer: AgentTracer, analyzer: AgentBehaviorAnalyzer):
        self.tracer = tracer
        self.analyzer = analyzer
        self.metrics: dict[str, list] = {
            "session_count": [],
            "avg_latency": [],
            "success_rate": [],
            "tool_error_rate": [],
            "avg_steps": [],
        }

    def record_completed_session(self, session_id: str):
        """會話完成後記錄聚合指標"""
        analysis = self.analyzer.analyze_session(session_id)
        if not analysis:
            return

        # 更新聚合指標
        self.metrics["session_count"].append(
            len(self.metrics["session_count"]) + 1
        )
        self.metrics["avg_latency"].append(
            analysis["efficiency"]["total_latency_ms"]
        )
        self.metrics["success_rate"].append(
            1.0 if self.tracer.sessions[session_id].success else 0.0
        )
        self.metrics["tool_error_rate"].append(
            1 - analysis["decision_quality"]["tool_success_rate"]
        )
        self.metrics["avg_steps"].append(
            analysis["overview"]["total_steps"]
        )

    def get_dashboard_data(self) -> dict:
        """產生儀表板資料"""
        if not self.metrics["session_count"]:
            return {}

        return {
            "summary": {
                "total_sessions": self.metrics["session_count"][-1],
                "avg_latency_ms": sum(self.metrics["avg_latency"]) / len(self.metrics["avg_latency"]),
                "avg_success_rate": sum(self.metrics["success_rate"]) / len(self.metrics["success_rate"]),
                "avg_tool_error_rate": sum(self.metrics["tool_error_rate"]) / len(self.metrics["tool_error_rate"]),
                "avg_steps_per_session": sum(self.metrics["avg_steps"]) / len(self.metrics["avg_steps"]),
            },
            "anomaly_alerts": self._get_recent_anomalies(),
        }

    def _get_recent_anomalies(self) -> list[dict]:
        alerts = []
        for sid, session in list(self.tracer.sessions.items())[-50:]:
            analysis = self.analyzer.analyze_session(sid)
            if analysis and analysis["anomalies"]:
                for anomaly in analysis["anomalies"][:3]:
                    alerts.append({
                        "session_id": sid,
                        **anomaly
                    })
        return alerts[:20]
```

## 實戰建議

1. **最小化可觀測性開銷**：Agent 的每一步都產生追蹤資料，確保資料收集不會顯著影響效能
2. **取樣策略**：100% 記錄中繼資料，根據重要性設定不同的內容取樣率
3. **即時警報**：設定閾值——工具失敗率 > 20%、迴圈偵測、Token 消耗異常
4. **軌跡可視化**：建立時間軸視圖，可視化 Agent 的決策鏈
5. **審計留存**：保留所有軌跡至少 30 天，滿足法規與除錯需求

## 參考資源

- [Agent Observability Patterns](https://www.google.com/search?q=AI+agent+observability+patterns+2027)
- [LangSmith Agent Tracing](https://www.google.com/search?q=LangSmith+agent+tracing+observability)
- [Agent Safety Auditing](https://www.google.com/search?q=AI+agent+safety+auditing+best+practices)
- [OpenTelemetry Agent SDK](https://www.google.com/search?q=OpenTelemetry+AI+agent+semantic+conventions)
