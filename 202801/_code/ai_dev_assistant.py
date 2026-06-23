"""
AI 輔助軟體工程工具 — 程式碼生成、測試生成、自動修復
"""

import ast
import random
import re
from dataclasses import dataclass, field

# --- 1. 程式碼生成模板 ---

TEMPLATES = {
    "fibonacci": {
        "signature": "def fibonacci(n: int) -> list[int]:",
        "description": "Generate first n Fibonacci numbers"
    },
    "sort": {
        "signature": "def quicksort(arr: list[int]) -> list[int]:",
        "description": "Sort list using quicksort"
    },
    "prime": {
        "signature": "def is_prime(n: int) -> bool:",
        "description": "Check if number is prime"
    }
}

def generate_code(template: str) -> str:
    """Simulate code generation (in production, use LLM)"""
    if template == "fibonacci":
        return """def fibonacci(n: int) -> list[int]:
    if n <= 0:
        return []
    result = [0, 1]
    for _ in range(2, n):
        result.append(result[-1] + result[-2])
    return result[:n]
"""
    elif template == "quicksort":
        return """def quicksort(arr: list[int]) -> list[int]:
    if len(arr) <= 1:
        return arr
    pivot = arr[0]
    left = [x for x in arr[1:] if x <= pivot]
    right = [x for x in arr[1:] if x > pivot]
    return quicksort(left) + [pivot] + quicksort(right)
"""
    return ""


# --- 2. 測試生成 ---

def generate_tests(code: str, func_name: str) -> str:
    """Generate test cases for a function"""
    tests = f"""
def test_{func_name}():
    # Test basic case
    result = {func_name}(5)
    assert len(result) == 5, "Should return 5 elements"
    
    # Test edge case
    result = {func_name}(0)
    assert result == [], "Should return empty"
    
    # Test type
    assert isinstance(result, list), "Should return list"
    print(f"All tests passed for {func_name}")
"""
    return tests


# --- 3. 程式碼審查 ---

REVIEW_PATTERNS = {
    "unused_variable": re.compile(r"(\w+)\s*=\s*.+\n(?!.*\1)"),
    "bare_except": re.compile(r"except\s*:"),
    "mutable_default": re.compile(r"def\s+\w+\(.*=\s*(\[\]|{{}}|set\(\))\)"),
}

def review_code(code: str) -> list[dict]:
    """Review code for common issues"""
    issues = []
    lines = code.split("\n")
    for i, line in enumerate(lines, 1):
        if REVIEW_PATTERNS["bare_except"].search(line):
            issues.append({"line": i, "message": "Bare except clause", "severity": "warning"})
        if REVIEW_PATTERNS["mutable_default"].search(line):
            issues.append({"line": i, "message": "Mutable default argument", "severity": "error"})
    return issues


# --- 4. 自動修復 ---

BUGGY_CODE = """
def divide(a, b):
    return a / b

def get_item(lst, idx):
    return lst[idx]
"""

SAFE_CODE = """
def divide(a, b):
    if b == 0:
        return None
    return a / b

def get_item(lst, idx):
    if not isinstance(lst, (list, tuple)):
        return None
    if idx < 0 or idx >= len(lst):
        return None
    return lst[idx]
"""

def fix_common_bugs(code: str) -> str:
    """Fix division by zero and out-of-bounds access"""
    fixed = code
    # Fix division by zero
    fixed = re.sub(
        r"def divide\(a,\s*b\):\s*\n\s+return a / b",
        "def divide(a, b):\n    if b == 0:\n        return None\n    return a / b",
        fixed
    )
    # Fix out-of-bounds
    fixed = re.sub(
        r"def get_item\(lst,\s*idx\):\s*\n\s+return lst\[idx\]",
        "def get_item(lst, idx):\n    if not isinstance(lst, (list, tuple)):\n        return None\n    if idx < 0 or idx >= len(lst):\n        return None\n    return lst[idx]",
        fixed
    )
    return fixed


# --- Demo ---

def demo():
    print("=== AI Software Engineering Assistant ===\n")

    # 1. Code Generation
    print("1. Code Generation:")
    for name in TEMPLATES:
        code = generate_code(name if name != "sort" else "quicksort")
        print(f"  [{name}]")
        for line in code.strip().split("\n")[:3]:
            print(f"    {line}")
        print()

    # 2. Test Generation
    print("2. Test Generation:")
    code = generate_code("fibonacci")
    tests = generate_tests(code, "fibonacci")
    print(tests)

    # 3. Code Review
    print("3. Code Review:")
    sample_code = """
def process(data):
    try:
        result = data / 2
    except:
        pass
    return result
"""
    issues = review_code(sample_code)
    for issue in issues:
        print(f"  Line {issue['line']}: [{issue['severity']}] {issue['message']}")
    print()

    # 4. Auto-fix
    print("4. Auto-fix:")
    fixed = fix_common_bugs(BUGGY_CODE)
    print(f"  Before ({len(BUGGY_CODE)} chars)")
    print(f"  After  ({len(fixed)} chars, +safety guards)")
    print()

    print("=== Demo Complete ===")


if __name__ == "__main__":
    demo()
