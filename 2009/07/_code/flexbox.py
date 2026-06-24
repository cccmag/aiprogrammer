#!/usr/bin/env python3
"""
Flexbox Layout Engine - CSS3 Flexbox Demo
"""

from dataclasses import dataclass, field
from typing import List, Tuple


@dataclass
class FlexItem:
    content: str
    flex_grow: float = 1.0
    flex_basis: float = 0.0


def demo():
    print("\n" + "#" * 60)
    print("# Flexbox Layout Demo")
    print("#" * 60 + "\n")

    items = [
        FlexItem("Header", flex_grow=1, flex_basis=10),
        FlexItem("Content", flex_grow=3, flex_basis=20),
        FlexItem("Sidebar", flex_grow=1, flex_basis=10),
    ]

    total_grow = sum(item.flex_grow for item in items)
    total_basis = sum(item.flex_basis for item in items)
    free_space = 60 - total_basis

    print("Items:", [item.content for item in items])
    print("Total flex-grow:", total_grow)
    print("Total flex-basis:", total_basis)
    print("Free space:", free_space)
    print()

    positions = []
    pos = 0
    for item in items:
        size = item.flex_basis + (item.flex_grow / total_grow) * free_space
        positions.append((item.content, pos, size))
        pos += size

    print("Layout:")
    for name, start, size in positions:
        bar = "█" * int(size)
        print(f"  {name:10}: [{bar}] {size:.1f}")


if __name__ == "__main__":
    demo()