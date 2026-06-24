#!/usr/bin/env python3
"""2009 Technology Year in Review"""


def demo():
    print("\n" + "#" * 60)
    print("# 2009 Technology Year in Review")
    print("#" * 60 + "\n")

    events = [
        ("1月", "Ruby 1.9.1 發布"),
        ("6月", "Firefox 3.5 / Safari 4.0 發布"),
        ("7月", "jQuery 1.4 發布"),
        ("8月", "MongoDB 1.0 發布"),
        ("8月", "Node.js 0.1 發布"),
        ("10月", "GitHub 突破 100 萬用戶"),
        ("11月", "Go 語言發布"),
    ]

    print("2009 年重要事件：")
    print("-" * 40)
    for month, event in events:
        print(f"  {month}: {event}")

    print("\n總結：")
    print("-" * 40)
    print("  - 雲端運算元年")
    print("  - NoSQL 運動興起")
    print("  - 前端技術革命")
    print("  - JavaScript 全端時代來臨")
    print("  - 分散式版本控制成主流")
    print("")


if __name__ == "__main__":
    demo()