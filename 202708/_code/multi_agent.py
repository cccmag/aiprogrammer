"""
Multi-Agent Collaboration Framework — from scratch in Python

Demonstrates: Agent roles, task decomposition, message passing, tool use, orchestration
"""

import json
import random
from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime


# ---------------------------------------------------------------------------
# Message Protocol
# ---------------------------------------------------------------------------

@dataclass
class Message:
    sender: str
    receiver: str
    msg_type: str  # "task", "result", "request", "response", "error"
    content: str
    task_id: str = ""
    timestamp: str = ""

    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()

    def to_dict(self) -> dict:
        return {
            "sender": self.sender,
            "receiver": self.receiver,
            "type": self.msg_type,
            "content": self.content[:100],
            "task_id": self.task_id,
        }


# ---------------------------------------------------------------------------
# Tool System
# ---------------------------------------------------------------------------

class ToolRegistry:
    """Registry for tools that agents can use"""

    def __init__(self):
        self.tools: dict[str, dict] = {}

    def register(self, name: str, description: str, fn: callable):
        self.tools[name] = {"description": description, "fn": fn}

    def execute(self, name: str, **kwargs) -> str:
        tool = self.tools.get(name)
        if not tool:
            return f"Error: tool '{name}' not found"
        try:
            return tool["fn"](**kwargs)
        except Exception as e:
            return f"Error executing {name}: {e}"

    def list_tools(self) -> str:
        return "\n".join(f"  {n}: {t['description']}" for n, t in self.tools.items())


def create_default_tools() -> ToolRegistry:
    registry = ToolRegistry()
    registry.register("search_knowledge", "Search internal knowledge base", lambda q: f"Results for '{q}'")
    registry.register("calculate", "Perform arithmetic", lambda expr: str(eval(expr)))
    registry.register("read_file", "Read file content", lambda path: f"[Content of {path}]")
    registry.register("write_file", "Write content to file", lambda path, content: f"Written to {path}")
    return registry


# ---------------------------------------------------------------------------
# Base Agent
# ---------------------------------------------------------------------------

@dataclass
class Agent:
    name: str
    role: str
    system_prompt: str
    tools: ToolRegistry = field(default_factory=create_default_tools)
    inbox: list[Message] = field(default_factory=list)
    sent: list[Message] = field(default_factory=list)
    memory: list[str] = field(default_factory=list)
    max_retries: int = 3

    def send(self, receiver: str, msg_type: str, content: str, task_id: str = "") -> Message:
        msg = Message(self.name, receiver, msg_type, content, task_id)
        self.sent.append(msg)
        return msg

    def receive(self, msg: Message):
        self.inbox.append(msg)

    def process(self, llm_simulator: callable) -> list[Message]:
        """Process all messages in inbox and generate responses"""
        responses = []
        while self.inbox:
            msg = self.inbox.pop(0)
            response = self._handle_message(msg, llm_simulator)
            if response:
                responses.append(response)
        return responses

    def _handle_message(self, msg: Message, llm: callable) -> Optional[Message]:
        prompt = f"[{self.name} ({self.role})]\n"
        prompt += f"Received from {msg.sender}: {msg.content}\n"
        prompt += f"System prompt: {self.system_prompt}\n"

        result = llm(prompt)
        self.memory.append(f"{msg.sender} -> {self.name}: {msg.content[:50]}")

        response_text = result

        if "TOOL:" in result:
            parts = result.split("TOOL:")
            response_text = parts[0].strip()
            for part in parts[1:]:
                tool_call = part.strip().split("\n")[0]
                if "(" in tool_call:
                    name = tool_call.split("(")[0].strip()
                    args_str = "(" + "(".join(tool_call.split("(")[1:])
                    try:
                        args = eval(args_str)
                        if isinstance(args, dict):
                            tool_result = self.tools.execute(name, **args)
                        else:
                            tool_result = self.tools.execute(name)
                        response_text += f"\n[tool: {name}] {tool_result}"
                    except:
                        response_text += f"\n[tool: {name}] (failed)"

        return Message(self.name, msg.sender, "response", response_text, msg.task_id)


