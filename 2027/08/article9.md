# 多 Agent 系統的效能與成本最佳化

## 前言

多 Agent 系統雖然強大，但 Token 消耗和 API 成本可能迅速失控。一個包含 5 個 Agent、每輪對話產生 2000 Tokens、執行 10 輪的系統，單次任務就可能消耗 100,000 Tokens。本文將探討如何在不犧牲品質的前提下，系統性地最佳化效能與成本。

---

## 一、成本分析模型

### 1.1 Token 成本追蹤

```python
from dataclasses import dataclass, field
from typing import List, Dict
from datetime import datetime
import json

@dataclass
class TokenUsage:
    prompt_tokens: int = 0
    completion_tokens: int = 0

    @property
    def total(self) -> int:
        return self.prompt_tokens + self.completion_tokens

    def cost(self, model: str = "gpt-4") -> float:
        pricing = {
            "gpt-4": {"prompt": 0.03, "completion": 0.06},
            "gpt-4-turbo": {"prompt": 0.01, "completion": 0.03},
            "gpt-3.5-turbo": {"prompt": 0.0005, "completion": 0.0015},
            "claude-3-opus": {"prompt": 0.015, "completion": 0.075},
            "claude-3-sonnet": {"prompt": 0.003, "completion": 0.015},
        }
        p = pricing.get(model, pricing["gpt-4"])
        return (self.prompt_tokens * p["prompt"] / 1000 +
                self.completion_tokens * p["completion"] / 1000)

@dataclass
class CostTracker:
    calls: List[dict] = field(default_factory=list)

    def log_call(self, agent: str, model: str, usage: TokenUsage):
        self.calls.append({
            "agent": agent,
            "model": model,
            "usage": usage,
            "cost": usage.cost(model),
            "timestamp": datetime.now().isoformat(),
        })

    def summary(self) -> Dict:
        if not self.calls:
            return {"total_cost": 0, "total_tokens": 0}
        total_cost = sum(c["cost"] for c in self.calls)
        total_tokens = sum(c["usage"].total for c in self.calls)
        by_agent = {}
        for c in self.calls:
            by_agent.setdefault(c["agent"], 0)
            by_agent[c["agent"]] += c["cost"]
        return {
            "total_cost": total_cost,
            "total_tokens": total_tokens,
            "total_calls": len(self.calls),
            "cost_by_agent": by_agent,
            "cost_by_model": {
                m: sum(c["cost"] for c in self.calls if c["model"] == m)
                for m in set(c["model"] for c in self.calls)
            },
        }

    def budget_check(self, budget: float) -> bool:
        return self.summary()["total_cost"] <= budget
```

### 1.2 成本即時監控

```python
class BudgetManager:
    def __init__(self, monthly_budget: float = 100.0):
        self.monthly_budget = monthly_budget
        self.tracker = CostTracker()
        self.warnings = []

    def check_before_call(self, agent: str, estimated_tokens: int) -> bool:
        total = self.tracker.summary()["total_cost"]
        estimated_cost = estimated_tokens * 0.03 / 1000

        if total + estimated_cost > self.monthly_budget:
            self.warnings.append(f"⚠ 預算不足：已用 ${total:.2f}，"
                                f"需要 ${estimated_cost:.4f}")
            return False

        if total + estimated_cost > self.monthly_budget * 0.8:
            print(f"⚠ 預算即將耗盡（已用 {total/self.monthly_budget*100:.0f}%）")

        return True
```

---

## 二、模型選擇策略

### 2.1 按任務分級

不同的 Agent 可以使用不同等級的模型：

```python
from typing import Optional

class ModelSelector:
    def __init__(self):
        self.model_tiers = {
            "premium": "gpt-4",
            "standard": "gpt-4-turbo",
            "economy": "gpt-3.5-turbo",
            "local": "llama-3-8b",
        }

    def select_model(self, task: dict) -> str:
        """根據任務特性選擇模型"""
        if task.get("requires_reasoning") or task.get("complexity", 0) > 7:
            return self.model_tiers["premium"]
        elif task.get("is_creative"):
            return self.model_tiers["standard"]
        elif task.get("is_routine"):
            return self.model_tiers["economy"]
        else:
            return self.model_tiers["standard"]

class CostAwareAgent:
    def __init__(self, name: str, selector: ModelSelector, tracker: CostTracker):
        self.name = name
        self.selector = selector
        self.tracker = tracker

    def process(self, task: dict, content: str) -> str:
        model = self.selector.select_model(task)

        # 小任務使用便宜模型
        response = call_llm(content, model=model)
        usage = TokenUsage(prompt_tokens=100, completion_tokens=50)
        self.tracker.log_call(self.name, model, usage)
        return response
```

| 任務類型 | 建議模型 | 每千 Token 成本 | 適合場景 |
|---------|---------|----------------|---------|
| 複雜推理 | GPT-4 / Claude Opus | $0.03–$0.06 | 程式碼生成、數學推理 |
| 一般任務 | GPT-4 Turbo / Sonnet | $0.01–$0.03 | 文件撰寫、資料分析 |
| 例行任務 | GPT-3.5 / Haiku | $0.0005–$0.003 | 分類、格式化、提取 |
| 批次處理 | 本地模型（Llama 3） | $0.0001 | 大規模批次、內部工具 |

---

## 三、快取策略

### 3.1 回應快取

