"""
Agent 工作流引擎 — 工作流定義、排程、執行、監控
"""
import time
import random
from dataclasses import dataclass, field
from typing import Optional, Callable

@dataclass
class WorkflowStep:
    name: str
    action: Callable
    retry_count: int = 0
    max_retries: int = 3
    timeout: float = 30.0

@dataclass
class Workflow:
    name: str
    steps: list[WorkflowStep] = field(default_factory=list)
    context: dict = field(default_factory=dict)

class WorkflowEngine:
    def __init__(self):
        self.workflows: dict[str, Workflow] = {}
        self.history: list[dict] = []

    def register(self, wf: Workflow):
        self.workflows[wf.name] = wf

    def run(self, name: str, **inputs) -> dict:
        wf = self.workflows.get(name)
        if not wf:
            return {"error": f"Workflow '{name}' not found"}
        wf.context.update(inputs)
        results = {}
        for step in wf.steps:
            for attempt in range(step.max_retries + 1):
                try:
                    start = time.time()
                    result = step.action(wf.context)
                    elapsed = time.time() - start
                    results[step.name] = {"status": "success", "result": result, "duration": elapsed}
                    wf.context[step.name] = result
                    self.history.append({"wf": name, "step": step.name, "status": "success", "time": elapsed})
                    break
                except Exception as e:
                    if attempt < step.max_retries:
                        time.sleep(0.1 * (attempt + 1))
                    else:
                        results[step.name] = {"status": "failed", "error": str(e)}
                        self.history.append({"wf": name, "step": step.name, "status": "failed", "error": str(e)})
                        return {"results": results, "failed_at": step.name}
        return {"results": results, "failed_at": None}

def demo():
    print("=== Agent Workflow Engine ===\n")
    def research(ctx): return {"topic": "AI Agents", "sources": 5}
    def draft(ctx): return f"Draft about {ctx['research']['topic']}"
    def review(ctx): return "Approved" if random.random() > 0.2 else "Needs revision"
    def publish(ctx): return f"Published: {ctx['draft']}"

    wf = Workflow("content_pipeline", [
        WorkflowStep("research", lambda ctx: research(ctx)),
        WorkflowStep("draft", lambda ctx: draft(ctx)),
        WorkflowStep("review", lambda ctx: review(ctx), max_retries=2),
        WorkflowStep("publish", lambda ctx: publish(ctx)),
    ])
    engine = WorkflowEngine()
    engine.register(wf)
    result = engine.run("content_pipeline")
    for name, r in result["results"].items():
        status = r["status"]
        print(f"  {name}: {status} ({r.get('duration', 0):.2f}s)")
    print(f"  Failed at: {result['failed_at']}")
    print(f"  History: {len(engine.history)} steps logged")
    print("\n=== Demo Complete ===")

if __name__ == "__main__":
    demo()
