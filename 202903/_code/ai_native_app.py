"""
AI 原生應用框架 — 提示詞管理、RAG 整合、成本追蹤、監控
"""
import hashlib
import json
import time
import random
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class PromptTemplate:
    name: str
    template: str
    version: str = "v1"
    variables: list[str] = field(default_factory=list)

class PromptManager:
    def __init__(self):
        self.templates: dict[str, list[PromptTemplate]] = {}
    def register(self, pt: PromptTemplate):
        self.templates.setdefault(pt.name, []).append(pt)
    def render(self, name: str, **kwargs) -> Optional[str]:
        versions = self.templates.get(name, [])
        if not versions: return None
        pt = versions[-1]
        return pt.template.format(**kwargs) if pt.variables else pt.template
    def rollback(self, name: str, version: str) -> bool:
        versions = self.templates.get(name, [])
        for pt in versions:
            if pt.version == version:
                versions.remove(pt)
                versions.append(pt)
                return True
        return False

class RAGRetriever:
    def __init__(self):
        self.docs: list[dict] = []
    def add(self, doc_id: str, content: str, metadata: dict = None):
        self.docs.append({"id": doc_id, "content": content, "metadata": metadata or {}})
    def retrieve(self, query: str, k: int = 2) -> list[str]:
        random.seed(hash(query) % (2**31))
        return [d["content"][:50] for d in random.sample(self.docs, min(k, len(self.docs)))]

class AINativeApp:
    def __init__(self):
        self.prompts = PromptManager()
        self.rag = RAGRetriever()
        self.calls: list[dict] = []
    def call_llm(self, prompt: str, model: str = "gpt-6") -> dict:
        time.sleep(0.001)
        cost = {"gpt-6": 0.005, "claude-5": 0.003, "gemini-3": 0.001}.get(model, 0.001)
        tokens = len(prompt) // 2
        result = {"response": f"Response to: {prompt[:30]}...", "tokens": tokens, "cost": tokens * cost / 1000}
        self.calls.append({"model": model, "tokens": tokens, "cost": result["cost"], "time": time.time()})
        return result
    def total_cost(self) -> float: return sum(c["cost"] for c in self.calls)

def demo():
    print("=== AI-Native App Framework ===\n")
    app = AINativeApp()
    app.prompts.register(PromptTemplate("qa", "Question: {question}\nContext: {context}\nAnswer:", variables=["question", "context"], version="v2"))
    app.rag.add("doc1", "Python is a high-level programming language.", {"topic": "programming"})
    rendered = app.prompts.render("qa", question="What is Python?", context=app.rag.retrieve("Python")[0])
    print(f"  Rendered prompt: {rendered[:80]}...")
    result = app.call_llm(rendered, "gpt-6")
    print(f"  LLM response: {result['response']}")
    print(f"  Cost: ${result['cost']:.6f}")
    print(f"  Total cost: ${app.total_cost():.6f}")
    print("\n=== Demo Complete ===")

if __name__ == "__main__":
    demo()
