# 安全與治理（2023-2026）

## Agent 權限最小化原則

每個 Agent 只應該擁有完成任務所需的最小權限。權限管理是多 Agent 系統安全的第一道防線：

```python
class Permission:
    def __init__(self, resource: str, action: str):
        self.resource = resource  # "filesystem", "network", "database"
        self.action = action      # "read", "write", "execute"

class AgentSecurityPolicy:
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self.allowed = []

    def grant(self, permission: Permission):
        self.allowed.append(permission)

    def check(self, resource: str, action: str) -> bool:
        for perm in self.allowed:
            if perm.resource == resource and perm.action == action:
                return True
        print(f"⚠️ 拒絕存取：{self.agent_name} 嘗試 {action} {resource}")
        return False

# 安全策略配置
coder_policy = AgentSecurityPolicy("coder")
coder_policy.grant(Permission("filesystem", "read"))
coder_policy.grant(Permission("filesystem", "write"))
coder_policy.grant(Permission("code_executor", "run"))

researcher_policy = AgentSecurityPolicy("researcher")
researcher_policy.grant(Permission("network", "http_get"))
researcher_policy.grant(Permission("filesystem", "read"))
# ❌ researcher 不能寫入檔案或執行程式碼
```

實作安全殼層（Sandbox）隔離 Agent 執行環境：

```python
class AgentSandbox:
    def __init__(self, agent, policy):
        self.agent = agent
        self.policy = policy

    def execute_tool(self, tool_name: str, args: dict):
        resource, action = self.parse_tool_permission(tool_name)
        if not self.policy.check(resource, action):
            return {"error": f"Permission denied: {tool_name}"}
        return self.agent.tools[tool_name](**args)
```

## 人類監督機制（Human-in-the-Loop）

高風險操作必須有人類確認。HITL（Human-in-the-Loop）模式在 Agent 做出關鍵決策前暫停，等待人類批准：

```python
class HumanInTheLoop:
    def __init__(self):
        self.pending_approvals = {}

    def request_approval(self, agent_name: str,
                         action: dict) -> bool:
        print(f"\n🔔 {agent_name} 請求核准：")
        print(f"   操作：{action['description']}")
        print(f"   風險等級：{action.get('risk', 'low')}")

        approval_id = f"ap_{id(action)}"
        self.pending_approvals[approval_id] = action

        # 等待人類回應
        response = input("核准？(y/n): ")
        del self.pending_approvals[approval_id]
        return response.lower() == 'y'

    def auto_approve(self, action: dict) -> bool:
        # 低風險操作自動核准
        if action.get("risk") == "low":
            return True

        # 高風險操作需要人類確認
        if action.get("risk") == "high":
            return self.request_approval("system", action)

        # 中風險：記錄但自動核准（可配置）
        print(f"📝 記錄中風險操作：{action['description']}")
        return True

# 整合到 Agent 執行流程
hitl = HumanInTheLoop()
if not hitl.auto_approve({
    "description": "刪除生產資料庫使用者表",
    "risk": "high"
}):
    print("操作已取消")
```

## 提示詞注入與跨 Agent 攻擊防護

提示詞注入（Prompt Injection）是多 Agent 系統特有的安全威脅。惡意輸入可以透過一個 Agent 傳播到其他 Agent：

```python
class PromptInjectionGuard:
    def __init__(self):
        self.dangerous_patterns = [
            "ignore previous instructions",
            "system prompt",
            "你是一個",
            "forget all",
            "ignore all rules"
        ]

    def sanitize(self, text: str) -> str:
        for pattern in self.dangerous_patterns:
            if pattern.lower() in text.lower():
                print(f"⚠️ 檢測到潛在注入：'{pattern}'")
                return "[內容已過濾]"

        return text

    def validate_message(self, message: dict) -> bool:
        payload = message.get("payload", "")
        if isinstance(payload, str):
            payload = self.sanitize(payload)
            message["payload"] = payload
        return True
```

跨 Agent 攻擊的典型場景：攻擊者讓 Researcher Agent 寫入惡意內容，然後 Coder Agent 相信並執行這些內容。隔離策略：

```python
class CrossAgentGuard:
    def check_message(self, sender: str, receiver: str,
                      message: dict) -> bool:
        # Coder Agent 不應該直接執行 Researcher 傳來的程式碼
        if receiver == "coder" and sender == "researcher":
            if message.get("type") == "execute_code":
                print(f"🛡️ 阻止：{sender} 試圖讓 {receiver} 執行程式碼")
                return False
        return True
```

## Agent 行為審計與合規

所有 Agent 行為必須可追溯、可審計。審計日誌是合規的基礎：

```python
class AuditTrail:
    def __init__(self):
        self.logs = []

    def record(self, agent_name: str, action: str,
               details: dict, approved_by: str = None):
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "agent": agent_name,
            "action": action,
            "details": details,
            "approved_by": approved_by
        }
        self.logs.append(entry)

    def query(self, agent_name: str = None,
              action: str = None,
              start_time: str = None) -> list:
        results = self.logs
        if agent_name:
            results = [r for r in results if r["agent"] == agent_name]
        if action:
            results = [r for r in results if r["action"] == action]
        if start_time:
            results = [r for r in results if r["timestamp"] >= start_time]
        return results

    def generate_report(self) -> str:
        report = ["# Agent 審計報告\n"]
        for log in self.logs:
            report.append(
                f"- [{log['timestamp']}] {log['agent']}: "
                f"{log['action']} (核准人：{log.get('approved_by', '自動')})"
            )
        return "\n".join(report)
```

---

**下一步**：[多 Agent 的未來](focus7.md)

## 延伸閱讀

- [OWASP LLM 安全性](https://www.google.com/search?q=OWASP+LLM+security+prompt+injection)
- [Human-in-the-Loop 設計](https://www.google.com/search?q=human+in+the+loop+AI+agent)
- [Agent 隔離技術](https://www.google.com/search?q=AI+agent+sandbox+isolation)
