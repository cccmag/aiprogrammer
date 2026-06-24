#!/usr/bin/env python3
"""
PLT Demo — Programming Language Theory 程式語言理論範例
Lambda calculus interpreter, type checker, higher-order functions, monads.
"""

from dataclasses import dataclass
from typing import Any, Callable, Generic, TypeVar, Union

T = TypeVar('T')
U = TypeVar('U')

# ====== 1. Lambda Calculus ======

CHURCH_ZERO = lambda f: lambda x: x
CHURCH_ONE = lambda f: lambda x: f(x)
CHURCH_TWO = lambda f: lambda x: f(f(x))
CHURCH_THREE = lambda f: lambda x: f(f(f(x)))

def church_succ(n):
    return lambda f: lambda x: f(n(f)(x))

def church_add(m, n):
    return lambda f: lambda x: m(f)(n(f)(x))

def church_mul(m, n):
    return lambda f: lambda x: m(n(f))(x)

def church_to_int(n):
    return n(lambda x: x + 1)(0)

Y = (lambda f: (lambda x: f(lambda v: x(x)(v)))(lambda x: f(lambda v: x(x)(v))))

# ====== 2. Type Checker ======

@dataclass
class TInt:
    def __str__(self): return "Int"
@dataclass
class TBool:
    def __str__(self): return "Bool"
@dataclass
class TFun:
    param: Any
    ret: Any
    def __str__(self): return f"({self.param} -> {self.ret})"

class Expr: pass
class EInt(Expr):
    def __init__(self, v): self.val = v
    def __repr__(self): return str(self.val)
class EBool(Expr):
    def __init__(self, v): self.val = v
    def __repr__(self): return str(self.val)
class EVar(Expr):
    def __init__(self, n): self.name = n
    def __repr__(self): return self.name
class EAbs(Expr):
    def __init__(self, v, vt, b):
        self.var = v; self.var_type = vt; self.body = b
    def __repr__(self): return f"(λ{self.var}:{self.var_type}.{self.body})"
class EApp(Expr):
    def __init__(self, fn, arg):
        self.fn = fn; self.arg = arg
    def __repr__(self): return f"({self.fn} {self.arg})"
class EAdd(Expr):
    def __init__(self, l, r):
        self.lhs = l; self.rhs = r
    def __repr__(self): return f"({self.lhs} + {self.rhs})"
class EIf(Expr):
    def __init__(self, c, t, e):
        self.cond = c; self.then_b = t; self.else_b = e
    def __repr__(self): return f"(if {self.cond} then {self.then_b} else {self.else_b})"

class TypeErrorE(Exception): pass

class TypeChecker:
    def __init__(self):
        self.env = {}
    def check(self, e):
        if isinstance(e, EInt): return TInt()
        if isinstance(e, EBool): return TBool()
        if isinstance(e, EVar):
            if e.name in self.env: return self.env[e.name]
            raise TypeErrorE(f"Unbound: {e.name}")
        if isinstance(e, EAbs):
            self.env[e.var] = e.var_type
            r = self.check(e.body)
            del self.env[e.var]
            return TFun(e.var_type, r)
        if isinstance(e, EApp):
            ft = self.check(e.fn)
            at = self.check(e.arg)
            if isinstance(ft, TFun):
                if str(ft.param) != str(at):
                    raise TypeErrorE(f"Type mismatch: expect {ft.param}, got {at}")
                return ft.ret
            raise TypeErrorE(f"Not a function: {ft}")
        if isinstance(e, EAdd):
            lt = self.check(e.lhs); rt = self.check(e.rhs)
            if str(lt) != "Int" or str(rt) != "Int":
                raise TypeErrorE(f"Cannot add {lt} + {rt}")
            return TInt()
        if isinstance(e, EIf):
            ct = self.check(e.cond)
            if str(ct) != "Bool":
                raise TypeErrorE(f"Cond must be Bool, got {ct}")
            tt = self.check(e.then_b); et = self.check(e.else_b)
            if str(tt) != str(et):
                raise TypeErrorE(f"Branch mismatch: {tt} vs {et}")
            return tt
        raise TypeErrorE(f"Unknown: {e}")

# ====== 3. Higher-Order Functions ======

def hof_map(f, lst): return [f(x) for x in lst]
def hof_filter(p, lst): return [x for x in lst if p(x)]
def hof_reduce(f, lst, init):
    acc = init
    for x in lst: acc = f(acc, x)
    return acc
def hof_compose(f, g): return lambda x: f(g(x))
def hof_curry(fn):
    def curried(a):
        def inner(b): return fn(a, b)
        return inner
    return curried
def hof_uncurry(fn):
    return lambda ab: fn(ab[0])(ab[1])

# ====== 4. Monad Simulation ======

