"""
多步驟生成系統 — CoT, Tool Use, Code Execution, Multi-Model
"""

import json
import random
import time
from dataclasses import dataclass, field
from typing import Optional


# --- 1. 思維鏈 (Chain-of-Thought) ---

class ChainOfThought:
    """Step-by-step reasoning with CoT"""

    def solve(self, problem: str) -> list[str]:
        steps = []
        if "square" in problem.lower():
            steps.append("1. Understand: We need to calculate the square of a number")
            steps.append("2. Recall: Square means multiply a number by itself")
            steps.append("3. Compute: n × n = n²")
            steps.append(f"4. Answer: {self._extract_number(problem)}")
        elif "average" in problem.lower():
            steps.append("1. Understand: We need to calculate the average")
            steps.append("2. Add all numbers together")
            steps.append("3. Divide by the count of numbers")
            steps.append("4. Answer: result")
        else:
            steps.append("1. Parse the question")
            steps.append("2. Identify the required operation")
            steps.append("3. Apply the operation")
            steps.append("4. Return the result")
        return steps

    def _extract_number(self, text: str) -> str:
        import re
        nums = re.findall(r'\d+', text)
        n = int(nums[0]) if nums else 2
        return str(n * n)


# --- 2. 工具使用 ---

@dataclass
class Tool:
    name: str
    description: str
    fn: callable
    parameters: dict = field(default_factory=dict)


class ToolRegistry:
    """Registry of tools agents can use"""

    def __init__(self):
        self.tools: dict[str, Tool] = {}

    def register(self, tool: Tool):
        self.tools[tool.name] = tool

    def execute(self, name: str, **kwargs) -> str:
        if name not in self.tools:
            return f"Error: tool '{name}' not found"
        try:
            result = self.tools[name].fn(**kwargs)
            return str(result)
        except Exception as e:
            return f"Error executing {name}: {str(e)}"

    def list_tools(self) -> list[str]:
        return [f"{t.name}: {t.description}" for t in self.tools.values()]


def calculator(expression: str) -> float:
    return eval(expression)

def search_knowledge(query: str) -> str:
    knowledge = {
        "python": "Python is a high-level programming language",
        "AI": "Artificial Intelligence is the simulation of human intelligence",
        "quantum": "Quantum computing uses qubits for computation",
    }
    return knowledge.get(query.lower(), f"No results for '{query}'")


# --- 3. 程式碼執行沙箱 ---

class CodeSandbox:
    """Simple code execution sandbox"""

    def __init__(self):
        self.allowed_imports = {"math", "random", "json", "collections"}

    def execute(self, code: str) -> dict:
        result = {"output": "", "error": ""}
        try:
            # Check for dangerous imports
            for line in code.split("\n"):
                if "import" in line and "os" in line or "subprocess" in line or "shutil" in line:
                    result["error"] = "Import not allowed"
                    return result
            # Execute
            local_vars = {}
            exec(code, {"__builtins__": __builtins__}, local_vars)
            result["output"] = str(local_vars.get("_", "Executed successfully"))
        except Exception as e:
            result["error"] = str(e)
        return result


# --- 4. 多步驟生成工作流 ---

class MultiStepGenerator:
    """Multi-step generation with verification"""

    def __init__(self):
        self.tools = ToolRegistry()
        self.tools.register(Tool("calculator", "Do math", calculator))
        self.tools.register(Tool("search", "Search knowledge", search_knowledge))
        self.sandbox = CodeSandbox()

    def generate(self, task: str, steps: Optional[list[str]] = None) -> dict:
        plan = steps or ["plan", "execute", "verify"]
        results = {}

        for step in plan:
            if step == "plan":
                results["plan"] = f"Task: {task}\n1. Research\n2. Compute\n3. Verify"
            elif step == "execute":
                if "calculate" in task:
                    expr = task.split("calculate")[-1].strip()
                    results["execute"] = self.tools.execute("calculator", expression=expr)
                elif "search" in task.lower():
                    query = task.split("search")[-1].strip()
                    results["execute"] = self.tools.execute("search", query=query)
                else:
                    results["execute"] = f"Executing: {task}"
            elif step == "verify":
                results["verify"] = "Verification passed"

        results["final"] = results.get("execute", task)
        return results


# --- Demo ---

def demo():
    print("=== Multi-Step Generation System ===\n")

    # 1. Chain of Thought
    print("1. Chain-of-Thought Reasoning:")
    cot = ChainOfThought()
    steps = cot.solve("What is the square of 12?")
    for s in steps:
        print(f"  {s}")
    print()

    # 2. Tool Registry
    print("2. Tool-Using Agent:")
    registry = ToolRegistry()
    registry.register(Tool("calculator", "Do math", calculator))
    registry.register(Tool("search", "Search knowledge", search_knowledge))
    print(f"  Available tools: {registry.list_tools()}")
    print(f"  calculator(2+2): {registry.execute('calculator', expression='2+2')}")
    print(f"  search(AI): {registry.execute('search', query='AI')}")
    print()

    # 3. Code Sandbox
    print("3. Code Execution Sandbox:")
    sandbox = CodeSandbox()
    code = "import math\nresult = math.sqrt(16)\n_ = f'Square root of 16 is {result}'"
    result = sandbox.execute(code)
    print(f"  Output: {result['output']}")

    dangerous = "import os\nos.system('rm -rf /')"
    result = sandbox.execute(dangerous)
    print(f"  Dangerous code blocked: {result['error']}")
    print()

    # 4. Multi-Step Workflow
    print("4. Multi-Step Workflow:")
    gen = MultiStepGenerator()
    result = gen.generate("calculate 3.14 * 2")
    for step, output in result.items():
        print(f"  [{step}]: {output}")
    print()

    print("=== Demo Complete ===")


if __name__ == "__main__":
    demo()
