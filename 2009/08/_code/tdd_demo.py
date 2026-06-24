#!/usr/bin/env python3
"""TDD Demo - Simplified Testing Framework"""

import sys


def expect(value):
    class A:
        def to_equal(self, expected):
            if value != expected:
                raise AssertionError(f"Expected {expected}, got {value}")
    return A()


def demo():
    print("\n" + "#" * 60)
    print("# TDD Testing Framework Demo")
    print("#" * 60 + "\n")

    class Calculator:
        def add(self, a, b):
            return a + b

    calc = Calculator()

    print("Testing Calculator.add(2, 3)...")
    expect(calc.add(2, 3)).to_equal(5)
    print("  PASS")

    print("\nAll tests passed!")


if __name__ == "__main__":
    try:
        demo()
    except AssertionError as e:
        print(f"  FAIL: {e}")
        sys.exit(1)