#!/usr/bin/env python3
"""
Python 物件導向程式設計範例
展示類別、繼承、封裝
"""

class Animal:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def speak(self):
        return "..."

    def info(self):
        return f"{self.name}，{self.age}歲"

class Dog(Animal):
    def speak(self):
        return f"{self.name} 說：汪汪！"

    def fetch(self):
        return f"{self.name} 去撿球"

class Cat(Animal):
    def speak(self):
        return f"{self.name} 說：喵喵！"

    def climb(self):
        return f"{self.name} 在爬樹"

class Person:
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

    animals = [
        Dog("小黑", 3),
        Cat("小咪", 2),
        Dog("大黃", 5)
    ]

    for animal in animals:
        print(f"{animal.info()} -> {animal.speak()}")

    person = Person("張小明")

    for animal in animals[:2]:
        print(person.adopt_pet(animal))

    print(f"張小明的寵物：{person.list_pets()}")

    print("=== OOP 展示完成 ===")

if __name__ == "__main__":
    demo()