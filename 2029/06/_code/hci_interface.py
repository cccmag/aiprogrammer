"""
人機協作介面 — 自適應互動、意圖理解、工作流整合
"""
import time
import random
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class UserIntent:
    action: str
    params: dict
    confidence: float

class IntentRecognizer:
    def recognize(self, text: str) -> UserIntent:
        if "search" in text.lower():
            return UserIntent("search", {"query": text.replace("search", "").strip()}, 0.9)
        if "create" in text.lower() or "generate" in text.lower():
            return UserIntent("generate", {"prompt": text}, 0.85)
        if "help" in text.lower():
            return UserIntent("help", {"topic": text.replace("help", "").strip()}, 0.95)
        return UserIntent("chat", {"message": text}, 0.6)

class AdaptiveInterface:
    def __init__(self):
        self.usage: dict[str, int] = {}
    def track(self, action: str):
        self.usage[action] = self.usage.get(action, 0) + 1
    def suggest_shortcuts(self) -> list[str]:
        sorted_actions = sorted(self.usage.items(), key=lambda x: -x[1])
        return [f"Quick {a}: {c} uses" for a, c in sorted_actions[:3]]
    def adapt_layout(self) -> str:
        if not self.usage: return "default"
        most_used = max(self.usage, key=self.usage.get)
        return f"{most_used}_optimized"

class CollaborationSession:
    def __init__(self):
        self.history: list[str] = []
    def turn(self, user: str, ai: str):
        self.history.append(f"User: {user}")
        self.history.append(f"AI: {ai}")
    def summary(self) -> str: return "\n".join(self.history[-6:])

def demo():
    print("=== Human-AI Collaboration Interface ===\n")
    recognizer = IntentRecognizer()
    interface = AdaptiveInterface()
    session = CollaborationSession()
    inputs = ["search AI papers", "generate a summary", "help with setup", "search datasets", "create report"]
    for inp in inputs:
        intent = recognizer.recognize(inp)
        interface.track(intent.action)
        response = f"Executing '{intent.action}' (confidence: {intent.confidence:.0%})"
        session.turn(inp, response)
        print(f"  '{inp}' → {response}")
    print(f"\n  Shortcuts: {interface.suggest_shortcuts()}")
    print(f"  Layout: {interface.adapt_layout()}")
    print(f"\n  Session history:\n  {session.summary()}")
    print("\n=== Demo Complete ===")

if __name__ == "__main__":
    demo()
