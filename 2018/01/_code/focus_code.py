#!/usr/bin/env python3
"""Python 3.6 特性演示"""

def demo():
    print("=" * 50)
    print("Python 3.6 特性演示")
    print("=" * 50)

    # 1. f-string
    print("\n1. f-string:")
    name = "Python"
    print(f"  Hello, {name}!")

    # 2. 數字底線
    print("\n2. 數字底線:")
    million = 1_000_000
    print(f"  Million: {million:,}")

    # 3. 型別提示
    print("\n3. 型別提示:")
    def add(a: int, b: int) -> int:
        return a + b
    print(f"  add(3, 4) = {add(3, 4)}")

    # 4. 變數型別提示
    print("\n4. 變數型別提示:")
    name: str = "Alice"
    age: int = 30
    print(f"  Name: {name}, Age: {age}")

    # 5. f-string 格式化
    print("\n5. f-string 格式化:")
    pi = 3.14159
    print(f"  Pi: {pi:.2f}")

    # 6. dict 保持插入順序
    print("\n6. Dict 順序:")
    d = {"a": 1, "b": 2, "c": 3}
    print(f"  Dict: {d}")

    # 7. async/await
    print("\n7. Async/Await:")
    import asyncio
    async def async_demo():
        await asyncio.sleep(0.01)
        return "async done"
    result = asyncio.run(async_demo())
    print(f"  {result}")

    print("\n" + "=" * 50)
    print("演示完成!")
    print("=" * 50)

if __name__ == "__main__":
    demo()