import time
import threading
import multiprocessing
import asyncio
from functools import wraps


def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"[timer] {func.__name__} took {elapsed:.4f}s")
        return result
    return wrapper


def fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


class TimerContext:
    def __enter__(self):
        self.start = time.perf_counter()
        return self
    def __exit__(self, *args):
        self.elapsed = time.perf_counter() - self.start
        print(f"[context] elapsed: {self.elapsed:.4f}s")


@timer
def slow_square(n):
    time.sleep(0.1)
    return n * n


def thread_worker(name, count):
    for i in range(count):
        print(f"  [thread {name}] step {i}")
        time.sleep(0.05)


def process_worker(name):
    print(f"  [process {name}] pid={multiprocessing.current_process().pid}")
    return name


@timer
def run_threads():
    threads = [threading.Thread(target=thread_worker, args=(f"T{i}", 3)) for i in range(3)]
    for t in threads: t.start()
    for t in threads: t.join()


@timer
def run_processes():
    with multiprocessing.Pool(processes=3) as pool:
        results = pool.map(process_worker, ["P1", "P2", "P3"])
    print(f"  results: {results}")


async def async_worker(name, delay):
    await asyncio.sleep(delay)
    print(f"  [async {name}] done after {delay}s")


@timer
def run_async():
    async def main():
        tasks = [async_worker("A", 0.1), async_worker("B", 0.2), async_worker("C", 0.15)]
        await asyncio.gather(*tasks)
    asyncio.run(main())


def demo():
    print("=== Decorator Demo ===")
    print(f"slow_square(4) = {slow_square(4)}")

    print("\n=== Generator Demo ===")
    fib = fibonacci()
    print(f"fibonacci first 10: {[next(fib) for _ in range(10)]}")

    print("\n=== Context Manager Demo ===")
    with TimerContext() as ctx:
        time.sleep(0.2)
    print(f"outside read: {ctx.elapsed:.4f}s")

    print("\n=== Threading Demo ===")
    run_threads()

    print("\n=== Multiprocessing Demo ===")
    run_processes()

    print("\n=== Async Demo ===")
    run_async()


if __name__ == "__main__":
    demo()
