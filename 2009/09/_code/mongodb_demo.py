#!/usr/bin/env python3
"""MiniDB - Simplified Document Database Demo"""

import json


def demo():
    print("\n" + "#" * 60)
    print("# MiniDB - Document Database Demo")
    print("#" * 60 + "\n")

    # 簡化的文件資料庫模擬
    documents = [
        {"_id": "1", "name": "張三", "age": 30, "city": "台北"},
        {"_id": "2", "name": "李四", "age": 25, "city": "台中"},
        {"_id": "3", "name": "王五", "age": 35, "city": "台北"},
    ]

    print("All users:")
    for doc in documents:
        print(f"  {doc['_id']}: {doc}")

    print("\nUsers in 台北:")
    for doc in documents:
        if doc.get("city") == "台北":
            print(f"  {doc['name']}")

    print("\nUsers over 30:")
    for doc in documents:
        if doc.get("age", 0) > 30:
            print(f"  {doc['name']}, age {doc['age']}")

    print("\nCount:", len(documents))


if __name__ == "__main__":
    demo()