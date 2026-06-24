#!/usr/bin/env python3
"""
Python 基礎語法範例
展示變數、運算子、控制流程、資料結構
"""

def demo():
    print("=== Python 基礎語法展示 ===")

    name = "張小明"
    age = 28
    height = 175.5
    is_student = True

    print(f"姓名：{name}，年齡：{age}，身高：{height}")

    fruits = ["蘋果", "香蕉", "橘子"]
    person = {
        "name": "張小明",
        "age": 28,
        "city": "台北"
    }

    print(f"水果列表：{fruits}")
    print(f"人物字典：{person}")

    if age >= 18:
        print("已成年")
    else:
        print("未成年")

    for fruit in fruits:
        print(f"水果：{fruit}")

    squares = [x ** 2 for x in range(10)]
    print(f"平方數：{squares}")

    def greet(name):
        return f"你好，{name}！"

    print(greet("Python"))

    print("=== 基礎語法展示完成 ===")

if __name__ == "__main__":
    demo()