# 附加：Python 實作範例

## 程式實作總覽

本期我們提供三個 Python 實作範例，展示 Python 基礎語法、OOP 和檔案操作的實際應用。

## 基礎語法範例

```python
#!/usr/bin/env python3
"""
Python 基礎語法範例
展示變數、運算子、控制流程、資料結構
"""

def demo():
    print("=== Python 基礎語法展示 ===")

    # 變數與資料型態
    name = "張小明"
    age = 28
    height = 175.5
    is_student = True

    print(f"姓名：{name}，年齡：{age}，身高：{height}")

    # 資料結構
    fruits = ["蘋果", "香蕉", "橘子"]
    person = {
        "name": "張小明",
        "age": 28,
        "city": "台北"
    }

    print(f"水果列表：{fruits}")
    print(f"人物字典：{person}")

    # 條件判斷
    if age >= 18:
        print("已成年")
    else:
        print("未成年")

    # 迴圈
    for fruit in fruits:
        print(f"水果：{fruit}")

    # 列表推導
    squares = [x ** 2 for x in range(10)]
    print(f"平方數：{squares}")

    # 函式
    def greet(name):
        return f"你好，{name}！"

    print(greet("Python"))

    print("=== 基礎語法展示完成 ===")

if __name__ == "__main__":
    demo()
```

## OOP 範例

```python
#!/usr/bin/env python3
"""
Python 物件導向程式設計範例
展示類別、繼承、封裝
"""

class Animal:
    """動物類別"""

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def speak(self):
        return "..."

    def info(self):
        return f"{self.name}，{self.age}歲"

class Dog(Animal):
    """狗類別"""

    def speak(self):
        return f"{self.name} 說：汪汪！"

    def fetch(self):
        return f"{self.name} 去撿球"

class Cat(Animal):
    """貓類別"""

    def speak(self):
        return f"{self.name} 說：喵喵！"

    def climb(self):
        return f"{self.name} 在爬樹"

class Person:
    """人類別"""

    def __init__(self, name):
        self._name = name
        self._pets = []

    @property
    def name(self):
        return self._name

    def adopt_pet(self, pet):
        self._pets.append(pet)
        return f"{self._name} 領養了 {pet.name}"

    def list_pets(self):
        return [pet.name for pet in self._pets]

def demo():
    print("=== Python OOP 展示 ===")

    # 創建物件
    animals = [
        Dog("小黑", 3),
        Cat("小咪", 2),
        Dog("大黃", 5)
    ]

    for animal in animals:
        print(f"{animal.info()} -> {animal.speak()}")

    # 物件互動
    person = Person("張小明")

    for animal in animals[:2]:
        print(person.adopt_pet(animal))

    print(f"張小明的寵物：{person.list_pets()}")

    print("=== OOP 展示完成 ===")

if __name__ == "__main__":
    demo()
```

## 檔案操作範例

```python
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

    # 文字檔案操作
    print("\n--- 文字檔案 ---")
    with open("demo.txt", "w", encoding="utf-8") as f:
        f.write("第一行文字\n")
        f.write("第二行文字\n")
        f.write(f"時間戳記：{datetime.now()}\n")

    with open("demo.txt", "r", encoding="utf-8") as f:
        print(f.read())

    # JSON 檔案操作
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

    # CSV 檔案操作
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

    # 清理測試檔案
    for filename in ["demo.txt", "demo.json", "demo.csv"]:
        if os.path.exists(filename):
            os.remove(filename)

    print("\n=== 檔案操作展示完成 ===")

if __name__ == "__main__":
    demo()
```

## 執行方式

```bash
python3 basics.py
python3 oop.py
python3 file_io.py
```

或使用 test.sh 自動執行所有範例。