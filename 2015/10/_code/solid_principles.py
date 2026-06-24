#!/usr/bin/env python3
"""SOLID 原則範例程式"""

from abc import ABC, abstractmethod


class Database(ABC):
    @abstractmethod
    def query(self, sql):
        pass

    @abstractmethod
    def connect(self):
        pass


class MySQLDatabase(Database):
    def query(self, sql):
        print(f"MySQL executing: {sql}")
        return [{"id": 1, "name": "John"}]

    def connect(self):
        print("Connected to MySQL")


class PostgreSQLDatabase(Database):
    def query(self, sql):
        print(f"PostgreSQL executing: {sql}")
        return [{"id": 1, "name": "John"}]

    def connect(self):
        print("Connected to PostgreSQL")


class UserRepository:
    def __init__(self, database: Database):
        self.database = database

    def find_all(self):
        self.database.connect()
        return self.database.query("SELECT * FROM users")

    def find_by_id(self, user_id):
        self.database.connect()
        return self.database.query(f"SELECT * FROM users WHERE id = {user_id}")


class Shape(ABC):
    @abstractmethod
    def area(self):
        pass


class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return 3.14159 * self.radius ** 2


class Square(Shape):
    def __init__(self, side):
        self.side = side

    def area(self):
        return self.side ** 2


class Triangle(Shape):
    def __init__(self, base, height):
        self.base = base
        self.height = height

    def area(self):
        return 0.5 * self.base * self.height


def total_area(shapes):
    return sum(shape.area() for shape in shapes)


class Subject:
    def __init__(self):
        self._observers = []
        self._state = None

    def attach(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer):
        self._observers.remove(observer)

    def notify(self):
        for observer in self._observers:
            observer.update(self._state)

    def set_state(self, state):
        self._state = state
        self.notify()


class Observer:
    def update(self, state):
        pass


class LoggingObserver(Observer):
    def update(self, state):
        print(f"LoggingObserver: State changed to {state}")


class AnalyticsObserver(Observer):
    def update(self, state):
        print(f"AnalyticsObserver: Tracking state {state}")


def demo():
    print("=" * 60)
    print("SOLID Principles Demo")
    print("=" * 60)

    print("\n--- DIP: Dependency Inversion Principle ---")
    mysql_db = MySQLDatabase()
    repo = UserRepository(mysql_db)
    users = repo.find_all()
    print(f"Found {len(users)} users")

    print("\n--- OCP: Open/Closed Principle ---")
    shapes = [Circle(5), Square(4), Triangle(3, 6)]
    print(f"Total area: {total_area(shapes)}")

    print("\n--- Observer Pattern ---")
    subject = Subject()
    subject.attach(LoggingObserver())
    subject.attach(AnalyticsObserver())
    subject.set_state("User logged in")
    subject.set_state("Data updated")

    print("\n" + "=" * 60)
    print("All demos completed!")
    print("=" * 60)


if __name__ == "__main__":
    demo()