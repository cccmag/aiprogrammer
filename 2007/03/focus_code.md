# 動態語言程式設計實作

## 前言

動態語言如 Python 和 Ruby 在 2007 年經歷了復興。本文透過對比展示動態語言的特性。

---

## Python 與 Ruby 對比

### 基本語法

```python
#!/usr/bin/env python3
"""動態語言對比：Python vs Ruby"""

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def greet(self):
        return f"Hello, I'm {self.name}"

class RubyPerson:
    def initialize(name, age)
        @name = name
        @age = age
    end

    def greet
        "Hello, I'm #{@name}"
    end

def demo():
    print("=== Python 動態語言範例 ===")
    print()

    # 動態型別
    x = 42
    print(f"x = {x} (type: {type(x).__name__})")
    x = "hello"
    print(f"x = {x} (type: {type(x).__name__})")
    print()

    # 鴨子型別
    class Dog:
        def speak(self): return "Woof!"

    class Cat:
        def speak(self): return "Meow!"

    def make_speak(obj):
        return obj.speak()

    dog, cat = Dog(), Cat()
    print(f"Dog says: {make_speak(dog)}")
    print(f"Cat says: {make_speak(cat)}")
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

    # 物件導向
    person = Person("John", 30)
    print(f"Person: {person.greet()}")

if __name__ == "__main__": demo()
```

---

## 執行結果

```
=== Python 動態語言範例 ===

x = 42 (type: int)
x = hello (type: str)

Dog says: Woof!
Cat says: Meow!

Squares: [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

add5(10) = 15

Person: Hello, I'm John
```

---

## 動態語言特性

### 鸭子型別

```python
# "如果它走起來像鸭子，叫起來像鸭子，那它就是一只鸭子"
# 不需要明確的介面定義
class Duck:
    def quack(self): return "Quack!"

class Person:
    def quack(self): return "I'm not a duck!"

def make_quack(obj):
    return obj.quack()

make_quack(Duck())   # OK
make_quack(Person()) # 也 OK！
```

### eval 與動態程式碼

```python
# 動態執行
code = "print('Hello from eval!')"
eval(code)

# 動態函式創建
def create_function(op, x, y):
    return eval(f"{x} {op} {y}")

print(create_function("+", 3, 4))  # 7
```

---

## 結論

動態語言的靈活性、簡潔性和生產力使其在 2007 年獲得了前所未有的關注。

---

*本篇文章為「AI 程式人雜誌 2007 年 3 月號」本期焦點系列補充文章。*