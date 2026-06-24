# Python functional examples

from functools import reduce, lru_cache

# Compose
def compose(*functions):
    def inner(x):
        result = x
        for f in reversed(functions):
            result = f(result)
        return result
    return inner

# Pipeline
def pipeline(*funcs):
    def inner(x):
        result = x
        for f in funcs:
            result = f(result)
        return result
    return inner

# Curry
def curry(func):
    def curried(*args):
        if len(args) >= func.__code__.co_argcount:
            return func(*args)
        return lambda *more: curried(*(args + more))
    return curried

# Map, Filter, Reduce
numbers = list(range(1, 11))
print(f"Numbers: {numbers}")

squares = list(map(lambda x: x ** 2, numbers))
print(f"Squares: {squares}")

evens = list(filter(lambda x: x % 2 == 0, numbers))
print(f"Evens: {evens}")

total = reduce(lambda acc, x: acc + x, numbers, 0)
print(f"Sum: {total}")

# Composition example
result = pipeline(
    lambda x: x * 2,
    lambda x: x + 1,
    lambda x: x ** 2
)(3)
print(f"Pipeline result: {result}")