class Monad(Generic[T]):
    @staticmethod
    def pure(v): raise NotImplementedError
    def bind(self, fn): raise NotImplementedError
    def fmap(self, fn):
        return self.bind(lambda v: self.__class__.pure(fn(v)))

class Maybe(Monad[T]):
    def __init__(self, v=None, just=True):
        self._val = v; self._is_just = just
    @staticmethod
    def just(v): return Maybe(v, True)
    @staticmethod
    def nothing(): return Maybe(just=False)
    @staticmethod
    def pure(v): return Maybe.just(v)
    def bind(self, fn):
        return fn(self._val) if self._is_just else Maybe.nothing()
    def __repr__(self):
        return f"Just({self._val})" if self._is_just else "Nothing"

class ListM(Monad[T]):
    def __init__(self, items):
        self._items = list(items)
    @staticmethod
    def pure(v): return ListM([v])
    def bind(self, fn):
        result = []
        for i in self._items:
            result.extend(fn(i)._items)
        return ListM(result)
    def __repr__(self): return f"ListM({self._items})"

class Either(Monad[T]):
    def __init__(self, v=None, right=True, err=None):
        self._val = v; self._is_right = right; self._error = err
    @staticmethod
    def right(v): return Either(v, True)
    @staticmethod
    def left(err): return Either(right=False, err=err)
    @staticmethod
    def pure(v): return Either.right(v)
    def bind(self, fn):
        return fn(self._val) if self._is_right else Either.left(self._error)
    def __repr__(self):
        return f"Right({self._val})" if self._is_right else f"Left({self._error})"

# ====== Demo ======

def demo():
    print("=" * 60)
    print("PLT Demo — Programming Language Theory")
    print("=" * 60)

    # 1. Lambda Calculus
    print("\n--- 1. Lambda Calculus ---")
    three = church_add(CHURCH_ONE, CHURCH_TWO)
    four = church_mul(CHURCH_TWO, CHURCH_TWO)
    print(f"1 + 2 = {church_to_int(three)}")
    print(f"2 * 2 = {church_to_int(four)}")

    fact = Y(lambda f: lambda n: 1 if n == 0 else n * f(n - 1))
    print(f"fact(5) = {fact(5)}")

    # 2. Type Checker
    print("\n--- 2. Type Checker ---")
    tc = TypeChecker()
    expr1 = EAbs("x", TInt(), EAdd(EVar("x"), EInt(1)))
    print(f"Type of (λx:Int. x + 1): {tc.check(expr1)}")

    expr2 = EIf(EBool(True), EInt(1), EInt(2))
    print(f"Type of (if true then 1 else 2): {tc.check(expr2)}")

    try:
        tc.check(EIf(EInt(1), EInt(1), EInt(2)))
    except TypeErrorE as e:
        print(f"Type error caught: {e}")

    # 3. Higher-Order Functions
    print("\n--- 3. Higher-Order Functions ---")
    nums = [1, 2, 3, 4, 5]
    print(f"map(x2, {nums}) = {hof_map(lambda x: x * 2, nums)}")
    print(f"filter(even, {nums}) = {hof_filter(lambda x: x % 2 == 0, nums)}")
    print(f"reduce(+, {nums}) = {hof_reduce(lambda a, b: a + b, nums, 0)}")

    inc = hof_curry(lambda a, b: a + b)(1)
    print(f"curry(+)(1)(5) = {inc(5)}")

    # 4. Monad
    print("\n--- 4. Monad ---")
    safe_div = lambda x, y: Maybe.just(x // y) if y != 0 else Maybe.nothing()
    r = Maybe.just(10).bind(lambda x: safe_div(x, 2))
    print(f"Just(10) >>= safe_div(_,2): {r}")
    r = Maybe.just(10).bind(lambda x: safe_div(x, 0))
    print(f"Just(10) >>= safe_div(_,0): {r}")

    ma = Maybe.just(3).bind(lambda x: Maybe.just(4).bind(lambda y: Maybe.just(x + y)))
    print(f"Maybe monadic add: {ma}")

    xs = ListM([1, 2])
    ys = ListM([3, 4])
    pairs = xs.bind(lambda x: ys.bind(lambda y: ListM.pure((x, y))))
    print(f"List cartesian product: {pairs}")

    r1 = Either.right(16).bind(lambda x: Either.right(x ** 0.5))
    r2 = Either.right(-1).bind(lambda x: Either.left("negative") if x < 0 else Either.right(x ** 0.5))
    print(f"Either sqrt(16): {r1}")
    print(f"Either sqrt(-1): {r2}")

    print("\n" + "=" * 60)
    print("Demo complete!")
    print("=" * 60)

if __name__ == "__main__":
    demo()