# ---------------------------------------------------------------------------
# Orchestrator
# ---------------------------------------------------------------------------

@dataclass
class Orchestrator:
    agents: dict[str, Agent] = field(default_factory=dict)
    message_log: list[Message] = field(default_factory=list)

    def add_agent(self, agent: Agent):
        self.agents[agent.name] = agent

    def send_message(self, msg: Message):
        self.message_log.append(msg)
        if msg.receiver in self.agents:
            self.agents[msg.receiver].receive(msg)
        else:
            print(f"Warning: agent '{msg.receiver}' not found")

    def run_step(self, sender: str, receiver: str, content: str, msg_type: str = "task",
                 task_id: str = "", llm: callable = None) -> list[Message]:
        """Send a message and process only the receiver's response"""
        msg = Message(sender, receiver, msg_type, content, task_id)
        self.send_message(msg)

        responses = []
        if receiver in self.agents:
            for r in self.agents[receiver].process(llm):
                self.message_log.append(r)
                responses.append(r)
        return responses

    def run_workflow(self, workflow: list[dict], llm: callable):
        for step in workflow:
            self.run_step(
                step["from"], step["to"], step["content"],
                step.get("type", "task"), step.get("task_id", ""), llm
            )

    def print_log(self):
        for msg in self.message_log:
            print(f"  [{msg.msg_type:8}] {msg.sender} -> {msg.receiver}: {msg.content[:60]}...")


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

def llm_simulator(prompt: str) -> str:
    """Simulate an LLM response (no real API call)"""
    if "Coder" in prompt and "write" in prompt.lower():
        return "Here's the implementation:\n```python\ndef hello():\n    print('hello world')\n```"
    if "Reviewer" in prompt and "code" in prompt.lower():
        return random.choice([
            "Code looks good, no issues found.",
            "I see a potential bug: missing error handling. TOOL: calculate(1+1)",
            "LGTM. The logic is correct and well-documented.",
        ])
    if "Researcher" in prompt:
        return "I found relevant information in the knowledge base."
    if "Tester" in prompt:
        return "Tests pass. Coverage is adequate."
    return f"I'll handle this task as {prompt.split('(')[1].split(')')[0] if '(' in prompt else 'the requested role'}."


def demo():
    print("=== Multi-Agent Collaboration Framework Demo ===\n")

    tools = create_default_tools()

    # Define agents
    agents = [
        Agent("Alice", "project manager", "You coordinate the team. Break down tasks, assign them, and collect results.",
              tools),
        Agent("Bob", "coder", "You write clean, efficient code. Respond with code blocks.", tools),
        Agent("Carol", "reviewer", "You review code for bugs, style, and correctness.", tools),
        Agent("Dave", "tester", "You write and run tests. Verify correctness.", tools),
    ]

    orchestrator = Orchestrator()
    for a in agents:
        orchestrator.add_agent(a)

    # Run a workflow: build a calculator app
    workflow = [
        {
            "from": "Alice", "to": "Bob", "task_id": "T1",
            "content": "Write a Python calculator that supports add, subtract, multiply, divide."
        },
        {
            "from": "Bob", "to": "Carol", "task_id": "T1",
            "content": "Please review my calculator implementation."
        },
        {
            "from": "Carol", "to": "Bob", "task_id": "T1",
            "content": "I found some issues. Please fix the divide-by-zero case."
        },
        {
            "from": "Bob", "to": "Dave", "task_id": "T1",
            "content": "Please test the calculator after fixes."
        },
        {
            "from": "Dave", "to": "Alice", "task_id": "T1",
            "content": "All tests pass. The calculator is ready."
        },
    ]

    orchestrator.run_workflow(workflow, llm_simulator)

    print("\n--- Message Log ---")
    orchestrator.print_log()

    print("\n--- Agent Memory ---")
    for agent in agents:
        print(f"  {agent.name} ({agent.role}): {len(agent.memory)} interactions")

    print("\n=== Demo Complete ===")


if __name__ == "__main__":
    demo()
