# Closures examples

# Factory function
def make_multiplier(factor):
    def multiplier(x):
        return x * factor
    return multiplier

double = make_multiplier(2)
triple = make_multiplier(3)

print(f"double(5): {double(5)}")  # 10
print(f"triple(5): {triple(5)}")  # 15

# Counter factory
def make_counter():
    count = 0
    def counter():
        nonlocal count
        count += 1
        return count
    return counter

counter1 = make_counter()
counter2 = make_counter()

print(f"counter1(): {counter1()}")  # 1
print(f"counter1(): {counter1()}")  # 2
print(f"counter1(): {counter1()}")  # 3
print(f"counter2(): {counter2()}")  # 1
print(f"counter2(): {counter2()}")  # 2

# Memoization with closure
def memoize(f):
    cache = {}
    def wrapper(*args):
        if args not in cache:
            cache[args] = f(*args)
        return cache[args]
    return wrapper

@memoize
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

print(f"fibonacci(10): {fibonacci(10)}")  # 55
print(f"fibonacci(20): {fibonacci(20)}")  # 6765