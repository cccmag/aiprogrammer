# 從程序式到物件導向

## 兩種典範的根本差異

程式設計典範的轉換不僅是語法層面的改變，更是一種思維方式的革命。程序式程式設計關注「做什麼」——一系列步驟序列；物件導向程式設計關注「誰來做」——物件之間的合作與分工。

### 程序式風格

```python
# 程序式：管理學生與成績
students = []
grades = []

def add_student(name):
    students.append(name)
    grades.append([])

def add_grade(student_id, grade):
    grades[student_id].append(grade)

def get_average(student_id):
    g = grades[student_id]
    return sum(g) / len(g) if g else 0

add_student("小明")
add_student("小華")
add_grade(0, 85)
add_grade(0, 92)
add_grade(1, 78)
print(f"小明平均: {get_average(0)}")
```

這種方式有什麼問題？所有資料都存在全域變數中，函式和資料是分離的。當系統變大時，很難追蹤哪個函式修改了哪個資料。

### 物件導向風格

```python
class Student:
    def __init__(self, name):
        self.name = name
        self._grades = []

    def add_grade(self, grade):
        self._grades.append(grade)

    def average(self):
        return sum(self._grades) / len(self._grades) if self._grades else 0

class GradeBook:
    def __init__(self):
        self._students = []

    def add_student(self, name):
        s = Student(name)
        self._students.append(s)
        return s

    def top_student(self):
        return max(self._students, key=lambda s: s.average())

book = GradeBook()
s1 = book.add_student("小明")
s2 = book.add_student("小華")
s1.add_grade(85)
s1.add_grade(92)
s2.add_grade(78)
print(f"小明平均: {s1.average()}")
print(f"第一名: {book.top_student().name}")
```

## 轉換的核心思考

從程序式轉換到 OOP，需要掌握三個關鍵思維轉變：

### 1. 識別物件

問自己：「這個系統中有哪些名詞？」每個名詞可能就是一個類別：

- 「學生管理系統」→ Student、Course、Enrollment
- 「電子商務平台」→ Product、Cart、Order、Customer
- 「遊戲引擎」→ Player、Enemy、Weapon、Level

### 2. 分配職責

每個物件應該有自己的職責。Student 負責自己的成績，GradeBook 負責總體統計。這就是「單一職責原則」。

### 3. 建立協作

物件之間透過方法呼叫協作，而不是直接操作對方的內部資料。

```python
class Order:
    def __init__(self, customer):
        self.customer = customer
        self._items = []
        self._total = 0

    def add_item(self, product, quantity):
        self._items.append((product, quantity))
        self._total += product.price * quantity

    def checkout(self, payment):
        if payment.process(self._total):
            self._items = []
            self._total = 0
            return True
        return False
```

## 轉換的好處

1. **資料安全**：物件控制自己的狀態，外部無法隨意修改
2. **易於測試**：每個類別可以獨立測試
3. **易於擴展**：新增功能通常只需要新增類別，不需要修改既有程式碼
4. **更貼近真實世界**：物件模型更符合人類的認知方式

## 小結

從程序式到物件導向的轉換，本質上是從「以函式為中心」轉變為「以資料為中心」。這個轉變在專案規模較小時可能感覺不到好處，但當程式碼量達到數萬行時，OOP 的威力就會真正展現出來。

## 延伸閱讀

- [程序式 vs 物件導向](https://www.google.com/search?q=procedural+vs+object+oriented+programming)
- [Python OOP 入門](https://www.google.com/search?q=Python+OOP+tutorial+beginner)
