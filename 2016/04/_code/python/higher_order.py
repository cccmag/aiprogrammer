# Higher-order functions examples

from functools import partial

# Apply twice
def apply_twice(f, x):
    return f(f(x))

def double(x):
    return x * 2

def add_ten(x):
    return x + 10

print(f"apply_twice(double, 5): {apply_twice(double, 5)}")  # 20
print(f"apply_twice(add_ten, 1): {apply_twice(add_ten, 1)}")  # 21

# Compose
def compose(f, g):
    return lambda x: f(g(x))

def inc(x):
    return x + 1

def square(x):
    return x * x

inc_then_square = compose(square, inc)
square_then_inc = compose(inc, square)

print(f"inc_then_square(5): {inc_then_square(5)}")  # 36
print(f"square_then_inc(5): {square_then_inc(5)}")  # 26

# Partial application
def power(base, exponent):
    return base ** exponent

square = partial(power, exponent=2)
cube = partial(power, exponent=3)

print(f"square(5): {square(5)}")  # 25
print(f"cube(5): {cube(5)}")  # 125

# Currying
def curried_sum(x):
    def inner(y):
        return x + y
    return inner

add5 = curried_sum(5)
add10 = curried_sum(10)

print(f"add5(3): {add5(3)}")  # 8
print(f"add10(3): {add10(3)}")  # 13