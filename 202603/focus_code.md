# Lambda Calculus 完整實作

## 前言

Lambda Calculus（λ 演算）是 Alonzo Church 在 1936 年提出的形式系統。本篇文章將完整實作 Lambda Calculus，從 Church 原本的符號開始，最後用 Python 的 lambda 實現一個可實際執行的版本。

---

## 原始碼

完整的 Python 實作請參考：[_code/lambdaCalculus.py](_code/lambdaCalculus.py)

```python
#!/usr/bin/env python3
"""Lambda Calculus Python Implementation"""

TRUE = lambda t: lambda f: t
FALSE = lambda t: lambda f: f
AND = lambda p: lambda q: p(q)(p)
OR = lambda p: lambda q: p(p)(q)
NOT = lambda p: lambda a: lambda b: p(b)(a)
IF = lambda p: lambda a: lambda b: p(a)(b)

def church_to_bool(b): return b(True)(False)

ZERO = lambda f: lambda x: x
ONE = lambda f: lambda x: f(x)
TWO = lambda f: lambda x: f(f(x))
THREE = lambda f: lambda x: f(f(f(x)))
FOUR = lambda f: lambda x: f(f(f(f(x))))
FIVE = lambda f: lambda x: f(f(f(f(f(x)))))
SIX = lambda f: lambda x: f(f(f(f(f(f(x))))))
SEVEN = lambda f: lambda x: f(f(f(f(f(f(f(x)))))))
EIGHT = lambda f: lambda x: f(f(f(f(f(f(f(f(x))))))))
NINE = lambda f: lambda x: f(f(f(f(f(f(f(f(f(x))))))))
TEN = lambda f: lambda x: f(f(f(f(f(f(f(f(f(f(x))))))))))

def church_to_int(n): return n(lambda x: x + 1)(0)

def int_to_church(n):
    if n == 0: return ZERO
    result = ZERO
    for _ in range(n): result = SUCC(result)
    return result

SUCC = lambda n: lambda f: lambda x: f(n(f)(x))
PLUS = lambda m: lambda n: lambda f: lambda x: m(f)(n(f)(x))
MULT = lambda m: lambda n: lambda f: m(n(f))
POWER = lambda m: lambda n: n(m)

IS_ZERO = lambda n: n(lambda _: FALSE)(TRUE)
PRED = lambda n: lambda f: lambda x: n(lambda g: lambda h: h(g(f)))(lambda _: x)(lambda a: a)
SUB = lambda m: lambda n: n(PRED)(m)
LEQ = lambda m: lambda n: IS_ZERO(SUB(m)(n))

Y = lambda f: (lambda x: f(lambda v: x(x)(v)))(lambda x: f(lambda v: x(x)(v)))

def test():
    print("Testing Church numbers:")
    for n, name in [(ZERO,"ZERO"),(ONE,"ONE"),(TWO,"TWO"),(THREE,"THREE"),(FOUR,"FOUR"),(FIVE,"FIVE"),(SIX,"SIX"),(SEVEN,"SEVEN"),(EIGHT,"EIGHT"),(NINE,"NINE"),(TEN,"TEN")]:
        print(f"{name} = {church_to_int(n)}")
    print()
    print("Testing operations:")
    print(f"PLUS(TWO, THREE) = {church_to_int(PLUS(TWO)(THREE))}")
    print(f"MULT(TWO, THREE) = {church_to_int(MULT(TWO)(THREE))}")
    print(f"POWER(TWO, THREE) = {church_to_int(POWER(TWO)(THREE))}")
    print()
    print("Testing arithmetic:")
    print(f"PLUS(POWER(TWO)(THREE), MULT(THREE)(THREE)) = {church_to_int(PLUS(POWER(TWO)(THREE))(MULT(THREE)(THREE)))}")
    print(f"SUB(POWER(THREE)(TWO), MULT(TWO)(FOUR)) = {church_to_int(SUB(POWER(THREE)(TWO))(MULT(TWO)(FOUR)))}")
    print()
    print("Testing comparisons:")
    print(f"LEQ(THREE, FOUR) = {church_to_bool(LEQ(THREE)(FOUR))}")
    print(f"LEQ(FOUR, THREE) = {church_to_bool(LEQ(FOUR)(THREE))}")
    print()
    print("Testing factorial:")
    def church_factorial(n):
        if church_to_bool(IS_ZERO(n)):
            return ONE
        return MULT(n)(church_factorial(PRED(n)))
    print(f"factorial(3) = {church_to_int(church_factorial(THREE))}")
    print()
    print("Testing factorial with Y combinator:")
    CBN_Y = lambda f: (lambda x: f(lambda v: x(x)(v)))(lambda x: f(lambda v: x(x)(v)))
    CBN_FACT_STEP = lambda f: lambda n: 1 if n == 0 else n * f(n - 1)
    CBN_FACT = CBN_Y(CBN_FACT_STEP)
    print(f"factorial(3) = {CBN_FACT(3)}")
    print(f"factorial(5) = {CBN_FACT(5)}")

if __name__ == "__main__": test()
```

