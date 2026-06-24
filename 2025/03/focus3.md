# 繼承與多型

## 繼承：程式碼重用的藝術

繼承是 OOP 中最強大的程式碼重用機制。當你有一個通用類別，而你想建立一個更專門的版本時，繼承可以讓你直接複用父類別的程式碼，只需專注於新增或覆寫的部分。

```python
class Animal:
    def __init__(self, name):
        self.name = name

    def eat(self):
        return f"{self.name} 正在進食"

class Dog(Animal):
    def bark(self):
        return f"{self.name} says 汪汪！"

class Cat(Animal):
    def meow(self):
        return f"{self.name} says 喵喵！"

dog = Dog("來福")
cat = Cat("小花")

print(dog.eat())   # 來福 正在進食（繼承自 Animal）
print(dog.bark())  # 來福 says 汪汪！
print(cat.eat())   # 小花 正在進食（繼承自 Animal）
print(cat.meow())  # 小花 says 喵喵！
```

### 方法覆寫

子類別可以覆寫父類別的方法，提供自己的實作：

```python
class Animal:
    def speak(self):
        return "...（無聲）"

class Dog(Animal):
    def speak(self):
        return "汪汪！"

class Cat(Animal):
    def speak(self):
        return "喵喵！"

animals = [Dog(), Cat(), Animal()]
for a in animals:
    print(a.speak())
# 汪汪！
# 喵喵！
# ...（無聲）
```

### super() 與父類別呼叫

使用 `super()` 可以呼叫父類別的版本：

```python
class Vehicle:
    def __init__(self, brand, model):
        self.brand = brand
        self.model = model
        print(f"Vehicle: {brand} {model}")

class Car(Vehicle):
    def __init__(self, brand, model, doors):
        super().__init__(brand, model)  # 呼叫父類別建構子
        self.doors = doors
        print(f"Car: {doors} doors")

c = Car("Toyota", "Corolla", 4)
# Vehicle: Toyota Corolla
# Car: 4 doors
```

## 多型：同一介面不同行為

多型允許不同類別的物件對同一訊息做出不同回應。在 Python 中，多型是自然支援的——你不需要宣告介面，只要物件有對應的方法即可。

```python
class Dog:
    def speak(self):
        return "汪汪！"

class Cat:
    def speak(self):
        return "喵喵！"

class Duck:
    def speak(self):
        return "呱呱！"

# 多型的使用
def animal_sound(animal):
    return animal.speak()

print(animal_sound(Dog()))   # 汪汪！
print(animal_sound(Cat()))   # 喵喵！
print(animal_sound(Duck()))  # 呱呱！
```

## Python 的 MRO 機制

當涉及多重繼承時，Python 使用 C3 線性化演算法來決定方法解析順序（MRO, Method Resolution Order）：

```python
class A:
    def method(self):
        return "A"

class B(A):
    def method(self):
        return "B"

class C(A):
    def method(self):
        return "C"

class D(B, C):
    pass

d = D()
print(d.method())  # B
print(D.__mro__)   # D -> B -> C -> A -> object
```

MRO 的規則是：子類別優先於父類別，先宣告的父類別優先於後宣告的父類別。

### 實際應用

```python
class Logger:
    def log(self, msg):
        print(f"[LOG] {msg}")

class TimestampMixin:
    def get_timestamp(self):
        from datetime import datetime
        return datetime.now().isoformat()

class SaveMixin:
    def save(self, data):
        print(f"儲存: {data}")

class UserService(Logger, TimestampMixin, SaveMixin):
    def create_user(self, name):
        ts = self.get_timestamp()
        self.log(f"建立使用者 {name} 於 {ts}")
        self.save({"name": name, "created_at": ts})

service = UserService()
service.create_user("Alice")
# [LOG] 建立使用者 Alice 於 2025-03-01T10:00:00
# 儲存: {'name': 'Alice', 'created_at': '2025-03-01T10:00:00'}
```

## 小結

繼承與多型是 OOP 的核心機制。繼承促進程式碼重用，多型提供靈活性。理解 MRO 對於正確使用 Python 的繼承至關重要。

## 延伸閱讀

- [Python 繼承官方教學](https://www.google.com/search?q=Python+inheritance+tutorial)
- [C3 線性化演算法](https://www.google.com/search?q=C3+linearization+algorithm)