```python
import hashlib
import json
import sqlite3
from typing import Optional

class ResponseCache:
    def __init__(self, db_path: str = "agent_cache.db"):
        self.conn = sqlite3.connect(db_path)
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS cache (
                key TEXT PRIMARY KEY,
                response TEXT,
                model TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.conn.commit()

    def _make_key(self, prompt: str, model: str) -> str:
        return hashlib.sha256(f"{model}:{prompt}".encode()).hexdigest()

    def get(self, prompt: str, model: str) -> Optional[str]:
        key = self._make_key(prompt, model)
        cursor = self.conn.execute(
            "SELECT response FROM cache WHERE key = ?", (key,)
        )
        row = cursor.fetchone()
        return row[0] if row else None

    def set(self, prompt: str, model: str, response: str):
        key = self._make_key(prompt, model)
        self.conn.execute(
            "INSERT OR REPLACE INTO cache (key, response, model) VALUES (?, ?, ?)",
            (key, response, model),
        )
        self.conn.commit()

    def hit_rate(self) -> float:
        """計算快取命中率"""
        # 簡化實作
        return 0.0
```

### 3.2 語義快取

對相似但不同的輸入進行模糊匹配：

```python
import numpy as np

class SemanticCache:
    def __init__(self, embedder, similarity_threshold: float = 0.95):
        self.embedder = embedder
        self.threshold = similarity_threshold
        self.cache: list = []

    def get(self, prompt: str) -> Optional[str]:
        query_vec = self.embedder.embed(prompt)
        for cached_prompt, response, vec in self.cache:
            similarity = np.dot(query_vec, vec) / (
                np.linalg.norm(query_vec) * np.linalg.norm(vec)
            )
            if similarity > self.threshold:
                return response
        return None

    def set(self, prompt: str, response: str):
        vec = self.embedder.embed(prompt)
        self.cache.append((prompt, response, vec))
```

---

## 四、並行執行與 Token 節省

### 4.1 批次處理

```python
import asyncio

class BatchProcessor:
    def __init__(self, max_concurrent: int = 5):
        self.semaphore = asyncio.Semaphore(max_concurrent)

    async def process_batch(self, items: list) -> list:
        """批次處理多個獨立任務"""
        async def process_one(item):
            async with self.semaphore:
                return await self._call_llm_async(item)

        tasks = [process_one(item) for item in items]
        return await asyncio.gather(*tasks)

    async def _call_llm_async(self, item):
        # 非同步 LLM 呼叫
        await asyncio.sleep(0.1)
        return f"processed: {item}"
```

### 4.2 Token 節省技術

```python
class TokenOptimizer:
    @staticmethod
    def truncate_history(messages: list, max_tokens: int = 3000) -> list:
        """保留最近的訊息，丟棄較舊的內容"""
        total = sum(len(m.get("content", "")) for m in messages)
        while total > max_tokens * 4 and len(messages) > 2:
            dropped = messages.pop(0)
            total -= len(dropped.get("content", ""))
        return messages

    @staticmethod
    def compress_prompt(prompt: str) -> str:
        """壓縮提示詞（移除多餘空白、註解）"""
        import re
        prompt = re.sub(r'\s+', ' ', prompt)
        prompt = re.sub(r'#.*?\n', '\n', prompt)
        return prompt.strip()

    @staticmethod
    def use_shorter_system_prompt(system_prompt: str) -> str:
        """將冗長的 system prompt 精簡為關鍵指令"""
        if len(system_prompt) > 500:
            lines = system_prompt.strip().split('\n')
            return '\n'.join(lines[:5] + ['...'] + lines[-3:])
        return system_prompt
```

---

## 五、成本控制策略總結

```python
class CostOptimizedPipeline:
    def __init__(self, monthly_budget: float):
        self.budget = BudgetManager(monthly_budget)
        self.cache = ResponseCache()
        self.selector = ModelSelector()
        self.optimizer = TokenOptimizer()

    async def run(self, agents: list, task: dict) -> dict:
        results = {}
        total_cost = 0

        for agent in agents:
            # 檢查預算
            if not self.budget.check_before_call(agent.name, 1000):
                print(f"⛔ 預算耗盡，跳過 {agent.name}")
                continue

            # 選擇模型
            model = self.selector.select_model(task)

            # 檢查快取
            cached = self.cache.get(task["prompt"], model)
            if cached:
                results[agent.name] = cached
                continue

            # 優化提示詞
            optimized = self.optimizer.compress_prompt(task["prompt"])

            # 執行
            response = agent.process({"model": model}, optimized)

            # 寫入快取
            self.cache.set(task["prompt"], model, response)
            results[agent.name] = response

        return {
            "results": results,
            "cost_report": self.budget.tracker.summary(),
        }
```

---

## 結語

多 Agent 系統的成本管理需要從架構設計就開始考慮。透過模型分級、回應快取、提示詞最佳化和預算監控，可以在維持輸出品質的同時，將成本控制在可接受的範圍內。隨著 LLM API 價格的持續下降和本地模型的成熟，多 Agent 系統的經濟性將會越來越好。

---

**參考資料**

- OpenAI API Pricing：https://openai.com/api/pricing/
- Anthropic API Pricing：https://docs.anthropic.com/en/docs/about-claude/pricing
- "Reducing LLM Costs in Production", https://www.databricks.com/blog/reducing-llm-costs-production
- LangSmith 成本追蹤：https://docs.smith.langchain.com/tracing/faq
