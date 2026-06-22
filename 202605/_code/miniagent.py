#!/usr/bin/env python3
"""MiniAgent - A minimal ReAct agent framework"""

import json
import re
from dataclasses import dataclass
from typing import Any, Callable

# =====================
# Data Types
# =====================

@dataclass
class Tool:
    name: str
    description: str
    func: Callable
    parameters: dict

@dataclass
class AgentMessage:
    role: str
    content: str

# =====================
# Memory
# =====================

class SimpleMemory:
    def __init__(self):
        self.messages = []
        self.summary = ""

    def add(self, role, content):
        self.messages.append(AgentMessage(role, content))
        if len(self.messages) > 20:
            self.compress()

    def compress(self):
        early = [m.content for m in self.messages[:10]]
        summary = " | ".join(early)
        self.summary = f"[SUMMARY] {summary} [END_SUMMARY]" if not self.summary else f"{self.summary} -> {summary[:100]}"
        self.messages = self.messages[-10:]

    def get_context(self):
        ctx = []
        if self.summary:
            ctx.append(("system", f"Previous conversation summary: {self.summary}"))
        for m in self.messages:
            ctx.append((m.role, m.content))
        return ctx

# =====================
# Tools
# =====================

class ToolRegistry:
    def __init__(self):
        self.tools = {}

    def register(self, name, description, func, parameters=None):
        self.tools[name] = Tool(name, description, func, parameters or {})

    def execute(self, name, **kwargs):
        if name not in self.tools:
            return f"Error: unknown tool '{name}'"
        try:
            return self.tools[name].func(**kwargs)
        except Exception as e:
            return f"Error executing {name}: {e}"

    def get_descriptions(self):
        return "\n".join([
            f"- {t.name}: {t.description}"
            for t in self.tools.values()
        ])

# =====================
# LLM Interface
# =====================

class LLMInterface:
    def generate(self, messages, tools_desc="") -> str:
        raise NotImplementedError

class MockLLM(LLMInterface):
    def __init__(self, responses=None):
        self.responses = responses or []
        self.idx = 0

    def generate(self, messages, tools_desc=""):
        if self.idx < len(self.responses):
            r = self.responses[self.idx]
            self.idx += 1
            return r
        return "Thought: I have completed the task.\nFinal Answer: Task completed."

# =====================
# ReAct Agent
# =====================

REACT_PROMPT = """You are an AI assistant with access to the following tools:

{tools}

You must respond in the following format:

Thought: your reasoning about what to do next
Action: tool_name
Action Input: {{"param": "value"}}

Or if you have the final answer:

Thought: I have all the information needed
Final Answer: your answer here

Begin!"""

class ReActAgent:
    def __init__(self, llm, tools: ToolRegistry, max_steps=10):
        self.llm = llm
        self.tools = tools
        self.max_steps = max_steps
        self.memory = SimpleMemory()

    def run(self, task: str) -> str:
        self.memory.add("user", task)
        context = self.memory.get_context()
        tools_desc = self.tools.get_descriptions()

        system_prompt = REACT_PROMPT.format(tools=tools_desc)
        messages = [("system", system_prompt)]
        messages.extend(context)

        for step in range(self.max_steps):
            response = self.llm.generate(messages)

            if "Final Answer:" in response:
                answer = response.split("Final Answer:")[-1].strip()
                self.memory.add("assistant", answer)
                return answer

            action = self._parse_action(response)
            if action:
                tool_name = action.get("tool")
                params = action.get("params", {})
                result = self.tools.execute(tool_name, **params)
                messages.append(("assistant", response))
                messages.append(("system", f"Observation: {result}"))
                self.memory.add("assistant", f"{response}\nObservation: {result}")

        return "Max steps reached without final answer."

    def _parse_action(self, response):
        tool_match = re.search(r"Action:\s*(\w+)", response)
        input_match = re.search(r"Action Input:\s*(\{.+?\}|.+)", response, re.DOTALL)
        if not tool_match:
            return None
        tool_name = tool_match.group(1)
        params = {}
        if input_match:
            try:
                params = json.loads(input_match.group(1))
            except json.JSONDecodeError:
                raw = input_match.group(1).strip()
                params = {"input": raw}
        return {"tool": tool_name, "params": params}

