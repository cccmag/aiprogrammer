# 程式碼範例

## f-string 範例

```python
#!/usr/bin/env python3
"""f-string 格式化範例"""

def demo():
    name = "Python"
    version = 3.6
    pi = 3.14159

    # 基本 f-string
    print(f"Welcome to {name} {version}!")

    # 數值格式化
    print(f"Pi: {pi:.2f}")
    print(f"Pi: {pi:10.2f}")

    # 大數字
    million = 1_000_000
    print(f"Million: {million:,}")

    # 對齊
    text = "center"
    print(f"[{text:^20}]")
    print(f"[{text:<20}]")
    print(f"[{text:>20}]")
    print(f"[{text:*>20}]")

    # 格式化表達式
    a, b = 10, 3
    print(f"{a} / {b} = {a / b:.2f}")

    # 日期時間格式化
    from datetime import datetime
    now = datetime.now()
    print(f"Date: {now:%Y-%m-%d}")
    print(f"Time: {now:%H:%M:%S}")

    # 除錯專用 (Python 3.8+)
    # print(f"{x=}")
```

## 型別提示範例

```python
#!/usr/bin/env python3
"""型別提示範例"""

from typing import List, Dict, Optional, Callable

def demo():
    # 變數型別提示
    name: str = "Alice"
    age: int = 30
    scores: List[int] = [90, 85, 88]
    info: Dict[str, str] = {"name": "Bob"}

    print(f"Name: {name}, Age: {age}")
    print(f"Scores: {scores}")
    print(f"Info: {info}")

    # 函式型別提示
    def greet(name: str) -> str:
        return f"Hello, {name}"

    def add(a: int, b: int) -> int:
        return a + b

    def find_user(user_id: int) -> Optional[str]:
        if user_id > 0:
            return "found"
        return None

    print(greet(name))
    print(f"Add: {add(3, 4)}")
    print(f"Find: {find_user(1)}")
    print(f"Find: {find_user(0)}")

    # Callable
    def apply(func: Callable[[int, int], int], a: int, b: int) -> int:
        return func(a, b)

    result = apply(lambda x, y: x + y, 3, 4)
    print(f"Apply result: {result}")
```

## async/await 範例

```python
#!/usr/bin/env python3
"""async/await 範例"""

import asyncio

def demo():
    async def say_after(delay, message):
        await asyncio.sleep(delay)
        print(message)

    async def main():
        # 依序執行
        # await say_after(1, "Hello")
        # await say_after(2, "World")

        # 併發執行
        task1 = asyncio.create_task(say_after(1, "Hello"))
        task2 = asyncio.create_task(say_after(2, "World"))

        await task1
        await task2

        print("Done!")

    asyncio.run(main())
```

## asyncio 佇列範例

```python
#!/usr/bin/env python3
"""asyncio 佇列範例"""

import asyncio

def demo():
    async def producer(queue):
        for i in range(5):
            await queue.put(i)
            await asyncio.sleep(0.5)
        await queue.put(None)

    async def consumer(queue):
        while True:
            item = await queue.get()
            if item is None:
                break
            print(f"Got: {item}")

    async def main():
        queue = asyncio.Queue()
        await asyncio.gather(
            producer(queue),
            consumer(queue)
        )

    asyncio.run(main())
```

## 完整演示

```python
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

    # 4. 型別提示 - 變數
    print("\n4. 變數型別提示:")
    name: str = "Alice"
    age: int = 30
    print(f"  Name: {name}, Age: {age}")

    # 5. f-string 格式化
    print("\n5. f-string 格式化:")
    pi = 3.14159
    print(f"  Pi: {pi:.2f}")

    print("\n" + "=" * 50)
    print("演示完成!")
    print("=" * 50)

if __name__ == "__main__":
    demo()
```