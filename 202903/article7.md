# AI 應用安全防護

## 前言

AI 原生應用面臨獨特的安全威脅：提示詞注入、資料外洩、模型劫持等。本文探討如何建立多層次的安全防護。

## 輸入驗證與消毒

```python
import re
from typing import Optional

class InputSanitizer:
    def __init__(self):
        self.blocked_patterns = [
            r"ignore\s+all\s+previous\s+instructions",
            r"system\s+prompt",
            r"你是一個",
            r"你是\w+模型",
        ]

    def sanitize(self, text: str) -> str:
        for pattern in self.blocked_patterns:
            text = re.sub(pattern, "[REDACTED]", text, flags=re.IGNORECASE)
        return text

    def detect_injection(self, text: str) -> bool:
        suspicious = [
            "forget", "ignore", "override", "system:",
            "## system", "role: system", "<|im_start|>system",
        ]
        return any(token in text.lower() for token in suspicious)

sanitizer = InputSanitizer()

async def safe_llm_call(user_input: str) -> str:
    clean_input = sanitizer.sanitize(user_input)
    if sanitizer.detect_injection(user_input):
        return "檢測到潛在的提示詞注入攻擊，已阻止請求"
    return await call_llm(clean_input)
```

## 輸出過濾

```python
class OutputFilter:
    def __init__(self):
        self.pii_patterns = [
            r"\b\d{3}-\d{2}-\d{4}\b",
            r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
            r"\b\d{16}\b",
        ]

    def filter_pii(self, text: str) -> str:
        for pattern in self.pii_patterns:
            text = re.sub(pattern, "[PII_REDACTED]", text)
        return text

    def validate_output(self, text: str) -> bool:
        forbidden_keywords = [
            "how to make a bomb", "如何製作炸彈",
            "sql injection example", "social security number"
        ]
        text_lower = text.lower()
        return not any(kw in text_lower for kw in forbidden_keywords)

output_filter = OutputFilter()

async def secure_output(response: str) -> str:
    filtered = output_filter.filter_pii(response)
    if not output_filter.validate_output(filtered):
        return "輸出內容違反安全政策"
    return filtered
```

## 速率限制與認證

```python
import time
from collections import defaultdict

class RateLimiter:
    def __init__(self, max_requests: int = 100, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window = window_seconds
        self.requests: dict[str, list[float]] = defaultdict(list)

    def check(self, user_id: str) -> bool:
        now = time.time()
        self.requests[user_id] = [
            t for t in self.requests[user_id]
            if now - t < self.window
        ]
        if len(self.requests[user_id]) >= self.max_requests:
            return False
        self.requests[user_id].append(now)
        return True

rate_limiter = RateLimiter(max_requests=30)

async def authenticated_llm_call(user_id: str, prompt: str) -> str:
    if not rate_limiter.check(user_id):
        raise PermissionError("Rate limit exceeded")
    sanitized = sanitizer.sanitize(prompt)
    response = await call_llm(sanitized)
    return await secure_output(response)
```

## 資料隔離

```python
class TenantIsolation:
    def __init__(self):
        self.tenants: dict[str, list[str]] = {}

    def add_context(self, tenant_id: str, context: str):
        self.tenants.setdefault(tenant_id, []).append(context)

    def build_prompt(self, tenant_id: str, user_query: str) -> str:
        tenant_context = self.tenants.get(tenant_id, [])
        context_block = "\n".join(tenant_context)
        return f"[Tenant: {tenant_id}]\n{context_block}\n\n{user_query}"
```

## 結語

AI 應用的安全防護需要從輸入、輸出、認證、隔離多個面向著手。提示詞注入是最常見的威脅，結合輸入消毒、輸出過濾和速率限制，可以有效降低風險。

---

**延伸閱讀**

- [OWASP LLM 安全指南](https://www.google.com/search?q=OWASP+LLM+security+top+10)
- [提示詞注入防禦](https://www.google.com/search?q=prompt+injection+defense+techniques)
- [AI 應用安全架構](https://www.google.com/search?q=AI+application+security+architecture)
