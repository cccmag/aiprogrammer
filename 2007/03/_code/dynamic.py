#!/usr/bin/env python3
"""動態語言程式設計實作：Python"""

def demo():
    print("=== Python 動態語言範例 ===")
    print()

    # 動態型別
    x = 42
    print(f"x = {x} (type: {type(x).__name__})")
    x = "hello"
    print(f"x = {x} (type: {type(x).__name__})")
    print()

    # 鸭子类
    class Dog:
        def speak(self): return "Woof!"
    class Cat:
        def speak(self): return "Meow!"

    def make_speak(obj):
        return obj.speak()

    print(f"Dog says: {make_speak(Dog())}")
    print(f"Cat says: {make_speak(Cat())}")
    print()

    # 列表推導
    squares = [i**2 for i in range(10)]
    print(f"Squares: {squares}")
    print()

    # 閉包
    def make_adder(n):
        return lambda x: x + n

    add5 = make_adder(5)
    print(f"add5(10) = {add5(10)}")
    print()

    print("=== 完成 ===")

if __name__ == "__main__": demo()