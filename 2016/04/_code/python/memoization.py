# Memoization examples

from functools import lru_cache
from time import time

# Manual memoization with closure
def make_memoize():
    cache = {}
    def memoize(func):
        def wrapper(*args):
            if args not in cache:
                cache[args] = func(*args)
            return cache[args]
        wrapper.cache = cache
        return wrapper
    return memoize

# Fibonacci without memoization
def fib_slow(n):
    if n < 2:
        return n
    return fib_slow(n-1) + fib_slow(n-2)

# Fibonacci with memoization
@memoize()
def fib_fast(n):
    if n < 2:
        return n
    return fib_fast(n-1) + fib_fast(n-2)

# Fibonacci with lru_cache
@lru_cache(maxsize=None)
def fib_lru(n):
    if n < 2:
        return n
    return fib_lru(n-1) + fib_lru(n-2)

# Test
print("Without memoization (slow):")
start = time()
# fib_slow(30)  # Too slow, skip
# print(f"fib_slow(30) = {fib_slow(30)}")
print("Skipped - too slow")

print("\nWith memoization (fast):")
start = time()
result = fib_fast(30)
print(f"fib_fast(30) = {result}")
print(f"Time: {time() - start:.6f}s")

print("\nWith lru_cache:")
start = time()
result = fib_lru(100)
print(f"fib_lru(100) = {result}")
print(f"Time: {time() - start:.6f}s")

# More complex example: edit distance
@memoize()
def edit_distance(s1, s2):
    if not s1:
        return len(s2)
    if not s2:
        return len(s1)
    if s1[0] == s2[0]:
        return edit_distance(s1[1:], s2[1:])
    return 1 + min(
        edit_distance(s1[1:], s2),
        edit_distance(s1, s2[1:]),
        edit_distance(s1[1:], s2[1:])
    )

print(f"\nedit_distance('kitten', 'sitting') = {edit_distance('kitten', 'sitting')}")