# =====================
# Built-in Tools
# =====================

def build_default_tools():
    registry = ToolRegistry()

    def calculator(expression: str):
        safe = re.sub(r'[^0-9+\-*/().,% ]', '', expression)
        try:
            return str(eval(safe))
        except Exception as e:
            return f"Error: {e}"

    def search_web(query: str):
        return f'[Simulated] Search results for "{query}": Found relevant information about {query}.'

    def get_time():
        from datetime import datetime
        return f"Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

    registry.register("calculator", "Execute mathematical expressions", calculator, {
        "expression": "string"
    })
    registry.register("search_web", "Search the web for information", search_web, {
        "query": "string"
    })
    registry.register("get_time", "Get the current date and time", get_time)

    return registry

# =====================
# Multi-Agent Team
# =====================

class AgentTeam:
    def __init__(self):
        self.agents = {}

    def add_agent(self, name, agent):
        self.agents[name] = agent

    def run(self, workflow):
        results = {}
        for step in workflow:
            agent_name = step["agent"]
            task = step["task"].format(**results)
            result = self.agents[agent_name].run(task)
            results[step.get("output_key", agent_name)] = result
        return results

# =====================
# Test
# =====================

def test():
    tools = build_default_tools()

    mock_responses = [
        """Thought: I need to calculate 2 + 3 first, then multiply by 4.
Action: calculator
Action Input: {"expression": "2 + 3"}""",
        """Observation: 5
Thought: Now I multiply 5 by 4.
Action: calculator
Action Input: {"expression": "5 * 4"}""",
        """Observation: 20
Thought: I have the result.
Final Answer: The result of (2 + 3) * 4 is 20.""",
    ]

    llm = MockLLM(mock_responses)
    agent = ReActAgent(llm, tools)

    result = agent.run("What is (2 + 3) * 4?")
    print(f"Task: (2 + 3) * 4")
    print(f"Result: {result}")
    print()

    mock_responses2 = [
        """Thought: I need to check the current time first.
Action: get_time
Action Input: {}""",
        """Observation: Current time: 2026-05-15 10:30:00
Thought: Now I have the time information.
Final Answer: The current time is 2026-05-15 10:30:00.""",
    ]

    llm2 = MockLLM(mock_responses2)
    agent2 = ReActAgent(llm2, tools)
    result2 = agent2.run("What time is it?")
    print(f"Task: What time is it?")
    print(f"Result: {result2}")
    print()

    print("=== Multi-Agent Team Demo ===")
    researcher = ReActAgent(MockLLM([
        """Thought: I need to search for information.
Action: search_web
Action Input: {"query": "latest AI news 2026"}""",
        """Thought: I found the information.
Final Answer: In 2026, AI technology has advanced significantly with GPT-6 and Llama 4."""
    ]), tools)

    writer = ReActAgent(MockLLM([
        """Thought: I need to organize the research into an article.
Final Answer: ## AI in 2026\n\nArtificial intelligence has made remarkable progress in 2026, with major releases from OpenAI (GPT-6) and Meta (Llama 4)."""
    ]), tools)

    team = AgentTeam()
    team.add_agent("researcher", researcher)
    team.add_agent("writer", writer)

    workflow = [
        {"agent": "researcher", "task": "Research latest AI developments", "output_key": "research"},
        {"agent": "writer", "task": "Write an article based on: {research}", "output_key": "article"},
    ]

    team_results = team.run(workflow)
    print(f"Research: {team_results['research']}")
    print(f"Article: {team_results['article']}")

if __name__ == "__main__":
    test()
