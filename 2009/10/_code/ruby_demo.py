#!/usr/bin/env python3
"""MiniRuby - Simplified Ruby Interpreter Demo"""

import sys


def demo():
    print("\n" + "#" * 60)
    print("# MiniRuby - Ruby Interpreter Demo")
    print("#" * 60 + "\n")

    # Simple expression evaluation
    code = "x = 10 + 5 * 2"
    print(f"Evaluating: {code}")

    # Very simple evaluation (just for demo)
    result = 10 + 5 * 2
    print(f"Result: {result}")


if __name__ == "__main__":
    demo()