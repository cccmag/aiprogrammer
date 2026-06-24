#!/usr/bin/env python3
"""Python 程式設計基礎 — 示範程式"""

import json
import os


def demo_variables():
    """示範變數與資料型別"""
    print("=== 變數與資料型別 ===")

    name = "Alice"
    age = 25
    height = 165.5
    is_student = True
    hobbies = ["閱讀", "旅行", "程式設計"]
    scores = {"math": 85, "english": 92, "science": 78}

    print(f"姓名：{name}")
    print(f"年齡：{age}")
    print(f"身高：{height} cm")
    print(f"是否為學生：{is_student}")
    print(f"興趣：{', '.join(hobbies)}")
    print(f"成績：{scores}")


def demo_functions():
    """示範函數定義與使用"""
    print("\n=== 函數定義與使用 ===")

    def add(a, b):
        return a + b

    def multiply(a, b=2):
        return a * b

    def process_numbers(*args):
        total = sum(args)
        average = total / len(args) if args else 0
        return {"total": total, "average": average, "count": len(args)}

    print(f"add(10, 5) = {add(10, 5)}")
    print(f"multiply(7) = {multiply(7)}")
    print(f"multiply(7, 3) = {multiply(7, 3)}")
    print(f"process_numbers(1, 2, 3, 4, 5) = {process_numbers(1, 2, 3, 4, 5)}")


def demo_lists_and_dicts():
    """示範列表與字典操作"""
    print("\n=== 列表與字典操作 ===")

    fruits = ["蘋果", "香蕉", "橘子"]
    fruits.append("葡萄")
    fruits.insert(1, "草莓")

    for i, fruit in enumerate(fruits):
        print(f"{i + 1}. {fruit}")

    squares = [x ** 2 for x in range(1, 6)]
    print(f"平方數列：{squares}")

    student = {
        "name": "Bob",
        "age": 30,
        "skills": ["Python", "JavaScript", "Rust"]
    }

    for key, value in student.items():
        if isinstance(value, list):
            print(f"{key}: {', '.join(value)}")
        else:
            print(f"{key}: {value}")

    a = {1, 2, 3, 4}
    b = {3, 4, 5, 6}
    print(f"集合聯集：{a | b}")
    print(f"集合交集：{a & b}")


def demo_file_io():
    """示範檔案讀寫操作"""
    print("\n=== 檔案讀寫操作 ===")

    data = [
        {"name": "Alice", "score": 85},
        {"name": "Bob", "score": 92},
        {"name": "Charlie", "score": 78}
    ]

    filename = "_output.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"已寫入 {filename}")

    with open(filename, "r", encoding="utf-8") as f:
        loaded = json.load(f)
    print(f"從檔案讀取：{loaded}")
    os.remove(filename)


def demo():
    """執行所有示範"""
    print("Python 程式設計基礎示範\n")
    demo_variables()
    demo_functions()
    demo_lists_and_dicts()
    demo_file_io()
    print("\n所有示範完成！")


if __name__ == "__main__":
    demo()
