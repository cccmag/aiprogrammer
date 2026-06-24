#!/usr/bin/env python3
"""
Python 檔案操作範例
展示文字檔、JSON、CSV 的讀寫
"""

import json
import csv
import os
from datetime import datetime

def demo():
    print("=== Python 檔案操作展示 ===")

    print("\n--- 文字檔案 ---")
    with open("demo.txt", "w", encoding="utf-8") as f:
        f.write("第一行文字\n")
        f.write("第二行文字\n")
        f.write(f"時間戳記：{datetime.now()}\n")

    with open("demo.txt", "r", encoding="utf-8") as f:
        print(f.read())

    print("\n--- JSON 檔案 ---")
    data = {
        "name": "張小明",
        "age": 28,
        "skills": ["Python", "JavaScript"],
        "active": True
    }

    with open("demo.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    with open("demo.json", "r", encoding="utf-8") as f:
        loaded = json.load(f)
        print(f"讀取的資料：{loaded}")

    print("\n--- CSV 檔案 ---")
    users = [
        ["ID", "Name", "Age"],
        [1, "張小明", 28],
        [2, "李小華", 35],
        [3, "王小美", 24]
    ]

    with open("demo.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(users)

    with open("demo.csv", "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            print(f"ID: {row['ID']}, Name: {row['Name']}, Age: {row['Age']}")

    for filename in ["demo.txt", "demo.json", "demo.csv"]:
        if os.path.exists(filename):
            os.remove(filename)

    print("\n=== 檔案操作展示完成 ===")

if __name__ == "__main__":
    demo()