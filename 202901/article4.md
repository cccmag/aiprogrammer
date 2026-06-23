# 錯誤處理與重試策略

## 1. 引言

AI 工作流中，錯誤是常態而非例外。LLM API 可能超時、回傳格式異常、或產生幻覺。一套完善的錯誤處理與重試策略，是生產級工作流的必備基礎設施。

## 2. 指數退避重試

最基本的重試策略，每次重試間隔時間呈指數增長，避免雪崩效應。

```python
import time
import random
from functools import wraps
from typing import Callable, Any

def retry_with_backoff(
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    exponential_base: float = 2.0,
):
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_exception = None
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt == max_retries:
                        raise
                    delay = min(
                        base_delay * (exponential_base ** attempt)
                        + random.uniform(0, 0.1),
                        max_delay,
                    )
                    print(f"[重試 {attempt+1}/{max_retries}] 等待 {delay:.1f}s")
                    time.sleep(delay)
            return None
        return wrapper
    return decorator

@retry_with_backoff(max_retries=3)
def call_llm_api(prompt: str) -> str:
    # 模擬 API 呼叫
    if random.random() < 0.5:
        raise ConnectionError("API 超時")
    return f"回應: {prompt}"
```

## 3. 智慧重試：區分可重試與不可重試錯誤

並非所有錯誤都值得重試。無效輸入、權限錯誤等不應重試。

```python
class RetryableError(Exception):
    """可重試的暫時性錯誤"""

class NonRetryableError(Exception):
    """不可重試的永久性錯誤"""

class SmartRetryHandler:
    RETRYABLE_CODES = {429, 500, 502, 503, 504}

    def should_retry(self, exception: Exception) -> bool:
        if isinstance(exception, NonRetryableError):
            return False
        if isinstance(exception, RetryableError):
            return True
        if hasattr(exception, "status_code"):
            return exception.status_code in self.RETRYABLE_CODES
        return True

    def handle_llm_error(self, response: dict) -> str:
        error_code = response.get("error", {}).get("code", "unknown")
        if error_code == "context_length_exceeded":
            raise NonRetryableError("輸入過長，需重新分段")
        if error_code == "rate_limit_exceeded":
            raise RetryableError("速率限制，可重試")
        if error_code == "internal_error":
            raise RetryableError("伺服器內部錯誤")
        raise NonRetryableError(f"未知錯誤: {error_code}")
```

## 4. 輸出驗證與型別強制轉換

LLM 的非確定性輸出常需驗證與修正。

```python
import json
import re
from typing import Optional

class OutputValidator:
    def __init__(self, retry_handler: SmartRetryHandler):
        self.retry_handler = retry_handler

    def extract_json(self, raw: str) -> Optional[dict]:
        json_match = re.search(r"\{.*\}", raw, re.DOTALL)
        if not json_match:
            return None
        try:
            return json.loads(json_match.group())
        except json.JSONDecodeError:
            return None

    def validate_and_fix(
        self, output: dict, schema: dict
    ) -> dict:
        validated = {}
        for key, expected_type in schema.items():
            value = output.get(key)
            if value is None:
                print(f"[驗證] 缺少欄位 {key}，使用預設值")
                validated[key] = expected_type()
            elif not isinstance(value, expected_type):
                print(f"[驗證] {key} 型別錯誤，嘗試轉換")
                validated[key] = expected_type(value)
            else:
                validated[key] = value
        return validated
```

## 5. Circuit Breaker 模式

當錯誤率過高時，暫時切斷請求以保護系統。

```python
import time
from collections import deque

class CircuitBreaker:
    def __init__(
        self, failure_threshold: int = 5, recovery_timeout: float = 30.0
    ):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failures: deque = deque(maxlen=failure_threshold)
        self.state = "closed"
        self.last_failure_time = 0.0

    def call(self, func: Callable, *args, **kwargs) -> Any:
        if self.state == "open":
            if time.time() - self.last_failure_time > self.recovery_timeout:
                self.state = "half-open"
            else:
                raise RuntimeError("Circuit breaker is OPEN")

        try:
            result = func(*args, **kwargs)
            if self.state == "half-open":
                self.state = "closed"
                self.failures.clear()
            return result
        except Exception as e:
            self.failures.append(time.time())
            self.last_failure_time = time.time()
            if len(self.failures) >= self.failure_threshold:
                self.state = "open"
            raise e
```

## 6. 實戰建議

- **區分暫時性 vs 永久性錯誤**：避免浪費重試資源
- **設定最大重試次數**：防止無限循環
- **加入抖動 (Jitter)**：避免多個客戶端同時重試
- **記錄完整錯誤上下文**：便於除錯與監控
- **Circuit Breaker + 重試**：雙層保護

---

**參考資料**
- [指數退避與抖動](https://www.google.com/search?q=exponential+backoff+jitter+retry+strategy)
- [Circuit Breaker 模式](https://www.google.com/search?q=circuit+breaker+pattern+microservices)
- [LLM 輸出驗證最佳實踐](https://www.google.com/search?q=LLM+output+validation+structured+generation)
