# Python 基礎實作程式碼

## 前言

本篇文章展示 `python_basics.py` 的完整程式碼，這是一個包含了本期所有基礎概念的 Python 程式。從變數宣告到檔案操作，展示了 Python 程式設計的核心語法。

---

## 原始碼

完整的 Python 實作請參考：[_code/python_basics.py](_code/python_basics.py)

```python
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
```

---

## 執行結果

```
Python 程式設計基礎示範

=== 變數與資料型別 ===
姓名：Alice
年齡：25
身高：165.5 cm
是否為學生：True
興趣：閱讀, 旅行, 程式設計
成績：{'math': 85, 'english': 92, 'science': 78}

=== 函數定義與使用 ===
add(10, 5) = 15
multiply(7) = 14
multiply(7, 3) = 21
process_numbers(1, 2, 3, 4, 5) = {'total': 15, 'average': 3.0, 'count': 5}

=== 列表與字典操作 ===
1. 蘋果
2. 草莓
3. 香蕉
4. 橘子
5. 葡萄
平方數列：[1, 4, 9, 16, 25]
name: Bob
age: 30
skills: Python, JavaScript, Rust
集合聯集：{1, 2, 3, 4, 5, 6}
集合交集：{3, 4}

=== 檔案讀寫操作 ===
已寫入 _output.json
從檔案讀取：[{'name': 'Alice', 'score': 85}, {'name': 'Bob', 'score': 92}, {'name': 'Charlie', 'score': 78}]

所有示範完成！
```

---

## 程式說明

### 1. demo_variables()

示範 Python 的各種資料型別：

| 型別 | 範例 | 說明 |
|------|------|------|
| `str` | `"Alice"` | 字串 |
| `int` | `25` | 整數 |
| `float` | `165.5` | 浮點數 |
| `bool` | `True` | 布林值 |
| `list` | `["閱讀", "旅行"]` | 列表 |
| `dict` | `{"math": 85}` | 字典 |

### 2. demo_functions()

示範函數的各種參數傳遞方式：

- **位置參數**：`add(a, b)` — 依位置對應
- **預設參數**：`multiply(a, b=2)` — 可省略的參數
- **可變長度參數**：`process_numbers(*args)` — 任意數量參數

### 3. demo_lists_and_dicts()

示範資料結構的常見操作：

- 列表的新增、插入、遍歷
- 列表推導式建立新列表
- 字典的鍵值對存取與遍歷
- 集合的聯集與交集運算

### 4. demo_file_io()

示範檔案操作的正確做法：

- 使用 `with` 語句確保檔案正確關閉
- JSON 序列化與反序列化
- 指定 UTF-8 編碼支援中文

---

## 延伸閱讀

- [Python 變數與型別](https://www.google.com/search?q=Python+variables+and+data+types)
- [Python 函數定義](https://www.google.com/search?q=Python+function+definition)
- [Python 檔案操作](https://www.google.com/search?q=Python+file+handling+tutorial)

---

*本篇文章為「AI 程式人雜誌 2025 年 1 月號」Python 基礎系列補充文章。*
