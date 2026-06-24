# 任務分解與排程（2018-2026）

## 任務分解策略

### Top-down：規劃→執行

最高層的 Agent 先將任務分解為子任務，再逐層遞迴。這種方式的優點是整體方向可控，缺點是規劃階段的錯誤會傳遞到所有子任務。

```python
class TopDownPlanner:
    def plan(self, task: str, depth: int = 0) -> list:
        if depth > 3 or self.is_atomic(task):
            return [task]

        sub_tasks = self.llm.generate(
            f"將以下任務分解為 3-5 個子任務：\n{task}"
        )
        result = []
        for sub in sub_tasks:
            result.extend(self.plan(sub, depth + 1))
        return result
```

### Bottom-up：結果聚合

多個 Agent 平行產生結果，再由聚合層合併。這種方式的優點是探索性強，缺點是可能產生衝突的結果。

```python
class BottomUpAggregator:
    def run(self, task: str, agents: list) -> str:
        results = {}
        for i, agent in enumerate(agents):
            perspective = f"從第 {i} 個角度分析：{agent.perspective}"
            results[i] = agent.run(f"{perspective}\n任務：{task}")

        # 聚合所有結果
        combined = self.llm.generate(
            f"請合併以下{'、'.join(results.values())}\n保持一致性，去重。"
        )
        return combined
```

## 依賴圖與 DAG 排程

大多數多 Agent 任務可以用有向無環圖（DAG）表示。每個節點是一個子任務，邊表示依賴關係：

```python
from collections import deque

class DAGScheduler:
    def __init__(self):
        self.graph = {}  # task_id -> [dependent_task_ids]
        self.tasks = {}

    def add_task(self, task_id: str, agent: str, prompt: str,
                 depends_on: list = None):
        self.tasks[task_id] = {"agent": agent, "prompt": prompt}
        self.graph[task_id] = depends_on or []

    def topological_sort(self) -> list:
        in_degree = {t: 0 for t in self.tasks}
        for deps in self.graph.values():
            for dep in deps:
                in_degree[dep] += 1

        queue = deque([t for t, d in in_degree.items() if d == 0])
        result = []

        while queue:
            task = queue.popleft()
            result.append(task)
            for dependent in self.graph[task]:
                in_degree[dependent] -= 1
                if in_degree[dependent] == 0:
                    queue.append(dependent)

        return result

    def execute(self, agent_pool: dict) -> dict:
        order = self.topological_sort()
        outputs = {}

        for task_id in order:
            task = self.tasks[task_id]
            deps = self.graph[task_id]
            context = {d: outputs[d] for d in deps}
            agent = agent_pool[task["agent"]]
            outputs[task_id] = agent.run(task["prompt"], context)

        return outputs
```

## 平行執行與結果合併

無依賴的子任務可以平行執行。Python 中可以用 `concurrent.futures`：

```python
from concurrent.futures import ThreadPoolExecutor, as_completed

class ParallelExecutor:
    def __init__(self, max_workers: int = 5):
        self.pool = ThreadPoolExecutor(max_workers=max_workers)

    def execute_parallel(self, tasks: list, agent_pool: dict) -> list:
        futures = []

        for task in tasks:
            agent = agent_pool[task["agent"]]
            future = self.pool.submit(agent.run, task["prompt"])
            futures.append((task["id"], future))

        results = []
        for task_id, future in as_completed(futures):
            results.append({"id": task_id, "output": future.result()})

        return self.merge_results(results)

    def merge_results(self, results: list) -> str:
        # 使用 Merge Agent 合併結果
        text = "\n".join(r["output"] for r in results)
        return merge_agent.run(f"合併以下內容：\n{text}")
```

## 動態重新規劃與錯誤恢復

執行過程中子任務可能失敗。好的多 Agent 系統需要能動態重新規劃：

```python
class AdaptivePlanner:
    def execute_with_retry(self, task: dict, agent_pool: dict,
                           max_retries: int = 3):
        for attempt in range(max_retries):
            try:
                return agent_pool[task["agent"]].run(task["prompt"])
            except AgentError as e:
                if attempt == max_retries - 1:
                    # 最後一次失敗：重新規劃
                    return self.replan(task, e)
                # 重試前先簡化任務
                task["prompt"] += "\n注意上一步錯誤，請避開。"

    def replan(self, failed_task: dict, error: AgentError) -> str:
        replan_prompt = (
            f"子任務失敗：{failed_task}\n"
            f"錯誤：{error}\n"
            "請提出替代方案："
        )
        return planner_agent.run(replan_prompt)
```

---

**下一步**：[Agent 通訊協議](focus4.md)

## 延伸閱讀

- [DAG 排程與任務分解](https://www.google.com/search?q=DAG+scheduling+multi+agent+system)
- [AutoGen 任務排程](https://www.google.com/search?q=AutoGen+task+decomposition)
- [動態重規劃](https://www.google.com/search?q=dynamic+replanning+LLM+agent)
