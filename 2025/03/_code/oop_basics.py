#!/usr/bin/env python3
"""OOP Basics - 物件導向程式設計基礎實作"""

from abc import ABC, abstractmethod


class Animal(ABC):
    def __init__(self, name: str):
        self._name = name

    @abstractmethod
    def speak(self) -> str:
        pass

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = value


class Dog(Animal):
    def __init__(self, name: str, breed: str):
        super().__init__(name)
        self._breed = breed

    def speak(self) -> str:
        return f"{self.name} says 汪汪!"

    @property
    def breed(self) -> str:
        return self._breed


class Cat(Animal):
    def __init__(self, name: str, color: str):
        super().__init__(name)
        self._color = color

    def speak(self) -> str:
        return f"{self.name} says 喵喵!"

    @property
    def color(self) -> str:
        return self._color


class Vector:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __add__(self, other: 'Vector') -> 'Vector':
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other: 'Vector') -> 'Vector':
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: float) -> 'Vector':
        return Vector(self.x * scalar, self.y * scalar)

    def __repr__(self) -> str:
        return f"Vector({self.x}, {self.y})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vector):
            return NotImplemented
        return self.x == other.x and self.y == other.y


class AnimalFactory:
    @staticmethod
    def create_animal(animal_type: str, name: str, **kwargs) -> Animal:
        if animal_type == "dog":
            return Dog(name, kwargs.get("breed", "米克斯"))
        elif animal_type == "cat":
            return Cat(name, kwargs.get("color", "橘色"))
        else:
            raise ValueError(f"Unknown animal type: {animal_type}")


class Duck:
    def __init__(self, name: str):
        self.name = name

    def speak(self) -> str:
        return f"{self.name} says 呱呱!"


def make_it_speak(entity) -> str:
    return entity.speak()


def demo():
    print("=" * 50)
    print("OOP 基礎實作展示")
    print("=" * 50)

    print("\n[1] 類別與繼承")
    dog = Dog("來福", "黃金獵犬")
    cat = Cat("小花", "虎斑")
    print(dog.speak())
    print(cat.speak())

    print("\n[2] 屬性封裝")
    print(f"狗的名稱: {dog.name}, 品種: {dog.breed}")
    dog.name = "阿福"
    print(f"改名後: {dog.name}")

    print("\n[3] 多型與鴨子型別")
    animals = [dog, cat, Duck("唐老鴨")]
    for a in animals:
        print(make_it_speak(a))

    print("\n[4] 運算子重載")
    v1 = Vector(2, 3)
    v2 = Vector(4, 5)
    print(f"v1 = {v1}")
    print(f"v2 = {v2}")
    print(f"v1 + v2 = {v1 + v2}")
    print(f"v1 - v2 = {v1 - v2}")
    print(f"v1 * 3 = {v1 * 3}")
    print(f"v1 == Vector(2, 3): {v1 == Vector(2, 3)}")

    print("\n[5] 工廠模式")
    new_dog = AnimalFactory.create_animal("dog", "小白", breed="柴犬")
    new_cat = AnimalFactory.create_animal("cat", "咪咪", color="黑白")
    print(new_dog.speak())
    print(new_cat.speak())

    print("\n[6] 抽象基底類別")
    try:
        a = Animal("抽象")
    except TypeError as e:
        print(f"無法實例化抽象類別: {e}")

    print("\n" + "=" * 50)
    print("展示結束")
    print("=" * 50)


if __name__ == "__main__":
    demo()
