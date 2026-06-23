"""
多模態 Agent 框架 — 視覺、語音、文字的統一 Agent
"""
import random
import time
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class MultiModalInput:
    text: Optional[str] = None
    image_caption: Optional[str] = None
    audio_transcript: Optional[str] = None

@dataclass
class AgentAction:
    tool: str
    params: dict
    reasoning: str = ""

class MultiModalAgent:
    def __init__(self, name: str = "Agent"):
        self.name = name
        self.memory: list[str] = []
    def perceive(self, inp: MultiModalInput) -> str:
        cues = []
        if inp.text: cues.append(f"text({inp.text[:30]})")
        if inp.image_caption: cues.append(f"image({inp.image_caption[:30]})")
        if inp.audio_transcript: cues.append(f"audio({inp.audio_transcript[:30]})")
        return f"Perceived: {', '.join(cues)}"
    def reason(self, perception: str) -> AgentAction:
        time.sleep(0.001)
        self.memory.append(perception)
        if "cat" in perception.lower():
            return AgentAction("search", {"query": "cat breeds"}, "User mentioned a cat")
        return AgentAction("respond", {"message": f"Understood based on: {perception[:40]}"})
    def execute(self, action: AgentAction) -> str:
        tools = {"search": lambda **kw: f"Results for '{kw.get('query', '')}': ...", "respond": lambda **kw: f"Agent says: {kw.get('message', '')}"}
        fn = tools.get(action.tool, lambda **kw: "Unknown tool")
        return fn(**action.params)

def demo():
    print("=== Multi-Modal Agent Framework ===\n")
    agent = MultiModalAgent("VisionBot")
    inputs = [
        MultiModalInput(text="What is that animal?", image_caption="A cat sitting on a windowsill"),
        MultiModalInput(audio_transcript="User said: hello"),
        MultiModalInput(text="Analyze this scene", image_caption="Sunset over mountains", audio_transcript="wind sounds"),
    ]
    for inp in inputs:
        perception = agent.perceive(inp)
        action = agent.reason(perception)
        result = agent.execute(action)
        print(f"  Input: {[v for v in [inp.text, inp.image_caption, inp.audio_transcript] if v][0][:25]}...")
        print(f"  Action: {action.tool}({action.params}) → {result[:40]}...")
        print()
    print(f"  Memory: {len(agent.memory)} items")
    print("\n=== Demo Complete ===")

if __name__ == "__main__":
    demo()
