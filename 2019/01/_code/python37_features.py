import asyncio
import sys
from dataclasses import dataclass, field
from typing import List, Optional


def demo():
    print("=" * 60)
    print("Python 3.7 特性展示")
    print("=" * 60)

    print("\n[1] Data Class 展示")
    demonstrate_dataclass()

    print("\n[2] Async/Await 展示")
    demonstrate_asyncio()

    print("\n[3] Type Hints 展示")
    demonstrate_type_hints()

    print("\n[4] Dict 效能展示")
    demonstrate_dict_performance()

    print("\n" + "=" * 60)
    print("展示完成")
    print("=" * 60)


@dataclass
class Point:
    x: float
    y: float
    label: str = ""


def demonstrate_dataclass():
    p1 = Point(1.0, 2.0)
    p2 = Point(1.0, 2.0)
    print(f"Point 建立：{p1}")
    print(f"Point 比較：{p1 == p2}")
    print(f"Point 屬性：x={p1.x}, y={p1.y}, label='{p1.label}'")


@dataclass
class Student:
    name: str
    age: int
    courses: List[str] = field(default_factory=list)


def demonstrate_type_hints():
    student = Student("Bob", 20, ["Math", "Physics"])
    print(f"學生：{student}")
    print(f"  姓名：{student.name}")
    print(f"  年齡：{student.age}")
    print(f"  課程：{student.courses}")


async def async_task1():
    await asyncio.sleep(0.1)
    return "Task 1 完成"


async def async_task2():
    await asyncio.sleep(0.05)
    return "Task 2 完成"


def demonstrate_asyncio():
    async def run_tasks():
        t1 = asyncio.create_task(async_task1())
        t2 = asyncio.create_task(async_task2())
        results = await asyncio.gather(t1, t2)
        return results

    print("開始非同步任務...")
    results = asyncio.run(run_tasks())
    for r in results:
        print(f"  {r}")
    print(f"並行結果：{results}")


def demonstrate_dict_performance():
    test_dict = {f"key_{i}": i for i in range(10000)}
    print(f"Dict 大小：{len(test_dict)}")
    print(f"Dict 前三：{list(test_dict.items())[:3]}")

    keys = list(test_dict.keys())
    print(f"插入順序保證：{keys[0] == 'key_0'}")


if __name__ == "__main__":
    demo()