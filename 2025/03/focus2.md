# 類別與物件

## 類別是藍圖，物件是實體

在 OOP 中，「類別」（Class）和「物件」（Object）是最基本的兩個概念。類別就像建築藍圖，定義了結構與行為；物件則是根據藍圖實際建造出來的房屋，佔據記憶體空間，擁有自己的狀態。

```python
class Dog:       # 類別定義（藍圖）
    def __init__(self, name):
        self.name = name

    def bark(self):
        return f"{self.name} says 汪汪！"

my_dog = Dog("來福")  # 物件建立（實際房屋）
print(my_dog.bark())   # 來福 says 汪汪！
```

一個類別可以產生多個物件，每個物件擁有自己獨立的狀態：

```python
dog1 = Dog("來福")
dog2 = Dog("小白")
print(dog1.bark())  # 來福 says 汪汪！
print(dog2.bark())  # 小白 says 汪汪！
```

## 建構子與初始化

Python 使用 `__init__` 方法作為建構子，在物件被建立時自動呼叫：

```python
class Student:
    def __init__(self, name, grade, scores=None):
        self.name = name
        self.grade = grade
        self.scores = scores if scores is not None else []

    def average(self):
        if not self.scores:
            return 0
        return sum(self.scores) / len(self.scores)

s = Student("小明", 5, [85, 92, 78])
print(f"{s.name} 的平均分數：{s.average()}")
```

注意 `__init__` 的第一個參數永遠是 `self`，它代表正在被建立的物件實體。

## 實體變數與類別變數

Python 的類別可以有兩種變數：

**實體變數**（Instance Variables）：每個物件獨自擁有，在 `__init__` 中定義。

**類別變數**（Class Variables）：所有物件共享，在類別主體中直接定義。

```python
class Employee:
    company = "AI 程式人公司"  # 類別變數（共享）

    def __init__(self, name, salary):
        self.name = name        # 實體變數（獨有）
        self.salary = salary

    def info(self):
        return f"{self.name} 在 {Employee.company} 工作，薪資 {self.salary}"

e1 = Employee("Alice", 50000)
e2 = Employee("Bob", 60000)

print(e1.info())  # Alice 在 AI 程式人公司工作，薪資 50000
print(e2.info())  # Bob 在 AI 程式人公司工作，薪資 60000

# 修改類別變數會影響所有物件
Employee.company = "新公司"
print(e1.info())  # Alice 在新公司工作
```

## 物件的生命週期

物件的生命週期包含三個階段：

1. **建立**：呼叫 `ClassName()`，Python 分配記憶體並呼叫 `__init__`
2. **使用**：透過物件存取屬性和方法
3. **銷毀**：當物件不再被參考時，Python 的垃圾回收器會自動回收記憶體

```python
class Resource:
    def __init__(self):
        print("資源已分配")

    def __del__(self):
        print("資源已釋放")

r = Resource()   # 資源已分配
r = None         # 資源已釋放（沒有參考了）
```

## 小結

類別與物件是 OOP 的基石。類別提供結構定義，物件提供實際的狀態與行為。理解 `__init__`、`self`、以及實體變數與類別變數的區別，是掌握 Python OOP 的第一步。

## 延伸閱讀

- [Python 類別官方教學](https://www.google.com/search?q=Python+classes+tutorial)
- [Python __init__ 方法](https://www.google.com/search?q=Python+__init__+method)