---

## 執行結果

```
Testing Church numbers:
ZERO = 0
ONE = 1
TWO = 2
THREE = 3
FOUR = 4
FIVE = 5
SIX = 6
SEVEN = 7
EIGHT = 8
NINE = 9
TEN = 10

Testing operations:
PLUS(TWO, THREE) = 5
MULT(TWO, THREE) = 6
POWER(TWO, THREE) = 8

Testing arithmetic:
PLUS(POWER(TWO)(THREE), MULT(THREE)(THREE)) = 17
SUB(POWER(THREE)(TWO), MULT(TWO)(FOUR)) = 1

Testing comparisons:
LEQ(THREE, FOUR) = True
LEQ(FOUR, THREE) = False

Testing factorial:
factorial(3) = 6

Testing factorial with Y combinator:
factorial(3) = 6
factorial(5) = 120
```

---

## Church 的原本符號

### 基本語法

Church 的 Lambda Calculus 使用以下符號：

```
┌─────────────────────────────────────────────────────┐
│                 Lambda Calculus 語法                   │
├─────────────────────────────────────────────────────┤
│                                                     │
│  變數：    x, y, z, ...                            │
│                                                     │
│  抽象：    λx.M    （建立函式）                    │
│                                                     │
│  應用：    M N    （函式調用）                     │
│                                                     │
│  括號：    (M)      （分組）                       │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### β-化簡規則

```
(λx.M) N → M[x := N]
```

這個規則的意思是：將 λx.M 中的 x 替換為 N。

---

## Church 編碼

Church 將布爾值、數字等基本資料型態編碼為 λ 項。

### Church 布林值

```scheme
; Church 布林值
TRUE  = λt.λf.t
FALSE = λt.λf.f
```

### Church 數字

```scheme
; Church 數字
0 = λf.λx.x                    ; 零：套用 f 零次
1 = λf.λx.f x                  ; 一：套用 f 一次
2 = λf.λx.f (f x)             ; 二：套用 f 兩次
3 = λf.λx.f (f (f x))         ; 三：套用 f 三次
```

### 視覺化 Church 數字

```
┌─────────────────────────────────────────────────────┐
│            Church 數字的結構                         │
├─────────────────────────────────────────────────────┤
│                                                     │
│  0 = λf.λx. x                                     │
│           └────┘                                   │
│              │                                      │
│           不套用 f                                  │
│                                                     │
│  1 = λf.λx. f x                                   │
│              └─┘                                    │
│                 │                                   │
│              套用 f 一次                           │
│                                                     │
│  2 = λf.λx. f (f x)                              │
│              └────┘                                 │
│                 └─┘                                │
│                    │                               │
│                 套用 f 兩次                        │
│                                                     │
│  3 = λf.λx. f (f (f x))                         │
│              └──────┘                              │
│                 └────┘                             │
│                    └─┘                            │
│                       │                            │
│                    套用 f 三次                      │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## 基本運算

### 後繼函式（Successor）

```scheme
; SUCC = λn.λf.λx.f (n f x)
; 將 n 套用 f 的次數加一
```

### 加法

```scheme
; PLUS = λm.λn.λf.λx.m f (n f x)
; 將 m 和 n 的 f 套用次數相加
```

### 乘法

```scheme
; MULT = λm.λn.λf.m (n f)
; 將 n f 套用 m 次
```

### 布林運算

```scheme
; AND = λp.λq.p q p
; OR  = λp.λq.p p q
; NOT = λp.λa.λb.p b a
```

---

## 條件與遞迴

### IF 條件表達式

```scheme
; IF = λp.λa.λb.p a b
; IF TRUE  a b → a
; IF FALSE a b → b
```

### Y 組合子（實現遞迴）

```scheme
; Y = λf.(λx.f (x x)) (λx.f (x x))
; Y g → g (Y g)
```

---

## 結論

透過這個實現，我們展示了：

1. **Church 原本的符號**如何表示基本概念
2. **Church 編碼**如何用 λ 項表示資料
3. **Python lambda**如何實現完整的 Lambda Calculus

Lambda Calculus 雖然簡單，卻是圖靈完整的——它可以表達任何可計算函式。這正是為什麼它成為計算理論的基石，也為什麼現代的函式程式語言都深受其影響。

---

## 延伸閱讀

- [Church 1936: An Unsolvable Problem of Elementary Number Theory](https://www.google.com/search?q=Church+Lambda+Calculus+1936)
- [Lambda Calculus 基礎](https://www.google.com/search?q=lambda+calculus+tutorial)
- [Haskell 與 Lambda Calculus](https://www.google.com/search?q=haskell+lambda+calculus)

---

*本篇文章為「AI 程式人雜誌 2026 年 3 月號」歷史回顧系列補充文章。*
